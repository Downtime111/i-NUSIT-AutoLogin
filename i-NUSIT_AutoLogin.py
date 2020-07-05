#ecoding:gbk
import os
import re
import json
import requests
import base64
import time
import winreg
import psutil
import subprocess
#import csv
#import struct

def kill_sub_process():
    state=0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['name'])
        except psutil.NoSuchProcess:
            pass
        else:
            #print(pinfo)
            if pinfo.get('name')=='i-NUSIT_subprocess.exe':
                state=1
            else:
                pass
    #print(state)
    if state == 1:
        os.system('TASKKILL /F /IM i-NUSIT_subprocess.exe')
        #print('kill')
    else:
        pass
    return state

def call_sub():
    subprocess.call('cscript D:\\NUSIT_autologin\\hidden_runsub.vbs')
    #print('vbs script has run.')

def find_sub_process():
    state = 0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['name'])
        except psutil.NoSuchProcess:
            pass
        else:
            #print(pinfo)
            if pinfo.get('name')=='i-NUSIT_subprocess.exe':
                pass
            else:
                state = 1
    #print(state)
    if state == 1:
        call_sub()
        #print('run')
    else:
        pass
    return state

def edit_regedit():
    global autorun_value_flag,autorun_value
    #读取联网自动弹出浏览器的注册表键值
    key_browser = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SYSTEM\\CurrentControlSet\\Services\\NlaSvc\\Parameters\\Internet")
    browser_value, type1 = winreg.QueryValueEx(key_browser, r'EnableActiveProbing')
    #读取是否设置开机启动项的键值
    try:
        key_autorun = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        autorun_value, type2 = winreg.QueryValueEx(key_autorun, r'i-NUSIT1.0')
        if autorun_value != 0:
            autorun_value_flag = 0
        #print(autorun_value)
    except FileNotFoundError:
        autorun_value_flag = 1
    except NameError:
        autorun_value_flag = 1
    list=[browser_value, autorun_value_flag]
    #print(browser_value)
    #print(list)
    if browser_value != 0:
        print("【关闭联网弹窗-注册表已写入】")
        print(' ')
        os.system('regedit /s D:\\NUSIT_autologin\\modify.reg')
    if autorun_value_flag != 0:
        print('【开机自启-注册表已写入】')
        print(' ')
        os.system('regedit /s D:\\NUSIT_autologin\\modify_run.reg')
    else:
        #print('【开机自启与关闭联网弹窗模块-已设置】')
        #print(' ')
        pass
    return browser_value,autorun_value_flag

def kill_process():
    os.system('TASKKILL /F /IM QQBrowser.exe')
    os.system('TASKKILL /F /IM MicrosoftEdge.exe')
    os.system('TASKKILL /F /IM chrome.exe')
    os.system('TASKKILL /F /IM iexplore.exe')
    """
    list=[]
    process_pid_list = psutil.pids()
    for id in process_pid_list:
        p=psutil.Process(id)
        #time=p.create_time()
        if str(p.name())=='QQBrowser.exe':
            os.system('TASKKILL /F /IM QQBrowser.exe')
            time.sleep(0.5)
        elif str(p.name())=='MicrosoftEdge.exe':
            os.system('TASKKILL /F /IM MicrosoftEdge.exe')
            time.sleep(0.5)
        elif str(p.name()) == 'chrome.exe':
            os.system('TASKKILL /F /IM chrome.exe')
            time.sleep(0.5)
        elif str(p.name()) == 'iexplore.exe':
            os.system('TASKKILL /F /IM iexplore.exe')
            time.sleep(0.5)
        else:
            pass
        """

def link_wifi():
    #os.system('netsh wlan set hostednetwork mode=allow ssid=i-NUIST ')
    #time.sleep(2)
    #os.system('netsh wlan start hostednetwork')
    #time.sleep(2)
    os.system('netsh wlan connect name=i-NUIST')
    time.sleep(2)
    #os.system('netsh wlan show hostednetwork')

def get_status():
    #login_html="https://www.baidu.com"
    login_html = "http://10.255.255.13"
    page_status = requests.get(login_html,timeout=1)
    response = page_status.status_code
    #print("登陆页面状态码：",response)
    return response

def test_internet():
    html="https://www.baidu.com"
    page_status = requests.get(html,timeout=10)
    response = page_status.status_code
    #print("外部网络状态码：",response)
    return response

def save_message(username, password, domain):
    with open('D:\\NUSIT_autologin\\login_cache.txt','w+',encoding='utf-8') as message:
        dict = {'username': username, 'password': password, 'domain': domain}
        message.write(str(dict))

