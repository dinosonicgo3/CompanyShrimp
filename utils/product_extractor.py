#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
商品資訊提取工具
"""

from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json


class ProductExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def from_url(self, url: str) -> Dict:
        """從網址提取商品資訊"""
        print(f"從網址提取：{url}")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 嘗試從常見的結構提取
            product_info = self._extract_from_html(soup, url)
            
            if not product_info.get("name"):
                print("警告：無法提取商品名稱，請手動填寫")
            
            return product_info
            
        except Exception as e:
            print(f"提取失敗：{e}")
            return self._empty_product()

    def from_file(self, file_path: str) -> Dict:
        """從檔案提取商品資訊"""
        print(f"從檔案提取：{file_path}")
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"檔案不存在：{file_path}")
            return self._empty_product()
        
        # 根據副檔名決定處理方式
        if file_path.suffix.lower() in (".json",):
            return self._from_json(file_path)
        elif file_path.suffix.lower() in (".txt", ".csv"):
            return self._from_text(file_path)
        elif file_path.suffix.lower() in (".html", ".htm"):
            return self._from_html(file_path)
        else:
            print(f"不支援的檔案格式：{file_path.suffix}")
            return self._empty_product()

    def _from_json(self, file_path: Path) -> Dict:
        """從 JSON 檔案提取"""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return self._normalize_product_info(data)

    def _from_text(self, file_path: Path) -> Dict:
        """從文字檔案提取"""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 嘗試解析文字內容
        lines = content.strip().split("\n")
        
        info = self._empty_product()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 簡單的鍵值對解析
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                
                if "名稱" in key or "name" in key:
                    info["name"] = value
                elif "描述" in key or "description" in key:
                    info["description"] = value
                elif "價格" in key or "price" in key:
                    info["price"] = value
                elif "分類" in key or "category" in key:
                    info["category"] = value
        
        return info

    def _from_html(self, file_path: Path) -> Dict:
        """從 HTML 檔案提取"""
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()
        
        soup = BeautifulSoup(html, "html.parser")
        return self._extract_from_html(soup, str(file_path))

    def _extract_from_html(self, soup, source: str) -> Dict:
        """從 HTML 提取商品資訊"""
        info = self._empty_product()
        
        # 嘗試從 meta 標籤提取
        meta_mapping = {
            "og:title": "name",
            "og:description": "description",
            "og:image": "images",
            "product:name": "name",
            "product:description": "description",
            "product:price:amount": "price",
            "twitter:title": "name",
            "twitter:description": "description",
            "twitter:image": "images"
        }
        
        for meta in soup.find_all("meta"):
            prop = meta.get("property") or meta.get("name")
            content = meta.get("content")
            
            if prop and content:
                for pattern, key in meta_mapping.items():
                    if pattern in prop.lower():
                        if key == "images":
                            info[key].append(content)
                        else:
                            info[key] = content
        
        # 嘗試從 JSON-LD 提取
        json_ld_scripts = soup.find_all("script", {"type": "application/ld+json"})
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    info.update(self._extract_from_jsonld(data))
                elif isinstance(data, list):
                    for item in data:
                        info.update(self._extract_from_jsonld(item))
            except:
                pass
        
        # 嘗試從 h1, h2 提取
        if not info.get("name"):
            for tag in soup.find_all(["h1", "h2"]):
                text = tag.get_text().strip()
                if text and len(text) < 200:
                    info["name"] = text
                    break
        
        # 提取所有圖片
        if not info["images"]:
            img_tags = soup.find_all("img")
            for img in img_tags:
                src = img.get("src") or img.get("data-src")
                if src and not src.startswith("data:"):
                    if len(info["images"]) < 10:  # 限制最多 10 張
                        if not src.startswith("http"):
                            src = self._resolve_url(src, source)
                        info["images"].append(src)
        
        return info

    def _extract_from_jsonld(self, data: Dict) -> Dict:
        """從 JSON-LD 提取"""
        info = {}
        
        if data.get("@type") == "Product":
            info["name"] = data.get("name", "")
            info["description"] = data.get("description", "")
            
            if "image" in data:
                images = data["image"]
                if isinstance(images, str):
                    info["images"] = [images]
                elif isinstance(images, list):
                    info["images"] = images
                else:
                    info["images"] = []
            
            if "offers" in data:
                offers = data["offers"]
                if isinstance(offers, dict):
                    info["price"] = offers.get("price", "")
        
        return info

    def _normalize_product_info(self, data: Dict) -> Dict:
        """標準化商品資訊"""
        info = self._empty_product()
        
        # 常見的欄位名稱對應
        field_mapping = {
            "name": ["name", "title", "product_name", "商品名稱", "名稱"],
            "description": ["description", "desc", "product_description", "商品描述", "描述", "介紹"],
            "price": ["price", "價格", "售價"],
            "category": ["category", "分類", "類別"],
            "images": ["images", "image", "圖片", "imgs"]
        }
        
        for field, possible_names in field_mapping.items():
            for name in possible_names:
                if name in data and data[name]:
                    if field == "images":
                        if isinstance(data[name], str):
                            info[field].append(data[name])
                        elif isinstance(data[name], list):
                            info[field].extend(data[name])
                    else:
                        info[field] = data[name]
                        break
        
        return info

    def _resolve_url(self, url: str, base: str) -> str:
        """解析相對 URL"""
        if url.startswith("http"):
            return url
        
        parsed_base = urlparse(base)
        base_url = f"{parsed_base.scheme}://{parsed_base.netloc}"
        
        if url.startswith("//"):
            return f"{parsed_base.scheme}:{url}"
        elif url.startswith("/"):
            return f"{base_url}{url}"
        else:
            path = "/".join(parsed_base.path.split("/")[:-1])
            return f"{base_url}{path}/{url}"

    def _empty_product(self) -> Dict:
        """空的商品資訊結構"""
        return {
            "name": "",
            "description": "",
            "price": "",
            "category": "",
            "images": [],
            "metadata": {}
        }


def main():
    """測試用"""
    extractor = ProductExtractor()
    
    # 測試網址
    test_url = "https://example.com"
    result = extractor.from_url(test_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
