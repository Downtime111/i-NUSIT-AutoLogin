import re
import json
import requests
import base64
import time
#import csv
#import struct
#import os

def get_status():
    #login_html="https://www.baidu.com"
    login_html = "http://10.255.255.13"
    page_status = requests.get(login_html,timeout=1)
    response = page_status.status_code
    #print("登陆页面状态码：",response)
    return response

def test_internet():
    html="https://www.baidu.com"
    page_status = requests.get(html,timeout=1)
    response = page_status.status_code
    #print("外部网络状态码：",response)
    return response

def save_message(username, password, domain):
    with open('D:/login_cache.txt','w+',encoding='utf-8') as message:
        dict = {'username': username, 'password': password, 'domain': domain}
        message.write(str(dict))
def read_message():
    try:
        with open('D:/login_cache.txt', 'r', encoding='utf-8') as message:
            dict = eval(message.read())
            #print(dict)
            username = dict['username']
            password = dict['password']
            domain = dict['domain']
            file_state = 1
            #print("read complite")
            return file_state,username,password,domain
    except SyntaxError:
        #print('no message')
        file_state = 0
        username = 0
        password = 0
        domain = 0
        return file_state,username,password,domain
    except KeyError:
        #print('no key')
        file_state = 0
        username = 0
        password = 0
        domain = 0
        return file_state,username,password,domain
    except FileNotFoundError:
        #print('no file')
        file_state = 0
        username = 0
        password = 0
        domain = 0
        return file_state,username,password,domain
    except TypeError:
        #print('no str')
        file_state = 0
        username = 0
        password = 0
        domain = 0
        return file_state,username,password,domain

def delete_message():
    with open('D:/login_cache.txt', 'w+', encoding='utf-8') as message:
        dict=[]
        message.write(str(dict))

def login(username,password,domain):
    global cookie
    #referer={'Referer':'http://10.255.255.13/'}
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400',
             'Content-Type':'application/x-www-form-urlencoded;charset=utf-8',
             'Referer':'http://10.255.255.13/'}
    params={
            "Origin":"http://10.255.255.13",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "X-Requested-With":"XMLHttpRequest"}
    data='username={0}&domain={1}&password={2}&enablemacauth=0'.format(username,domain,password)
    #data='username=1000000000&domain=Unicom&password=NTffgDk3&enablemacauth=0' #err_test
    response=requests.request(
        'POST',
        'http://10.255.255.13/index.php/index/login',
        #cookies=cookie,
        headers=headers,
        params=params,
        data=data,
        timeout=10)
    context = json.loads(response.text)
    PHPSESSID = re.findall(r"=(.+?);",(response.headers['Set-Cookie']))
    for id in PHPSESSID:
        cookie = {'Cookie': 'sunriseUsername={0}; sunriseDomain={1}; think_language=zh-CN; PHPSESSID={2}'.format(username,domain,id)}
    #print(context)
    #print(cookie)
    """
        #登录成功
        {"info":"\u8ba4\u8bc1\u6210\u529f",
        "status":1,
        "logout_username":"1300011007",
        "logout_domain":"\u4e2d\u56fd\u8054\u901a",
        "logout_ip":"10.0.10.87",
        "logout_location":"\u6ee8\u6c5f\u697c\u65e0\u7ebf",
        "logout_timer":0,
        "logout_window":0}
        #已成功登录
        {"data":null,
        "info":"\u7528\u6237\u5df2\u767b\u5f55",
        "status":0}
        #登陆失败
        {"data":null,
        "info":"\u8ba4\u8bc1\u5931\u8d25, \u8bf7\u68c0\u67e5\u5bc6\u7801\u53ca\u8d26\u6237\u72b6\u6001",
        "status":0}
    """
    return context,cookie