def read_message():
    try:
        with open('D:\\NUSIT_autologin\\login_cache.txt', 'r', encoding='utf-8') as message:
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
    with open('D:\\NUSIT_autologin\\login_cache.txt', 'w+', encoding='utf-8') as message:
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
    print(
    """
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      ╔═╗         ╔══     ╔═╗  ╔═╗    ╔═╗  ╔═╗  ╔═══════╗ ╔═══════╗
      ╚═╝         ║ ╔ ╲  ║ ║  ║ ║    ║ ║  ║ ║  ║ ╔═════╝  ╚══╗ ╔══╝ 
     ╔═╗  ╔═══╗  ║ ║╲ ╲ ║ ║  ║ ║    ║ ║  ║ ║  ║ ╚═════╗     ║ ║  
    ║ ║  ╚═══╝  ║ ║ ╲ ╲║ ║  ║ ║    ║ ║  ║ ║  ╚═════╗ ║     ║ ║    
   ║ ║         ║ ║   ╲  ║  ║ ╚════╝ ║  ║ ║  ╔═════╝ ║     ║ ║       
  ╚═╝         ╚═╝     ╚═╝  ╚════════╝  ╚═╝  ╚═══════╝     ╚═╝  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """
    )
    kill_flag = 1
    browser, autorun = edit_regedit()
    while True:
        flag = 0
        try:
            code=str(get_status())
            if code == '200':
                if kill_flag:
                    #kill_process()
                    if browser:
                        edit_regedit()
                    if autorun:
                        edit_regedit()
                    else:
                        pass
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
                        print('本地已保存登录信息，正在自动登录...')
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
                            call_sub()#调用监听程序
                            print(' ')
                            print('Successfully connected to the Internet.')
                            print(' ')
                            time.sleep(0.5)
                            print('---------------------------------')
                            q = str(input('按q键退出登录程序，按l键注销登录，按d键删除保存的登录信息：')).lower()
                            if q == 'l' :
                                logout(username, password, domain)
                                print(' ')
                                kill_sub_process()
                                print('  ========== 校园网注销成功 =========')
                                print(' ')
                                q8 = str(input('回车重新登录，q键退出程序：')).lower()
                                if q8 == 'q':
                                    flag = True
                                    break
                                else:
                                    kill_flag = 0
                                #flag = True
                                #break
                            elif q == 'd':
                                delete_message()
                                logout(username, password, domain)
                                print(' ')
                                kill_sub_process()
                                print('本地保存的登录信息已删除')
                                print(' ')
                            elif q == 'q':
                                print('程序已退出')
                                flag = True
                                break
                            else:
                                print('程序已退出')
                                flag = True
                                break
                        else:
                            print(' ')
                            print('Connection network error.')
                            print('校园网设备故障，请稍后重试。')
                            print(' ')
                            print('---------------------------------')
                            q5 = str(input('回车重新登录，q键退出程序：')).lower()
                            if q5 == 'q':
                                flag = True
                                break
                            else:
                                pass
                    elif status == 0:
                        info=back_data['info']
                        print(' ')
                        print('['+info+']')
                        print(' ')
                        if info == '用户已登录':
                            print('正在验证网络连通性，请稍后...')
                            time.sleep(1)
                            save_message(username, password, domain)  # 保存登录信息
                            if test_internet() == 200:
                                print('Successfully connected to the Internet.')
                                print(' ')
                            else:
                                print('Connection network error.')
                                print('校园网设备故障，请稍后重试。')
                                print(' ')
                            time.sleep(0.5)
                            print('---------------------------------')
                            q2 = str(input('按q键退出登录程序，按l键注销登录，按d键删除保存的登录信息：')).lower()
                            if q2 == 'l':
                                print(' ')
                                kill_sub_process()
                                print('['+logout(username,password,domain)+']')
                                print(' ')
                                print('---------------------------------')
                                q7 = str(input('回车重新登录，q键退出程序：')).lower()
                                if q7 == 'q':
                                    flag = True
                                    break
                                else:
                                    kill_flag = 0
                                #flag = True
                                break
                            elif q2 == 'd':
                                delete_message()
                                print(' ')
                                kill_sub_process()
                                print('本地保存的登录信息已删除')
                                print(' ')
                                logout(username, password, domain)
                            elif q2 == 'q':
                                print('程序已退出')
                                flag = True
                                break
                            else:
                                print('程序已退出')
                                flag = True
                                break
                        elif info == '认证失败, 请检查密码及账户状态':
                            print('---------------------------------')
                            q3 = str(input('回车重新登录，q键退出程序：')).lower()
                            if q3 == 'q':
                                flag = True
                                break
                            else:
                                delete_message()
                                kill_sub_process()
                        elif info == 'UserName_Err':
                            print('---------------------------------')
                            q4 = str(input('回车重新登录，q键退出程序：')).lower()
                            if q4 == 'q':
                                flag = True
                                break
                            else:
                                delete_message()
                                kill_sub_process()
                        else:
                            print('[认证失败, 请检查密码及账户状态]')
                            print('---------------------------------')
                            q6 = str(input('回车重新登录，q键退出程序：')).lower()
                            if q6 == 'q':
                                flag = True
                                break
                            else:
                                delete_message()
                                kill_sub_process()
                    else:
                        print('校园网设备故障，请稍后重试。')
            else:
                print('[i-NUIST]校园网登录页面通讯失败')
                print('正在尝试连接到i-NUSIT...')
                enter = input('按任意键继续:')
                while (enter !=0):
                    kill_flag = True
            #break  ##############
        except WindowsError:
            #print('[i-NUIST]校园网未连接，请先连接校园网')
            #print('网络开关未打开，请先打开网络开关')
            print('正在尝试连接到i-NUSIT...')
            kill_flag = True
            link_wifi()
            time.sleep(0.5)
            print(' ')
            #enter = input('按任意键退出程序:')
            #while (enter !=0):
            #    break
        if flag :
            break
if __name__=='__main__':
    main()
    #save_message('5','2','0')
    #print(read_message())
    #delete_message()
    #str(read_message()[0])
    #link_wifi()
    #get_process()
    #os.system('regedit /s D:\python_file\modify.reg')
    #browser, autorun = edit_regedit()
"""
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
"""
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
