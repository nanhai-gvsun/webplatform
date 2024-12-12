#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import shutil
from pathlib import Path

class gsFile:
    def __init__(self, path, autoLoad=False, monitor=False):
        self.path = os.path.abspath(path)
        self._content = None
        if autoLoad:
            self.read()
        # TODO: 实现文件监控功能
        self.monitor = monitor
    
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value):
        self._content = value
    
    @property
    def exists(self):
        return os.path.exists(self.path)
    
    def parent(self, data=None):
        if data is None:
            parent_path = os.path.dirname(self.path)
            return gsFolder(parent_path, autoMake=True)
        else:
            new_path = os.path.join(data, os.path.basename(self.path))
            self.move(new_path)
            return self
    
    def __str__(self):
        stat = os.stat(self.path) if self.exists else None
        info = {
            "name": os.path.basename(self.path),
            "path": self.path,
            "size": stat.st_size if stat else 0,
            "mode": stat.st_mode if stat else 0,
            "mtime": stat.st_mtime if stat else 0,
            "uid": stat.st_uid if stat else 0,
            "gid": stat.st_gid if stat else 0
        }
        return json.dumps(info, indent=2)

    # 实现其他方法...

class gsFolder:
    def __init__(self, path, autoMake=True):
        self.path = os.path.abspath(path)
        if autoMake and not os.path.exists(self.path):
            os.makedirs(self.path)
    
    @property
    def exists(self):
        return os.path.exists(self.path)
    
    def list(self):
        result = []
        for item in os.listdir(self.path):
            full_path = os.path.join(self.path, item)
            if os.path.isdir(full_path):
                result.append(gsFolder(full_path))
            else:
                result.append(gsFile(full_path))
        return result

    # 实现其他方法...