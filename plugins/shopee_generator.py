#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蝦皮上架資料生成器
"""

from typing import Dict, List
import json


class ShopeeListingGenerator:
    def __init__(self, pricing_rules: List[str] = None, ai_config: Dict = None):
        self.pricing_rules = pricing_rules or []
        self.ai_config = ai_config or {}

    def generate(self, product_info: Dict) -> Dict:
        """生成蝦皮上架資料"""
        listing = {
            "title": self._generate_title(product_info),
            "description": self._generate_description(product_info),
            "price": self._calculate_price(product_info),
            "category": self._determine_category(product_info),
            "images": product_info.get("images", []),
            "stock": self._estimate_stock(product_info),
            "attributes": self._extract_attributes(product_info),
            "shipping": self._get_shipping_settings(),
            "tags": self._generate_tags(product_info)
        }
        
        # 驗證資料完整性
        self._validate_listing(listing)
        
        return listing

    def _generate_title(self, product_info: Dict) -> str:
        """生成商品標題"""
        name = product_info.get("name", "").strip()
        
        if not name:
            return "待填寫商品名稱"
        
        # 蝦皮標題建議：簡潔 + 關鍵字
        # 限制長度（蝦皮通常約 40-60 字）
        max_length = 60
        if len(name) > max_length:
            name = name[:max_length] + "..."
        
        return name

    def _generate_description(self, product_info: Dict) -> str:
        """生成商品描述"""
        desc = product_info.get("description", "").strip()
        
        if not desc:
            desc = "商品描述待填寫"
        
        # 結構化描述
        description = f"""商品名稱：{product_info.get('name', '未設定')}

商品描述：
{desc}

注意事項：
- 實際商品以收到的為主
- 如有疑問請先詢問"""
        
        return desc

    def _calculate_price(self, product_info: Dict) -> str:
        """計算價格"""
        # 嘗試從商品資訊取得原價
        original_price = product_info.get("price", "")
        
        if original_price:
            try:
                # 移除非數字字元
                price_num = float("".join(filter(str.isdigit, original_price)))
                
                # 套用定價規則
                if self.pricing_rules:
                    price_num = self._apply_pricing_rules(price_num)
                
                return str(int(price_num))
            except:
                pass
        
        return "0"

    def _apply_pricing_rules(self, base_price: float) -> float:
        """套用定價規則"""
        # 這裡可以根據具體規則來計算
        # 例如：加成、折扣等
        
        price = base_price
        
        for rule in self.pricing_rules:
            if isinstance(rule, str):
                if "加成" in rule or "markup" in rule.lower():
                    try:
                        percentage = float("".join(filter(str.isdigit, rule)))
                        price *= (1 + percentage / 100)
                    except:
                        pass
                elif "折扣" in rule or "discount" in rule.lower():
                    try
                        percentage = float("".join(filter(str.isdigit, rule)))
                        price *= (1 - percentage / 100)
                    except:
                        pass
        
        return max(1, price)  # 確保價格至少為 1

    def _determine_category(self, product_info: Dict) -> str:
        """決定商品分類"""
        category = product_info.get("category", "").strip()
        
        if not category:
            category = "未分類"
        
        # 可以根據商品名稱或描述推測分類
        # 這裡可以加入 AI 分類邏輯
        
        return category

    def _estimate_stock(self, product_info: Dict) -> str:
        """估計庫存數量"""
        return "99"  # 預設值

    def _extract_attributes(self, product_info: Dict) -> Dict:
        """提取商品屬性"""
        # 根據商品類型提取不同屬性
        return {
            "品牌": "未設定",
            "顏色": "多色",
            "尺寸": "未設定"
        }

    def _get_shipping_settings(self) -> Dict:
        """取得運送設定"""
        return {
            "shipping_fee": "0",  # 免運
            "logistics": "宅配"  # 宅配
        }

    def _generate_tags(self, product_info: Dict) -> List[str]:
        """生成標籤"""
        name = product_info.get("name", "").lower()
        category = product_info.get("category", "").lower()
        
        tags = []
        
        # 從商品名稱提取關鍵字
        if "優惠" in name:
            tags.append("優惠")
        if "限量" in name:
            tags.append("限量")
        if "新品" in name:
            tags.append("新品")
        
        # 分類標籤
        if category and category != "未分類":
            tags.append(category)
        
        return tags

    def _validate_listing(self, listing: Dict):
        """驗證上架資料完整性"""
        required_fields = ["title", "description", "price", "category"]
        
        missing_fields = []
        for field in required_fields:
            if not listing.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"警告：缺少必要欄位：{', '.join(missing_fields)}")


def main():
    """測試用"""
    generator = ShopeeListingGenerator()
    
    test_product = {
        "name": "測試商品",
        "description": "這是一個測試商品",
        "price": "100",
        "category": "電子產品",
        "images": ["https://example.com/image1.jpg"]
    }
    
    listing = generator.generate(test_product)
    print(json.dumps(listing, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
