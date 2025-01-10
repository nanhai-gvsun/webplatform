# -*- coding: utf-8 -*-
import json,sys,os
from abc import ABC, abstractmethod
from typing import Union, Optional, List, Dict, Any

class Edict(dict):
    """
    扩展的字典类，支持通过属性访问和链式操作
    """
    def __init__(self, *args, **kwargs):
        """
        初始化 Edict 实例。
        
        参数:
            *args: 传递给 dict 的参数
            **kwargs: 传递给 dict 的关键字参数
        """
        super(Edict, self).__init__(*args, **kwargs)
        self.__dict__ = {}  # 使用单独的 __dict__ 存储属性，避免循环引用
    
    def __getattr__(self, name):
        """
        当访问一个不存在的属性时，返回一个新的 Edict 实例。
        
        参数:
            name (str): 属性名称
        
        返回:
            Edict: 一个新的 Edict 实例
        """
        if name not in self:
            self[name] = Edict()  # 返回一个新的 Edict 实例
        return self[name]

    def __setattr__(self, name, value):
        """
        设置属性值。
        
        参数:
            name (str): 属性名称
            value: 属性值
        """
        if name == '__dict__':
            # 如果属性名是 __dict__，使用 super 方法设置属性，避免循环引用
            super(Edict, self).__setattr__(name, value)
        else:
            # 否则，将属性值存储在字典中
            self[name] = value

    def __repr__(self):
        """
        返回 Edict 实例的字符串表示形式，使用 json.dumps 序列化。
        
        返回:
            str: 格式化的 JSON 字符串
        """
        return json.dumps(self, ensure_ascii=False, indent=4)
class EdictAll(dict):
    """
    扩展的字典类，支持通过属性访问和链式操作
    """
    def __init__(self, *args, **kwargs):
        """
        初始化 Edict 实例。
        
        参数:
            *args: 传递给 dict 的参数
            **kwargs: 传递给 dict 的关键字参数
        """
        self._dict = {}  # 使用 _dict 属性存储数据，避免循环引用
        super(EdictAll, self).__init__(*args, **kwargs)  # 调用父类 dict 的初始化方法
        
        # 遍历传入的参数，将字典类型的值转换为 EdictAll 实例
        for k, v in dict(*args, **kwargs).items():
            if isinstance(v, dict):
                self._dict[k] = EdictAll(v)  # 递归创建 EdictAll 实例
            else:
                self._dict[k] = v  # 直接存储非字典类型的值

    def __getattr__(self, key):
        """
        当访问一个不存在的属性时，返回一个新的 EdictAll 实例。
        
        参数:
            key (str): 属性名称
        
        返回:
            EdictAll: 一个新的 EdictAll 实例
        """
        if key not in self._dict:
            self._dict[key] = EdictAll()  # 如果属性不存在，创建一个新的 EdictAll 实例
        return self._dict[key]

    def __setattr__(self, key, value):
        """
        设置属性值。
        
        参数:
            key (str): 属性名称
            value: 属性值
        """
        if key == '_dict':
            # 如果属性名是 _dict，使用 super 方法设置属性，避免循环引用
            super(EdictAll, self).__setattr__(key, value)
        else:
            # 如果值是字典类型，递归创建 EdictAll 实例
            if isinstance(value, dict):
                self._dict[key] = EdictAll(value)
            else:
                # 否则，直接存储值
                self._dict[key] = value

    def __repr__(self):
        """
        返回 EdictAll 实例的字符串表示形式，使用 json.dumps 序列化。
        
        返回:
            str: 格式化的 JSON 字符串
        """
        return json.dumps(self._dict, indent=2, ensure_ascii=False)
