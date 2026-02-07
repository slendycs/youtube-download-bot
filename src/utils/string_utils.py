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

def serialize_request(request:str) -> dict[str, str]:
    """
    Переводит строку вида `itag_{itag}:id_{id}` в словарь с ключами `itag` и `video_id`
    
    :param answer: Строка вида `itag_{itag}:id_{id}`
    :type answer: str
    :return: Cловарь с ключами `itag` и `video_id`
    :rtype: dict[str, str]
    """
    data = {}
    data['itag'] = request.split(':')[0].replace('itag_', '')
    data['video_id'] = request.split(':')[1].replace('id_', '')
    return data