from python:3.11.6-alpine

copy ./ app/

WORKDIR app/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
