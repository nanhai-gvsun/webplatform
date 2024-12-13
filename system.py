import datetime
import json
import os
import platform
import socket
import stat
import subprocess
import sys
import threading
import time
from abc import ABC, abstractmethod
from typing import Union, Optional, List, Dict, Any

import paramiko
import psutil

from dataclasses import dataclass

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

class Process:
    """单个进程对象"""
    def __init__(self, pid: Optional[int] = None):
        self.pid = pid
        self._process: Optional[psutil.Process] = None
        if pid:
            try:
                self._process = psutil.Process(pid)
                self.update()
            except psutil.NoSuchProcess:
                pass

    def update(self) -> None:
        """更新进程信息"""
        if not self._process:
            return
        
        try:
            self.name = self._process.name()
            self.cmd = ' '.join(self._process.cmdline())
            self.status = self._process.status()
            self.start_time = datetime.datetime.fromtimestamp(self._process.create_time())
            self.end_time = None
            
            self.port = self._get_listening_port()
        except psutil.NoSuchProcess:
            self._process = None

    def _get_listening_port(self) -> Optional[int]:
        """获取进程监听的端口"""
        try:
            connections = self._process.connections()
            listen_conns = [c for c in connections if c.status == 'LISTEN']
            return listen_conns[0].laddr.port if listen_conns else None
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return None

class FileSystem:
    """文件系统操作类"""
    def __init__(self, ssh_config: Optional[Dict] = None):
        self.ssh = None
        if ssh_config:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(**ssh_config)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ssh:
            self.ssh.close()

    def file(self, path: str) -> File:
        return File(path, self.ssh)
    
    def dir(self, path: str) -> Folder:
        return Folder(path, self.ssh) 