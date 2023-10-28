from fastapi import FastAPI, UploadFile
from ultralytics import YOLO
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from PIL import Image
from pathlib import Path
import shutil
import io
import cv2

app = FastAPI()

# Добавление заголовков CORS для разрешения запросов с вашего домена
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Здесь укажите ваш домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = YOLO("/Users/20674940/Downloads/best.pt")

# Обработка загрузки изображения и обнаружение объектов
@app.post("/detect")
async def detect_objects(file: UploadFile):
    try:
        # Выведите информацию о файле для отладки
        print(f"Received file: {file.filename}")
        print(f"File content type: {file.content_type}")

        # Сохраните загруженное изображение или видео во временный файл
        temp_file_path = f"temp/{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
        print(temp_file_path)

        # Откройте изображение или видео с использованием PIL
        if file.content_type.startswith("image"):
            image = Image.open(temp_file_path)
            print(image)

            # Обработайте изображение с использованием модели YOLO
            result_image = model(source=image, imgsz=640)

            # Сохраните результат обработки
            result_image_path = f"runs/detect/predict/{file.filename}"
            for r in result_image:
                im_array = r.plot()  # plot a BGR numpy array of predictions
                im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
                im.save(result_image_path)  # save image

            return FileResponse(result_image_path, headers={"Content-Type": "image/jpeg"})
        elif file.content_type.startswith("video"):
            # Если загружено видео, вернем его как исходное
            cap = cv2.VideoCapture(temp_file_path)

            # Получите параметры видео (ширина, высота, количество кадров в секунду)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            fps = int(cap.get(5))

            # Создайте объект VideoWriter для записи аннотированного видео
            output_path = f"runs/detect/predict/{file.filename}"
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

            while cap.isOpened():
                success, frame = cap.read()

                if success:
                    # Выполните инференс YOLO на каждом кадре
                    results = model(frame)

                    # Получите аннотированный кадр
                    annotated_frame = results[0].plot()

                    # Запишите аннотированный кадр в видеофайл
                    out.write(annotated_frame)

                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    break

            cap.release()
            out.release()
            cv2.destroyAllWindows()

            video_content = open(output_path, "rb")
            return StreamingResponse(video_content, media_type=file.content_type)
        else:
            return {"error": "Unsupported file format"}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    Path("temp").mkdir(parents=True, exist_ok=True)
    Path("runs/detect/predict").mkdir(parents=True, exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
