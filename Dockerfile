FROM python:3.12-slim

WORKDIR /app

COPY . .

# Dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Porta    
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
