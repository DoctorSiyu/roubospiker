# coding: utf-8
import json


class Tool(object):
    config = {}

    def __init__(self):
        with open("./config.json", "r", encoding='utf-8') as f:
            self.config = json.load(f)

    def getBaiduApiAk(self):
        return self.config['BaiduAk']

    def getFileKey(self):
        return self.config['FileKey']

    def getKeyWord(self):
        return self.config['KeyWord']

    def getRedisHost(self):
        return self.config['RedisHost']

    def getRedisPass(self):
        return self.config['RedisPass']

    def getRedisPort(self):
        return self.config['RedisPort']

    def getMysqlConfig(self):
        return self.config["MysqlConf"]


tool = Tool()
