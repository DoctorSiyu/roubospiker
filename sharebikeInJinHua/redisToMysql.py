# coding: utf-8
import redis
from tool.tool import tool
import time
import pandas as pd
from sqlalchemy import create_engine
import pymysql


def connectRedis():
    """
    连接Redis
    :return: redis connect
    """
    re = redis.Redis(
        host=tool.getRedisHost(),
        port=tool.getRedisPort(),
        password=tool.getRedisPass(),
        decode_responses=True)
    return re


def connectMysql():
    """
    连接mysql数据库
    :return: engine connect
    """
    config = tool.getMysqlConfig()
    engine = create_engine(str(r"mysql+pymysql://%s:%s@%s/%s?charset=utf8") %
                           (config['User'],
                            config['Pass'],
                            config['Host'],
                            config['Name']))
    return engine


def redisToMysql(re, en, redis_key, mysql_table, is_append):
    """
    :param re: redis connect
    :param en: mysql engine connect
    :param redis_key: mysql engine connect
    :param mysql_table: mysql engine connect
    :return:
    """
    now = time.strftime("%Y_%m_%d_%H")
    res = []
    index = 0
    need_append = False
    for item in re.sscan_iter(redis_key):
        tmp = eval(item.encode('utf-8').decode('utf-8'))
        res.append(tmp)
        index += 1
        if index >= 100:
            df = pd.DataFrame(res)
            if is_append or need_append:
                df.to_sql(mysql_table, con=en, if_exists='append', index=False)
            else:
                df.to_sql(mysql_table, con=en, if_exists='replace', index=False)
            need_append = True
            index = 0
            res = []
    if index != 0:
        df = pd.DataFrame(res)
        if need_append:
            df.to_sql(name=mysql_table, con=en, if_exists='append', index=False)
        else:
            df.to_sql(name=mysql_table, con=en, if_exists='replace', index=False)

    try:
        with en.connect() as con:
            con.execute("alter table " + mysql_table + " add COLUMN id INT NOT NULL AUTO_INCREMENT  primary key first")
    except Exception as e:
        print('add id pass')


def main():
    today = time.strftime("%Y_%m_%d")
    todayKey = tool.getFileKey() + '_' + today
    re = connectRedis()
    en = connectMysql()
    # 将今日数据写入mysql
    redisToMysql(re, en, todayKey, 'respage02', True)


if __name__ == '__main__':
    main()
