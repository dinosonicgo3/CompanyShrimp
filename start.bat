@echo off
REM ========================================
REM 公司蝦 - 啟動腳本
REM ========================================

REM 啟用虛擬環境
call venv\Scripts\activate.bat

REM 檢查是否有參數
if "%~1"=="" (
    echo 用法：start.bat ^<商品網址或檔案^> [--upload]
    echo.
    echo 範例：
    echo   start.bat https://example.com/product
    echo   start.bat product_info.json
    echo   start.bat https://example.com/product --upload
    echo.
    pause
    exit /b 0
)

REM 執行程式
python main.py %*

pause
