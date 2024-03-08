
import datetime

def print_message(message):
    """
    Prints a simple message with a timestamp.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] {message}")

def log_info(message, logfile='project_log.log'):
    """
    Logs an informational message to a specified logfile with a timestamp.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, 'a') as file:
        file.write(f"[INFO] [{current_time}] {message}\n")

def log_error(message, logfile='project_log.log'):
    """
    Logs an error message to a specified logfile with a timestamp.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, 'a') as file:
        file.write(f"[ERROR] [{current_time}] {message}\n")
