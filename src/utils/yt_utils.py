from pytubefix import StreamQuery

def get_resolution_dict(streams:StreamQuery) -> dict[str, str]:
    """
    Возвращает словарь `resolution:itag` для заданного списка потоков\n
    Потоки отсортированы в порядке увеличения разрешения
    
    :param streams: Список потоков
    :type streams: StreamQuery
    :return: Словарь `resolution:itag`
    :rtype: dict[str, str]
    """
    sorted_streams = streams.order_by('resolution')
    resolutions = {}
    for stream in sorted_streams:
        if stream.resolution != None:
            resolutions[stream.resolution] = str(stream.itag)
    return resolutions
