# Модель классификации и детекции огнестреьного оружия:
Репозиторий команды Уральские Мандарины с веб-приложением для детектирования оружия.

# Стек технологий:

- YOLOv8: Уникальнообученая модель для детектирования и классификации огнестрельного оружия обученая на уникальном датасете.
- FastAPI: Современный, быстрый (высокопроизводительный) веб-фреймворк для создания API. Реализация серверной части.
- React: Современный фреймворк для реализации клиентской части веб-приложения
- Docker: Платформа для простого создания, мастабируемости и запуска распределенных приложений.
- Docker: платформа для простого создания, доставки и запуска распределенных приложений.
- Telegram API: API  для 

<img width="100%" src="https://raw.githubusercontent.com/ultralytics/assets/main/yolov8/yolo-comparison-plots.png"></a>

---
# Инструкция по установке

У вас есть 2 способа запустить приложение. Через Docker или локально.

## Using Docker
Чтобы запустить через docker запустите следующий код:
```
git clone https://github.com/RomanLazovskiy/gun_detection.git
cd gun_detection
docker-compose up
```

## Locally
Чтобы запустить приложение локально необходимо по отдельности запустить серверную часть, клиентску часть и телеграм бота:

1. Запуск серверной части:

```
cd /back-end
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
2.  Запуск телеграм бота:
```
cd /back-end/tg_bot
python notification_bot.py
```  
*Note: You can change the address and port in the file **docker-compose.yaml***

3.
Запуск клиентской части:
```
cd front-end/gun-detection-app
npm install
npm start
```
```