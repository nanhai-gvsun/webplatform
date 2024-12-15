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

### Edict对象
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




### 全局函数
- 单例函数

- 运行外部命令