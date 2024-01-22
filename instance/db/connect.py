from flask_sqlalchemy import SQLAlchemy
from util.getEnv import init_env, get_env

db = SQLAlchemy()

init_env()


class DatabaseConfig:
    """数据配置类"""
    DB_TYPE = 'mysql'
    DB_USER = 'vagmr'
    DB_PASSWORD = get_env('DB_PASSWORD')
    DB_HOST = get_env('DB_HOST')
    DB_NAME = 'vagmr$flask'
    SQLALCHEMY_DATABASE_URI = f'{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLAlchemy_TRACK_MODIFICATIONS = False


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def create_role(cls, name):
        role = cls(name=name)
        db.session.add(role)
        db.session.commit()
        return role


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        role = Role.query.get(self.role_id)
        return {
            'id': self.id,
            'username': self.username,
            'role': role.name
        }


class Saying(db.Model):
    __tablename__ = 'saying'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))

    def __str__(self):
        return "{'id': %d, 'content': '%s'}" % (self.id, self.content)

    # 用于打印
    def __repr__(self):
        return self.__str__()

    # 转化为字典
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content
        }

    @classmethod
    def create_saying(cls, content):
        saying = cls(content=content)
        db.session.add(saying)
        db.session.commit()
        return saying
