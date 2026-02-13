# 公司蝦 (Shopee Assistant)

蝦皮自動上架工具 - 一鍵下載圖片、提取資訊、自動上架

## 功能特色

- ✅ **讀取商品資料**：支援網址和檔案格式
- 🖼️ **下載並優化圖片**：自動壓縮至 1MB 以下
- 📝 **提取商品資訊**：智能解析名稱、描述、價格
- 💰 **自動定價**：根據規則計算售價
- 🚀 **自動上架**：填寫蝦皮商品並發布

## 快速開始

### Windows 一鍵安裝

```bash
# 直接下載並執行安裝
curl -fsSL https://raw.githubusercontent.com/dinosonicgo3/CompanyShrimp/main/install.sh | bash
```

或使用批次檔：

```cmd
install.bat
```

### 手動安裝

```bash
# 1. 安裝 Python 3.8+

# 2. 建立虛擬環境
python -m venv venv

# 3. 啟用虛擬環境
venv\Scripts\activate

# 4. 安裝依賴
pip install -r requirements.txt

# 5. 設定配置
cp .env.example .env
# 編輯 .env 和 config.json
```

## 使用方法

### 基本使用

```cmd
# 從網址提取商品資料
python main.py https://example.com/product

# 從檔案提取商品資料
python main.py product_info.json

# 自動上架到蝦皮
python main.py https://example.com/product --upload
```

### 使用啟動腳本

```cmd
start.bat https://example.com/product
start.bat product_data.json --upload
```

## 設定說明

### config.json

```json
{
  "app_name": "公司蝦",
  "version": "1.0.0",
  "shopee": {
    "shop_url": "https://shopee.tw",
    "api_key": "你的蝦皮 API 金鑰",
    "shop_id": "你的賣場 ID"
  },
  "pricing": {
    "base_price": 0,
    "markup_percentage": 30,
    "rules": [
      "原價加成 30%",
      "最低售價 50 元"
    ]
  },
  "image_settings": {
    "max_size_kb": 1024,
    "formats": ["jpg", "jpeg", "png"],
    "download_folder": "./downloads"
  }
}
```

### .env 檔案

```env
# OpenAI API (用於 AI 功能)
OPENAI_API_KEY=your_openai_api_key_here

# 蝦皮 API
SHOPEE_API_KEY=your_shopee_api_key_here
SHOPEE_SHOP_ID=your_shop_id_here
```

## 結構說明

```
CompanyShrimp/
├── main.py                 # 主程式
├── config.json            # 配置檔
├── requirements.txt       # Python 依賴
├── install.bat            # 安裝腳本
├── start.bat              # 啟動腳本
├── utils/                 # 工具模組
│   ├── image_downloader.py    # 圖片下載
│   └── product_extractor.py   # 商品資商品資訊提取
├── plugins/               # 外掛模組
│   ├── shopee_generator.py    # 上架資料生成
│   └── shopee_uploader.py     # 蝦皮上傳
├── prompts/               # AI 提示
│   └── shopee_system.md      # 系統提示
└── downloads/             # 下載圖片儲存
```

## 定價規則

在 `config.json` 中設定定價規則：

```json
{
  "pricing": {
    "rules": [
      "加成 30%",
      "最低售價 50 元",
      "滿 500 元免運"
    ]
  }
}
```

## 蝦皮設定

### 方式一：使用 Shopee Open API（推薦）

1. 申請 Shopee Open API 權限
2. 取得 API Key、Shop ID、Partner ID
3. 填入 `config.json` 和 `.env`

### 方式二：使用 Selenium 自動化

1. 安裝 Chrome 驅動程式
2. 程式會自動操作瀏覽器
3. 需要先手動登入蝦皮賣家中心

## 支援的輸入格式

- 網址：任何商品頁面網址
- JSON 檔案：結構化的商品資料
- 文字檔案：簡單的文字格式

## 常見問題

### Q：圖片下載失敗？
A：檢查網路連線，確保圖片 URL 可存取

### Q：上架失敗？
A：
1. 檢查 API 金鑰是否正確
2. 確認賣場權限
3. 檢查檔案大小是否超過限制

### Q：定價計算錯誤？
A：檢查 `config.json` 中的定價規則設定

## 授權

MIT License

## 作者

DINO (dinosonicgo)

---

**注意**：使用本工具前請先閱讀蝦平台的相關規範，確保符合使用條款。
