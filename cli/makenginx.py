#!/usr/bin/env python3
import json
import os
from pathlib import Path

def load_gateway_config(config_path):
    """加载网关配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_nginx_config(gw_config):
    """根据网关配置生成nginx配置内容"""
    config_templates = []
    
    for server in gw_config.get('servers', []):
        server_name = server.get('server_name', '')
        listen_port = server.get('listen', 80)
        locations = server.get('locations', [])
        
        server_config = [
            f"server {{",
            f"    listen {listen_port};",
            f"    server_name {server_name};",
        ]
        
        # 添加locations配置
        for location in locations:
            path = location.get('path', '/')
            proxy_pass = location.get('proxy_pass', '')
            
            location_config = [
                f"    location {path} {{",
                f"        proxy_pass {proxy_pass};",
                "        proxy_set_header Host $host;",
                "        proxy_set_header X-Real-IP $remote_addr;",
                "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
                "    }"
            ]
            server_config.extend(location_config)
        
        server_config.append("}")
        config_templates.append('\n'.join(server_config))
    
    return '\n\n'.join(config_templates)

def save_nginx_config(config_content, output_path):
    """保存nginx配置文件"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(config_content)

def main():
    # 设置配置文件路径
    current_dir = Path(__file__).parent.parent
    gw_config_path = current_dir / 'etc' / 'conf' / 'gw.json'
    nginx_output_path = current_dir / 'etc' / 'nginx' / 'conf.d' / 'gateway.conf'
    
    try:
        # 加载网关配置
        gw_config = load_gateway_config(gw_config_path)
        
        # 生成nginx配置
        nginx_config = generate_nginx_config(gw_config)
        
        # 保存nginx配置
        save_nginx_config(nginx_config, nginx_output_path)
        
        print(f"Nginx配置文件已生成: {nginx_output_path}")
        
    except FileNotFoundError:
        print(f"错误: 找不到配置文件 {gw_config_path}")
    except json.JSONDecodeError:
        print(f"错误: 配置文件 {gw_config_path} 格式不正确")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()
