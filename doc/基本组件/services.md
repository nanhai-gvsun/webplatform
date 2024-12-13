## 全局服务的需求文档
说有代码使用python编写，支持python2和python3的语法，代码保存在module/services/__init__.py文件中。其中操作支持在windows和linux下都可以运行

### 定义模块版本信息
- __version__ = '0.0.1' # 版本号
- __author__ = '李品勇' # 作者
- __email__ = 'lipy.sh.gvsun.com@gmail.com' # 邮箱
- __description__ = '模块描述' # 描述
- __url__ = 'https://github.com/nanhai-gvsun/webplatform' # 项目地址
- __license__ = 'MIT' # 许可证
- __copyright__ = 'Copyright 2024 lipinyong' # 版权
- __release_date__ = '2024-12-13' # 发布时间

### 全局常量
- isPY2：判断当前环境是否为python2
- isPY3：判断当前环境是否为python3
- isWindows：判断当前环境是否为windows系统
- isLinux：判断当前环境是否为linux系统
- isMac：判断当前环境是否为mac系统
- isARM CPU：判断当前环境是否为ARM CPU
- isX86 CPU：判断当前环境是否为X86 CPU
- is64bit OS：判断当前环境是否为64位系统
- is32bit OS：判断当前环境是否为32位系统

### 全局定义
#### 汇总
- SingletonMeta 元类：单例元类，确保每个类只有一个实例。
- Bus 类：路由总线类，用于注册和执行路由。
- File 类：文件操作类，支持文件的读取、写入、删除、复制和移动。
- Folder 类：目录操作类，支持目录的创建、删除和列出内容。
- FileSystem 类：文件系统操作类，支持文件和目录的操作。
- CommandResult 类：命令执行结果类，包含标准输出、标准错误和返回码。
- Console 类：控制台操作类，支持命令执行、日志记录、光标操作和屏幕清除。
- SystemInfo 类：系统信息类，提供 CPU、内存、磁盘和网络信息的获取。
- Process 类：进程对象类，包含进程的详细信息和操作。
- Processes 类：进程管理类，支持进程的启动、停止、监控和查找。
- Device 类：设备对象类，支持设备的连接、断开、读取和写入。
- Devices 类：设备管理类，支持设备的添加、移除和查找。
- _System 类：系统对象组，包含进程管理、控制台、文件系统、系统信息和设备管理。
- 其他全局函数：提供获取 CPU、内存、磁盘和网络信息的函数。
#### Edict对象
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
#### 路由总线对象
在当前主进程中存在的命令总线，继承自Edict，可注册命令，并可通过关键字执行命令。
注册命令使用的是key，执行命令使用的是value。key支持目录结构，规则满足restful风格。比如以下的key：
- /users/list                       : 获取用户列表
- /users/{id}                       : 获取指定用户对象
- /users/{id}/info                  : 获取指定用户的信息，等于users.get(id).info
- /auth/from_card/{card_no}         ：验证卡号的权限
- /auth/from_token/{token}          ：验证token的权限
- /auth/from_username/{username}    ：验证用户名的权限
- /auth/login/{username}/{password} ：返回用户的权限信息

注册方式支持装饰符形式，比如：
```python
@bus.register('/users/list')
def get_user_list():
    return 'user list'
```

运行方式比如：
```python
userdata=Edict({"id": '', "name": "User Name", "email": "user@example.com"})
@bus.register('/users/{id}')
def get_user_info(id):
    userdata.id=id
    return userdata
@bus.register('/users/{id}/set')
def set_user_info(id,*args,**kwargs):
    user=bus.execute('/users/{}'.format(id))
    for k,v in kwargs.items():
        user[k]=v
    return self
@bus.register('/users/{id}')
def get_user_info(id):
    return {"id": id, "name": "User Name", "email": "user@example.com"}
print(bus.execute("/users/123"))  # 输出: {'id': 123, 'name': 'User Name', 'email': 'user@example.com'}
print(bus.execute("/users/123/set",name="New Name",email="new@example.com").execute("/users/123"))  # 输出: {'id': 123, 'name': 'New Name', 'email': 'user@example.com'}
```
路由总线对象有成员__call__,等价于执行execute方法
#### FileSystem对象
简称fs，是文件系统的抽象，提供文件的读写、删除、复制、移动、列出目录、创建目录等操作。因此fs系统至少包含两个对象，一个针对文件，一个针对目录。 。初始化时能够确定是访问本地的文件系统，还是通过ssh访问远程服务器上的文件系统，默认是本地文件系统，可通过初始化参数可以通过ssh操作远程服务器。
#### Console对象
简称con，是命令行的抽象，提供命令的执行、输出重定向、输入重定向、获取命令执行结果等操作。因此con系统至少包含两个对象，一个用于执行命令，一个用于获取命令执行结果。

console对象，还有两个静态成员,log和info。
- log方法的需求：
    - log支持在屏幕上打印并写入到日志文件中，如果console对象设定了日志目录，则在输出到日志文件时，已最后行附加的方式写到日志目录/yyyymmdd.log中，如果设定了日志文件的话，则写入到日志文件中,无需动态生成要写入的文件

    - 在打印和写入日志文件时，使用的一行日志的格式：[yyyy-mm-dd hh:mm:ss] [info] [message]。默认是info，还可以是warn、error、debug、critical等。
    
    - log方法需要针对写入的内容使用\n分割，写入到日志文件中。

- info方法的需求：
    - 支持在屏幕上打印信息，支持不换行打印信息，支持光标的操作
#### SystemInfo对象
简称si，是系统信息的抽象，提供获取CPU、内存、磁盘、网络、系统信息等操作。因此si系统至少包含多个对象，每个对象对应一个系统信息，例如CPU、内存、磁盘、网络等。
#### Prosseses对象
- processes对象是进程管理的对象，管理当前进程
- 支持返回当前进程列表
- 单一进程是process对象，包含
    - pid：进程id
    - name：进程名
    - cmd：进程启动命令
    - port：进程监听端口
    - status：进程状态
    - start_time：进程启动时间
    - end_time：进程结束时间
    - 停止：停止进程
    - 重启：重启进程
- 支持启动进程
- 支持通过pid返回指定process对象
- 支持通过进程名返回指定process对象(或数组)
- 支持通过监听端口返回指定的process对象
- 支持启动一个线程，监控后台进程池里的进程，如果进程不存在，则自动启动。
- 支持创建pid文件，内容是主进程的pid，如果主进程再次启动，则将之前记录的pid杀掉，将当前的pid写入pid文件。
#### devices对象
- devices对象是设备管理对象，管理当前设备
- 支持返回当前设备列表
- 单一设备是device对象，包含
    - name：设备名
    - ip：设备ip
    - port：设备端口
- 读写设备
#### 系统对象组
这是一组系统对象，是全局单例对象，在初始化时，会自动创建，并赋值给全局变量。对象结构如下：
System
├── Processes        ：进程对象
├── Console        ：控制台对象
├── FileSystem     ：文件系统对象
├── SystemInfo     ：文件系统对象
├── cmds           ：路由总线对象
#### 其他全局函数
- getCPUInfo：获取CPU信息
- getMemoryInfo：获取内存信息
- getDiskInfo：获取磁盘信息
- getNetworkInfo：获取网络信息
- getSystemInfo：获取系统信息,返回Edict对象数据