def logout(username,password,domain):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': 'http://10.255.255.13/'}
    params = {
        "Origin": "http://10.255.255.13",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest"}
    response = requests.request(
        'POST',
        'http://10.255.255.13/index.php/index/logout',
        cookies=login(username,password,domain)[1],
        headers=headers,
        params=params)
    context = json.loads(response.text)['info']
    return context

def main():
    try:
        code=str(get_status())
        if code == '200':
            print('[i-NUIST]校园网登录页面通讯成功')
            while True:
                global username,password,domain
                if str(read_message()[0]) == '0':
                    ################## username,password,domain #####################
                    username = input('请输入用户名:')
                    password = base64.b64encode(input('请输入密码：').encode('utf-8')).decode('utf-8')
                    print("请选择网络运营商:",'\n',
                        '   [1]:南京信息工程大学（NUSIT）','\n',
                        '   [2]:中国联通(China Unicom)','\n',
                        '   [3]:中国移动(China Mobile)','\n',
                        '   [4]:中国电信(China Telecom)')
                    domain_num = input('输入序号【1-4】进行选择：')
                    while True:
                        if domain_num == '1':
                            domain = 'NUSIT'
                            break
                        elif domain_num == '2':
                            domain = 'Unicom'
                            break
                        elif domain_num == '3':
                            domain = 'CMCC'
                            break
                        elif domain_num == '4':
                            domain = 'ChinaNet'
                            break
                        else:
                            domain_num = input('输入序号错误，请重新选择运营商：')
                    #################################################################
                elif str(read_message()[0]) == '1':
                    print('本地已保存登录信息，正在自动登录，请稍后...')
                    username=read_message()[1]
                    password=read_message()[2]
                    domain=read_message()[3]
                    #print(username)
                    #print(password)
                    #print(domain)
                else:
                    pass
                print('正在连接到校园网，请稍后...')
                back_data = login(username, password, domain)[0]
                status = back_data['status']
                if status == 1:
                    save_message(username,password,domain)  #保存登录信息
                    info = back_data['info']
                    logout_username = back_data['logout_username']
                    logout_domain = back_data['logout_domain']
                    logout_ip = back_data['logout_ip']
                    logout_location = back_data['logout_location']
                    print(  '  ============', info, '===========', '\n',
                            '  用户名：', logout_username, '\n',
                            '  网络运营商：', logout_domain, '\n',
                            '  登录地址:', logout_location+'['+logout_ip+']', '\n',
                            ' =================================')
                    print('正在验证网络连通性，请稍后...')
                    time.sleep(1)
                    if test_internet() == 200:
                        print(' ')
                        print('Successfully connected to the Internet.')
                        print(' ')
                        q = str(input('按q键退出登录程序，按l键注销登录，按d键删除保存的登录信息：')).lower()
                        if q == 'l' :
                            logout(username, password, domain)
                            print(' ')
                            print('  ========== 校园网注销成功 =========')
                            print(' ')
                            break
                        elif q == 'd':
                            delete_message()
                            print('本地保存的登录信息已删除')
                        elif q == 'q':
                            print('程序已退出')
                            break
                        else:
                            print('程序已退出')
                            break
                    else:
                        print(' ')
                        print('Connection network error.')
                        print('校园网设备故障，请稍后重试。')
                        print(' ')
                elif status == 0:
                    info=back_data['info']
                    print(' ')
                    print('['+info+']')
                    print(' ')
                    print('正在验证网络连通性，请稍后...')
                    time.sleep(1)
                    if info == '用户已登录':
                        save_message(username, password, domain)  # 保存登录信息
                        if test_internet() == 200:
                            print('Successfully connected to the Internet.')
                            print(' ')
                        else:
                            print('Connection network error.')
                            print('校园网设备故障，请稍后重试。')
                            print(' ')
                        q2 = str(input('按q键退出登录程序，按l键注销登录，按d键删除保存的登录信息：')).lower()
                        if q2 == 'l':
                            print(' ')
                            print('['+logout(username,password,domain)+']')
                            print(' ')
                            break
                        elif q2 == 'd':
                            delete_message()
                            print('本地保存的登录信息已删除')
                        elif q2 == 'q':
                            print('程序已退出')
                            break
                        else:
                            print('程序已退出')
                            break
                    elif info == '认证失败, 请检查密码及账户状态':
                         q3 = str(input('回车重新登录，q键退出程序：')).lower()
                         if q3 == 'q':
                            break
                         else:
                            continue
                    else:
                        print('校园网设备故障，请稍后重试。')
                else:
                    print('校园网设备故障，请稍后重试。')
        else:
            print('[i-NUIST]校园网登录页面通讯失败')
            print('校园网设备故障，请稍后重试。')
            enter = input('按任意键继续:')
            while (enter !=0):
                pass
    except WindowsError:
        print('[i-NUIST]校园网未连接，请先连接校园网')
        enter = input('按任意键退出程序:')
        while (enter !=0):
            break
if __name__=='__main__':
    main()
    #save_message('5','2','0')
    #print(read_message())
    #delete_message()
    #str(read_message()[0])
'''
Invoke-WebRequest 
-Uri "http://10.255.255.13/index.php/index/login" 
-Method "POST" 
-Headers @{
    "Cookie"="think_language=zh-Hans-CN; PHPSESSID=500000000m99rscop3n4"; 
    "Origin"="http://10.255.255.13"; 
    "Accept-Encoding"="gzip, deflate"; 
    "Accept-Language"="zh-CN,zh;q=0.9"; 
    "User-Agent"="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3765.400 QQBrowser/10.6.4153.400"; 
    "Accept"="application/json, text/javascript, */*; q=0.01"; 
    "Referer"="http://10.255.255.13/"; 
    "X-Requested-With"="XMLHttpRequest"} 
-ContentType "application/x-www-form-urlencoded" 
-Body "username=13151000000&domain=Unicom&password=N0000003&enablemacauth=0"
'''
"""
curl 'http://10.255.255.13/index.php/index/logout' 
-X POST 
-H 'Cookie: sunriseUsername=13151590097; 
sunriseDomain=Unicom; 
think_language=zh-CN; 
PHPSESSID=r2gqs2emdvbct6fp248a7soe14' 
-H 'Origin: http://10.255.255.13' 
-H 'Accept-Encoding: gzip, deflate' 
-H 'Accept-Language: zh-CN,zh;q=0.9' 
-H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400' 
-H 'Content-Type: application/x-www-form-urlencoded' 
-H 'Accept: application/json, text/javascript, */*; q=0.01' 
-H 'Referer: http://10.255.255.13/' 
-H 'X-Requested-With: XMLHttpRequest' 
-H 'Connection: keep-alive' 
-H 'Content-Length: 0' --compressed
"""
