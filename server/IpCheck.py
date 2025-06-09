import os
import time
import subprocess
import logging
from datetime import datetime
import platform
import sys

# 创建日志目录
log_dir = "../log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


# 配置日志文件命名
def configure_logger():
    current_time = datetime.now().strftime("%Y-%m-%d_%H")
    log_file = os.path.join(log_dir, f"log_{current_time}.txt")
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', filemode='a')
    print(f"日志文件地址: {log_file}")


# 读取配置文件中的IP地址
def read_ip_config(file_path):
    if not os.path.exists(file_path):
        print(f"错误: 文件 {file_path} 不存在。请创建配置文件：config.txt")
        logging.error(f"文件 {file_path} 不存在。")
        sys.exit(1)  # 退出程序
    with open(file_path, 'r') as file:
        ip_addresses = [line.strip() for line in file.readlines() if line.strip()]
        print(f"配置文件内容: {ip_addresses}")
        logging.info(f"配置文件内容: {ip_addresses}")
    return ip_addresses


# 检测IP地址的连通性
def ping_ip_addresses(ip_addresses):
    for ip in ip_addresses:
        try:
            # 根据不同的操作系统选择不同的ping参数
            if platform.system() == 'Windows':
                response = subprocess.run(['ping', '-n', '4', ip], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:  # 假设为Unix/Linux/MacOS
                response = subprocess.run(['ping', '-c', '4', ip], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logging.info(f"{ip} 是可访问的:\n{response.stdout}")
            print(f"{ip} 是可访问的:\n{response.stdout}")
        except subprocess.CalledProcessError as e:
            logging.info(f"{ip} 不可访问:\n{e.stderr}")
            print(f"{ip} 不可访问:\n{e.stderr}")


# 主程序
def main():
    while True:
        # 每次循环配置新的日志文件
        configure_logger()
        ip_addresses = read_ip_config('config.txt')

        ping_ip_addresses(ip_addresses)

        # 等待3分钟后再进行下一次检测
        time.sleep(180)


if __name__ == "__main__":
    main()
