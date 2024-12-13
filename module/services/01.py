#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import platform
import json
import os
import datetime
import psutil
import subprocess
from threading import Thread
from abc import ABC, abstractmethod
from typing import Union, Optional, List, Dict, Any
# 2. 使用 dataclasses 来简化一些类的定义
from dataclasses import dataclass

# 定义模块版本信息
# 版本号
__version__ = '1.0.0'
# 作者
__author__ = '李品勇'
# 邮箱
__email__ = 'lipy.sh.gvsun.com@gmail.com'
# 描述
__description__ = '模块描述'
# 项目地址
__url__ = 'https://github.com/nanhai-gvsun/webplatform'
# 许可证
__license__ = 'MIT'
# 版权
__copyright__ = 'Copyright 2024 lipinyong'
# 发布时间
__release_date__ = '2024-12-13'


# 全局常量定义
isPY2 = sys.version_info[0] == 2
isPY3 = sys.version_info[0] == 3
isWindows = platform.system().lower() == 'windows'
isLinux = platform.system().lower() == 'linux'
isMac = platform.system().lower() == 'darwin'
isARM = platform.machine().lower().startswith('arm')
isX86 = platform.machine().lower() in ['x86_64', 'amd64', 'i386', 'i686']
is64bit = platform.machine().endswith('64')
is32bit = not is64bit

# Edict类定义
class Edict(dict):
    def __init__(self, *args, **kwargs):
        super(Edict, self).__init__(*args, **kwargs)
        self.__dict__ = {}
        for k, v in dict(*args, **kwargs).items():
            if isinstance(v, dict):
                self[k] = Edict(v)
            else:
                self[k] = v

    def __getattr__(self, name):
        if name not in self:
            self[name] = Edict()
        return self[name]

    def __setattr__(self, name, value):
        if name == '__dict__':
            super(Edict, self).__setattr__(name, value)
        else:
            self[name] = value

    def __repr__(self):
        return json.dumps(self, indent=2, ensure_ascii=False)
# 单例元类，确保每个类只有一个实例
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
# 路由总线类定义
class Bus(Edict):
    """路由总线类，用于注册和执行路由处理函数
    
    主要功能:
    1. 注册路由处理函数
    2. 执行路由并传递参数
    3. 支持带参数的动态路由匹配
    """
    def __init__(self):
        super(Bus, self).__init__()
        self.routes = {}  # 存储路由映射
    
    def register(self, path: str):
        """注册路由处理函数的装饰器
        
        Args:
            path: 路由路径，支持 {param} 形式的参数
            
        Returns:
            decorator: 装饰器函数
        """
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator
    
    def execute(self, path: str, *args, **kwargs):
        """执行路由对应的处理函数
        
        Args:
            path: 要执行的路由路径
            *args: 传递给处理函数的位置参数
            **kwargs: 传递给处理函数的关键字参数
            
        Returns:
            Any: 处理函数的返回值
            
        Raises:
            ValueError: 当找不到匹配的路由时抛出
        """
        # 查找精确匹配的路由
        if path in self.routes:
            return self.routes[path](*args, **kwargs)
            
        # 处理带参数的路由
        for route in self.routes:
            if self._match_route(route, path):
                params = self._extract_params(route, path)
                return self.routes[route](*params, *args, **kwargs)
        raise ValueError(f"未找到路由: {path}")
    
    def _match_route(self, route_pattern, path):
        pattern_parts = route_pattern.split('/')
        path_parts = path.split('/')
        
        if len(pattern_parts) != len(path_parts):
            return False
            
        for p, pp in zip(pattern_parts, path_parts):
            if p and p[0] == '{' and p[-1] == '}':
                continue
            if p != pp:
                return False
        return True
    
    def _extract_params(self, route_pattern, path):
        pattern_parts = route_pattern.split('/')
        path_parts = path.split('/')
        params = []
        
        for p, pp in zip(pattern_parts, path_parts):
            if p and p[0] == '{' and p[-1] == '}':
                params.append(pp)
        return params
    
    def __call__(self, path, *args, **kwargs):
        return self.execute(path, *args, **kwargs)
