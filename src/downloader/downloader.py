import os
from pytubefix import AsyncYouTube
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
from pathlib import Path
from moviepy import VideoFileClip
from moviepy import AudioFileClip

from config.logger_config import logger
from utils.string_utils import format_time_from_seconds


class Downloader:
    def __init__(self, url:str | None = None, video_id:str | None = None):
        try:
            if url != None:
                self.video = AsyncYouTube(url)
            elif video_id != None:
                self.video = AsyncYouTube.from_id(video_id)
            else:
                self.video = None
        except RegexMatchError as e:
            self.video = None
            logger.error(e)

    def __get_download_path(self, destination:str='downloads') -> str:
        current_path = Path(__file__).resolve()
        project_root = current_path.parents[2]
        downloads_path = project_root.joinpath(destination)
        logger.debug(f'Downloads path: {downloads_path}')
        return str(downloads_path)

    async def get_streams_info(self) -> dict[str, str] | None:
        """
        Возвращает словарь `resolution:'itag_{itag}:id_{id}'` для заданного списка потоков\n
        Потоки отсортированы в порядке увеличения разрешения\n
        
        :return: Словарь `resolution:'itag_{itag}:id_{id}'`
        :rtype: dict[str, str] | None
        """
        if self.video == None:
            return None
        try:
            streams = await self.video.streams()
            sorted_streams = streams.filter(file_extension='mp4').order_by('resolution')
            resolutions = {}
            for stream in sorted_streams:
                resolution = stream.resolution
                if resolution != None:
                    if stream.includes_audio_track == True:
                        resolution = f'{resolution} + Аудио без склейки'
                    else:
                        resolution = f'{resolution} + Аудио со склейкой'
                    resolutions[resolution] = f'itag_{stream.itag}:id_{self.video.video_id}'
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
        if self.video == None:
            return None
        info = {}
        try:
            info['title'] = await self.video.title()
            info['author'] = await self.video.author()
            info['duration'] = format_time_from_seconds(await self.video.length())
            return info
        except (VideoUnavailable, AttributeError) as e:
            logger.error(e)
            return None

    async def download(self, stream_itag:int) -> str | None:
        """
        Загружает видео по указанному номеру потока\n
        Если поток загружается без аудио, отдельно дозагружает аудио и склеивает
        
        :param stream_itag: `itag` потока который нужно загрузить
        :type stream_itag: int
        :return: Абсолютный путь до загруженного файла
        :rtype: str | None
        """
        if self.video == None:
            return None
        video_title = await self.video.title()
        # Загружаем видео
        video_stream = await self.video.get_stream_by_itag(stream_itag)
        download_path = self.__get_download_path()
        temp_path = self.__get_download_path('temp')
        
        # Проверяем нужно ли склеивать аудио и видео
        if video_stream.includes_audio_track == True:
            logger.debug('No need to splice videos')
            video_path = video_stream.download(download_path, f'{video_title}.mp4')
            return video_path
        else:
            logger.debug('Need to splice videos')
            video_path = video_stream.download(temp_path, "video_only")
            
            #Загружаем аудио
            audio_stream = await self.video.streams()
            audio_stream = audio_stream.filter(only_audio=True).first()
            audio_path = audio_stream.download(temp_path, "audio_only")
          
            # Объединяем аудио и видео
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            final = video.with_audio(audio)

            # Записываем финальный резульат
            final_path = f'{download_path}/{video_title}.mp4'
            final.write_videofile(final_path, temp_audiofile_path=temp_path)
            os.remove(video_path)
            os.remove(audio_path)
            return final_path
