from loader import redis_cli

CACHE = {}


async def write_data(**kwargs):
    user_id = kwargs["user_id"]
    obj = {
        "id": kwargs["id_"],
        "name": kwargs["name"]
    }
    if user_id not in CACHE:
        CACHE.setdefault(user_id, {})
    CACHE[user_id].update(
        {
            obj["id"]: [[], obj["name"]]
        }
    )


async def changer_data(id_, person):
    CACHE[person][id_ - 1][0].append(id_)


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
