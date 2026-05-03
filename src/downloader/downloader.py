import os
import ffmpeg
from pytubefix import AsyncYouTube
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
from pathlib import Path
from urllib.error import HTTPError

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
    
    def __merge_audio_and_video(self, video_path:str, audio_path:str, output_path:str) -> str | None:
        for p in (video_path, audio_path):
            if not Path(p).exists():
                raise FileNotFoundError(f"File not found: {p}")
            
        try:
            video_stream = ffmpeg.input(video_path)
            audio_stream = ffmpeg.input(audio_path)

            out = ffmpeg.output(
                video_stream.video,
                audio_stream.audio,
                output_path,
                vcodec='copy',
                acodec='aac',
                **{'shortest': None} 
            )

            out.run(overwrite_output=True)
            logger.info(f'Video was merged: {output_path}')
            return output_path
        except ffmpeg.Error as e:
            err = e.stderr.decode('utf8', errors='ignore') if e.stderr else 'No logs'
            logger.error(f'FFmpeg error: {err}')
            return None


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
        final_path = f'{download_path}/{video_title}.mp4'
        
        # Проверяем нужно ли склеивать аудио и видео
        try:
            if video_stream.includes_audio_track == True:
                logger.debug('No need to splice videos')
                video_path = video_stream.download(download_path, f'{video_title}.mp4')
                return video_path
            else:
                logger.debug('Need to splice videos')
                video_path = video_stream.download(temp_path, "video_only")
                if video_path is None:
                    logger.error('Error while downloading video stream')
                    return None
                
                #Загружаем аудио
                audio_stream = await self.video.streams()
                audio_stream = audio_stream.filter(only_audio=True).first()
                audio_path = audio_stream.download(temp_path, "audio_only")
                if audio_path is None:
                    logger.error('Error while downloading audio stream')
                    return None
            
                # Объединяем аудио и видео
                final_path = self.__merge_audio_and_video(video_path, audio_path, final_path)

                # Удаляем временные файлы
                os.remove(video_path)
                os.remove(audio_path)

                return final_path
        except HTTPError as e:
            logger.error(f'Some problem with request: {e}')
            return None
