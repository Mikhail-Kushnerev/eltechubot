from loader import redis_cli

CACHE = {}


async def write_data(**kwargs):
    user_id = kwargs["user_id"]
    obj = {
        "id": int(kwargs["id_"]),
        "name": kwargs["name"],
        "target": kwargs["target"]
    }
    if user_id not in CACHE:
        CACHE.setdefault(user_id, {"cart": []})
    CACHE[user_id].update(
        {
            obj["id"]: [obj["target"], obj["name"]]
        }
    )
    print(CACHE)


async def changer_data(id_: int, person, id_1):
    print(CACHE, id_, id_1)
    if len(CACHE[person][int(id_)]) == 1:
        CACHE[person][int(id_)].insert(0, id_1)


async def checker(find_target, user_id):
    print(redis_cli.hgetall(user_id))
    print(find_target.encode() in redis_cli.hgetall(user_id))
    if find_target.encode() not in redis_cli.hgetall(user_id):
        redis_cli.hset(user_id, find_target, '+')
        print(redis_cli.hgetall(user_id))
        result = True
    else:
        result = False
    return result
