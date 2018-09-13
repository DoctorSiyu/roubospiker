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
BaiduAk = tool.getBaiduApiAk()
FileKey = tool.getFileKey()
KeyWord = tool.getKeyWord()
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
    'xNum': 10.0,
    'yNum': 10.0
}


def getSmallRect(bigRect, windowSize, windowIndex):
    """
    获取小矩形的左上角和右下角坐标字符串（百度坐标系） 
    :param bigRect: 关注区域坐标信息
    :param windowSize:  细分窗口数量信息
    :param windowIndex:  Z型扫描的小矩形索引号
    :return: lat,lng,lat,lng
    """
    offset_x = (bigRect['right']['x'] - bigRect['left']['x']) / windowSize['xNum']
    offset_y = (bigRect['right']['y'] - bigRect['left']['y']) / windowSize['yNum']
    left_x = bigRect['left']['x'] + offset_x * (windowIndex % windowSize['xNum'])
    left_y = bigRect['left']['y'] + offset_y * (windowIndex // windowSize['yNum'])
    right_x = (left_x + offset_x)
    right_y = (left_y + offset_y)
    return str(left_y) + ',' + str(left_x) + ',' + str(right_y) + ',' + str(right_x)


def requestBaiduApi(keyWords, smallRect, baiduAk, index, fileKey):
    today = time.strftime("%Y_%m_%d")
    pageNum = 0
    logfile = open("./log/" + fileKey + "-" + today + ".log", 'a+', encoding='utf-8')
    file = open("./result/" + fileKey + "-" + today + ".txt", 'a+', encoding='utf-8')
    while True:
        try:
            URL = "http://api.map.baidu.com/place/v2/search?query=" + keyWords + \
                  "&bounds=" + smallRect + \
                  "&output=json" + \
                  "&ak=" + baiduAk + \
                  "&scope=2" + \
                  "&page_size=20" + \
                  "&page_num=" + str(pageNum)
            resp = requests.get(URL)
            res = json.loads(resp.text)
            if len(res['results']) == 0:
                logfile.writelines(
                    time.strftime("%Y%m%d%H%M%S") + " stop " + str(index) + " " + smallRect + " " + str(pageNum) + '\n')
                break
            else:
                for r in res['results']:
                    file.writelines(str(r).strip() + '\n')
                    # 增加标准输出
                    print(str(r).strip(), flush=True)
            pageNum += 1
            time.sleep(1)
        except:
            logfile.writelines(
                time.strftime("%Y%m%d%H%M%S") + " except " + str(index) + " " + smallRect + " " + str(pageNum) + '\n')
            break


def main():
    for index in range(int(WindowSize['xNum'] * WindowSize['yNum'])):
        smallRect = getSmallRect(BigRect, WindowSize, index)
        requestBaiduApi(keyWords=KeyWord, smallRect=smallRect, baiduAk=BaiduAk, index=index, fileKey=FileKey)
        time.sleep(1)
    sys.stderr.close()


if __name__ == '__main__':
    main()
