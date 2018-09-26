# coding: utf-8
import requests
import json
import time
from tool.tool import tool
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

"""
    查询关键字：
"""
FileKey = tool.getFileKey()
"""
    关注区域的左下角和右上角百度地图坐标
"""
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
    定义细分窗口的数量，横向X * 纵向Y
"""
WindowSize = {
    'xNum': 20.0,
    'yNum': 20.0
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


def requestMBikeApi(lat, lng, index, fileKey):
    today = time.strftime("%Y_%m_%d_%H")
    logfile = open("./log/" + fileKey + "-" + today + ".log", 'a+', encoding='utf-8')
    file = open("./result/" + fileKey + "-" + today + ".txt", 'a+', encoding='utf-8')
    try:
        URL = "https://mwx.mobike.com/nearby/nearbyBikeInfo?biketype=0" + \
              "&latitude=" + lat + \
              "&longitude=" + lng + \
              "&userid=56971952127272093696470926" + \
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
        time.sleep(10)
    except:
        logfile.writelines(
            time.strftime("%Y%m%d%H%M%S") + " except " + str(index) + " " + str(lat) + " " + str(lng) + '\n')
        time.sleep(10)


def main():
    for index in range(int(WindowSize['xNum'] * WindowSize['yNum'])):
        print('---------------')
        print(index)
        print('---------------')
        lng, lat = getSmallRect(BigRect, WindowSize, index)
        requestMBikeApi(lat=lat, lng=lng, index=index, fileKey=FileKey)
    sys.stderr.close()


if __name__ == '__main__':
    main()
