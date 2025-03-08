# Utilisation de l'image python
FROM python:3.8-slim

# Répertoire de travail
WORKDIR /app

# Copier le fichier de configuration
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le reste de l'application
COPY . .

# Commande par défaut
CMD ["python", "./fastapi_app/main.py"]
