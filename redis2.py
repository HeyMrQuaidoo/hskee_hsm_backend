# import asyncio

# # from redis.asyncio import Redis
# import ssl
# import certifi
# import redis

# host = "oregon-redis.render.com"
# port = 6379
# pwd = "07xFUFyU4SPV5d3ZytFnR2TafG1nFEET"
# username = "red-cspapqd6l47c73eqvelg"
# url = f"rediss://{username}:{pwd}@{host}:{port}"

# # Use certifi's CA bundle for SSL context
# ssl_context = ssl.create_default_context(cafile=certifi.where())


# async def main():
#     try:
#         # redis_client = Redis.from_url(
#         #     url,
#         #     socket_keepalive=True,
#         #     socket_timeout=5,
#         #     retry_on_timeout=True,
#         #     # ssl=ssl_context
#         # )
#         # await redis_client.ping()
#         # rediss://red-cspapqd6l47c73eqvelg:07xFUFyU4SPV5d3ZytFnR2TafG1nFEET@oregon-redis.render.com:6379
#         # r = redis.from_url(
#         #     url="rediss://red-cspapqd6l47c73eqvelg:07xFUFyU4SPV5d3ZytFnR2TafG1nFEET@oregon-redis.render.com:6379",
#         #     decode_responses=True,
#         # )

#         r = redis.Redis(
#             host="oregon-redis.render.com",
#             port=6379,
#             username="red-cspapqd6l47c73eqvelg",
#             password="07xFUFyU4SPV5d3ZytFnR2TafG1nFEET",
#             ssl=True,
#             ssl_cert_reqs=None,
#             decode_responses=True,
#         )
#         r.ping()
#         r.set("foo", "bar")
#         # True

#         print(r.get("foo"))
#         print("Connection successful")
#     except Exception as e:
#         print(f"Connection failed: {e}")


# asyncio.run(main())
