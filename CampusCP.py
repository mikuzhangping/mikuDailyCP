import sys
import requests
import json
import time


def login(session_temp, username, password):
    session_temp.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/plain, */*",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded"
    })

    referer = "http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/pages/funauth-login.do?service=%2Fxsfw%2Fsys" \
              "%2Fswmxsyqxxsjapp%2F*default%2Findex.do "
    session_temp.get(
        "http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/pages/funauth-login.do?service=%2Fxsfw%2Fsys%2Fswmxsyqxxsjapp%2F"
        "*default%2Findex.do")

    # loginValidate
    session_temp.headers.update({"Referer": referer})
    session_temp.post("http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/loginValidate.do",
                      data={"userName": username, "password": password, "isWeekLogin": "false"})

    # redirect
    session_temp.get(
        "http://stu.hfut.edu.cn/xsfw/sys/emaphome/redirect.do?service=%2Fxsfw%2Fsys%2Fswmxsyqxxsjapp%2F*default"
        "%2Findex.do")

    # appShow
    session_temp.get("http://stu.hfut.edu.cn/xsfw/sys/emaphome/appShow.do?name=swmxsyqxxsjapp")

    # getSelRoleConfig
    session_temp.headers.update(
        {"Accept": "application/json, text/plain, */*",
         "Referer": "http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/*default/index.do?THEME=cherry&EMAP_LANG=zh"})
    session_temp.post("http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getSelRoleConfig.do",
                      data={"data": json.dumps(
                          {"APPID": "5811260348942403", "APPNAME": "swmxsyqxxsjapp"})})  # 此处APPID是否为静态内容存疑

    # swmxsyqxxsjapp
    session_temp.get("http://stu.hfut.edu.cn/xsfw/sys/emappagelog/config/swmxsyqxxsjapp.do")

    # getMenuInfo
    session_temp.headers.update(
        {"Accept": "application/json, text/plain, */*"})
    ret = session_temp.post("http://stu.hfut.edu.cn/xsfw/sys/swpubapp/MobileCommon/getMenuInfo.do",
                            data={"data": json.dumps(
                                {"APPID": "5811260348942403", "APPNAME": "swmxsyqxxsjapp"})})  # 此处APPID是否为静态内容存疑
    ret = json.loads(ret.text)
    return ret["code"]
    pass


def fill_form(session_temp):
    # getStuXx.do
    session_temp.headers.update({"Accept": "application/json, text/plain, */*"})
    local_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    response = session_temp.post("http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/getStuXx.do",
                                 data={"data": json.dumps({"TBSJ": local_time})})
    dic = json.loads(response.text)
    # with open("./form.json", "w", encoding="utf8") as f:
    #     json.dump(dic, f, ensure_ascii=False, indent=4)
    dic = dic["data"]
    dic["DZ_SFSB"] = "1"
    dic["GCJSRQ"] = ""
    dic["BY1"] = "1"
    dic["GCKSRQ"] = ""
    dic["DFHTJHBSJ"] = ""

    response = session_temp.post("http://stu.hfut.edu.cn/xsfw/sys/swmxsyqxxsjapp/modules/mrbpa/saveStuXx.do",
                                 data={"data": json.dumps(dic)})
    return response.text
    pass


if __name__ == "__main__":

    i = 1
    while i < len(sys.argv):
        print(sys.argv[i])
        session = requests.session()
        # print(sys.argv[i+1])
        if login(session, sys.argv[i], sys.argv[i + 1]) != "0":
            print("登陆失败请重试")
            exit(1)
        i += 2
        print(fill_form(session))
        print()
