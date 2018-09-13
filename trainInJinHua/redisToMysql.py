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
    engine = create_engine(str(r"mysql+pymysql://%s:%s@%s/%s") %
                           (config['User'],
                            config['Pass'],
                            config['Host'],
                            config['Name']))
    return engine


def redisToMysql(re, en):
    """
    :param re: redis connect
    :param en: mysql engine connect
    :return:
    """
    today = time.strftime("%Y_%m_%d")
    tableName = tool.getFileKey() + '_' + today
    res = []
    index = 0
    for item in re.sscan_iter(tool.getFileKey() + '_' + today):
        tmp = eval(item)
        tmp['time'] = today
        res.append(tmp)
        index += 1
        if index >= 100:
            df = pd.DataFrame(res)
            df.to_sql('respage01', con=en, if_exists='append', index=False)
            index = 0
            res = []
    if index != 0:
        df = pd.DataFrame(res)
        df.to_sql(name='respage01', con=en, if_exists='append', index=False)

    # 添加主键
    # print("xxxxxxxx")
    # with en.connect() as con:
    #     con.execute('ALTER TABLE ' + tableName + ' ADD PRIMARY KEY ("ID");')


def main():
    re = connectRedis()
    en = connectMysql()
    redisToMysql(re, en)


if __name__ == '__main__':
    main()
