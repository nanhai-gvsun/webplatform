import os
import json
import shutil

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