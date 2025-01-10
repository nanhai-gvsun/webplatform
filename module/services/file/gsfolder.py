import os
import json
import shutil
from .gsfile import gsFile

class gsFolder:
    def __init__(self, path, autoMake=True):
        self.path = os.path.abspath(path)
        if autoMake and not os.path.exists(self.path):
            os.makedirs(self.path)
    
    @property
    def exists(self):
        return os.path.exists(self.path)
    
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