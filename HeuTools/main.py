#-*- encoding:utf8 -*-

import requests
from PIL import Image
from bs4 import BeautifulSoup


class HeuSpider():
    def __init__(self):
        #这里是用到的所有入口及页面地址
        self.urls = {
            'proxy_login':'https://ssl.hrbeu.edu.cn/por/login_psw.csp',
            'office_login':'https://ssl.hrbeu.edu.cn/web/1/http/2/jw.hrbeu.edu.cn/ACTIONLOGON.APPPROCESS?mode=4',
            'office_agnomen':'https://ssl.hrbeu.edu.cn/web/1/http/0/jw.hrbeu.edu.cn/web/0/http/2/jw.hrbeu.edu.cn/ACTIONVALIDATERANDOMPICTURE.APPPROCESS',
        }
        #这里定义请求头
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Accept-Encoding':'gzip, deflate, br',
            'Referer':'https://ssl.hrbeu.edu.cn/por/login_psw.csp',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'Upgrade-Insecure-Requests':'1',
        }

        self.student_id = '2015040524' #学号
        self.student_pw = '392712' #密码
        self.Session = requests.Session()

    def proxy_login(self):
        #创建Session
        session = self.Session
        session.headers.update(self.headers)
        #创建表单
        data_proxy = {
            'svpn_name': self.student_id,
            'svpn_password': self.student_pw,
            'svpn_rand_code': '',
        }
        res = session.post(self.urls['proxy_login'], data=data_proxy,
                           verify=False)
        return session

    def office_login(self, Session):
        #得到验证码
        agnomen_pic = Session.get(self.urls['office_agnomen']).content
        with open('agn.png', 'wb') as pic:
            pic.write(agnomen_pic)
        #打开图片
        img = Image.open('agn.png')
        img.show()
        agnomen = raw_input('your agnomen:')
        #创建表单
        data_office = {
            'WebUserNO': self.student_id,
            'Password': self.student_pw,
            'Agnomen': '',
            'submit.x': '23',
            'submit.y': '2',
        }
        data_office['Agnomen'] = agnomen
        test = Session.post(self.urls['office_login'], data=data_office,
                     verify=False)
        return Session

    def Crawl(self):
        self.office_login(self.proxy_login())

if __name__ == "__main__":
    mySpider = HeuSpider()
    mySpider.Crawl()

