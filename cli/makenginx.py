#!/usr/bin/python
import json
import os
from pathlib import Path
import argparse

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

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='生成Nginx配置文件')
    parser.add_argument('-c', '--config', 
                      help='网关配置文件路径 (默认: etc/conf/gw.json)',
                      default=None)
    parser.add_argument('-o', '--output',
                      help='Nginx配置输出路径 (默认: etc/nginx/conf.d/gateway.conf)',
                      default=None)
    args = parser.parse_args()
    
    # 获取当前工作目录和脚本所在目录
    current_dir = Path(__file__).parent.parent
    work_dir = Path.cwd()
    
    # 处理配置文件路径
    if args.config:
        config_path = Path(args.config)
        if not config_path.is_absolute():
            config_path = work_dir / config_path
    else:
        config_path = current_dir / 'etc' / 'conf' / 'apps' / 'gw.json'
    
    # 处理输出文件路径
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = work_dir / output_path
    else:
        output_path = current_dir / 'etc' / 'nginx' / 'conf.d' / 'gateway.conf'
    
    # 打印处理后的路径信息
    print(f"配置文件路径: {os.path.abspath(config_path.absolute())}")
    print(f"输出文件路径: {output_path.absolute()}")
    
    return config_path.absolute(), output_path.absolute()

def main():
    # 获取解析后的绝对路径
    gw_config_path, nginx_output_path = parse_args()
    
    try:
        # 检查配置文件是否存在
        if not gw_config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {gw_config_path}")
            
        # 检查输出目录是否可写
        output_dir = nginx_output_path.parent
        if output_dir.exists() and not os.access(output_dir, os.W_OK):
            raise PermissionError(f"输出目录无写入权限: {output_dir}")
        
        # 加载网关配置
        gw_config = load_gateway_config(gw_config_path)
        
        # 生成nginx配置
        nginx_config = generate_nginx_config(gw_config)
        
        # 保存nginx配置
        save_nginx_config(nginx_config, nginx_output_path)
        
        print(f"Nginx配置文件已生成: {nginx_output_path}")
        
    except FileNotFoundError as e:
        print(f"错误: {str(e)}")
    except json.JSONDecodeError:
        print(f"错误: 配置文件 {gw_config_path} 格式不正确")
    except PermissionError as e:
        print(f"错误: {str(e)}")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()
