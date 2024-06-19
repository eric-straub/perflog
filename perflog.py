# perflog 0.2
# Eric Straub
# 6/18/2024

import psutil
import time
from datetime import datetime

def get_integer_or_empty(prompt):
    while True:
        user_input = input(prompt)
        if user_input == '':
            return user_input
        try:
            return int(user_input)
        except ValueError:
            print("Please enter a valid integer or leave empty.")

def gen_perf_stats():
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
    
    # Generate and return output string
    log_message = f"{timestamp}, CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Disk Usage: {disk_usage}%, Bytes Sent: {bytes_sent}, Bytes Received: {bytes_recv}\n"
    label_message = f"{timestamp}\n\nCPU Usage: {cpu_usage}%\nMemory Usage: {memory_usage}%\nDisk Usage: {disk_usage}%\nBytes Sent: {bytes_sent}\nBytes Received: {bytes_recv}\n"
    log_and_label = [log_message, label_message]
    return log_and_label

def log_system_performance(period, green_light):
    with open("system_performance_log.txt", "a") as file:
        while green_light == True:
            # Gather performance information
            log_and_label = gen_perf_stats()

            # Write message to file
            file.write(log_and_label[0])
            
            # Print the message to console
            print(log_and_label[1])
            
            # Wait for a minute
            time.sleep(period)

def main():
    period = get_integer_or_empty('Set logging period in seconds (default 60 seconds): ')
    if period == '': period = 60
    green_light = True
    log_system_performance(period, green_light)

if __name__ == "__main__":
    main()
