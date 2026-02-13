#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蝦皮上架工具
"""

from typing import Dict
import requests
import time


class ShopeeUploader:
    def __init__(self, shop_url: str, api_key: str, shop_id: str):
        self.shop_url = shop_url
        self.api_key = api_key
        self.shop_id = shop_id
        self.session = requests.Session()

    def upload(self, listing_data: Dict) -> Dict:
        """上傳商品到蝦皮"""
        try:
            print("正在上傳到蝦皮...")
            
            # 這裡有兩種方式：
            # 1. 使用 Shopee Open API（需要 API 權限）
            # 2. 使用 Selenium 自動化（模擬人工操作）
            
            # 使用 API 方式（推薦）
            result = self._upload_via_api(listing_data)
            
            # 或使用自動化方式（備用）
            # result = self._upload_via_selenium(listing_data)
            
            return result
            
        except Exception as e:
            print(f"上傳失敗：{e}")
            return {"success": False, "error": str(e)}

    def _upload_via_api(self, listing_data: Dict) -> Dict:
        """透過 Shopee API 上傳"""
        # 注意：這是框架，實際使用需要申請 Shopee Open API 權限
        
        endpoint = f"https://partner.shopee.tw/api/v2/product/create_item"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        # 準備資料
        payload = {
            "shop_id": self.shop_id,
            "item_name": listing_data["title"],
            "description": listing_data["description"],
            "original_price": listing_data["price"],
            "price": listing_data["price"],
            "stock": listing_data["stock"],
            "images": self._upload_images(listing_data["images"]),
            "category_id": self._get_category_id(listing_data["category"]),
            "logistics": [1],  # 宅配
            "weight": 0.5  # 預設重量
        }
        
        try:
            response = self.session.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("error") == "":
                return {
                    "success": True,
                    "item_id": result.get("item_id"),
                    "message": "上傳成功"
                }
            else:
                return {
                    "success": False,
                    "error": result.get("message", "未知錯誤")
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API 請求失敗：{e}"
            }

    def _upload_images(self, image_paths: list) -> list:
        """上傳圖片到蝦皮圖床"""
        # 先上傳圖片取得蝦皮圖片 ID
        image_ids = []
        
        for image_path in image_paths:
            try:
                image_id = self._upload_single_image(image_path)
                if image_id:
                    image_ids.append(image_id)
            except Exception as e:
                print(f"圖片上傳失敗：{image_path} - {e}")
        
        return image_ids

    def _upload_single_image(self, image_path: str) -> str:
        """上傳單張圖片"""
        # 這需要實際的 API 實現
        # 目前返回模擬 ID
        return f"img_{hash(image_path) % 100000}"

    def _get_category_id(self, category_name: str) -> str:
        """取得分類 ID"""
        # 這需要實際的分類映射
        # 目前返回預設值
        category_map = {
            "未分類": "0",
            "電子產品": "100",
            "服飾": "200",
            "居家用品": "300"
        }
        
        return category_map.get(category_name, "0")

    def _upload_via_selenium(self, listing_data: Dict) -> Dict:
        """透過 Selenium 自動化上傳（備用方案）"""
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # 設定 Chrome 驅動
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless")  # 無頭模式
            
            driver = webdriver.Chrome(options=options)
            
            try:
                # 1. 登入蝦皮賣家中心
                print("正在登入蝦皮賣家中心...")
                driver.get("https://shopee.tw/web/login")
                
                # 這裡需要實際的登入邏輯
                # 可能需要手動登入或使用帳號密碼
                
                time.sleep(5)
                
                # 2. 進入上架頁面
                print("進入上架頁面...")
                driver.get("https://shopee.tw/web/seller/products/add")
                
                # 等待頁面載入
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "shopee-input__input"))
                )
                
                # 3. 填寫商品資訊
                print("填寫商品資訊...")
                
                # 填寫標題
                title_input = driver.find_element(By.XPATH, "//input[@placeholder='請輸入商品名稱']")
                title_input.clear()
                title_input.send_keys(listing_data["title"])
                
                # 填寫描述
                desc_input = driver.find_element(By.XPATH, "//textarea[@placeholder='請輸入商品描述']")
                desc_input.clear()
                desc_input.send_keys(listing_data["description"])
                
                # 填寫價格
                price_input = driver.find_element(By.XPATH, "//input[@placeholder='請輸入售價']")
                price_input.clear()
                price_input.send_keys(listing_data["price"])
                
                # 上傳圖片
                print("上傳圖片...")
                # 需要實際的圖片上傳邏輯
                
                time.sleep(2)
                
                # 4. 提交
                print("提交上架...")
                submit_button = driver.find_element(By.XPATH, "//button[contains(text(), '發布')]")
                submit_button.click()
                
                time.sleep(3)
                
                return {
                    "success": True,
                    "message": "透過自動化上傳成功（需驗證）"
                }
                
            finally:
                driver.quit()
                
        except ImportError:
            print("請先安裝 Selenium: pip install selenium")
            return {
                "success": False,
                "error": "未安裝 Selenium"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"自動化上傳失敗：{e}"
            }

    def test_connection(self) -> bool:
        """測試連線"""
        try:
            test_url = f"{self.shop_url}/test"
            response = self.session.get(test_url, timeout=10)
            return response.status_code < 500
        except:
            return False


def main():
    """測試用"""
    uploader = ShopeeUploader(
        shop_url="https://shopee.tw",
        api_key="test_api_key",
        shop_id="test_shop_id"
    )
    
    test_listing = {
        "title": "測試商品",
        "description": "測試描述",
        "price": "100",
        "stock": "99",
        "category": "未分類",
        "images": []
    }
    
    result = uploader.upload(test_listing)
    print(result)


if __name__ == "__main__":
    main()
