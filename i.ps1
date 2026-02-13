# 公司蝦安裝腳本

Write-Host "正在下載公司蝦..." -ForegroundColor Green
Invoke-WebRequest -Uri "https://codeload.github.com/dinosonicgo3/CompanyShrimp/zip/refs/heads/main" -OutFile "s.zip" -UseBasicParsing

Write-Host "正在解壓縮..." -ForegroundColor Green
Expand-Archive -Path "s.zip" -DestinationPath "." -Force

Write-Host "正在建立虛擬環境..." -ForegroundColor Green
cd CompanyShrimp-main
python -m venv venv

Write-Host "正在安裝依賴..." -ForegroundColor Green
.\venv\Scripts\pip.exe install -r requirements.txt

Write-Host "建立配置檔..." -ForegroundColor Green
Copy-Item .env.example .env

Write-Host ""
Write-Host "安裝完成！" -ForegroundColor Yellow
Write-Host "啟動方法：cd CompanyShrimp-main && .\start.bat" -ForegroundColor Cyan
Write-Host "網址：http://localhost:18080" -ForegroundColor Cyan
