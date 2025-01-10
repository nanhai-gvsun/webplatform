import os
import json
import shutil
from pathlib import Path

class gsFile:
    def __init__(self, path, autoLoad=False, monitor=False):
        self.path = os.path.abspath(path)
        self.content = None
        if autoLoad:
            self.read()
        # TODO: implement file monitoring
        self.monitor = monitor
    
    @property
    def exists(self):
        return os.path.isfile(self.path)
    
    def parent(self, data=None):
        if data is None:
            parent_path = os.path.dirname(self.path)
            return gsFolder(parent_path)
        else:
            new_path = os.path.join(data, os.path.basename(self.path))
            self.move(new_path)
            return self
    
    def __str__(self):
        if not self.exists:
            return json.dumps({
                "exists": False,
                "path": self.path
            })
        
        stat = os.stat(self.path)
        return json.dumps({
            "name": os.path.basename(self.path),
            "path": self.path,
            "size": stat.st_size,
            "mode": stat.st_mode,
            "mtime": stat.st_mtime,
            "uid": stat.st_uid,
            "gid": stat.st_gid
        })
    
    def read(self, binary=False):
        mode = 'rb' if binary else 'r'
        with open(self.path, mode) as f:
            self.content = f.read()
        return self.content
    
    def write(self, data=None):
        if data is not None:
            self.content = data
        if self.content is not None:
            mode = 'wb' if isinstance(self.content, bytes) else 'w'
            with open(self.path, mode) as f:
                f.write(self.content)
        return self
    
    def readJson(self):
        content = self.read()
        return json.loads(content)
    
    def writeJson(self, data=None):
        if data is not None:
            self.content = json.dumps(data)
        return self.write()
    
    def rename(self, data=None):
        if data:
            new_path = os.path.join(os.path.dirname(self.path), data)
            os.rename(self.path, new_path)
            self.path = new_path
        return self
    
    def copy(self, data=None):
        if data:
            shutil.copy2(self.path, data)
        return self
    
    def move(self, data=None):
        if data:
            shutil.move(self.path, data)
            self.path = data
        return self

class gsFolder:
    def __init__(self, path, autoMake=True):
        self.path = os.path.abspath(path)
        if autoMake and not self.exists:
            os.makedirs(self.path)
    
    @property
    def exists(self):
        return os.path.isdir(self.path)
    
    def parent(self, data=None):
        if data is None:
            parent_path = os.path.dirname(self.path)
            return gsFolder(parent_path)
        else:
            new_path = os.path.join(data, os.path.basename(self.path))
            self.move(new_path)
            return self
    
    def __str__(self):
        if not self.exists:
            return json.dumps({
                "exists": False,
                "path": self.path
            })
        
        stat = os.stat(self.path)
        return json.dumps({
            "name": os.path.basename(self.path),
            "path": self.path,
            "size": stat.st_size,
            "mode": stat.st_mode,
            "mtime": stat.st_mtime,
            "uid": stat.st_uid,
            "gid": stat.st_gid
        })
    
    def list(self):
        result = []
        for item in os.listdir(self.path):
            full_path = os.path.join(self.path, item)
            if os.path.isdir(full_path):
                result.append(gsFolder(full_path))
            else:
                result.append(gsFile(full_path))
        return result
    
    def rename(self, data=None):
        if data:
            new_path = os.path.join(os.path.dirname(self.path), data)
            os.rename(self.path, new_path)
            self.path = new_path
        return self
    
    def mkdir(self, data=None):
        if data:
            new_path = os.path.join(self.path, data)
            os.makedirs(new_path, exist_ok=True)
            return gsFolder(new_path)
        return self
    
    def rmdir(self, data=None):
        target_path = os.path.join(self.path, data) if data else self.path
        shutil.rmtree(target_path)
        return self
    
    def copy(self, data=None):
        if data:
            shutil.copytree(self.path, data)
        return self
    
    def move(self, data=None):
        if data:
            shutil.move(self.path, data)
            self.path = data
        return self
    
    def delete(self, data=None):
        if data:
            target_path = os.path.join(self.path, data)
            if os.path.exists(target_path):
                if os.path.isdir(target_path):
                    shutil.rmtree(target_path)
                else:
                    os.remove(target_path)
        return self
 