from pytubefix.async_youtube import AsyncYouTube
from pytubefix.exceptions import VideoUnavailable
from urllib.error import HTTPError

class VideoDownloader:

    def __init__(self, output_path:str) -> None:
        self.output_path:str = output_path
    
    async def download_video(self, url) -> str | None:
        try:
            video:AsyncYouTube = AsyncYouTube(url,
                                              use_oauth=True, 
                                              allow_oauth_cache=True)
            streams = await video.streams()
            highest_stream = streams.get_highest_resolution()
            return highest_stream.download(output_path=self.output_path)
        except (VideoUnavailable, HTTPError):
            return None
