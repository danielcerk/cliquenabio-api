# Importar a imagem

FROM python:3.10-slim-bullseye

# Define uma área de trabalho

WORKDIR /app

# Evita que o Python crie arquivos .pyc e ativa modo "não bufferizado"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copia e instala as dependencias

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do aquivo

COPY . .

# Roda as migrações

RUN python manage.py migrate --noinput

# Aqui, expõe para a porta 8000

EXPOSE 8000

# Roda os comandos

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]