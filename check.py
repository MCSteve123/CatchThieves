from json import load
from tkinter.messagebox import showerror

def check(settings: list) -> list:
    try:
        file = open('files/config.json', 'r', encoding='utf-8')
        settings = load(file)
        file.close()
    except FileNotFoundError:
        showerror('配置读取', '''错误：未检测到配置文件
    可能的原因：
        1.DependentFlies文件夹下不存在config.json或被重命名为其它名字；
        2.文件损坏
        3.电脑硬盘损坏
    解决方法：
        1.去游戏的GitHub仓库下载纯净版
        2.换个硬盘……''')
        exit()
    except UnicodeDecodeError:
        showerror('配置读取', '''错误：配置文件编码错误
    可能的原因：
        config.json编码不是UTF-8（比如用了GBK等等）
    解决方法
        用编码转换工具转换为UTF-8编码''')
        exit()
    except BaseException as e:
        showerror('配置读取', '未知错误：\n', e)
    
    return settings