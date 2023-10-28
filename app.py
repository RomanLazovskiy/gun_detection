from fastapi import FastAPI, UploadFile
from ultralytics import YOLO
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from PIL import Image

from pathlib import Path
import shutil
import io
import base64

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

        # Сохраните загруженное изображение во временный файл
        temp_image_path = f"temp/{file.filename}"
        with open(temp_image_path, "wb") as image_file:
            shutil.copyfileobj(file.file, image_file)
        print(temp_image_path)

        # Откройте изображение с использованием PIL
        image = Image.open(temp_image_path)
        print(image)

        # Обработайте изображение с использованием модели YOLO
        result_image = model(source=image, imgsz=640)

        # Сохраните результат обработки
        result_image_path = f"runs/detect/predict/{file.filename}"
        # Show the results
        for r in result_image:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            im.save(result_image_path)  # save image

        return FileResponse(result_image_path, headers={"Content-Type": "image/jpeg"})

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    Path("temp").mkdir(parents=True, exist_ok=True)
    Path("runs/detect/predict").mkdir(parents=True, exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
