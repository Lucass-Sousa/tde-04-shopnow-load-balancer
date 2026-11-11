FROM python:3.12-slim

WORKDIR /app
COPY . .

# A imagem é compartilhada pelo balanceador e pelas instâncias.
CMD ["python", "balanceador/app.py"]
