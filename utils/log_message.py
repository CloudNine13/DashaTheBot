from datetime import datetime


def log_message(message: str):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f'{now} - {message}')
