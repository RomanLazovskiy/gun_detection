# Используем официальный образ Python в качестве базового образа
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /back-end

# Копируем файл зависимостей и файл с зависимостями
COPY requirements.txt .

# Копируем файлы модели из локальной директории в контейнер
COPY models/model_image.pt /models/model_image.pt
COPY models/model_video.pt /models/model_video.pt

# Update pip
RUN python -m pip install --upgrade pip

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Install libGL.so.1 library
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Копируем все файлы из текущей директории (включая приложение) в контейнер
COPY . /back-end

# По умолчанию FastAPI использует порт 8000, поэтому мы должны его открыть
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run your Python script
CMD ["python", "tg_bot/notification_bot.py"]

# Запускаем FastAPI приложение
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
