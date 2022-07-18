import json

from loader import redis_cli


CACHE = {}


async def write_data(obj):
    with redis_cli:
        redis_cli.lpush("messages", json.dumps(obj))


def get_data():
    for i in (redis_cli.lrange("messages", 0, -1)):
        row = json.loads(i)
        user_id, message_id, callback_id = row[0], row[1], row[2]
        if user_id not in CACHE:
            CACHE.update(
                {
                    user_id: {
                        message_id: row[2]
                    }
                }
            )
        # elif user_id in CACHE and len(CACHE[user_id][message_id][0]) == 0:
    return CACHE


async def changer_data(id_, person, name):
    datas = get_data()
    id_ -= 1
    if person in datas and id_ in datas[person]:
        datas[person][id_] = [id_ + 1, name]
    else:
        datas[person].update(
            {
                id_: [id_ + 1, name]
            }
        )
    return datas
