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
   docker-compose up --build
   .\env\Scripts\Activate.ps1
   python .\hello_world\receive.py
   python .\hello_world\send.py
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
   docker-compose up --build
   .\env\Scripts\Activate.ps1
   python .\work_queues\worker.py                # consumer1
   python .\work_queues\worker.py                # consumer2
   python .\work_quaes\new_task.py <message>     # где количество точек в message устанавливает задержку времени в секундах которое worker будет ожидать.
   ```

3. publish_subscribe

   Сообщение будет отправлено всем подписчикам. Шаблон известен как «публикация/подписка».
   ТУт будет использован обменик (exchange). Производитель может отправлять сообщения только на обменник. Обменник (exchange) — это очень простая вещь, с одной стороны, он получает сообщения от производителей, а с другой — отправляет их в очереди. Обменник должен точно знать, что делать с полученным сообщением.

   ```
                                   -----> queue1----> consumer1
                                   |
       publisher -> exchange(fanout)
                                   |
                                   -----> queue2----> consumer2

   ```

   ```
   docker-compose up --build
   .\env\Scripts\Activate.ps1

   python .\publish_subscribe\subscriber.py                               # consumer1
   python .\publish_subscribe\subscriber.py                               # consumer2
   python .\publish_subscribe\subscriber.py logs_from_rabbit.log          # consumer3

   python .\publish_subscribe\publisher.py <message>                      # где количество точек в message устанавливает задержку времени в секундах которое worker будет ожидать.
   ```

4. routing

   Сообщение будет отправлено в очереди где routing_key(queue-exchange) соответствует routing_key сообщения.

   ```
                                   ---(routing_key = error)--> queue1 (binding_key=error)----> consumer1
                                   |
       publisher -> exchange(direct)
                                   |
                                   ---(routing_key = info)    ---
                                   |                            |--->  queue2 (binding_key='info warning') ---> consumer2
                                   ---(routing_key = warning) ---
   ```

   ```
   docker-compose up --build
   .\env\Scripts\Activate.ps1

   # запуск потребителей
   python .\routing\consumer.py -t error -f error_log.txt   # consumer1 обрабатывает сообщения error
   python .\routing\consumer.py -t 'info warning'           # consumer2 обрабатывает сообщения info warning

   # запуск отправителя
   python .\routing\publisher.py -t error -m 'error msg'
   python .\routing\publisher.py -t info -m 'info msg'
   python .\routing\publisher.py -t warning -m 'warning msg'
   ```

5. topic

   В этом проекте мы будем связывать Обменник с Очередью посредством routing_key но в routing_key мы будем передавать паттерн.
   Таким образом мы добавим гибкости Подписчику.

   Есть следующие шаблоны:

   '\*' (звездочка) - может заменять ровно одно слово.

   '#' (решетка) - может заменять ноль или более слов.

   ```
                                     ---(routing_key = lazy.#)----------> queue1 (binding_key=lazy.#)----------------- ---> consumer1
                                     |
       publisher -> exchange(topic)--
                                     |
                                     ---(routing_key = *.orange.*) ----
                                     |                                |--> queue2 (binding_key= '*.orange.* fast.*.*')----> consumer2
                                     ---(routing_key = fast.*.*)   ----
                                     |
                                     ---(routing_key = *.*.rabbit)-------> queue3 (binding_key= *.*.rabbit)----------------> consumer3

   ```

   ```
   docker-compose up --build
   .\env\Scripts\Activate.ps1

   # запуск потребителей
   python .\topic\consumer.py
   python .\topic\consumer.py -t '*.orange.* fast.#'
   python .\topic\consumer.py -t *.*.rabbit

   # запуск источника
   python .\topic\publisher.py -t fast.red.rabbit -m 'this is fast animal'
   ```

   NOTE: сообщение ('this is fast animal') получат consumer2 и consumer3 т.к. они подписаны по шаблону (fast и rabbit)

6. rpc_pattern

   В этом руководстве мы будем использовать RabbitMQ для создания системы RPC: клиента и масштабируемого сервера RPC.
   Сделаем как хороший пример (.\rpc_pattern\client.py) так и не очень (.\rpc_pattern\client_bad_practice.py).
   Плохой поскольку будет создаваться очередь обратных вызовов для каждого запроса RPC.
   Лучше создать одну очередь обратных вызовов для каждого клиента и там создавать хот миллион этих вызовов.

   ```
   # клиент подписывается на свою очередь (callback_name_queue) и делает запрос (публикует) в основную очередь (main_rpc), при запросе указывает
   # имя Очереди куда нужно слать ответ (reply_to=callback_name_queue).
   # Сервер подписывается на очередь (main_rpc) и ждет сообщений. При получении, шлет в указанную в сообщении очередь

       client -> create_queue() -> consuming(queue_name) -> call_rpc(queue='main_queue', reply_to='queue_name') ---> server_rpc -> do_business_logic() -----
                                           ^                                                                                                               |
                                           |                                                                                                               |
                                           ----------------------------------------------------------------------------------------------------------------|

   ```

   ```
   docker-compose up --build
   .\env\Scripts\Activate.ps1

   #### ------------------------------       хороший пример
   # запуск клиента (плохой пример)
   python .\rpc_pattern\client.py -t 10

   # запуск rpc сервера (плохой пример)
   python .\rpc_pattern\server.py --queue rpc_good_test


   #### ------------------------------       плохой пример
   # запуск клиента
   python .\rpc_pattern\client_bad_practice.py -t 10

   # запуск rpc сервера
   python .\rpc_pattern\server.py --queue 'rpc_bad_test'

   ```


7. stream

   Поток — это абстракция журнала с возможностью только добавления, которая позволяет многократно использовать сообщения до истечения срока их действия. Рекомендуется всегда определять политику хранения. В приведенном выше примере размер потока ограничен 5 ГиБ.
   ```

       publisher ----> rabbitMq_stream() <---- consumer

   ```

   ```
   # python 3.9>=
   pip install rstream

   docker run -it --rm --name rabbitmq -p 5552:5552 -p 15672:15672 -p 5672:5672  -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS='-rabbitmq_stream advertised_host localhost'  rabbitmq:3.13
   docker exec rabbitmq rabbitmq-plugins enable rabbitmq_stream rabbitmq_stream_management
   .\env\Scripts\Activate.ps1


   # запуск consumer
   python .\stream\receive.p

   # запуск publisher
   python .\stream\send.py

   ```
