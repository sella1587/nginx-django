FROM python:alpine3.19
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "double_codification.asgi:application", "--host", "0.0.0.0", "--port", "8000"]