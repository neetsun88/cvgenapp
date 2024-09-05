FROM python:3.11-slim

EXPOSE 5000/tcp

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

COPY . /app

WORKDIR /app

# Specify the command to run on container start
CMD [ "python", "./app.py" ]