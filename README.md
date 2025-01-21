producers ->  queue -> consumers

### create env
python -m venv env

### enter to env
.\env\Scripts\activate

### for install client
python -m pip install pika --upgrade

### for pull image. (https://hub.docker.com/_/rabbitmq)
docker pull rabbitmq

### for run container
docker run -d -p 8080:15672 -p 5672:5672 --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest rabbitmq:3-management


### for manage rabbitmq
http://localhost:8080



