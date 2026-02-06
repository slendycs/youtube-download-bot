from datetime import time

def format_time_from_seconds(seconds:int) -> str:
    """
    Переводит количество секунд в строку с временем
    
    :param seconds: Количество секунд
    :type seconds: int
    :return: Строка времени формата `%H:%M:%S`
    :rtype: str
    """
    time_struct = time(hour=seconds // 3600,
                       minute=(seconds % 3600) // 60,
                       second=(seconds % 3600) % 60)
    return time_struct.strftime('%H:%M:%S')