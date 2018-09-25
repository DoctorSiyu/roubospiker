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
    today = time.strftime("%Y_%m_%d")
    res = []
    index = 0
    need_append = False
    for item in re.sscan_iter(redis_key):
        tmp = eval(item.encode('utf-8').decode('utf-8'))
        tmp['time'] = today
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
        print('add id error')


def getKeyList(re):
    """
    获取所有的key的列表
    :return:
    """
    return re.keys(tool.getFileKey() + "_*")


def getKeyListExceptToday(re):
    """
    获取除了今天以外的所有key的列表
    :return:
    """
    today = time.strftime("%Y_%m_%d")
    keyList = re.keys(tool.getFileKey() + '_*')
    try:
        keyList.remove(tool.getFileKey() + '_' + today)
    except Exception as e:
        pass
    return keyList


def getUnionData(re):
    """
    获得所有数据的并集并保存到trainunion中
    :param re:
    :return:
    """
    keyList = getKeyList(re)
    re.sunionstore(tool.getFileKey() + 'union', keyList)
    try:
        re.delete(tool.getFileKey() + 'unionmp')
    except Exception as e:
        pass
    finally:
        re.sunionstore(tool.getFileKey() + 'uniontmp', getKeyListExceptToday(re))


def getNewDiffData(re):
    """
    获取新增的数据
    :param re:
    :return:
    """
    today = time.strftime("%Y_%m_%d")
    if 'train_' + today in getKeyList(re):
        re.delete(tool.getFileKey() + 'new')
        re.sdiffstore(tool.getFileKey() + 'new', tool.getFileKey() + '_' + today, tool.getFileKey() + 'uniontmp')
    else:
        pass


def getGoneDiffData(re):
    """
    获取消失的数据
    :param re:
    :return:
    """
    today = time.strftime("%Y_%m_%d")
    if tool.getFileKey() + '_' + today in getKeyList(re):
        re.delete(tool.getFileKey() + 'gone')
        re.sdiffstore(tool.getFileKey() + 'gone', tool.getFileKey() + 'union', tool.getFileKey() + '_' + today)
    else:
        pass


def main():
    today = time.strftime("%Y_%m_%d")
    todayKey = tool.getFileKey() + '_' + today
    newKey = tool.getFileKey() + 'new'
    goneKey = tool.getFileKey() + 'gone'
    unionKey = tool.getFileKey() + 'union'
    re = connectRedis()
    en = connectMysql()
    getUnionData(re)
    getGoneDiffData(re)
    getNewDiffData(re)
    # 将今日数据写入mysql
    redisToMysql(re, en, todayKey, 'respage01', True)
    # 将今日新增数据写入mysql
    redisToMysql(re, en, newKey, 'respage01New', False)
    # 将今日消失数据写入mysql
    redisToMysql(re, en, goneKey, 'respage01Gone', False)
    # 将并集数据写入mysql
    redisToMysql(re, en, unionKey, 'respage01Union', False)


if __name__ == '__main__':
    main()
