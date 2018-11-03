# coding: utf-8
import requests
import json
import time
from tool.tool import tool
import io
import sys
import multiprocessing

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

"""
    查询关键字：
"""
FileKey = tool.getFileKey()
"""
    关注区域的左下角和右上角百度地图坐标
    全市：
    BigRect = {
    'left': {
        'x': 119.58962425017401,
        'y': 29.02371358317696
    },
    'right': {
        'x': 119.787499394624553,
        'y': 29.149153586357146
    }
}
"""
BigRect1 = {
    'left': {
        'x': 119.634998,
        'y': 29.046372
    },
    'right': {
        'x': 119.6727628,
        'y': 29.077628
    }
}

BigRect2 = {
    'left': {
        'x': 119.628268,
        'y': 29.072232
    },
    'right': {
        'x': 119.67208,
        'y': 29.098397
    }
}

"""
    定义细分窗口的数量，横向X * 纵向Y
"""
WindowSize = {
    'xNum': 30.0,
    'yNum': 30.0
}


def getSmallRect(bigRect, windowSize, windowIndex):
    """
    获取小矩形的中心点的坐标（百度坐标系）
    :param bigRect: 关注区域坐标信息
    :param windowSize:  细分窗口数量信息
    :param windowIndex:  Z型扫描的小矩形索引号
    :return: lat,lng
    """
    offset_x = (bigRect['right']['x'] - bigRect['left']['x']) / windowSize['xNum']
    offset_y = (bigRect['right']['y'] - bigRect['left']['y']) / windowSize['yNum']
    left_x = bigRect['left']['x'] + offset_x * (windowIndex % windowSize['xNum'])
    left_y = bigRect['left']['y'] + offset_y * (windowIndex // windowSize['yNum'])
    middle_x = (left_x + offset_x / 2)
    middle_y = (left_y + offset_y / 2)
    return str(middle_x), str(middle_y)


def requestMBikeApi(lat, lng, index, file, logfile, userId):
    try:
        URL = "https://mwx.mobike.com/nearby/nearbyBikeInfo?biketype=0" + \
              "&latitude=" + lat + \
              "&longitude=" + lng + \
              "&userid=" + userId + \
              "&citycode=0579"
        resp = requests.get(URL)
        res = json.loads(resp.text)
        if len(res['object']) == 0:
            logfile.writelines(
                time.strftime("%Y%m%d%H%M%S") + " stop " + str(index) + " " + str(lat) + " " + str(lng) + '\n')
        else:
            for r in res['object']:
                file.writelines(str(r).strip() + '\n')
                # 增加标准输出
                print(str(r).strip(), flush=True)
        time.sleep(1)
    except:
        logfile.writelines(
            time.strftime("%Y%m%d%H%M%S") + " except " + str(index) + " " + str(lat) + " " + str(lng) + '\n')
        time.sleep(1)


def worker(bigrect, userId, FileKey):
    today = time.strftime("%Y_%m_%d_%H")
    for count in range(0, 10):
        logfile = open("./log/" + FileKey + "-" + str(count) + '_' + today + ".log", 'a+', encoding='utf-8')
        file = open("./result/" + FileKey + "-" + str(count) + '_' + today + ".txt", 'a+', encoding='utf-8')
        for index in range(int(WindowSize['xNum'] * WindowSize['yNum'])):
            print('---------------')
            print(index)
            print('---------------')
            lng, lat = getSmallRect(bigrect, WindowSize, index)
            requestMBikeApi(lat=lat, lng=lng, index=index, file=file, logfile=logfile, userId=userId)
        time.sleep(1200)
    sys.stderr.close()


def main():
    # for index in range(int(WindowSize['xNum'] * WindowSize['yNum'])):
    #     print('---------------')
    #     print(index)
    #     print('---------------')
    #     lng, lat = getSmallRect(BigRect, WindowSize, index)
    #     requestMBikeApi(lat=lat, lng=lng, index=index, fileKey=FileKey)
    # sys.stderr.close()
    userIds = tool.getMBikeUserID()
    p1 = multiprocessing.Process(target=worker, name='p1', args=(BigRect1, userIds[0], 'shareBike01'))
    p2 = multiprocessing.Process(target=worker, name='p2', args=(BigRect2, userIds[1], 'shareBike02'))
    p1.start()
    p2.start()


if __name__ == '__main__':
    main()
