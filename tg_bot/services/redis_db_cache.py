from loader import redis_cli

CACHE: dict[
    int, dict[
        str | int, list[tuple[bool, object] | int | str]
    ]
] = {}


async def write_data(**kwargs) -> None:
    user_id: int = kwargs["user_id"]
    obj: dict[int | str, int | str | object] = {
        "id": int(kwargs["msg_id"]),
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


async def changer_data(id_: int, person: int, id_1: int) -> None:
    print(CACHE, id_, id_1)
    if len(CACHE[person][int(id_)]) == 2:
        CACHE[person][int(id_)].insert(1, id_1)


async def checker(find_target: str, user_id: int) -> bool:
    """
    :param find_target:
    :param user_id:
    :return:
    """
    if find_target.encode() not in redis_cli.hgetall(user_id):
        redis_cli.hset(user_id, find_target, "+")
        # print(redis_cli.hgetall(user_id))
        result: bool = True
    else:
        result: bool = False
    return result
