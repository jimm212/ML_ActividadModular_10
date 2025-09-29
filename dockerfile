# Imagen base: una versión ligera de Python
FROM python:3.11-slim

# Evita buffering en los logs
ENV PYTHONUNBUFFERED=1

# Carpeta donde estará tu app
WORKDIR /app

# Copia archivos de dependencias y artefactos
COPY requirements.txt .
# Instala librerías necesarias
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY artifacts/ artifacts/



# Expone el puerto de la API
EXPOSE 5000

# Comando que corre la API
CMD ["python", "app.py"]
