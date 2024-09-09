FROM python:3.11.9-bookworm
WORKDIR /app
COPY . /app/backend
EXPOSE 8000
RUN pip install --no-cache-dir --upgrade -r backend/requirements.txt
CMD fastapi run backend/app/app.py --port 8000
