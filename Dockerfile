FROM python:3.12-slim

WORKDIR /app
COPY . .

# A imagem é usada pelas instâncias da ShopNow. O Nginx atua como balanceador.
CMD ["python", "instancias/app.py"]
