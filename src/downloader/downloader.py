from pytubefix import AsyncYouTube
from pytubefix.exceptions import VideoUnavailable, RegexMatchError

from config.logger_config import logger
from utils.string_utils import format_time_from_seconds


class Downloader:
    def __init__(self, url:str):
        self.url = url
        try:
            self.video = AsyncYouTube(self.url)
        except RegexMatchError as e:
            self.video = None
            logger.error(e)

    async def get_streams_info(self) -> dict[str, str] | None:
        """
        Возвращает словарь `resolution:'itag_{itag}:id_{id}'` для заданного списка потоков\n
        Потоки отсортированы в порядке увеличения разрешения\n
        
        :return: Словарь `resolution:'itag_{itag}:id_{id}'`
        :rtype: dict[str, str] | None
        """
        try:
            streams = await self.video.streams()
            sorted_streams = streams.order_by('resolution').otf(False)
            resolutions = {}
            for stream in sorted_streams:
                if stream.resolution != None:
                    resolutions[stream.resolution] = f'itag_{stream.itag}:id_{self.video.video_id}'
            return resolutions
        except (VideoUnavailable, AttributeError) as e:
            logger.error(e)
            return None

    async def get_video_info(self) -> dict[str, str] | None:
        """
        Получает информацию о заданном видео
        
        :return: Словарь с ключами `title`, `author`, `duration`
        :rtype: dict[str, str]
        """
        info = {}
        try:
            info['title'] = await self.video.title()
            info['author'] = await self.video.author()
            info['duration'] = format_time_from_seconds(await self.video.length())
            return info
        except (VideoUnavailable, AttributeError) as e:
            logger.error(e)
            return None
