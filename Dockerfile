FROM python:3.8-alpine
COPY . /app
WORKDIR /app
RUN apk add --no-cache sqlite socat
RUN pip install -r -q --no-input requirements_dev.txt 
EXPOSE 8081 8080
ENTRYPOINT [ "python" ] 
CMD [ "app.py" ] 
