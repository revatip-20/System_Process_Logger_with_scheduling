import os
import psutil
import time
import schedule
from datetime import datetime

def log_processes(log_folder):
    """Logs running system processes into a timestamped file."""
    
    # Create log folder if it doesn't exist
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Timestamped log filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_folder, f"process_log_{timestamp}.txt")

    # Open log file for writing
    with open(log_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write(f"System Process Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        f.write("{:<10} {:<30} {:<20} {:<15}\n".format("PID", "Process Name", "User", "Memory %"))
        f.write("-"*75 + "\n")

        # Fetch process details
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
            try:
                pid = proc.info['pid']
                name = proc.info['name']
                user = proc.info['username']
                memory = round(proc.info['memory_percent'], 2)
                f.write("{:<10} {:<30} {:<20} {:<15}\n".format(pid, name, user, memory))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    print(f"✅ Log file created: {log_file}")


def schedule_process_logger(folder_name, interval_minutes):
    """Schedules process logging at given intervals."""
    
    print("\n=== System Process Logger with Scheduling ===")
    print(f"Logs will be saved in: {folder_name}")
    print(f"Logging interval: Every {interval_minutes} minute(s)\n")
    
    # Schedule the task
    schedule.every(interval_minutes).minutes.do(log_processes, log_folder=folder_name)

    # Run indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # Get custom folder name and interval from user
    folder = input("Enter folder name to save logs (default: 'Process_Logs'): ") or "Process_Logs"
    interval = input("Enter interval in minutes (default: 1): ") or "1"

    try:
        interval = int(interval)
    except ValueError:
        print("⚠️ Invalid interval, using default of 1 minute.")
        interval = 1

    # Start scheduled process logging
    schedule_process_logger(folder, interval)
