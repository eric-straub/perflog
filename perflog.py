# perflog 0.1
# Eric Straub
# 3/12/24

# if you want to change the period between logs just edit the sleep length on line 40

import psutil
import time
from datetime import datetime

def log_system_performance():
    with open("system_performance_log.txt", "a") as file:
        while True:
            # Timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # CPU usage
            cpu_usage = psutil.cpu_percent()
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # Disk usage for the root partition
            disk_usage = psutil.disk_usage('/').percent
            
            # Network information (sent and received bytes)
            net_io = psutil.net_io_counters()
            bytes_sent = net_io.bytes_sent
            bytes_recv = net_io.bytes_recv
            
            # Log the collected information
            log_message = f"{timestamp}, CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Disk Usage: {disk_usage}%, Bytes Sent: {bytes_sent}, Bytes Received: {bytes_recv}\n"
            file.write(log_message)
            
            # Print the message to console (optional)
            print(log_message)
            
            # Wait for a minute
            time.sleep(60)

if __name__ == "__main__":
    log_system_performance()
