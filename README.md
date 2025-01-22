## For preparation the project

### create env

`python -m venv env`

### enter to env

`.\env\Scripts\activate`

### for install client

`pip install -r requirements.txt`

### for pull image. (<https://hub.docker.com/_/rabbitmq>)

`docker pull rabbitmq`

### for run container

`docker run -d -p 8080:15672 -p 5672:5672 --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest rabbitmq:3-management`

### for manage rabbitmq

<http://localhost:8080>

### cmd

```
# Чтобы получить список exchange на сервере
rabbitmqctl list_exchanges
```

```
# перечислить существующие привязки, queues and exchanges
rabbitmqctl list_bindings
```

## Main info about rabbitmq

<Производитель(publisher)> — это пользовательское приложение, которое отправляет сообщения.

<Очередь(queue)> — это буфер, в котором хранятся сообщения.

<Потребитель(consumer)> — это пользовательское приложение, которое получает сообщения.

## Guide on project

1. hello_world

   ```
   publisher ---> rabbitmq ---> consumer
   ```

   ```
   - docker-compose up --build
   - python .\hello_world\receive.py
   - python .\hello_world\send.py
   ```

2. work_queues
   В этом руководстве мы создадим рабочую очередь, которая будет использоваться для распределения трудоёмких задач между несколькими исполнителями. Сообщения делятся межу потребителями поровну.

   ```
                       -----> consumer1
                       |
   publisher -> rabbitmq
                       |
                       -----> consumer2
   ```

   ```
   - docker-compose up --build
   - python .\work_queues\worker.py                # consumer1
   - python .\work_queues\worker.py                # consumer2
   - python .\work_quaes\new_task.py <message>     # где количество точек в message устанавливает задержку времени в секундах которое worker будет ожидать.
   ```

3. publish_subscribe

   Сообщение будет отправлено всем подписчикам. Шаблон известен как «публикация/подписка».
   ТУт будет использован обменик (exchange). Производитель может отправлять сообщения только на обменник. Обменник (exchange) — это очень простая вещь, с одной стороны, он получает сообщения от производителей, а с другой — отправляет их в очереди. Обменник должен точно знать, что делать с полученным сообщением.

   ```
                           -----> queue1
                           |
       publisher -> exchange
                           |
                           -----> queue2

   ```

   ```
   - docker-compose up --build
   - python .\publish_subscribe\subscriber.py                               # consumer1
   - python .\publish_subscribe\subscriber.py                               # consumer2
   - python .\publish_subscribe\subscriber.py > logs_from_rabbit.log        # consumer3
   - python .\publish_subscribe\publisher.py <message>                      # где количество точек в message устанавливает задержку времени в секундах которое worker будет ожидать.
   ```
