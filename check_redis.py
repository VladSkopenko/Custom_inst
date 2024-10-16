import redis

r = redis.Redis(
    host="redis-14349.c273.us-east-1-2.ec2.redns.redis-cloud.com",
    port=14349,
    password="Gdaah2L17lLsKfbqeqJhEQn4sUAkttXA",
    decode_responses=True,
)

try:

    r.ping()
    print("Подключение к Redis успешно!")

    r.set("test_key", "test_value")
    print("Значение установлено:", r.get("test_key"))

except redis.ConnectionError as e:
    print("Ошибка подключения к Redis:", e)
except Exception as e:
    print("Произошла ошибка:", e)
