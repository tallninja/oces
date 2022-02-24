FROM ernestwambua/oces-compilers:focal

WORKDIR /app

ENV FLASK_APP routes.py

COPY ./requirements.txt ./requirements.txt

RUN set -xe && \
    python3 -m venv env && \
    . ./env/bin/activate

RUN pip3 install -r requirements.txt

COPY ./ ./

ENTRYPOINT ["python3", "-m", "flask", "run", "--host=0.0.0.0"]