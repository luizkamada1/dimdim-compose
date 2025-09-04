FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1       PYTHONUNBUFFERED=1

# Dependências do sistema (curl para o healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends       curl     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências Python primeiro (cache de camadas)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar código
COPY src /app

# Criar usuário sem privilégios
RUN groupadd -r app && useradd -r -g app app     && chown -R app:app /app

USER app

EXPOSE 8000

# Comando padrão: Gunicorn servindo a aplicação Flask
# O objeto WSGI "app" é definido em app.py
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
