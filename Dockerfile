git
FROM python:alpine3.7

COPY ./app /app

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 3000

CMD ["python", "main.py"]


# docker tag log-query-manager4 your-dockerhub-username/log-query-manager4:latest
