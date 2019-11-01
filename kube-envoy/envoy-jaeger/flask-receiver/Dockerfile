FROM python:3-alpine3.7
RUN pip3 install Flask==0.11.1 && pip install requests
COPY ./flask-receiver.py /opt/service.py
ENTRYPOINT ["python", "/opt/service.py"]
