#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import paramiko
from datetime import datetime
from . import gsFileSystemObject

class SSHClient:
    def __init__(self, host, username=None, password=None, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self._client = None
        
    def connect(self):
        if not self._client:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password
            )
        return self._client

class gsFile(gsFileSystemObject):
    def __init__(self, path, autoLoad=False, monitor=False, sshhandle=None,
                 username=None, password=None, port=22, host=None):
        super().__init__(path)
        self.content = None
        self._monitor = monitor
        
        if sshhandle:
            self.ssh = sshhandle
        elif all([username, password, host]):
            self.ssh = SSHClient(host, username, password, port)
        else:
            raise ValueError("Either sshhandle or (username, password, host) must be provided")
            
        if autoLoad:
            self.read()
    
    @property
    def exists(self):
        try:
            self.ssh.sftp.stat(self.path)
            return True
        except:
            return False
            
    def read(self, binary=False):
        mode = 'rb' if binary else 'r'
        with self.ssh.sftp.file(self.path, mode) as f:
            self.content = f.read()
        return self.content

class gsFolder(gsFileSystemObject):
    def __init__(self, path, autoMake=True, sshhandle=None,
                 username=None, password=None, port=22, host=None):
        super().__init__(path)
        if sshhandle:
            self.ssh = sshhandle
        elif all([username, password, host]):
            self.ssh = SSHClient(host, username, password, port)
        else:
            raise ValueError("Either sshhandle or (username, password, host) must be provided")
            
        if autoMake and not self.exists:
            self.ssh.sftp.mkdir(self.path)
    
    @property
    def exists(self):
        try:
            self.ssh.sftp.stat(self.path)
            return True
        except FileNotFoundError:
            return False
    
    def list(self):
        result = []
        for item in self.ssh.sftp.listdir(self.path):
            full_path = os.path.join(self.path, item)
            try:
                self.ssh.sftp.stat(full_path)
                result.append(gsFolder(full_path, sshhandle=self.ssh))
            except:
                result.append(gsFile(full_path, sshhandle=self.ssh))
        return result 