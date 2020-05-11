import os
import yaml
import urllib3

HOME = os.getenv("HOME")
YAML_PATH = os.path.join(HOME, ".config/clash/config.yaml")

#读取yaml文件
def get_yaml_data(yaml_file):
    # 打开yaml文件
    print("***获取yaml文件数据***")
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    
    print(file_data)
    print("类型：", type(file_data))

    # 将字符串转化为字典或列表
    print("***转化yaml数据为字典或列表***")
    data = yaml.load(file_data)
    #print(data)
    print("类型：", type(data))
    return data


#下载config
def download_yaml(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    with open(os.path.join(HOME, ".config/clash/config.yaml"), "wb") as f:
        f.write(response.data)
    get_yaml_data(YAML_PATH)
    write_url(url)

    #检查下载的config是否为空
    if response:
        return None
    else:
        return 1


#将url写入文件
def write_url(url):
    with open(os.path.join(HOME, ".config/clash/config_url"), "w") as f:
        f.write(url)
    return None


#从文件中读出url
def read_url():
    with open(os.path.join(HOME, ".config/clash/config_url"), "a+") as f:
        f.seek(0)
        url = f.readline()
    return url

def set_proxy():
    host='localhost'
    data=get_yaml_data(YAML_PATH)
    port=data['port']
    print(data['socks-port'])
    s_port=data["socks-port"]
    os.system(f"gsettings set org.gnome.system.proxy.http host '{host}'")
    os.system(f"gsettings set org.gnome.system.proxy.http port {port}")
    os.system(f"gsettings set org.gnome.system.proxy.https host '{host}'")
    os.system(f"gsettings set org.gnome.system.proxy.https port {port}")
    os.system(f"gsettings set org.gnome.system.proxy.ftp host '{host}'")
    os.system(f"gsettings set org.gnome.system.proxy.ftp port {port}")
    os.system(f"gsettings set org.gnome.system.proxy.socks host '{host}'")
    os.system(f"gsettings set org.gnome.system.proxy.socks port {s_port}")
    os.system(f"gsettings set org.gnome.system.proxy mode 'manual' ")
    return None


def set_none_proxy():
    os.system(f"gsettings set org.gnome.system.proxy mode 'none' ")
    return None