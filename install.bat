@echo off
REM ========================================
REM 公司蝦 - Windows 一鍵安裝腳本
REM ========================================

echo.
echo ===============================================
echo           公司蝦 (Shopee Assistant)
echo           蝦皮自動上架工具
echo ===============================================
echo.

REM 檢查 Python
echo [1/4] 檢查 Python 環境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤：未安裝 Python
    echo 請先安裝 Python 3.8 或以上版本
    echo 下載網址：https://www.python.org/downloads/
   pause
    exit /b 1
)
echo Python 環境正常
echo.

REM 建立虛擬環境
echo [2/4] 建立虛擬環境...
if not exist "venv" (
    python -m venv venv
    echo 已建立虛擬環境
) else (
    echo 虛擬環境已存在
)
echo.

REM 啟用虛擬環境並安裝依賴
echo [3/4] 安裝依賴套件...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 錯誤：依賴安裝失敗
    pause
    exit /b 1
)
echo 依賴安裝完成
echo.

REM 建立設定檔
echo [4/4] 建立配置檔...
if not exist ".env" (
    copy .env.example .env >nul 2>&1
    echo 已建立 .env 檔案
) else (
    echo .env 檔案已存在
)
echo.

echo ===============================================
echo 安裝完成！
echo ===============================================
echo.
echo 使用方法：
echo   1. 設定 config.json 中的蝦皮 API 資訊
echo   2. 設定 .env 檔案中的環境變數
echo   3. 執行：python main.py ^<商品網址或檔案^>
echo.
echo 或使用啟動腳本：start.bat
echo.
pause
