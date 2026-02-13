import os
import requests
import logging
from uuid import uuid4

class ImageDownloader:
    def __init__(self, download_dir="downloads"):
        self.download_dir = download_dir
        self.logger = logging.getLogger("shrimp.downloader")
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download(self, urls):
        downloaded_paths = []
        for url in urls:
            try:
                self.logger.info(f"正在下載圖片: {url}")
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    filename = f"{uuid4().hex}.jpg"
                    filepath = os.path.join(self.download_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    downloaded_paths.append(filepath)
            except Exception as e:
                self.logger.error(f"下載圖片失敗: {url}, 錯誤: {str(e)}")
        return downloaded_paths
