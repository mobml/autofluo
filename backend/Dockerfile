FROM python:3.12-bookworm

WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer puerto para API
EXPOSE 8000

# Comando por defecto (recarga automática en desarrollo)
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]