FROM python:alpine
COPY . /app
WORKDIR /app
RUN apk add --no-cache sqlite socat
RUN pip install -r requirements_dev.txt 
EXPOSE 8081 8080
ENTRYPOINT [ "python" ] 
CMD [ "app.py" ] 
