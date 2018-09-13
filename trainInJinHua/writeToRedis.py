# coding: utf-8
import fileinput
import redis
import time
from tool.tool import tool
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


def connectRedis():
    re = redis.Redis(
        host=tool.getRedisHost(),
        port=tool.getRedisPort(),
        password=tool.getRedisPass(),
        decode_responses=True)
    return re


def main():
    today = time.strftime("%Y_%m_%d")
    setName = tool.getFileKey() + "_" + today
    try:
        re = connectRedis()
        for line in fileinput.input(mode='rb'):
            re.sadd(setName, line.decode('utf-8').strip())
        exit(0)
    except Exception as e:
        print(e)
        exit(-1)

if __name__ == '__main__':
    main()
