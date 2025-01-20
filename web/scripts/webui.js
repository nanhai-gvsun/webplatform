// 全局变量
let activeWindow = null;
let windows = new Map();
let windowZIndex = 100;

// 工具函数
function generateWindowId() {
    return 'window-' + Math.random().toString(36).substr(2, 9);
}

function updateClock() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('zh-CN', { hour12: false });
    document.getElementById('clock').textContent = timeStr;
}

// 窗口管理
class WindowManager {
    static createWindow(title, url, width = 800, height = 600) {
        const windowId = generateWindowId();
        
        // 克隆窗口模板
        const template = document.getElementById('window-template');
        const windowElement = template.cloneNode(true);
        windowElement.id = windowId;
        windowElement.style.display = 'flex';
        windowElement.classList.remove('hidden');
        
        // 设置窗口属性
        windowElement.style.width = width + 'px';
        windowElement.style.height = height + 'px';
        windowElement.style.left = '50%';
        windowElement.style.top = '50%';
        windowElement.style.transform = 'translate(-50%, -50%)';
        
        // 设置标题
        windowElement.querySelector('.window-title').textContent = title;
        
        // 设置iframe源
        const iframe = windowElement.querySelector('iframe');
        iframe.src = url;
        
        // 添加到容器
        document.getElementById('windows-container').appendChild(windowElement);
        
        // 创建任务栏按钮
        const taskbarItem = document.createElement('button');
        taskbarItem.className = 'taskbar-item';
        taskbarItem.textContent = title;
        taskbarItem.dataset.windowId = windowId;
        document.getElementById('running-apps').appendChild(taskbarItem);
        
        // 存储窗口信息
        windows.set(windowId, {
            element: windowElement,
            taskbarItem: taskbarItem,
            title: title,
            url: url
        });
        
        // 绑定事件
        this.bindWindowEvents(windowId);
        
        // 激活窗口
        this.activateWindow(windowId);
        
        return windowId;
    }
    
    static bindWindowEvents(windowId) {
        const window = windows.get(windowId);
        const element = window.element;
        const titlebar = element.querySelector('.window-titlebar');
        const taskbarItem = window.taskbarItem;
        
        // 窗口点击激活
        element.addEventListener('mousedown', () => this.activateWindow(windowId));
        
        // 任务栏按钮点击
        taskbarItem.addEventListener('click', () => {
            if (element.classList.contains('hidden')) {
                element.classList.remove('hidden');
                this.activateWindow(windowId);
            } else if (element === activeWindow) {
                element.classList.add('hidden');
                taskbarItem.classList.remove('active');
            } else {
                this.activateWindow(windowId);
            }
        });
        
        // 窗口控制按钮
        element.querySelector('.close-btn').addEventListener('click', () => this.closeWindow(windowId));
        element.querySelector('.minimize-btn').addEventListener('click', () => {
            element.classList.add('hidden');
            taskbarItem.classList.remove('active');
        });
        element.querySelector('.maximize-btn').addEventListener('click', () => this.toggleMaximize(windowId));
        
        // 拖动功能
        this.enableDrag(windowId, titlebar);
    }
    
    static activateWindow(windowId) {
        if (activeWindow) {
            activeWindow.classList.remove('active');
            windows.get(activeWindow.id).taskbarItem.classList.remove('active');
        }
        
        const window = windows.get(windowId);
        window.element.classList.add('active');
        window.taskbarItem.classList.add('active');
        window.element.style.zIndex = ++windowZIndex;
        activeWindow = window.element;
    }
    
    static closeWindow(windowId) {
        const window = windows.get(windowId);
        window.element.remove();
        window.taskbarItem.remove();
        windows.delete(windowId);
        
        if (activeWindow === window.element) {
            activeWindow = null;
        }
    }
    
    static toggleMaximize(windowId) {
        const window = windows.get(windowId);
        const element = window.element;
        
        if (element.classList.contains('maximized')) {
            element.classList.remove('maximized');
            element.style.width = element.dataset.prevWidth;
            element.style.height = element.dataset.prevHeight;
            element.style.left = element.dataset.prevLeft;
            element.style.top = element.dataset.prevTop;
        } else {
            // 保存当前尺寸和位置
            element.dataset.prevWidth = element.style.width;
            element.dataset.prevHeight = element.style.height;
            element.dataset.prevLeft = element.style.left;
            element.dataset.prevTop = element.style.top;
            
            // 最大化
            element.classList.add('maximized');
            element.style.width = '100%';
            element.style.height = '100%';
            element.style.left = '0';
            element.style.top = '0';
        }
    }
    
    static enableDrag(windowId, titlebar) {
        let pos = { x: 0, y: 0 };
        const window = windows.get(windowId).element;
        
        titlebar.onmousedown = dragMouseDown;
        
        function dragMouseDown(e) {
            e.preventDefault();
            pos.x = e.clientX;
            pos.y = e.clientY;
            document.onmousemove = elementDrag;
            document.onmouseup = closeDragElement;
        }
        
        function elementDrag(e) {
            e.preventDefault();
            const dx = pos.x - e.clientX;
            const dy = pos.y - e.clientY;
            pos.x = e.clientX;
            pos.y = e.clientY;
            
            window.style.left = (window.offsetLeft - dx) + 'px';
            window.style.top = (window.offsetTop - dy) + 'px';
        }
        
        function closeDragElement() {
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
}

// 桌面图标管理
class DesktopManager {
    static async loadIcons() {
        try {
            const response = await fetch('./data/desktop.json');
            const data = await response.json();
            const container = document.getElementById('icons-container');
            
            data.icons.forEach(icon => {
                const iconElement = document.createElement('div');
                iconElement.className = 'desktop-icon';
                iconElement.innerHTML = `
                    <img src="${icon.icon}" alt="${icon.title}">
                    <span>${icon.title}</span>
                `;
                
                iconElement.addEventListener('dblclick', () => {
                    WindowManager.createWindow(icon.title, icon.url);
                });
                
                container.appendChild(iconElement);
            });
        } catch (error) {
            console.error('加载桌面图标失败:', error);
        }
    }
}

// 开始菜单管理
class StartMenu {
    static init() {
        const startButton = document.getElementById('start-button');
        const startMenu = document.getElementById('start-menu');
        const logoutButton = document.getElementById('logout-button');
        const settingsButton = document.getElementById('settings-button');
        
        startButton.addEventListener('click', () => {
            startMenu.classList.toggle('hidden');
        });
        
        // 点击其他地方关闭开始菜单
        document.addEventListener('click', (e) => {
            if (!startMenu.contains(e.target) && e.target !== startButton) {
                startMenu.classList.add('hidden');
            }
        });
        
        // 退出按钮
        logoutButton.addEventListener('click', () => {
            sessionStorage.removeItem('user');
            window.location.reload();
        });
        
        // 设置按钮
        settingsButton.addEventListener('click', () => {
            WindowManager.createWindow('系统设置', './page/settings/index.html');
            startMenu.classList.add('hidden');
        });
    }
}

// 时钟管理
class ClockManager {
    static init() {
        const clockElement = document.getElementById('clock');
        
        // 更新时钟
        updateClock();
        setInterval(updateClock, 1000);
        
        // 点击时钟打开日期时间设置
        clockElement.addEventListener('click', () => {
            WindowManager.createWindow('日期和时间', './page/datetime/index.html', 400, 300);
        });
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    StartMenu.init();
    ClockManager.init();
    DesktopManager.loadIcons();
}); 