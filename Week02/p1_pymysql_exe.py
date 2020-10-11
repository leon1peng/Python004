"""
Python 3.7 连接到 MySQL 数据库的模块推荐使用 pymysql 模块
pip install pymysql

一般流程
开始 -> 创建 connection -> 获取 cursor -> CRUD (查询并获取数据) -> 关闭 cursor -> 关闭 connection -> 结束
"""
import pymysql


DBInfo = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123',
    'db': 'test1'
}

SQL_S = ['select 1', 'select VERSION()']

result = []


class ConnDB(object):
    def __init__(self, db_info, sql_s):
        self.host = db_info['host']
        self.port = db_info['port']
        self.user = db_info['user']
        self.password = db_info['password']
        self.db = db_info['db']
        self.sql_s = sql_s

    def run(self):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            charset='utf8mb4'
        )

        #
        cur = conn.cursor()
        try:
            for command in self.sql_s:
                cur.execute(command)
                result.append(cur.fetchone())
            #
            cur.close()
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        #
        conn.close()


if __name__ == '__main__':
    db = ConnDB(DBInfo, SQL_S)
    db.run()
    print(result)

