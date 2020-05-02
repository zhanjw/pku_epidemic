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

    # 以下不需要修改
    'sfqwhb14': 'n',  # 14日内是否途径湖北或前往湖北 (y/n)
    'sfjchb14': 'n',  # 14日内是否接触过来自湖北地区的人员 (y/n)
    'sfqwjw14': 'n',  # 14日内是否有境外旅居史 (y/n)
    'sfjcjw14': 'n',  # 14日内是否接触过境外人员 (y/n)

    'jrtw': '36.{}'.format(random.randint(0, 6)),  # 今日体温（如'36.8')
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

sender = ''  # 发送方邮件地址
password = ''  # 密码，一些国内邮件服务提供商可能会要求独立密码
receiver = ''  # 接收方邮件地址，可以与发送方一致
server_addr = ''  # 邮箱的SMTP服务器地址，详见邮箱设置
server_port = 25  # SMTP服务器的端口，默认为25，可不修改
ssl = False  # 是否采用SSL加密，可不修改

logger = create_logger()


def report():
    sess = requests.Session()

    # 登录
    portal_url = 'https://iaaa.pku.edu.cn/iaaa/oauthlogin.do'
    login_data = {'appid': 'portal2017', 'userName': sid, 'password': pwd,
                  'redirUrl': 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'}
    r = sess.post(portal_url, login_data)
    token = json.loads(r.text)['token']

    sess.get('https://portal.pku.edu.cn/portal2017/ssoLogin.do?token=' + token)
    sess.get('https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=epidemic')
    sess.get('https://portal.pku.edu.cn/portal2017/account/insertUserLog.do?portletId=epidemic'
             '&portletName=%E7%87%95%E5%9B%AD%E4%BA%91%E6%88%98%E2%80%9C%E7%96%AB%E2%80%9D')
    r = sess.post('https://ssop.pku.edu.cn/stuAffair/edu/pku/stu/sa/jpf/yqfk/stu/saveMrtb.do',
                  data=info)
    return r.text


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