# 文件操作类，支持本地和远程文件操作
class File:
    """文件操作类，支持本地和远程文件操作
    
    主要功能:
    1. 读写文件内容
    2. 删除文件
    3. 复制和移动文件
    4. 支持SSH远程操作
    """
    def __init__(self, path: str, ssh_client: Optional[Any] = None):
        self.path = path
        self.ssh = ssh_client
        
    def read(self) -> str:
        """读取文件内容
        
        Returns:
            str: 文件内容
            
        Raises:
            FileNotFoundError: 文件不存在时抛出
            IOError: 读取失败时抛出
        """
        try:
            if self.ssh:
                sftp = self.ssh.open_sftp()
                with sftp.file(self.path, 'r') as f:
                    return f.read()
            with open(self.path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"文件不存在: {self.path}")
        except Exception as e:
            raise IOError(f"读取文件失败: {str(e)}")
            
    def write(self, content: str):
        """写入文件内容"""
        if self.ssh:
            sftp = self.ssh.open_sftp()
            with sftp.file(self.path, 'w') as f:
                f.write(content)
        else:
            with open(self.path, 'w') as f:
                f.write(content)
                
    def delete(self):
        """删除文件"""
        if self.ssh:
            sftp = self.ssh.open_sftp()
            sftp.remove(self.path)
        else:
            os.remove(self.path)
            
    def copy(self, dst_path: str):
        """复制文件"""
        import shutil
        if self.ssh:
            sftp = self.ssh.open_sftp()
            sftp.get(self.path, dst_path)
        else:
            shutil.copy2(self.path, dst_path)
            
    def move(self, dst_path: str):
        """移动文件"""
        self.copy(dst_path)
        self.delete()
# 目录操作类
class Folder:
    """目录操作类"""
    def __init__(self, path: str, ssh_client=None):
        self.path = path
        self.ssh = ssh_client
        
    def list(self) -> List[str]:
        """列出目录内容"""
        if self.ssh:
            sftp = self.ssh.open_sftp()
            return sftp.listdir(self.path)
        return os.listdir(self.path)
        
    def create(self):
        """创建目录"""
        if self.ssh:
            sftp = self.ssh.open_sftp()
            sftp.mkdir(self.path)
        else:
            os.makedirs(self.path, exist_ok=True)
            
    def delete(self):
        """删除目录"""
        if self.ssh:
            sftp = self.ssh.open_sftp()
            self._rmtree_sftp(sftp, self.path)
        else:
            import shutil
            shutil.rmtree(self.path)
            
    def _rmtree_sftp(self, sftp, path):
        """递归删除远程目录"""
        for f in sftp.listdir_attr(path):
            filepath = os.path.join(path, f.filename)
            if stat.S_ISDIR(f.st_mode):
                self._rmtree_sftp(sftp, filepath)
            else:
                sftp.remove(filepath)
        sftp.rmdir(path)
# 文件系统操作类
class FileSystem:
    """文件系统操作类"""
    def __init__(self, ssh_config: Dict = None):
        self.ssh = None
        if ssh_config:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(**ssh_config)
            
    def file(self, path: str) -> File:
        """获取文件对象"""
        return File(path, self.ssh)
        
    def dir(self, path: str) -> Folder:
        """获取目录对象"""
        return Folder(path, self.ssh)

# 命令执行结果类
@dataclass
class CommandResult:
    """命令执行结果"""
    stdout: str
    stderr: str
    returncode: int

    @property
    def success(self) -> bool:
        return self.returncode == 0

    def __str__(self):
        return self.stdout if self.success else self.stderr
# 控制台操作类
class Console:
    """控制台操作类"""
    def __init__(self, ssh_client=None, log_dir=None, log_file=None):
        self.ssh = ssh_client
        self._stdout = None
        self._stderr = None
        self.log_dir = log_dir
        self.log_file = log_file
        
    @staticmethod
    def _get_timestamp():
        """获取当前时间戳"""
        return datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        
    def log(self, message: str, level: str = 'info'):
        """记录日志"""
        timestamp = self._get_timestamp()
        level = level.lower()
        lines = message.split('\n')
        
        for line in lines:
            log_line = f"{timestamp} [{level}] {line}\n"
            # 打印到屏幕
            print(log_line, end='')
            
            # 写入日志文件
            if self.log_dir:
                log_file = os.path.join(
                    self.log_dir,
                    datetime.datetime.now().strftime('%Y%m%d.log')
                )
                with open(log_file, 'a') as f:
                    f.write(log_line)
            elif self.log_file:
                with open(self.log_file, 'a') as f:
                    f.write(log_line)
                    
    def info(self, message: str, end='\n', flush=True):
        """打印信息"""
        print(message, end=end, flush=flush)
        
    def move_cursor_up(self, lines=1):
        """向上移动光标"""
        print(f"\033[{lines}A", end='')
        
    def move_cursor_down(self, lines=1):
        """向下移动光标"""
        print(f"\033[{lines}B", end='')
        
    def clear_line(self):
        """清除当前行"""
        print("\033[2K", end='')
        
    def clear_screen(self):
        """清除屏幕"""
        print("\033[2J", end='')
        
    def execute(self, command: str) -> CommandResult:
        """执行命令"""
        if self.ssh:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return CommandResult(
                stdout.read().decode(),
                stderr.read().decode(),
                stdout.channel.recv_exit_status()
            )
        else:
            import subprocess
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE if self._stdout is None else self._stdout,
                stderr=subprocess.PIPE if self._stderr is None else self._stderr
            )
            stdout, stderr = process.communicate()
            return CommandResult(
                stdout.decode() if stdout else '',
                stderr.decode() if stderr else '',
                process.returncode
            )
            
    def redirect_stdout(self, file):
        """重定向标准输出"""
        self._stdout = file
        
    def redirect_stderr(self, file):
        """重定向标准错误"""
        self._stderr = file
        
    def reset_redirect(self):
        """重置重定向"""
        self._stdout = None
        self._stderr = None
