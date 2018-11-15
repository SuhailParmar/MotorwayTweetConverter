# docker build . -t mtw:01

FROM alpine:3.7
WORKDIR /app

RUN mkdir /app/lib
COPY lib /app/lib
COPY main.py /app
COPY requirements.txt /app

# Volume Mount Is Neccesary for id storage
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
rm -r /root/.cache

# 2 External dependencies
RUN pip install -r /app/requirements.txt

CMD ["python3", "/app/main.py"]