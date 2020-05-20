# -*- coding=utf-8 -*-
import requests
import json
import random
from datetime import datetime

from remote import EmailReporter
from log import create_logger

"""
Part I 必需填写
"""

sid = ''  # 学号
pwd = ''  # 密码
health_status = '健康'  # 疫情诊断：健康，医学观察，疑似，确诊，治愈或解除观察

"""
Part II 下面的内容依照个人情况填写

省市区的编号格式 与 身份证前六位的编码格式是对应的，

可以百度“xx省xx市xx区 身份证号码前六位” 来获得。
如北京市海淀区 身份证号码前六位 为 110108
则省编号 = "11" 市编号 = "01" 区编号 = "08"
"""

info = {
    'xh': sid,
    'sfhx': 'n',  # 是否回校 (y/n)

    # 回校需填写
    'hxsj': '',  # 回校时间，格式为“20200409 170200” 2020年4月9日17点02分00秒
    'cfdssm': '',  # 出发地省编号
    'cfddjsm': '',  # 出发地市编号
    'cfdxjsm': '',  # 出发地区编号
    'sflsss': '',  # 是否留宿宿舍 (y/n)
    'sfcx': '',  # 是否出校 (y/n)

    # 不在校需填写
    'dqszdxxdz': '',  # 当前所在地详细地址
    'dqszdsm': '',  # 当前所在地省编号
    'dqszddjsm': '',  # 当前所在地市编号
    'dqszdxjsm': '',  # 当前所在地区编号
    'dqszdgbm': '',  # 当前所在国家

    # 以下不需要修改
    'sfqwhb14': 'n',  # 14日内是否途径湖北或前往湖北 (y/n)
    'sfjchb14': 'n',  # 14日内是否接触过来自湖北地区的人员 (y/n)
    'sfqwjw14': 'n',  # 14日内是否有境外旅居史 (y/n)
    'sfjcjw14': 'n',  # 14日内是否接触过境外人员 (y/n)

    'jrtw': '36.{}'.format(random.randint(2, 8)),  # 今日体温（如'36.8')
    'sfczzz': 'n',  # 是否存在病症
    'jqxdgj': '',  # 行动轨迹
    'qtqksm': '',  # 其他情况说明
    'tbrq': datetime.now().strftime('%Y%m%d'),  # 填报日期，自动生成
    'yqzd': health_status,  # 疫情诊断

    'dwdzxx': '',  # 定位地址信息
    'dwjd': '',  # 定位经度
    'dwwd': '',  # 定位纬度
    'sfdrfj': '',
    'chdfj': '',
    'jkm': '绿码',  # 健康码状态
    'simstoken': '',
}

"""
Part III 配置邮件自动汇报结果

需要开启邮箱的SMTP功能
"""
use_email_reporter = False
debug = False

sender = '@163.com'  # 发送方邮件地址
password = ''  # 密码，一些国内邮件服务提供商可能会要求独立密码
receiver = '@qq.com'  # 接收方邮件地址，可以与发送方一致
server_addr = 'smtp.163.com'  # 邮箱的SMTP服务器地址，详见邮箱设置
server_port = 25  # SMTP服务器的端口，默认为25，可不修改
ssl = False  # 是否采用SSL加密，可不修改

logger = create_logger()


def report():
    sess = requests.Session()
    browser_headers = {
        'Host': 'iaaa.pku.edu.cn',
        'DNT': '1',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
        'Referer': 'https://portal.pku.edu.cn/portal2017/',
        'Sec-Fetch-User': '?1',
        'Cookie': 'JSESSIONID=0',
    }
    default_headers = sess.headers

    if debug:
        print(default_headers)
        print(browser_headers)

    # 模拟浏览器请求，idea by https://github.com/pkucode/pku_epidemic.git
    sess.headers = browser_headers
    if debug: print('==========1==========')
    cookie_url = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=portal2017&appName=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E6%A0%A1%E5%86%85%E4%BF%A1%E6%81%AF%E9%97%A8%E6%88%B7%E6%96%B0%E7%89%88&redirectUrl=https://portal.pku.edu.cn/portal2017/ssoLogin.do'
    res = sess.get(cookie_url)
    if debug:
        print(res)  # 状态码
        print(sess.headers)  # 请求头
        print(res.headers)  # 响应头
        print(sess.cookies)  # Cookies

    # 登录拿token
    if debug: print('==========2==========')
    portal_url = 'https://iaaa.pku.edu.cn/iaaa/oauthlogin.do'
    login_data = {'appid': 'portal2017', 'userName': sid, 'password': pwd,
                  'redirUrl': 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'}
    res = sess.post(portal_url, data=login_data)
    token = json.loads(res.text)['token']
    if debug:
        print(res)  # 状态码
        print(sess.headers)  # 请求头
        print(res.headers)  # 响应头
        print(sess.cookies)  # Cookies
        print(token)  # Token

    # token换portal的cookie
    if debug: print('==========3==========')
    sess.headers['Host'] = 'portal.pku.edu.cn'
    ssoLogin_url = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do?token=' + token
    res = sess.get(ssoLogin_url)
    if debug:
        print(res)  # 状态码
        print(sess.headers)  # 请求头
        print(res.headers)  # 响应头
        print(sess.cookies)  # Cookies
    # 不给个cookie的placeholder的话，portal的cookie拿不到，现在拿到了就没用了，删掉防止冲突
    del sess.headers['Cookie']

    # 再用portal的cookie去搞个ssop的cookie
    if debug: print('==========4==========')
    sess.headers = default_headers
    ep_url = 'https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=epidemic'
    res = sess.get(ep_url)
    if debug:
        print(res)  # 状态码
        print(sess.headers)  # 请求头
        print(res.headers)  # 响应头
        print(sess.cookies)  # Cookies

    # 不知道干啥的，看流程中有，原版也有，就不分析了
    if debug: print('==========5==========')
    link0 = "https://portal.pku.edu.cn/portal2017/account/insertUserLog.do?portletId=epidemic&portletName=%E7%87%95%E5%9B%AD%E4%BA%91%E6%88%98%E2%80%9C%E7%96%AB%E2%80%9D"
    res = sess.get(link0)
    if debug:
        print(res)  # 状态码
        print(sess.headers)  # 请求头
        print(res.headers)  # 响应头
        print(sess.cookies)  # Cookies

    # 保存表单
    if debug: print('==========6==========')
    Tb_url = "https://ssop.pku.edu.cn/stuAffair/edu/pku/stu/sa/jpf/yqfk/stu/saveMrtb.do"
    res = sess.post(Tb_url, data=info)
    if debug:
        print(res)  # 状态码
        print(sess.headers)  # 请求头
        print(res.headers)  # 响应头
        print(sess.cookies)  # Cookies

    return res.text


if __name__ == '__main__':
    try:
        result = report()
        content = '填报成功。返回值：' + result
    except Exception as e:
        content = '填报失败。错误内容：' + str(e)
    logger.info(content)
    if use_email_reporter:
        reporter = EmailReporter(sender, password, receiver, server_addr, server_port, ssl)
        reporter.login()
        reporter.send(content, '燕园云战“疫” ' + datetime.now().strftime('%Y%m%d'))
        reporter.exit()