# 系统信息获取类
class SystemInfo:
    """系统信息获取类
    
    提供各种系统信息的获取方法，包括:
    - CPU信息
    - 内存信息
    - 磁盘信息
    - 网络信息
    - 系统基本信息
    """
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """获取CPU信息
        
        Returns:
            Dict: CPU信息，包含:
                - count: CPU核心数
                - percent: CPU使用率
                - freq: CPU频率信息
        """
        return {
            'count': psutil.cpu_count(logical=False),  # 物理核心数
            'logical_count': psutil.cpu_count(),  # 逻辑核心数
            'percent': psutil.cpu_percent(interval=1),
            'freq': psutil.cpu_freq()._asdict() if hasattr(psutil.cpu_freq(), '_asdict') else None,
            'stats': psutil.cpu_stats()._asdict()
        }

    @staticmethod
    def get_memory_info() -> Dict:
        return psutil.virtual_memory()._asdict()

    @staticmethod
    def get_disk_info() -> List[Dict]:
        return [p._asdict() for p in psutil.disk_partitions()]

    @staticmethod
    def get_network_info() -> Dict:
        return psutil.net_if_addrs()

# 单个进程对象
class Process:
    """单个进程对象"""
    def __init__(self, pid=None):
        self.pid = pid
        self._process = psutil.Process(pid) if pid else None
        self.update()

    def update(self):
        """更新进程信息"""
        if not self._process:
            return
        
        try:
            self.name = self._process.name()
            self.cmd = ' '.join(self._process.cmdline())
            self.status = self._process.status()
            self.start_time = datetime.fromtimestamp(self._process.create_time())
            self.end_time = None
            
            # 获取进程监听的端口
            self.port = None
            try:
                connections = self._process.connections()
                listen_conns = [c for c in connections if c.status == 'LISTEN']
                if listen_conns:
                    self.port = listen_conns[0].laddr.port
            except:
                pass
        except psutil.NoSuchProcess:
            self._process = None

    def stop(self):
        """停止进程"""
        if self._process:
            self._process.terminate()
            self.end_time = datetime.now()

    def restart(self, cmd=None):
        """重启进程"""
        self.stop()
        if cmd:
            return Processes.start(cmd)
        elif self.cmd:
            return Processes.start(self.cmd)
        return None
    def _get_listening_port(self) -> Optional[int]:
        """获取进程监听的端口"""
        try:
            connections = self._process.connections()
            listen_conns = [c for c in connections if c.status == 'LISTEN']
            return listen_conns[0].laddr.port if listen_conns else None
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return None

