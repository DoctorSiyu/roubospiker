# coding: utf-8
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from tool.tool import tool
from sqlalchemy import create_engine


def connectMysql():
    """
    连接mysql数据库
    :return: engine connect
    """
    config = tool.getMysqlConfig()
    engine = create_engine(str(r"mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4") %
                           (config['User'],
                            config['Pass'],
                            config['Host'],
                            config['Name']))
    return engine


def writeToMysql(en, mysql_table, is_append, data):
    """
    :param en: mysql engine connect
    :param mysql_table: mysql engine connect
    :param data: data
    :return:
    """
    df = pd.DataFrame(data)
    if is_append:
        df.to_sql(name=mysql_table, con=en, if_exists='append', index=False)
    else:
        df.to_sql(name=mysql_table, con=en, if_exists='replace', index=False)
    try:
        with en.connect() as con:
            con.execute("alter table " + mysql_table + " add COLUMN id INT NOT NULL AUTO_INCREMENT  primary key first")
    except Exception as e:
        print('add id pass')


def doOAuth():
    """
    获取 Oauth2 的 token
    :return: token
    """
    config = tool.getProductHuntConfig()
    token = tool.getOAuth2Token(client_id=config['Client_Id'],
                                client_secret=config['Client_Secret'],
                                token_url=config['Token_Url'])
    return token[u'access_token']


def getTechPostsByPage(token, page):
    """
    按页获取内容
    :param token:
    :param page:
    :return:
    """
    data = {
        'page': page,
    }
    header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "Host": "api.producthunt.com"
    }
    res = requests.get('https://api.producthunt.com/v1/posts', params=data, headers=header)
    print(res.text)


def getMostUpvotedPostByDay(token, year, month, day):
    """
    获取自从某天以来的以天为单位的热门排行
    :param token:
    :param year:
    :param month:
    :param day:
    :return:
    """
    data = {
        'search[featured_year]': year,
        'search[featured_month]': month,
        'search[featured_day]': day,
        'sort_by': 'votes_count',
        'order': 'desc'
    }
    header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "Host": "api.producthunt.com"
    }
    resp = requests.get('https://api.producthunt.com/v1/posts/all', params=data, headers=header)
    if resp.status_code == 200:
        res = []
        for item in json.loads(resp.text)['posts']:
            res.append({
                'comments_count': item['comments_count'],
                'day': item['day'],
                'phid': item['id'],
                'name': item['name'],
                'tagline': item['tagline'],
                'slug': item['slug'],
                'votes_count': item['votes_count'],
                'category_id': item['category_id'],
                'created_at': item['created_at'],
                'discussion_url': item['discussion_url'],
                'image_url': item['thumbnail']['image_url'],
                'user_id': item['user']['id'],
                'user_name': item['user']['name'],
                'user_twitter_username': item['user']['twitter_username'],
                'user_website_url': item['user']['website_url'],
                'profile_url': item['user']['profile_url'],
                'days': str(year) + '-' + str(month) + '-' + str(day)
            })
    return res


def getMostUpvotedPostByMonth(token, year, month):
    """
    获取自从某月以来的以月为单位的热门排行
    :param token:
    :param year:
    :param month:
    :return:
    """

    data = {
        'search[featured_year]': year,
        'search[featured_month]': month,
        'sort_by': 'votes_count',
        'order': 'desc'
    }
    header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "Host": "api.producthunt.com"
    }
    resp = requests.get('https://api.producthunt.com/v1/posts/all', params=data, headers=header)
    if resp.status_code == 200:
        res = []
        for item in json.loads(resp.text)['posts']:
            res.append({
                'comments_count': item['comments_count'],
                'day': item['day'],
                'phid': item['id'],
                'name': item['name'],
                'tagline': item['tagline'],
                'slug': item['slug'],
                'votes_count': item['votes_count'],
                'category_id': item['category_id'],
                'created_at': item['created_at'],
                'discussion_url': item['discussion_url'],
                'image_url': item['thumbnail']['image_url'],
                'user_id': item['user']['id'],
                'user_name': item['user']['name'],
                'user_twitter_username': item['user']['twitter_username'],
                'user_website_url': item['user']['website_url'],
                'profile_url': item['user']['profile_url'],
                'month': str(year) + '-' + str(month)
            })
    return res


def getPostDetail(token, id):
    """
    获取详情
    :param token:
    :param id:
    :return:
    """
    header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "Host": "api.producthunt.com"
    }
    res = requests.get('https://api.producthunt.com/v1/posts/' + id, headers=header)
    print(res.text)


def getRangeMonths():
    """
    获取月列表
    :return:
    """
    res = []
    now = datetime.now().month
    for i in range(1, now + 1):
        res.append((2018, i))
    return res


def getRangeDays(begin_date, end_date):
    dates = []
    dt = datetime.strptime(begin_date, "%Y-%m-%d")
    date = begin_date[:]
    while date <= end_date:
        dates.append((dt.year, dt.month, dt.day))
        dt += timedelta(days=1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def main():
    en = connectMysql()
    token = doOAuth()

    is_append = False
    for year, month in getRangeMonths():
        data = getMostUpvotedPostByMonth(token, year=year, month=month)
        if len(data) != 0:
            writeToMysql(en=en, mysql_table='ph_month_top', is_append=is_append, data=data)
            is_append = True

    is_append = False
    for year, month, day in getRangeDays('2018-01-01', datetime.today().strftime('%Y-%m-%d')):
        data = getMostUpvotedPostByDay(token, year, month, day)
        if len(data) != 0:
            writeToMysql(en=en, mysql_table='ph_day_top', is_append=is_append, data=data)
            is_append = True


if __name__ == '__main__':
    main()
