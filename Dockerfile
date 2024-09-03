FROM python:3.11-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

COPY . /app

WORKDIR /app

EXPOSE 5000
ENV FLASK_APP=flaskapp.py

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "flaskapp:app"]
# CMD ["gunicorn","--config","gunicorn_config.py","flaskapp:app"]

# ENTRYPOINT ["python", "flaskapp.py"]
# Run the Flask app directly [fail]
# CMD ["python", "flaskapp.py"] 

ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]