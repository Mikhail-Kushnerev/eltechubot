import json

from loader import redis_cli


dd = {}


async def write_data(obj):
    with redis_cli:
        redis_cli.lpush("messages", json.dumps(obj))


def get_data():
    for i in (redis_cli.lrange("messages", 0, -1)):
        a = json.loads(i)
        if a[0] not in dd or len(dd[a[0]][0]) == 0:
            dd.update({a[0]: a[1:]})
    return dd


async def changer_data(id_):
    datas = get_data()
    id_ -= 1
    if id_ in datas:
        datas[id_][0].append(id_ + 1)
    return datas
