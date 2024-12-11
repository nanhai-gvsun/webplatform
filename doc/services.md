## 全局服务的需求文档
### 1. 文件服务(gsFileService)
在module/services/file目录下编写文件服务，可支持本地fs系统以及通过ssh操作远端设备的fs系统，使用python编写，支持python2和python3的语法。

#### fs系统(gsFileSystemObject)
fs系统是文件系统的抽象，提供文件的读写、删除、复制、移动、列出目录、创建目录等操作。因此fs系统至少包含两个对象，一个针对文件，一个针对目录。

文件对象(gsFile)初始化参数：
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

文件夹对象(gsFolder)的初始化参数：
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