class SingletonMeta(type):
    """
    单例元类，确保每个类只有一个实例
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        确保每个类只有一个实例。
        
        参数:
            cls: 类本身
            *args: 传递给类的参数
            **kwargs: 传递给类的关键字参数
        
        返回:
            object: 类的唯一实例
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
class System(metaclass=SingletonMeta):
    """
    系统对象，包含网络、进程、控制台和文件系统对象
    """
    def __init__(self):
        """
        初始化 System 实例。
        """
        super(System, self).__init__()
        self.Net = Net()  # 初始化网络对象
        self.Process = Process()  # 初始化进程对象
        self.Console = Console()  # 初始化控制台对象
        self.FileSystem = gsFileSystemObject()  # 初始化文件系统对象
class Net(EdictAll):
    """
    网络对象
    """
    def getPidfromPort(self, port):
        """
        获取指定端口的进程ID。
        
        参数:
            port (int): 端口号
        
        返回:
            int: 进程ID
        """
        # 实现获取端口对应进程ID的逻辑
        pass
class Process(EdictAll):
    """
    进程对象
    """
    def list(self):
        """
        获取进程列表。
        
        返回:
            list: 进程列表
        """
        # 实现获取进程列表的逻辑
        pass
    
    def getPidfromCmd(self, cmd):
        """
        根据命令获取进程ID。
        
        参数:
            cmd (str): 命令
        
        返回:
            int: 进程ID
        """
        # 实现根据命令获取进程ID的逻辑
        pass
    
    def kill(self, pid):
        """
        杀死指定进程。
        
        参数:
            pid (int): 进程ID
        """
        # 实现杀死进程的逻辑
        pass
class Console(EdictAll):
    """
    控制台对象
    """
    def log(self, message):
        """
        打印日志。
        
        参数:
            message (str): 日志消息
        """
        print(f"[LOG] {message}")
    
    def info(self, message):
        """
        打印信息。
        
        参数:
            message (str): 信息消息
        """
        print(f"[INFO] {message}")
class gsFileSystemObject:
    """文件系统工厂类，用于创建本地或远程文件系统对象"""
    
    def __init__(self, path, is_remote=False, ssh_config=None):
        self.path = path
        self.ssh_config = ssh_config
        
        if is_remote and ssh_config:
            from .sshfs import gsFile as RemoteFile, gsFolder as RemoteFolder
            self.file_class = RemoteFile
            self.folder_class = RemoteFolder
        else:
            from .gsfs import gsFile as LocalFile, gsFolder as LocalFolder
            self.file_class = LocalFile
            self.folder_class = LocalFolder
    
    def file(self, path, **kwargs):
        return self.file_class(path, **kwargs)
    
    def folder(self, path, **kwargs):
        return self.folder_class(path, **kwargs)
class gsFile(ABC):
    """文件对象基类"""
    
    @abstractmethod
    def __init__(self, path: str, autoLoad: bool = False, 
                 monitor: bool = False, ssh_params: Optional[dict] = None):
        """
        初始化文件对象
        
        Args:
            path: 文件路径
            autoLoad: 是否自动加载文件内容
            monitor: 是否监控文件变化
            ssh_params: SSH连接参数(远程文件系统使用)
        """
        pass
    
    @property
    @abstractmethod
    def content(self) -> Union[str, bytes]:
        """获取文件内容"""
        pass
    
    @property
    @abstractmethod
    def exists(self) -> bool:
        """判断文件是否存在"""
        pass
    
    @abstractmethod
    def parent(self, data: Optional[str] = None) -> 'gsFolder':
        """
        获取或设置父目录
        
        Args:
            data: 目标父目录路径，None表示获取当前父目录
            
        Returns:
            父目录对象
        """
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """返回文件信息的JSON字符串"""
        pass
    
    @abstractmethod
    def read(self) -> Union[str, bytes]:
        """读取文件内容"""
        pass
    
    @abstractmethod
    def write(self, data: Optional[Union[str, bytes]] = None) -> None:
        """写入文件内容"""
        pass
    
    @abstractmethod
    def readJson(self) -> Dict[str, Any]:
        """读取并解析JSON文件"""
        pass
    
    @abstractmethod
    def writeJson(self, data: Optional[Dict[str, Any]] = None) -> None:
        """写入JSON数据到文件"""
        pass
    
    @abstractmethod
    def rename(self, data: Optional[str] = None) -> 'gsFile':
        """重命名文件"""
        pass
    
    @abstractmethod
    def copy(self, data: Optional[str] = None) -> 'gsFile':
        """复制文件"""
        pass
    
    @abstractmethod
    def move(self, data: Optional[str] = None) -> 'gsFile':
        """移动文件"""
        pass
class gsFolder(ABC):
    """文件夹对象基类"""
    
    @abstractmethod
    def __init__(self, path: str, autoMake: bool = True, 
                 ssh_params: Optional[dict] = None):
        """
        初始化文件夹对象
        
        Args:
            path: 文件夹路径
            autoMake: 路径不存在时是否自动创建
            ssh_params: SSH连接参数(远程文件系统使用)
        """
        pass
    
    @property
    @abstractmethod
    def exists(self) -> bool:
        """判断文件夹是否存在"""
        pass
    
    @abstractmethod
    def parent(self, data: Optional[str] = None) -> 'gsFolder':
        """
        获取或设置父目录
        
        Args:
            data: 目标父目录路径，None表示获取当前父目录
            
        Returns:
            父目录对象
        """
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        """返回文件夹信息的JSON字符串"""
        pass
    
    @abstractmethod
    def list(self) -> List[Union['gsFolder', 'gsFile']]:
        """列出目录内容"""
        pass
    
    @abstractmethod
    def rename(self, data: Optional[str] = None) -> 'gsFolder':
        """重命名文件夹"""
        pass
    
    @abstractmethod
    def mkdir(self, data: Optional[str] = None) -> 'gsFolder':
        """创建文件夹"""
        pass
    
    @abstractmethod
    def rmdir(self, data: Optional[str] = None) -> 'gsFolder':
        """删除文件夹"""
        pass
    
    @abstractmethod
    def copy(self, data: Optional[str] = None) -> 'gsFolder':
        """复制文件夹"""
        pass
    
    @abstractmethod
    def move(self, data: Optional[str] = None) -> 'gsFolder':
        """移动文件夹"""
        pass
    
    @abstractmethod
    def delete(self, data: Optional[str] = None) -> 'gsFile':
        """删除文件"""
        pass

    