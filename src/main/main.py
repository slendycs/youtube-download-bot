import asyncio

from youtube_client.youtube_client import VideoDownloader


async def main():
    url = 'https://www.youtube.com/watch?v=BLUVshRTqwo'
    downloader = VideoDownloader('/home/slendycs/Загрузки')
    path = await downloader.download_video(url)
    print(path)


if __name__ == '__main__':
    asyncio.run(main())