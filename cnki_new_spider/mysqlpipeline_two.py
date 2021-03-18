import pymysql
import copy
from twisted.enterprise import adbapi

class MysqlPipelineTwo(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor  # 指定cursor类型
        )
        dbpool = adbapi.ConnectionPool('pymysql',**adbparams)

        return cls(dbpool)

    def process_item(self, item, spider):
        insert_sql = '''INSERT INTO t_cnki_new_8 (key_word,primary_topic,secondary_topic) VALUES ("{key_word}","{primary_topic}","{secondary_topic}");'''
        asyncItem = copy.deepcopy(item)
        query = self.dbpool.runInteraction(self.do_insert, asyncItem, insert_sql)
        query.addCallback(self.handle_error)
        return item

    def do_insert(self, cursor, item, insert_sql):
        sql = insert_sql.format(
            key_word = item['key_word'],
            primary_topic = item['primary_topic'],
            secondary_topic = item['secondary_topic']
        )
        cursor.execute(sql)

    def handle_error(self,failure):
        if failure:
            print('*_**'*25)
            print(failure)