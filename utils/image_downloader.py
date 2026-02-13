#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
圖片下載工具
"""

import os
from pathlib import Path
from typing import List
from urllib.parse import urlparse
import requests
from PIL import Image
import io


class ImageDownloader:
    def __init__(self, download_folder: str = "./downloads", max_size_kb: int = 1024):
        self.download_folder = Path(download_folder)
        self.download_folder.mkdir(parents=True, exist_ok=True)
        self.max_size_kb = max_size_kb
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def download_urls(self, urls: List[str]) -> List[str]:
        """下載多張圖片並返回本地路徑"""
        downloaded = []
        
        for i, url in enumerate(urls, 1):
            try:
                local_path = self.download_image(url, index=i)
                if local_path:
                    downloaded.append(str(local_path))
                    print(f"✅ 已下載：{url[:50]}... -> {local_path}")
            except Exception as e:
                print(f"❌ 下載失敗：{url[:50]}... - {e}")
        
        return downloaded

    def download_image(self, url: str, index: int = None) -> Path:
        """下載單張圖片"""
        # 從 URL 推斷檔名
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path)
        
        if not filename or "." not in filename:
            filename = f"image_{index or 1}.jpg"
        
        # 確保副檔名正確
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            filename = filename.rsplit(".", 1)[0] + ".jpg"
        
        local_path = self.download_folder / filename
        
        # 下載
        response = self.session.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # 優化圖片大小
        image_data = response.content
        optimized_image = self.optimize_image(image_data)
        
        # 儲存
        with open(local_path, "wb") as f:
            f.write(optimized_image)
        
        return local_path

    def optimize_image(self, image_data: bytes) -> bytes:
        """優化圖片大小"""
        try:
            img = Image.open(io.BytesIO(image_data))
            
            # 轉換為 RGB
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # 維持比例，限制最大尺寸
            max_dimension = 1920
            if max(img.size) > max_dimension:
                ratio = max_dimension / max(img.size)
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            
            # 壓縮
            output = io.BytesIO()
            img.save(output, format="JPEG", quality=85, optimize=True)
            optimized_data = output.getvalue()
            
            # 檢查大小
            size_kb = len(optimized_data) / 1024
            if size_kb > self.max_size_kb:
                # 進一步壓縮
                for quality in [75, 65, 55, 45]:
                    output = io.BytesIO()
                    img.save(output, format="JPEG", quality=quality, optimize=True)
                    optimized_data = output.getvalue()
                    if len(optimized_data) / 1024 <= self.max_size_kb:
                        break
            
            print(f"圖片優化：{len(image_data) / 1024:.1f} KB -> {len(optimized_data) / 1024:.1f} KB")
            
            return optimized_data
            
        except Exception as e:
            print(f"圖片優化失敗：{e}")
            return image_data

    def clear_downloads(self):
        """清空下載目錄"""
        for file in self.download_folder.iterdir():
            if file.is_file():
                file.unlink()
        print(f"已清空下載目錄：{self.download_folder}")


def main():
    """測試用"""
    downloader = ImageDownloader()
    
    test_urls = [
        "https://via.placeholder.com/800x600.png?text=Test+Image+1",
        "https://via.placeholder.com/600x400.png?text=Test+Image+2"
    ]
    
    print("開始下載測試圖片...")
    downloaded = downloader.download_urls(test_urls)
    print(f"\n下載完成：{len(downloaded)} 張圖片")


if __name__ == "__main__":
    main()
