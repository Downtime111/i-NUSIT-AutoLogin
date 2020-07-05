# i-NUSIT-AutoLogin
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/Downtime111/i-NUSIT-AutoLogin.svg)](https://github.com/Downtime111/i-NUSIT-AutoLogin)  [![Github All Releases](https://img.shields.io/github/downloads/Downtime111/i-NUSIT-AutoLogin/total.svg)](http://github.com/Downtime111/i-NUSIT-AutoLogin/releases)  [![GitHub release](https://img.shields.io/github/release/Downtime111/i-NUSIT-AutoLogin.svg)](http://github.com/Downtime111/i-NUSIT-AutoLogin/releases)  [![GitHub issues](https://img.shields.io/github/issues/Downtime111/i-NUSIT-AutoLogin.svg)](https://github.com/Downtime111/i-NUSIT-AutoLogin/issues)

**i-NUSIT-AutoLogin是南信大i-NUIST校园网自动认证登录工具。**

再提醒一遍，名称没有写错，“i-NUSIT”只是恶搞而已..

作为一个懒的人，一定会觉得校园网的验证很繁琐，每次开机都要选择连接到 i-NUIST，然后等待偶尔才会自动弹出的登录页面。有时候打开了登录页面却刷新不出来，真的是很无语。于是乎本着一次劳动终身受益的原则，写了这段代码。

主要运行在CMD下，已打包成EXE自解压文件

* **Windows版本：**

    [**点击进入下载地址**](https://github.com/Downtime111/i-NUSIT-AutoLogin/releases)

* **Linux版本：**

    没有

现已支持自动设置开机自启，自动连接校园网WLAN，可实现无需人工操作开机自动联网。
最新版已支持后台运行，实时监听网络连接状态，当网络连接异常时，自动在后台运行主程序，实现全天候自动的无感联网体验。

## 0x01 版本说明
## v1.0

* 实现了保存登录信息以便下次自动登录
* 实现了登出功能
* 实现了登录成功后验证网络连通性


![image](
https://github.com/Downtime111/i-NUSIT-AutoLogin/raw/master/pic/Image.png)

## v2.0

* 优化了界面，添加了一个还说得过去的Logo
* 实现了开机自启
* 实现了在网络开关打开状态下自动连接 i-NUSIT（连不到网就一直循环直到连上为止，but一般都能连上，在校外就不要运行了，否则会一直尝试连接）

![image](
https://github.com/Downtime111/i-NUSIT-AutoLogin/raw/master/pic/Image%20%5B2%5D.png)

## v2.1

* 修改了read_message( )与save_message( )读取的路径，解决了开机自启时读取login_cache.txt文件失败的问题
* 修改了test_internet( )的timeout时延数，解决了因网络波动导致的检测连通性失败的问题
* 修改了自解压的更新与覆写模式，保留了用户的登录信息

## v3.0

* 实现了后台驻留
* 实现了实时监听网络状态
* 实现了后台静默运行并释放

## 0x02 安装
安装时请不要修改安装路径，否则会导致程序出错

默认解压至 D:\NUSIT_autologin

修改路径会导致注册表文件读取失败

## 0x03 使用
### 自动修改注册表
设置的是每次启动程序都要检测如下两个注册表键值：

1. EnableActiveProbing 键值

    默认值为1，当该值为1的时候，连接需要验证的网络，就会弹出浏览器窗口，所以设置0值禁用
```
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet]
"EnableActiveProbing"=dword:0
```

2. Run项新增 i-NUSIT1.0 键，该目录下添加键，将会使开机自动运行键值对应目录下的可执行文件

```
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run]
"i-NUSIT1.0"="D:\\NUSIT_autologin\\i-NUSIT_autologin.exe --startup"
```
每当程序运行的时候，都会检测一遍注册表，如果检测到 EnableActiveProbing 键值为1，或者 
i-NUSIT1.0 键值为空or不存在的时候，都会触发修改注册表。

如需还原注册表，请下载如下文件运行即可：
[注册表还原.reg](https://github.com/Downtime111/i-NUSIT-AutoLogin/blob/master/注册表恢复.reg)

### 后台运行的实现
程序的后台运行使用了VBS脚本语言，当联网成功后，调用VBS语句开启后台进程。
```
set ws = WScript.CreateObject("WScript.Shell")
ws.Run "D:\NUSIT_autologin\i-NUSIT_subprocess.exe /c *" ,0
```
后台进程调用主进程后台执行同理。

### 登录
输入用户名回车，输入密码回车，输入序号选择运营商回车即可自动连接。
![image](
https://github.com/Downtime111/i-NUSIT-AutoLogin/raw/master/pic/Image%20%5B3%5D.png)


### 删除登录信息
![image](
https://github.com/Downtime111/i-NUSIT-AutoLogin/raw/master/pic/Image%20%5B4%5D.png)

在如图所示界面输入‘d’，即可删除本地保存的登录信息（用户名，密码，运营商）。

在最新的v3.0中执行删除信息，可同时将后台进程关闭。

保存的密码存放在 D:\NUSIT_autologin\login_cache.txt ，密码默认以Base64编码方式加密。

### 注销
在上一个图的界面输入‘l’，即可注销网络登录状态。
![image](
https://github.com/Downtime111/i-NUSIT-AutoLogin/raw/master/pic/Image%20%5B5%5D.png)

回车再次登录。
在最新的v3.0中执行注销认证，可同时将后台进程关闭。

### 退出程序
在上一个图的界面输入‘q’，即可退出登录程序。
在最新的v3.0中执行退出程序，仅关闭主进程，后台进程继续。

## 0x04 其他
### 0x01 TODO

* **~~实现打开程序自动登录~~**
* ~~**实现注销网络功能**~~
* **~~实现自动联网~~**
* **~~实现开机自启~~**
* 实现自动打开网络开关
* 编写GUI图形界面
* **~~实现休眠后登陆时自动联网~~**
* 支持关闭修改注册表功能（目前默认开启不支持关闭）
* **~~实现后台运行~~**

### 0x02 LICNESE
i-NUSIT-AutoLogin的代码使用MIT License发布，此外，禁止使用i-NUSIT-AutoLogin以及i-NUSIT-AutoLogin的修改程序用于商业目的。
