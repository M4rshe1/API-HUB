from colorama import Fore, Style
from datetime import datetime

# DEBUG = 0
# INFO = 1
# WARNING = 2
# ERROR = 3
# CRITICAL = 4


def log(message: str, level: int, header: str, enabled: bool, lvl: int):
    current_time = datetime.now()
    time = current_time.strftime('[%d/%b/%Y %H:%M:%S]')
    log_msg = ""
    if level == 0:
        print(f"{time} {Fore.BLUE}[LOGGER] - [DEBUG]: message: {message}, level: {level}, enabled: {enabled}, "
              f"lvl: {lvl}{Style.RESET_ALL}")
    if enabled:
        if level <= lvl == 0:
            log_msg = f"{time} {Fore.BLUE}{header} - [DEBUG]: {message}{Style.RESET_ALL}"
        elif level <= lvl == 1:
            log_msg = f"{time} {Fore.GREEN}{header} - [INFO]: {message}{Style.RESET_ALL}"
        elif level <= lvl == 2:
            log_msg = f"{time} {Fore.RED}{header} - [WARNING]: {message}{Style.RESET_ALL}"
        elif level <= lvl == 3:
            log_msg = f"{time} {Fore.RED}{header} - [ERROR]: {message}{Style.RESET_ALL}"
        elif level <= lvl == 4:
            log_msg = f"{time} {Fore.RED}{header} - [CRITICAL]: {message}{Style.RESET_ALL}"
        # else:
        #     log_msg = f"{time} {Fore.RED}{header} - [UNKNOWN]: {message}{Style.RESET_ALL}"
        print(log_msg)

    return 0


if __name__ == '__main__':
    print("This is a module, not a script!")
