import signal
import os
import config
import webbrowser
import atexit

#这个模块来自 https://github.com/poulp/zenipy
from zenipy.zenipy import *

from multiprocessing import Process,Pool
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from subprocess import  Popen

HOME = os.getenv("HOME")
APPINDICATOR_ID = 'ClashR Pro'
LOGO_W='/opt/ClashR_Pro/logo-w.svg'
LOGO_B='/opt/ClashR_Pro/logo-b.svg'
indicator = appindicator.Indicator.new(APPINDICATOR_ID,LOGO_W, appindicator.IndicatorCategory.SYSTEM_SERVICES)
clashr=Popen(args='/opt/ClashR_Pro/clashr/clashr-linux-amd64',shell=True)
def main():
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()


#此段代码（这个class）引用ssr-gtk项目 https://github.com/Baloneo/ssr-gtk
class SettingWindow(Gtk.Window):

    def on_ok_btn_clicked(self, *args):
        global clashr
        url = self.entry.get_text()
        clashr.kill()
        if config.download_yaml(url):
            self.label_msg.set_text("加载失败")
        else:
            self.label_msg.set_text("加载成功")
        clashr = Popen(args='/opt/ClashR_Pro/clashr/clashr-linux-amd64',shell=True)

    def on_clash_btn_clicked(self, *args):
        url = self.entry.get_text()
        ok = SSRSub2ClashR.start
        if not ok:
            self.label_msg.set_text("转换失败")
        else:
            self.label_msg.set_text("clashr订阅文件已保存到home目录")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("设置ClashR订阅信息")
        self.set_default_size(380, 50)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  # 垂直的盒子把水平占满

        self.entry = Gtk.Entry()
        old_url = config.read_url()
        self.entry.set_text(old_url or "设置clash订阅地址")
        self.vbox.pack_start(self.entry, False, False, 0)

        # 在一个水平的容器添加两个元素 vv_box 用来占用所有的左边空余空间 button使用剩下的必须空间大小
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        # vv_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.label_msg = Gtk.Label("订阅存储在~/.config/clash/")
        self.label_msg.set_selectable(True)
        self.button_clash = Gtk.Button("ssr转clashr")
        self.button_clash.connect("clicked", self.on_clash_btn_clicked)
        self.button_ok = Gtk.Button("确认")
        self.button_ok.connect("clicked", self.on_ok_btn_clicked)
        hbox.pack_start(self.label_msg, True, True, 0)
        hbox.pack_start(self.button_clash, False, False, 0)
        hbox.pack_start(self.button_ok, False, False, 0)
        self.vbox.pack_start(hbox, False, False, 0)

        self.add(self.vbox)

        self.present()
        self.show_all()


#系统托盘
def build_menu():
    menu = gtk.Menu()
    if switch == 0:
        item_ztxtdl = gtk.MenuItem('暂停代理')
        item_ztxtdl.connect('activate', ztxtdl)
        menu.append(item_ztxtdl)
    else:
        item_xtdl = gtk.MenuItem('继续代理')
        item_xtdl.connect('activate', xtdl)
        menu.append(item_xtdl)
    item_zddl = gtk.MenuItem('复制终端代理命令')
    item_zddl.connect('activate', zddl)
    item_pz = gtk.MenuItem('配置')
    item_pz.connect('activate', pz)
    item_console = gtk.MenuItem('控制台')
    item_console.connect('activate', console)
    item_quit = gtk.MenuItem('退出')
    item_quit.connect('activate', quit)
    menu.append(item_zddl)
    menu.append(item_console)
    menu.append(item_pz)
    menu.append(item_quit)
    menu.show_all()
    return menu

def zddl(source):
    print("已复制到剪贴板")

def ztxtdl(source):
    global switch
    switch = 1
    #print(switch)
    indicator.set_menu(build_menu())
    #clashr.kill()
    config.set_none_proxy()

def xtdl(source):
    global switch#,clashr
    switch = 0
    #print(switch)
    indicator.set_menu(build_menu())
    #clashr = Popen(args='/opt/ClashR_Pro/clashr/clashr-linux-amd64',shell=True)
    config.set_proxy()


def console(source):
    webbrowser.open("http://clash.razord.top/", new=0, autoraise=True)


def pz(source):
    SettingWindow()
    print("配置按键被按下")

def quit(source):
    config.set_none_proxy()
    clashr.kill()
    gtk.main_quit()

@atexit.register
def _atexit():
    print("程序退出")
    clashr.kill()
    config.set_none_proxy()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    switch = 0
    config.set_proxy()
    main()