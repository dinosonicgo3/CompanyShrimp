#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公司蝦 - 蝦皮自動上架工具
"""

import os
import json
import sys
from pathlib import Path

# 將專案根目錄加入路徑
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

class CompanyShrimp:
    def __init__(self):
        self.config = self.load_config()
        self.download_folder = Path(self.config["image_settings"]["download_folder"])
        self.download_folder.mkdir(exist_ok=True)
        self.setup_environment()

    def load_config(self):
        """載入配置檔"""
        config_path = ROOT_DIR / "config.json"
        if not config_path.exists():
            return self.create_default_config()
        
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def create_default_config(self):
        """建立預設配置"""
        default_config = {
            "app_name": "公司蝦",
            "version": "1.0.0",
            "shopee": {
                "shop_url": "",
                "api_key": "",
                "shop_id": ""
            },
            "pricing": {
                "base_price": 0,
                "markup_percentage": 0,
                "rules": [
                    "價格規則待設定"
                ]
            },
            "image_settings": {
                "max_size_kb": 1024,
                "formats": ["jpg", "jpeg", "png"],
                "download_folder": "./downloads"
            },
            "ai": {
                "api_endpoint": "",
                "model": "",
                "temperature": 0.7
            }
        }
        
        config_path = ROOT_DIR / "config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        print("已建立預設配置檔：config.json")
        print("請在 config.json 中填入您的設定")
        
        return default_config

    def setup_environment(self):
        """設定環境變數"""
        from dotenv import load_dotenv
        
        env_path = ROOT_DIR / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        else:
            print("警告：未找到 .env 檔案")

    def download_images(self, urls, folder=None):
        """下載圖片"""
        from utils.image_downloader import ImageDownloader
        
        downloader = ImageDownloader(
            download_folder=folder or self.download_folder,
            max_size_kb=self.config["image_settings"]["max_size_kb"]
        )
        
        return downloader.download_urls(urls)

    def extract_product_info(self, source):
        """提取商品資訊"""
        from utils.product_extractor import ProductExtractor
        
        extractor = ProductExtractor()
        
        if source.startswith("http"):
            # 從網址提取
            return extractor.from_url(source)
        else:
            # 從檔案提取
            return extractor.from_file(source)

    def generate_listing(self, product_info):
        """生成蝦皮上架資料"""
        from plugins.shopee_generator import ShopeeListingGenerator
        
        generator = ShopeeListingGenerator(
            pricing_rules=self.config["pricing"]["rules"],
            ai_config=self.config["ai"]
        )
        
        return generator.generate(product_info)

    def upload_to_shopee(self, listing_data):
        """上傳到蝦皮"""
        from plugins.shopee_uploader import ShopeeUploader
        
        uploader = ShopeeUploader(
            shop_url=self.config["shopee"]["shop_url"],
            api_key=self.config["shopee"]["api_key"],
            shop_id=self.config["shopee"]["shop_id"]
        )
        
        return uploader.upload(listing_data)

    def run_flow(self, source, auto_upload=False):
        """執行完整流程"""
        try:
            print(f"開始處理來源：{source}")
            
            # 1. 提取商品資訊
            print("步驟 1: 提取商品資訊...")
            product_info = self.extract_product_info(source)
            print(f"找到商品：{product_info.get('name', '未知')}")
            
            # 2. 下載圖片
            print("步驟 2: 下載圖片...")
            image_urls = product_info.get("images", [])
            downloaded_images = self.download_images(image_urls)
            print(f"下載了 {len(downloaded_images)} 張圖片")
            
            # 3. 生成上架資料
            print("步驟 3: 生成上架資料...")
            listing_data = self.generate_listing(product_info)
            print(f"生成上架資料：{listing_data.get('title', '未知')}")
            print(f"建議售價：{listing_data.get('price', '未知')}")
            
            # 4. 上傳到蝦皮
            if auto_upload:
                print("步驟 4: 上傳到蝦皮...")
                result = self.upload_to_shopee(listing_data)
                print(f"上傳結果：{result}")
            else:
                print("步驟 4: 跳過自動上傳（設定 auto_upload=True 以啟用）")
                print("生成的上架資料已準備好")
            
            return listing_data
            
        except Exception as e:
            print(f"錯誤：{e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """主程式入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="公司蝦 - 蝦皮自動上架工具")
    parser.add_argument("source", help="來源（網址或檔案路徑）")
    parser.add_argument("--upload", action="store_true", help="自動上傳到蝦皮")
    parser.add_argument("--config", help="指定配置檔路徑")
    
    args = parser.parse_args()
    
    app = CompanyShrimp()
    
    result = app.run_flow(args.source, auto_upload=args.upload)
    
    if result:
        print("\n✅ 完成！")
        print(f"商品名稱：{result.get('title', '未知')}")
        print(f"價格：{result.get('price', '未知')}")
        print(f"分類：{result.get('category', '未知')}")
    else:
        print("\n❌ 失敗")

if __name__ == "__main__":
    main()
