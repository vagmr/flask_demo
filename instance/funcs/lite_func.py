"""
@文件        :lite_func.py
@说明        :sqlite数据库的通用函数 
@时间        :2024/01/17 14:55:06
@作者        :vagmr
@版本        :1.1
@详细文档    :
"""


import sqlite3
from typing import Any, List, Tuple, Union, Optional


def db_sql(sql: str, data: Optional[Union[Tuple, List[Tuple]]] = None, database: str = 'data.db') -> None:
    """
    执行指定数据库上的给定SQL语句。

    参数:
        sql (str): 要执行的SQL语句。
        data (Optional[Union[Tuple, List[Tuple]]]): 传递给SQL语句的数据。此参数为可选，默认为None。
        database (str): 要连接的数据库名称。此参数为可选，默认为'data.db'。

    返回:
        None

    异常:
        sqlite3.Error: 执行SQL语句时发生错误。
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    try:
        if data is None:
            cursor.execute(sql)
        elif isinstance(data, list):
            cursor.executemany(sql, data)
        else:
            cursor.execute(sql, data)
        print("执行成功")
        connection.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()


def db_query(sql: str, data: Optional[Tuple] = None, database: str = 'data.db') -> List[Tuple[Any, ...]]:
    """
    执行 SQL 查询并返回获取的结果。

    参数:
        sql (str): 要执行的 SQL 查询语句。
        data (Optional[Tuple]): SQL 查询的可选参数元组。
        database (str): 要连接的数据库文件。

    返回值:
        List[Tuple]: 表示查询结果的元组列表。
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    try:
        if data is not None:
            cursor.execute(sql, data)
        else:
            cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
