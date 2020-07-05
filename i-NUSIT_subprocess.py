#ecoding:gbk
import time
import psutil
import os
import requests
import subprocess

def kill_main_process():
    state=0
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['name'])
        except psutil.NoSuchProcess:
            pass
        else:
            #print(pinfo)
            if pinfo.get('name')=='i-NUSIT_autologin.exe':
                state=1
            else:
                pass
    #print(state)
    if state == 1:
        os.system('TASKKILL /F /IM i-NUSIT_autologin.exe')
        #print('kill')
    else:
        pass
    return state

def test_connect():
    #state = 1
    return1=os.system('ping www.baidu.com')
    #print(return1)
    if return1:
        WLAN=os.system('netsh wlan connect name=i-NUIST')
        if WLAN:
            state = 1
        else:
            state = 0
            # print('ping failed')
        #os.system('msdt.exe /id NetworkDiagnosticsNetworkAdapter')#调用系统网络诊断
    else:
        #print('ping success')
        state = 1
    return state

def test_internet():
    html="http://www.baidu.com"
    page_status = requests.get(html,timeout=10)
    response = page_status.status_code
    print("外部网络状态码：",response)
    return response

def call_main():
    subprocess.call('cscript D:\\NUSIT_autologin\\hidden_runmain.vbs')
    #print('vbs script has run.')

def main():
    time.sleep(30)
    while True:
        kill_main_process()
        while True:
            if test_connect() == 1:
                print('network is not-open or OK')
                time.sleep(5)
                os.system('cls')
            else:
                call_main()
                time.sleep(10)
                break

if __name__ == '__main__':
    main()