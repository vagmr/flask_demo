from flask import Flask, render_template, jsonify
from App.router.user import user_router
from App.router.saying import saying_router
from App.router.item import item_router
from instance.db.connect import db, DatabaseConfig
from util.getEnv import init_env, get_env
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__, template_folder="App/templates",
            static_folder="App/static")
# 初始化环境变量
init_env()
# 配置JWT
app.config['JWT_SECRET_KEY'] = get_env('KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(get_env('EXPIREDTIME')))
jwt = JWTManager(app)

app.register_blueprint(user_router)
app.register_blueprint(saying_router)
app.register_blueprint(item_router)

app.config.from_object(DatabaseConfig)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', err=error), 404


@app.route("/")
def index():
    return render_template("index.html")


@app.get('/cs')
@jwt_required()
def cs():
    # 获取到的是用户的id
    uid = get_jwt_identity()
    return jsonify({'code': 200, 'msg': 'success', 'data': {'id': uid}}), 200


if __name__ == '__main__':
    app.run(debug=True)
