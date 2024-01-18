import random

from flask import Blueprint, jsonify, request
from instance.db.connect import Saying, insert_data

saying_router = Blueprint('saying', __name__, url_prefix='/saying')
sayings = [{"id": 16, "content": "害怕失败是成功的最大障碍，勇敢尝试才是通往成功的道路。"},
           {"id": 17, "content": "成功的关键在于不停地学习和不断地进步。"},
           {"id": 18, "content": "每一次的努力都是为了让明天的自己更加优秀。"},
           {"id": 19, "content": "生命不是等待风暴过去，而是学会在雨中前行。"},
           {"id": 20, "content": "相信自己，你比想象中更强大。"},
           {"id": 21, "content": "每一次的付出都是为了迎接更好的自己。"},
           {"id": 22, "content": "成功来自于每一天的积累，而不是一夜之间的奇迹。"},
           {"id": 23, "content": "不要被困境所困扰，而是要用坚持战胜困境。"},
           {"id": 24, "content": "做最好的自己，成为最优秀的自己。"},
           {"id": 25, "content": "生命的真正意义在于不断地挑战自己，超越自己。"},
           {"id": 26, "content": "勇敢追逐梦想，因为梦想是通向成功的路。"},
           {"id": 27, "content": "成功的关键在于始终保持对梦想的热情。"},
           {"id": 28, "content": "每一次的努力都是为了离梦想更近一步。"},
           {"id": 29, "content": "成功的人不是没有失败，而是在失败中找到了前进的力量。"},
           {"id": 30, "content": "坚持不懈，终将迎来辉煌的一刻。"},
           {"id": 31, "content": "不要轻言放弃，因为下一秒可能就是奇迹发生的时刻。"},
           {"id": 32, "content": "成功需要付出代价，而这个代价就是不断的努力和坚持。"},
           {"id": 33, "content": "相信自己的选择，为自己的决定负责。"},
           {"id": 34, "content": "只有拥有勇气面对未知，才能发现更广阔的天地。"},
           {"id": 35, "content": "成功不是偶然的结果，而是对目标坚持不懈的过程。"},
           {"id": 36, "content": "不怕慢，就怕停。每一步都是向前的力量。"},
           {"id": 37, "content": "成功的背后往往是不为人知的努力和坚持。"},
           {"id": 38, "content": "对自己有信心，对生活充满期待，成功将不可避免。"},
           {"id": 39, "content": "坚持不是一时的决定，而是每时每刻都在持续的努力。"},
           {"id": 40, "content": "用心去追求，用行动去实现，你就是生命的奇迹。"},
           {"id": 41, "content": "成功不是一蹴而就的，而是一步一个脚印的积累。"},
           {"id": 42, "content": "不管多么艰难，只要有梦想，就有前行的动力。"},
           {"id": 43, "content": "成功离不开困难，因为困难是成功的催化剂。"},
           {"id": 44, "content": "在困境中看到机会，是成功者与普通人的区别。"},
           {"id": 45, "content": "每一份付出都是为了创造更好的未来。"},
           {"id": 46, "content": "生命中最重要的不是所站的位置，而是所朝的方向。"},
           {"id": 47, "content": "成功的路上没有捷径，只有脚印的坚持。"},
           {"id": 48, "content": "用心去经营每一天，成功会在不经意间找上门。"},
           {"id": 49, "content": "坚持不是一时的决定，而是每时每刻都在持续的努力。"},
           {"id": 50, "content": "用心去追求，用行动去实现，你就是生命的奇迹。"}
           ]


@saying_router.get('/')
def get_sayings():
    data = random.choice(sayings)
    res = {
        'code': 200,
        'msg': 'success',
        'data': data
    }
    return jsonify(res)

# @saying_router.post('/', endpoint='create_saying')


@saying_router.post('/')
def create_saying():
    data = request.get_json()
    new_saying = {
        'id': len(sayings) + 1,
        'content': data['content']
    }
    sayings.append(new_saying)
    res = {
        'code': 200,
        'msg': 'success',
        'data': new_saying
    }
    return jsonify(res)


@saying_router.get('/<int:sid>')
def get_saying(sid):
    filtered_sayings = filter(lambda x: str(sid) == str(x['id']), sayings)
    data = next(filtered_sayings, None)
    if data is None:
        res = {
            'code': 404,
            'msg': 'saying not found',
            'data': None
        }
        return jsonify(res), 404
    res = {
        'code': 200,
        'msg': 'success',
        'data': data
    }
    return jsonify(res)


@saying_router.post("/v1", endpoint='create_saying_db')
def create_saying():
    data = request.get_json()
    insert_data(content=data["content"])
    return jsonify({"code": 200, "msg": "success"})


@saying_router.get("/v1")
def get_form_database():
    all_sayings = Saying.query.all()[0]
    return jsonify(all_sayings.to_dict())
