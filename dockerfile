FROM python:latest

# Installez les dépendances nécessaires
RUN pip install pandas pymongo

# Copiez votre code dans le conteneur
COPY . /app
WORKDIR /app

CMD ["python", "main.py"]
