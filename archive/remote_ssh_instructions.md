# SSH 连接脚本使用说明

## 1. 安装依赖
```bash
pip3 install paramiko
```

## 2. 修改脚本参数
在 `remote_ssh_script.py` 中修改以下参数：
```python
# Connection parameters (update with your information)
HOST = "192.168.1.100"    # 远程电脑的 IP 地址
PORT = 22                  # SSH 端口（默认是 22）
USERNAME = "your_username" # 远程电脑的用户名
```

## 3. 运行脚本
```bash
python3 remote_ssh_script.py
```

## 4. 功能说明
- 自动获取密码（安全输入，不显示）
- 执行基本命令：
  - `uname -a` - 显示系统信息
  - `whoami` - 显示当前用户
- 自动关闭连接

## 5. 安全注意事项
- 不要在公共场合运行此脚本
- 确保密码安全保管
- 不要在脚本中硬编码密码
- 使用后及时关闭连接

## 6. 进阶功能
你可以修改 `execute_command` 函数来执行其他命令，例如：
```python
execute_command(client, "ls -la")     # 列出目录内容
execute_command(client, "uptime")     # 显示系统运行时间
execute_command(client, "df -h")      # 显示磁盘使用情况
```