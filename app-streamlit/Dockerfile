FROM public.ecr.aws/lambda/python:3.10

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src src

COPY main.py main.py

CMD ["main.main_func"]