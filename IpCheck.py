import os
import time
import subprocess
import logging
from datetime import datetime

# 创建日志目录
log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


# 配置日志文件命名
def configure_logger():
    current_time = datetime.now().strftime("%Y-%m-%d_%H")
    log_file = os.path.join(log_dir, f"log_{current_time}.txt")
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s', filemode='a')


# 读取配置文件中的IP地址
def read_ip_config(file_path):
    with open(file_path, 'r') as file:
        ip_addresses = [line.strip() for line in file.readlines() if line.strip()]
    return ip_addresses


# 检测IP地址的连通性
def ping_ip_addresses(ip_addresses):
    for ip in ip_addresses:
        try:
            # 在Windows上使用['ping', '-n', '1', ip]
            response = subprocess.run(['ping', '-c', '1', ip], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logging.info(f"{ip} 是可访问的:\n{response.stdout}")
        except subprocess.CalledProcessError as e:
            logging.info(f"{ip} 不可访问:\n{e.stderr}")


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
