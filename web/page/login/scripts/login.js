// 生成随机token
function generateToken() {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
}

// 加载工作域列表
async function loadDomains() {
    try {
        const response = await fetch('../../data/domains.json');
        const data = await response.json();
        const domainSelect = document.getElementById('domain');
        
        data.domains.forEach(domain => {
            const option = document.createElement('option');
            option.value = domain.id;
            option.textContent = `${domain.name} - ${domain.description}`;
            option.dataset.authUrl = domain.authUrl;
            domainSelect.appendChild(option);
        });

        // 设置默认选中项
        domainSelect.value = data.default;
    } catch (error) {
        console.error('加载工作域失败:', error);
    }
}

// 本地验证
async function validateLocalUser(username, password) {
    try {
        const response = await fetch('../../data/user.json');
        const data = await response.json();
        const user = data.users.find(user => 
            user.username === username && user.password === password
        );
        
        if (user) {
            // 更新token和最后访问时间
            user.token = generateToken();
            user.lastaccesstime = new Date().toISOString();
            return user;
        }
        return null;
    } catch (error) {
        console.error('本地验证失败:', error);
        return null;
    }
}

// 处理登录表单提交
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const domain = document.getElementById('domain');
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const authUrl = domain.selectedOptions[0].dataset.authUrl;

    let user = null;

    if (domain.value === 'local') {
        user = await validateLocalUser(username, password);
    } else {
        // 其他环境的验证逻辑（未实现）
        alert('该环境暂未实现');
        return;
    }

    if (user) {
        // 保存用户信息到 sessionStorage
        sessionStorage.setItem('user', JSON.stringify({
            ...user,
            domain: domain.value
        }));
        // 跳转到桌面
        window.location.href = '../../index.html';
    } else {
        alert('用户名或密码错误');
    }
});

// 页面加载时加载工作域列表
loadDomains();

// 添加切换密码显示的函数
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleButton = document.querySelector('.password-toggle');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleButton.textContent = '👁️‍🗨️';
    } else {
        passwordInput.type = 'password';
        toggleButton.textContent = '👁️';
    }
} 