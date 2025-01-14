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

### 根对象gsObject
gsObject是以下所有面向文件或设备的文件对象的根对象，通过参数获取数据读写、打印输出等方面的信息
1. **核心功能**
   - **配置管理**：
     - 通过 `_Config` 方法初始化对象的配置。
     - 支持动态设置和获取对象的属性。
     - 支持通过 `cfg` 参数传递配置字典。
   - **命令执行**：
     - 通过 `__call__` 方法实现对象调用，支持执行命令。
     - 通过 `Do` 方法解析和执行命令，支持命令的路由和嵌套调用。
   - **数据模型管理**：
     - 通过 `DataModel` 方法设置和获取数据模型（如 `bin` 或 `ascii`）。
   - **打开模式管理**：
     - 通过 `OpenModel` 方法设置和获取文件的打开模式（如 `r`、`w`、`a` 等）。
   - **状态管理**：
     - 通过 `isOpen` 方法管理对象的打开状态。
2. **日志和错误处理**
   - **日志显示**：
     - 通过 `ShowLog` 方法控制是否显示日志信息。
     - 通过 `_logprint` 方法输出日志信息，支持异步调用外部日志处理函数。
   - **错误处理**：
     - 通过 `_errormsg` 方法输出错误信息，支持异步调用外部错误处理函数。
   - **数据读取**：
     - 通过 `_readdata` 方法处理读取到的数据，支持异步调用外部数据处理函数。

3. **工具方法**
   - **数据格式化**：
     - 通过 `_MakeData` 方法将输入数据格式化为字符串。
   - **控制台输出**：
     - 通过 `_printf` 方法将数据输出到控制台，支持 Python 2 和 Python 3 的兼容性。
   - **异步调用**：
     - 使用 `threading.Timer` 实现异步调用外部处理函数（如日志、错误、数据读取）。

4. **扩展接口**
   - **虚接口**：
     - `_Watch` 和 `_Service` 是虚接口方法，需要在子类中实现扩展功能。
     - `_Watch` 用于监控某种模式（如 `append`）。
     - `_Service` 用于实现服务逻辑。

5. **依赖和兼容性**
   - **依赖模块**：
     - 使用 `threading` 模块实现异步调用。
     - 使用 `sys` 模块实现控制台输出。
     - 使用 `datetime` 模块获取时间戳。
   - **兼容性**：
     - 支持 Python 2 和 Python 3 的字符串编码兼容性。

6. **对象属性**
   - **配置属性**：
     - `cfg`：存储配置字典。
     - `_modulename`：模块名称。
     - `_index`：索引值。
     - `_stopreaddata`：是否停止读取数据。
     - `_lasterrormsg`：最后一次错误信息。
     - `_lastlogmsg`：最后一次日志信息。
     - `_cmdsplit`：命令分隔符。
     - `__isopen`：对象是否打开。
     - `__isopen_default`：对象打开状态的默认值。
     - `__model_open_default`：打开模式的默认值。
     - `__data_model_default`：数据模型的默认值。
   - **处理函数**：
     - `handle_LogData`：日志处理函数。
     - `handle_ReadData`：数据读取处理函数。
     - `handle_ErrorMsg`：错误处理函数。

7. **设计模式**
   - **命令模式**：
     - 通过 `Do` 方法实现命令的路由和执行。
   - **观察者模式**：
     - 通过 `handle_LogData`、`handle_ReadData` 和 `handle_ErrorMsg` 实现事件通知。
   - **模板方法模式**：
     - `_Watch` 和 `_Service` 是模板方法，需要在子类中实现具体逻辑。


### 全局函数
- 单例函数

- 运行外部命令