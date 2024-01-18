from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse
from instance.db.lite_connect import ItemModel

item_router = Blueprint('item', __name__, url_prefix='/item')
api = Api(item_router)


class Item(Resource):
    def __str__(self) -> str:
        return self.__repr__()

    def get(self, name: str):
        """通过名字获取获取指定的item
        Args:
            name (str): 每个item唯一的名字

        Returns:
            json: 返回的json响应
        """
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'code': 404, 'msg': 'not found'}, 404
        res = {
            'code': 200,
            'msg': 'success',
            'data': item.to_dict()
        }
        return jsonify(res)

    def post(self, name: str):
        """添加一个item
        Args:
            name (str): 每个item唯一的名字

        Returns:
            json: 返回的json响应
        """
        if ItemModel.find_by_name(name) is not None:
            return {'code': 400, 'msg': 'item %s already exists' % name}, 400
        item = request.get_json(silent=True)
        res = {
            'code': 200,
            'msg': 'success',
            'data': None
        }
        if item is None:
            print('no data')
            res['code'] = 400
            res['msg'] = 'no data'
            res = jsonify(res)
            res.status_code = 400
            return res
        if item.get('price') is None:
            res['code'] = 400
            res['msg'] = 'price is required'
            return res, 400
        new_item = {
            'name': name,
            'price': item.get('price', 0)
        }
        iid = ItemModel.count_rows()
        model_item = ItemModel(iid, **new_item)
        model_item.insert_value()
        return {'code': 201, 'msg': 'success', 'data': new_item}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'code': 404, 'msg': 'not found'}, 404
        item.delete_item(item.id)
        return {'code': 200, 'msg': 'success', 'data': item.to_dict()}

    def put(self, name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)
        if item is None:
            return {'code': 404, 'msg': 'not found'}, 404
        if 'price' in data:
            item.price = data['price']
            return jsonify({'code': 200, 'msg': 'updated', 'item': item.to_dict()})
        else:
            return {'code': 400, 'msg': 'price not provided'}, 400


class ItemList(Resource):
    @staticmethod
    def get():
        items_cls = ItemModel.find_all()
        items = [cls.to_dict() for cls in items_cls]
        return jsonify({'code': 200, 'msg': 'success', 'data': items})


api.add_resource(ItemList, '/')
api.add_resource(Item, '/<string:name>')