# 进程管理类
class Processes:
    """进程管理类"""
    def __init__(self):
        self.monitored_processes = {}
        self._monitor_thread = None
        self.load_monitored_processes()
        self._create_pid_file()
        self._start_monitor()

    def _create_pid_file(self):
        """创建PID文件"""
        pid_file = 'main.pid'
        if os.path.exists(pid_file):
            try:
                with open(pid_file, 'r') as f:
                    old_pid = int(f.read().strip())
                try:
                    os.kill(old_pid, 9)
                except:
                    pass
            except:
                pass
        
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))

    def _start_monitor(self):
        """启动监控线程"""
        def monitor():
            while True:
                for name, info in self.monitored_processes.items():
                    if info['active']:
                        process = self.find_by_name(name)
                        if not process:
                            self.start(info['command'])
                time.sleep(5)

        self._monitor_thread = threading.Thread(target=monitor, daemon=True)
        self._monitor_thread.start()

    @staticmethod
    def list() -> List[Process]:
        """返回所有进程列表"""
        return [Process(p.pid) for p in psutil.process_iter()]

    @staticmethod
    def start(command: str) -> Process:
        """启动新进程"""
        import subprocess
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return Process(process.pid)

    @staticmethod
    def get(pid: int) -> Union[Process, None]:
        """通过PID获取进程"""
        try:
            return Process(pid)
        except psutil.NoSuchProcess:
            return None

    def find_by_name(self, name: str) -> Union[Process, List[Process]]:
        """通过进程名查找进程"""
        processes = []
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == name:
                processes.append(Process(proc.pid))
        return processes[0] if len(processes) == 1 else processes

    def find_by_port(self, port: int) -> Union[Process, None]:
        """通过端口号查找进程"""
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                return Process(conn.pid)
        return None

    def monitor_process(self, name: str, command: str):
        """添加进程到监控池"""
        self.monitored_processes[name] = {
            'command': command,
            'active': True
        }
        self.save_monitored_processes()

    def save_monitored_processes(self):
        """保存监控进程配置"""
        with open('monitored_processes.json', 'w') as f:
            json.dump(self.monitored_processes, f)

    def load_monitored_processes(self):
        """加载监控进程配置"""
        try:
            with open('monitored_processes.json', 'r') as f:
                self.monitored_processes = json.load(f)
        except FileNotFoundError:
            self.monitored_processes = {}

# 设备对象
class Device:
    """设备对象"""
    def __init__(self, name: str, ip: str, port: int):
        self.name = name
        self.ip = ip
        self.port = port
        self._socket = None
        
    def connect(self):
        """连接设备"""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.ip, self.port))
            return True
        except:
            return False
            
    def disconnect(self):
        """断开连接"""
        if self._socket:
            self._socket.close()
            self._socket = None
            
    def read(self, size: int = 1024) -> bytes:
        """读取数据"""
        if not self._socket:
            raise ConnectionError("Device not connected")
        return self._socket.recv(size)
        
    def write(self, data: bytes):
        """写入数据"""
        if not self._socket:
            raise ConnectionError("Device not connected")
        self._socket.send(data)
        
    def __del__(self):
        """析构函数"""
        self.disconnect()
# 设备管理类
class Devices:
    """设备管理类"""
    def __init__(self):
        self._devices = {}
        
    def add_device(self, name: str, ip: str, port: int):
        """添加设备"""
        device = Device(name, ip, port)
        self._devices[name] = device
        return device
        
    def remove_device(self, name: str):
        """移除设备"""
        if name in self._devices:
            self._devices[name].disconnect()
            del self._devices[name]
            
    def get_device(self, name: str) -> Union[Device, None]:
        """获取设备"""
        return self._devices.get(name)
        
    def list_devices(self) -> List[Device]:
        """列出所有设备"""
        return list(self._devices.values())
# 系统对象组
class _System(metaclass=SingletonMeta):
    """系统对象组"""
    def __init__(self):
        self.Processes = Processes()
        self.Console = Console()
        self.FileSystem = FileSystem()
        self.SystemInfo = SystemInfo()
        self.Devices = Devices()
        self.cmds = Bus()
        for p, pp in zip(pattern_parts, path_parts):
            if p and p[0] == '{' and p[-1] == '}':
                continue
            if p != pp:
                return False
        return True
    
    def _extract_params(self, route_pattern, path):
        pattern_parts = route_pattern.split('/')
        path_parts = path.split('/')
        params = []
        
        for p, pp in zip(pattern_parts, path_parts):
            if p and p[0] == '{' and p[-1] == '}':
                params.append(pp)
        return params
    
    def __call__(self, path, *args, **kwargs):
        return self.execute(path, *args, **kwargs)
# 创建全局系统对象
System = _System()

# 全局函数
getCPUInfo = SystemInfo.get_cpu_info
getMemoryInfo = SystemInfo.get_memory_info
getDiskInfo = SystemInfo.get_disk_info
getNetworkInfo = SystemInfo.get_network_info
getSystemInfo = lambda: Edict(
    cpu=getCPUInfo(),
    memory=getMemoryInfo(),
    disk=getDiskInfo(),
    network=getNetworkInfo()
) 