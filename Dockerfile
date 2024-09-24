# Utiliser l'image officielle Python 3.11
FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Mettre à jour pip avant d'installer les dépendances
RUN pip install --upgrade pip

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Exposer le port par défaut de Streamlit
EXPOSE 8501

# Lancer Streamlit
CMD ["streamlit", "run", "app.py"]
