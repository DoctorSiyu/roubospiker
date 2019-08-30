# coding: utf-8
import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


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

    def getProductHuntConfig(self):
        return self.config["ProductHunt"]

    def getOAuth2Token(self, client_id, client_secret, token_url):
        """
        获取 Oauth Token 获取
        :param client_id:
        :param client_secret:
        :param token_url:
        :return:
        """
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
        return token

    def printAsJSON(self, out):
        if isinstance(out, str):
            print(json.dumps(eval(out.replace('\"', '"')), indent=4))
        else:
            print(json.dumps(out, indent=4))


tool = Tool()
