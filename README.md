## For preparation the project

### create env
```python -m venv env```

### enter to env
```.\env\Scripts\activate```

### for install client
```pip install -r requirements.txt```

### for pull image. (https://hub.docker.com/_/rabbitmq)
```docker pull rabbitmq```

### for run container
```docker run -d -p 8080:15672 -p 5672:5672 --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest rabbitmq:3-management```


### for manage rabbitmq
http://localhost:8080


## Guide on project

1. hello_world

    publisher -> rabbitmq -> consumer

    ```
    - docker-compose up --build
    - python .\hello_world\receive.py
    - python .\hello_world\send.py
    ```
2. work_queues
    - Note: В этом руководстве мы создадим рабочую очередь, которая будет использоваться для распределения трудоёмких задач между несколькими исполнителями.


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