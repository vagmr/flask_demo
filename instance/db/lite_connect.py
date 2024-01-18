"""
@文件        :lite_connect.py
@说明        :sqlite数据库 
@时间        :2024/01/17 14:32:14
@作者        :vagmr
@版本        :1.1
"""
from instance.funcs.lite_func import db_sql, db_query


class ItemModel:
    def __init__(self, iid, name, price):
        self.id = iid
        self.name = name
        self.price = price

    def __str__(self):
        return "{'id': %d, 'name': '%s', 'price': %d}" % (self.id, self.name, self.price)

    def to_dict(self):
        return eval(str(self))

    def insert_value(self):
        db_sql("insert into item (id, name, price) values (?, ?, ?)",
               (self.id, self.name, self.price))

    @classmethod
    def find_all(cls):
        query = "select * from item"
        res = db_query(query)
        return [cls(*item) for item in res]

    @classmethod
    def find_by_id(cls, iid):
        query = "select * from item where id = ?"
        res = db_query(query, (iid,))
        if res:
            return cls(*(res[0]))
        else:
            return None

    @classmethod
    def find_by_name(cls, name):
        query = "select * from item where name = ?"
        res = db_query(query, (name,))
        if res:
            return cls(*(res[0]))
        else:
            return None

    @staticmethod
    def create_table():
        sql = "create table if not exists item (id integer primary key, name text unique, price real)"
        db_sql(sql)

    @staticmethod
    def count_rows():
        sql = "select count(*) from item"
        res = db_query(sql)
        print(res)
        return res[0][0]

    @staticmethod
    def update_value(iid, name, price):
        sql = f"update item set name = '{name}',price = {price} where id = {iid}"
        db_sql(sql)

    @staticmethod
    def add_item(iid, name, price):
        sql = f"insert into item (id, name, price) values ({iid}, '{name}', {price})"
        db_sql(sql)

    @staticmethod
    def delete_item(iid):
        sql = f"delete from item where id = {iid}"
        db_sql(sql)


if __name__ == '__main__':
    ItemModel.count_rows()
