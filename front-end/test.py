import requests
import shutil

# Замените URL на адрес вашего сервера FastAPI
url = 'http://0.0.0.0:8000/detect'

# Замените путь на путь к вашему изображению
image_path = '/Users/20674940/Desktop/Projects/hackaton_gun_detection/temp/1.jpg'

# Отправляем POST-запрос с изображением
with open(image_path, 'rb') as image_file:
    files = {'file': ('1.jpg', image_file)}
    response = requests.post(url, files=files)

# Проверяем, что запрос завершился успешно (код ответа 200)
if response.status_code == 200:
    print("Request was successful")
    print(response.headers)

else:
    print(f"Request failed with status code: {response.status_code}")
