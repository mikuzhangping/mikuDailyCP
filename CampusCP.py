import sys
import requests
import json
import time
import datetime
import pytz
import base64
from Crypto.Cipher import AES
from requests.sessions import session


class hfuter:
    def __init__(self, username, password) -> None:
        super().__init__()

        self.session = requests.session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
            "Accept": "application/json, text/plain, */*",
        })

        self.username = username
        self.password = password

        ret = self.__login()
        if ret:
            print("{username}登录成功".format(username=self.username))
            self.logged_in = True
        else:
            print("{username}登录失败！".format(username=self.username))
            self.logged_in = False

    def __login(self) -> bool:
        def encrypt_password(text: str, key: str):
            """encrypt password"""
            def pad(data_to_pad, block_size, style='pkcs7'):
                """Apply standard padding.
                Args:
                data_to_pad (byte string):
                    The data that needs to be padded.
                block_size (integer):
                    The block boundary to use for padding. The output length is guaranteed
                    to be a multiple of :data:`block_size`.
                style (string):
                    Padding algorithm. It can be *'pkcs7'* (default), *'iso7816'* or *'x923'*.
                Return:
                byte string : the original data with the appropriate padding added at the end.
                """
                def bchr(s):
                    return bytes([s])

                padding_len = block_size-len(data_to_pad) % block_size
                if style == 'pkcs7':
                    padding = bchr(padding_len)*padding_len
                elif style == 'x923':
                    padding = bchr(0)*(padding_len-1) + bchr(padding_len)
                elif style == 'iso7816':
                    padding = bchr(128) + bchr(0)*(padding_len-1)
                else:
                    raise ValueError("Unknown padding style")
                return data_to_pad + padding
            key = key.encode('utf-8')
            text = text.encode('utf-8')

            text = pad(text, len(key), style='pkcs7')

            aes = AES.new(key, AES.MODE_ECB)
            password = aes.encrypt(text)
            password = base64.b64encode(password)
            return password

        ret = self.session.get("https://cas.hfut.edu.cn/cas/login")
        # JSESSIONID
        ret = self.session.get('https://cas.hfut.edu.cn/cas/vercode')
        # check if needs Vercode
        millis = int(round(time.time() * 1000))
        ret = self.session.get(
            'https://cas.hfut.edu.cn/cas/checkInitVercode', params={'_': millis})
        key = ret.cookies['LOGIN_FLAVORING']

        if ret.json():
            # needs OCR! will be done later.
            print('需验证码，目前该功能此脚本未支持')
            return False
        else:
            print('无需验证码')

        # 加密密码
        password = encrypt_password(self.password, key)

        # 先get
        ret = self.session.get(
            'https://cas.hfut.edu.cn/cas/policy/checkUserIdenty',
            params={'_': millis+1, 'username': self.username, 'password': password})

        ret = ret.json()

        # 判断是否成功
        if ret['msg'] != 'success' and not ret['data']['authFlag']:
            return False

        if ret['data']['mailRequired'] or ret['data']['phoneRequired']:
            print("你需要先进行手机或者邮箱的认证，请在PC上打开cas.hfut.edu.cn页面进行登录之后才可使用此脚本")
            return False

        # 然后post
        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"})
        ret = self.session.post(
            'https://cas.hfut.edu.cn/cas/login',
            data={
                'username': self.username,
                'capcha': "",
                'execution': "e1s1",
                '_eventId': "submit",
                'password': password,
                'geolocation': "",
                'submit': "登录"
            })
        self.session.headers.pop("Content-Type")

        if ret.text.find("cas协议登录成功跳转页面") != -1:
            return True
        else:
            return False

    def basic_infomation(self):
        if not self.logged_in:
            return {}

        self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/swmjbxxapp/*default/index.do")

        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        })
        self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/welcomeAutoIndex.do"
        )
        self.session.headers.pop("Content-Type")
        self.session.headers.pop("X-Requested-With")

        ret = self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/casValidate.do",
            params={
                'service': '/xsfw/sys/swmjbxxapp/*default/index.do'
            }
        )

        self.session.headers.update({"X-Requested-With": "XMLHttpRequest"})
        self.session.headers.update(
            {"Referer": "http://stu.hfut.edu.cn/xsfw/sys/swmjbxxapp/*default/index.do"})
        ret = self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/emappagelog/config/swmjbxxapp.do")
        self.session.headers.pop("X-Requested-With")

        config_data = {"APPID": "4930169432823497", "APPNAME": "swmjbxxapp"}
        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"})
        ret = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getSelRoleConfig.do",
            data={"data": json.dumps(config_data)}
        ).json()
        if ret["code"] != "0":
            print(ret["msg"])
            return {}
        ret = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getMenuInfo.do",
            data={"data": json.dumps(config_data)}
        ).json()
        if ret["code"] != "0":
            print(ret["msg"])
            return {}
        self.session.headers.pop("Content-Type")

        info = self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/swmjbxxapp/StudentBasicInfo/initPageConfig.do", params={"data": "{}"}).json()
        self.session.headers.pop("Referer")

        return info['data']

    def daily_checkin(self) -> bool:
        if not self.logged_in:
            return False

        today = datetime.datetime.now(
            tz=pytz.timezone('Asia/Shanghai')).timetuple()[:3]
        self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/*default/index.do")

        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        })
        self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/welcomeAutoIndex.do"
        )
        self.session.headers.pop("Content-Type")
        self.session.headers.pop("X-Requested-With")

        ret = self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/casValidate.do",
            params={
                'service': '/xsfw/sys/swmjbxxapp/*default/index.do'
            }
        )

        self.session.headers.update({"X-Requested-With": "XMLHttpRequest"})
        self.session.headers.update(
            {"Referer": "http://stu.hfut.edu.cn/xsfw/sys/swmjbxxapp/*default/index.do"})
        ret = self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/emappagelog/config/swmxsyqxxsjapp.do")
        self.session.headers.pop("X-Requested-With")

        config_data = {"APPID": "5811260348942403",
                       "APPNAME": "swmxsyqxxsjapp"}
        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"})
        ret = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getSelRoleConfig.do",
            data={"data": json.dumps(config_data)}
        ).json()
        if ret["code"] != "0":
            print(ret["msg"])
            return False
        ret = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getMenuInfo.do",
            data={"data": json.dumps(config_data)}
        ).json()
        if ret["code"] != "0":
            print(ret["msg"])
            return False
        self.session.headers.pop("Content-Type")

        info = self.session.get(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getSetting.do",
            data={"data": "{}"}
        ).json()

        start_time = "%04d-%02d-%02d " % today + \
            info['data']['DZ_TBKSSJ'] + " +0800"
        start_time = datetime.datetime.strptime(
            start_time, "%Y-%m-%d %H:%M:%S %z")
        end_time = "%04d-%02d-%02d " % today + \
            info['data']['DZ_TBJSSJ'] + " +0800"
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S %z")
        now_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))

        print("打卡起始时间:", start_time)
        print("打卡结束时间:", end_time)
        print("　　现在时间:", now_time)
        if start_time < now_time and now_time < end_time:
            print("在打卡时间内")
        else:
            print("不在打卡时间内")
            return False

        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"})
        last_form = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getStuXx.do",
            data={"data": json.dumps({"TBSJ": "%.2d-%.2d-%.2d" % today})}
        ).json()
        if last_form['code'] != "0":
            return False

        new_form = last_form['data']
        new_form.update({
            "DZ_SFSB": "1",
            "GCKSRQ": "",
            "GCJSRQ": "",
            "DFHTJHBSJ": "",
            "BY1": "1",
            "TBSJ": "%.2d-%.2d-%.2d" % today
        })

        ret = self.session.post(
            "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/saveStuXx.do",
            data={"data": json.dumps(new_form)}
        ).json()

        self.session.headers.pop("Content-Type")
        self.session.headers.pop("Referer")
        return ret['code'] == "0"


if __name__ == "__main__":

    i = 1
    while i < len(sys.argv):
        print(sys.argv[i])
        stu = hfuter(username=sys.argv[i], password=sys.argv[i+1])
        if stu.daily_checkin():
            print("签到成功~")
        else:
            print("签到失败！")
        print()
        i+=2
