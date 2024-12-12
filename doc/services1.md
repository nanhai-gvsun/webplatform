## 全局服务的需求文档
### 全局定义(module/services/__init__.py)
##### Edict对象
Edict对象继承自dict，将dict[key]转换成dict.key，支持链式操作。
- __init__ 方法：
初始化 Edict 实例时，使用一个单独的 __dict__ 字典来存储属性，而不是直接将 self 赋值给 self.__dict__。这样可以避免循环引用问题。

- __getattr__ 方法：
当访问一个不存在的属性时，返回一个新的 Edict 实例。这样可以支持链式操作，例如 data.a.b.c = 1。

- __setattr__ 方法：
当设置属性时，将属性值存储在字典中。
如果属性名是 __dict__，则使用 super 方法设置属性，以避免循环引用。

- __repr__ 方法：
使用 json.dumps 序列化 Edict 实例，并返回格式化的 JSON 字符串。这样可以方便地打印 Edict 实例的内容。

#### 系统对象组
这是一组系统对象，是全局单例对象，在初始化时，会自动创建，并赋值给全局变量。对象结构如下：
System
├── Net            ：网络对象
│ ├── getPidfromPort  ：获取网络对象
├── Process        ：进程对象
│ ├── list         ：进程列表
│ ├── getPidfromCmd：获取进程对象
│ ├── kill         ：杀死进程
├── Console        ：控制台对象
│ ├── log          ：打印日志
│ ├── info         ：打印日志
├── FileSystem     ：文件系统对象
│ ├── list         ：文件系统列表
│ ├── get          ：获取文件系统对象


### 文件服务(gsFileService)
在module/services/file目录下编写文件服务，可支持本地fs系统以及通过ssh操作远端设备的fs系统，使用python编写，支持python2和python3的语法。

#### fs系统(gsFileSystemObject)
在module/services/file/__init__.py中设计gsFileSystemObject，初始化时能够确定是访问本地的文件系统，还是通过ssh访问远程服务器上的文件系统，本地文件系统调用gsfs.py里的进行操作，远程的通过sshfs.py进行操作。

fs系统是文件系统的抽象，提供文件的读写、删除、复制、移动、列出目录、创建目录等操作。因此fs系统至少包含两个对象，一个针对文件，一个针对目录。

文件对象(gsfs.gsFile)初始化参数：
- path：文件路径。自动换成绝对路径
- autoLoad：自动加载
- monitor：启动文件监控

成员：
- content：文件内容
- exits：文件是否存在，如果不存在为False，存在是True
- partent:文件的父目录，参数data=None，如data等于None，返回当前文件的父目录，如不存在则建立。data不为None，则将当前文件移到data所对应的目录中
- __str__:返回文件相关信息的json数据，包括名字，路径，大小，权限，最后修改时间，用户，组
- read：读，支持两进制和文本读写，返回读取内容，同时更新content
- write：写，参数data=None，如果data不为None，则content=data。最后写入文件
- readJson:在之前读的基础上，尝试将读取的内容转换成json后返回
- writeJson：在之前写的基础上，如果data不为None，data内容要求是json格式，默认转换成string，再写入文件
- rename：重命名，参数data=None，如果data不为None，则将当前文件夹重命名为data。最后返回当前文件夹对象
- mkdir：创建文件夹，参数data=None，如果data不为None，则创建data所对应的文件夹。最后返回当前文件夹对象
- rmdir：删除文件夹，参数data=None，如果data不为None，则删除data所对应的文件夹。最后返回当前文件夹对象
- copy：复制文件夹，参数data=None，如果data不为None，则复制data所对应的文件夹。最后返回当前文件夹对象
- move：移动文件夹，参数data=None，如果data不为None，则移动data所对应的文件夹。最后返回当前文件夹对象

文件夹对象(gsfs.gsFolder)的初始化参数：
- path：文件夹路径。自动换成绝对路径
- autoMake：=True，如果path不存在的话，自动生成

成员：
- exits：文件夹是否存在，如果不存在为False，存在是True
- partent:文件夹的父目录，参数data=None，如data等于None，返回当前文件夹的父目录的文件夹对象，如不存在则建立。data不为None，则将当前文件移到data所对应的目录中
- __str__:返回文件相关信息的json数据，包括名字，路径，大小，权限，最后修改时间，用户，组
- list：返回当前目录的子目录和子文件列表，返回值为列表，列表的元素为文件夹对象和文件对象
- rename：重命名，参数data=None，如果data不为None，则将当前文件夹重命名为data。最后返回当前文件夹对象
- mkdir：创建文件夹，参数data=None，如果data不为None，则创建data所对应的文件夹。最后返回当前文件夹对象
- rmdir：删除文件夹，参数data=None，如果data不为None，则删除data所对应的文件夹。最后返回当前文件夹对象
- copy：复制文件夹，参数data=None，如果data不为None，则复制data所对应的文件夹。最后返回当前文件夹对象
- move：移动文件夹，参数data=None，如果data不为None，则移动data所对应的文件夹。最后返回当前文件夹对象
- delete：删除文件，参数data=None，如果data不为None，则删除data所对应的文件。最后返回当前文件对象

远程sshclient对象
用于连接远程ssh服务器，可执行远程命令，上传和下载以及实现远程命令的交互模式。
初始化参数：
- username:用户名
- password:密码 
- port:端口
- host:主机

远程文件夹对象(sshfs.gsFolder)的初始化参数：
- path：文件夹路径。自动换成绝对路径
- autoMake：=True，如果path不存在的话，自动生成
- sshhandle:ssh连接对象，
- username:用户名
- password:密码 
- port:端口
- host:主机

说明：
sshhandle和username、password、port、host是互斥的，如果sshhandle不为None，则username、password、port、host无效。

当远程文件夹对象返回子目录和子文件时，子目录和子文件的类型为sshfs.gsFolder和sshfs.gsFile，在初始化时可将sshhandle传递给sshfs.gsFolder和sshfs.gsFile，这样在sshfs.gsFolder和sshfs.gsFile中就可以使用sshhandle进行操作。

成员：
- exits：文件夹是否存在，如果不存在为False，存在是True
- partent:文件夹的父目录，参数data=None，如data等于None，返回当前文件夹的父目录的文件夹对象，如不存在则建立。data不为None，则将当前文件移到data所对应的目录中
- __str__:返回文件相关信息的json数据，包括名字，路径，大小，权限，最后修改时间，用户，组
- list：返回当前目录的子目录和子文件列表，返回值为列表，列表的元素为文件夹对象和文件对象
- rename：重命名，参数data=None，如果data不为None，则将当前文件夹重命名为data。最后返回当前文件夹对象
- mkdir：创建文件夹，参数data=None，如果data不为None，则创建data所对应的文件夹。最后返回当前文件夹对象
- rmdir：删除文件夹，参数data=None，如果data不为None，则删除data所对应的文件夹。最后返回当前文件夹对象
- copy：复制文件夹，参数data=None，如果data不为None，则复制data所对应的文件夹。最后返回当前文件夹对象
- move：移动文件夹，参数data=None，如果data不为None，则移动data所对应的文件夹。最后返回当前文件夹对象
- delete：删除文件，参数data=None，如果data不为None，则删除data所对应的文件。最后返回当前文件对象
