# celery-example

This repo contains a simple task queue built using celery. 

It uses Redis,
1. As a message broker 
2. To store completed results.

To run the example -

1. Install requirements with `pip install -r requirements.txt` 
2. Run the server with `fastapi dev server.py --port 55556 --host 0.0.0.0`
3. Run the worker with `celery -A worker.celery_app worker -l INFO -P threads -c 10`. Note: This command will start a worker with concurrency set to 10 threads. If you are hosting a ML model this might have to be changed to 1.
4. POST request to `/hello-world` endpoint with the following body
```
{
    "msg": "Bla Blaaaa"
}
```
Curl:
```
curl --location 'http://localhost:55556/hello-world' \
--header 'Content-Type: application/json' \
--data '{
    "msg": "Bla Blaaaa"
}'
```
The API will responds with the `result_id`.
5. GET request to `/hello-world/{result_id}` endpoint with the `result_id` from previous step.
```
curl --location 'http://localhost:55556/hello-world/cfd25df5-aded-4d7c-b58d-300649a5cb49'
```