"""
user.py
-------

本模块定义了Flask应用中用户操作相关的路由和视图，使用SQLAlchemy作为ORM，使用Flask-JWT-Extended处理认证。

导入项：

- Flask的Blueprint，用于创建用户路由的模块结构。
- Flask的jsonify，将Python字典转换为JSON响应。
- Flask的request对象，用于访问请求数据。
- 从instance.db.connect导入的SQLAlchemy模型User和Role，以及数据库实例'db'。
- Flask-JWT-Extended的JWT函数，用于处理认证令牌。

蓝图：

- user_router：一个用于用户相关路由的Blueprint实例，url前缀为'/user'。

功能函数：

- check_permission(rid: int) -> bool:
  检查给定角色ID 'rid' 的角色是否具有''admin'权限。

路由：

- GET /：get_users()
  如果请求者具有管理员权限，则获取所有用户的列表。

- GET /<int:uid>：get_user(uid)
  如果请求者具有管理员权限，则根据用户ID 'uid' 获取特定用户。

- POST /register：register()
  允许新用户通过提供用户名和密码来注册。

- POST /login：auth()
  在成功登录后，验证用户并提供JWT访问令牌。

每个路由都受到Flask-JWT-Extended的@jwt_required()装饰器的保护，该装饰器要求请求头中存在有效的JWT访问令牌。

代码包括对权限检查、缺失或无效请求数据以及请求用户未找到情况的错误处理。
"""
from flask import Blueprint, jsonify, request
from instance.db.connect import User, Role, db
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, verify_jwt_in_request

user_router = Blueprint('user', __name__, url_prefix='/user')


# 权限判断
def check_permission(rid: int):
    role = Role.query.get(rid)
    if role.name != 'admin':
        return False
    return True


@user_router.get('/')
@jwt_required()
def get_users():
    """
    获取用户列表。

    该函数是用户路由器（user_router）根路径（'/'）的GET请求的处理程序。
    它返回一个包含用户列表的JSON响应。

    参数：
        无

    返回：
        Response：一个具有以下结构的JSON响应：
            {
                'code': int，      # 响应的状态码（成功为200）
                'msg': str，       # 描述请求结果的消息（'success'）
                'data': list       # 用户列表
            }
    """
    current_user = User.query.get(get_jwt_identity())
    if not check_permission(current_user.role_id):
        res = {
            'code': 403,
            'msg': '你没有权限访问',
            'data': None
        }
        return jsonify(res), 403
    raw_user = [user.to_dict() for user in User.query.all()]
    res = {
        'code': 200,
        'msg': 'success',
        'data': raw_user
    }
    return jsonify(res)


@user_router.get('/<int:uid>')
@jwt_required()
def get_user(uid):
    # 一个是查询参数一个是路径参数
    query_user = User.query.get(get_jwt_identity())
    if not check_permission(query_user.role_id):
        return jsonify({'code': 403, 'msg': '你没有权限访问此api'}), 403
    qid = request.args.get('uid') or request.view_args.get('uid')
    if qid is None:
        return jsonify({'code': 400, 'msg': 'no uid provided'}), 400
    all_users_instance = User.query.all()
    users = [user.to_dict() for user in all_users_instance]
    filtered_users = filter(lambda x: str(qid) == str(x['id']), users)
    data = next(filtered_users, None)
    if data is None:
        res = {
            'code': 404,
            'msg': 'user not found',
            'data': None
        }
        return jsonify(res), 404
    res = {
        'code': 200,
        'msg': 'success',
        'data': data
    }
    return jsonify(res)


@user_router.post('/register')
def register():
    """注册用户
    """
    if request.get_json(silent=True) is None:
        return jsonify({'code': 400, 'msg': 'no data'}), 400
    req = request.get_json(silent=True)
    username = req.get('username')
    password = req.get('password')
    if username is None or password is None:
        return jsonify({'code': 400, 'msg': 'username or password not provided'}), 400
    user = User(username=username, password=password, role_id=2)
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'success', 'data': user.id}), 200


@user_router.post('/login')
def auth():
    """登录
    """
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"code": "302", "msg": '不要重复登录'}), 302
    req = request.get_json(silent=True) or None
    if req is None:
        return jsonify({'code': 400, 'msg': 'no data'}), 400
    username = req.get('username')
    password = req.get('password')
    if username is None or password is None:
        return jsonify({'code': 400, 'msg': 'username or password not provided'}), 400
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        return jsonify({'code': 404, 'msg': 'not found'}), 404
    access_token = create_access_token(identity=user.id)
    return jsonify({'code': 200, 'msg': 'success', 'access_token': 'Bearer ' + access_token}), 200
