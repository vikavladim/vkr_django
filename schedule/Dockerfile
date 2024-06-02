# Используйте официальный образ Python
FROM quay.io/fedora/python-311

# Установите рабочую директорию внутри контейнера
WORKDIR /app

# Установите pip и зависимости
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# Копируйте файлы проекта внутрь контейнера
COPY . /app

# Установите зависимости проекта
RUN pip install -r requirements.txt

USER root
# Установите зависимости для PostgreSQL
RUN dnf install -y postgresql postgresql-server


# Запустите приложение
CMD ["sh", "-c", "python manage.py migrate && \
    python manage.py createsuperuser --noinput --username 1234 --email vikavladim@mail.ru --password '12345678' && \
    python manage.py runserver 0.0.0.0:8000"]
