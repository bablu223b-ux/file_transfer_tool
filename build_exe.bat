@echo off

REM 局域网文件传输工具打包脚本
REM 使用PyInstaller将Python程序打包为单文件EXE

echo 开始打包局域网文件传输工具...

REM 检查是否安装了PyInstaller
where pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未安装PyInstaller，请先运行 pip install pyinstaller
    pause
    exit /b 1
)

echo 正在清理旧的打包文件...
REM 清理旧的打包文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist *.spec del /q *.spec

REM 清理子目录中的__pycache__
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"

echo 正在打包程序...
REM 使用PyInstaller打包程序
pyinstaller --onefile --windowed --add-data "static;static" --add-data "web/templates;web/templates" --add-data "config.json;.", --icon="" main.py

if %errorlevel% neq 0 (
    echo 错误: 打包失败
    pause
    exit /b 1
)

echo 打包成功！
echo 可执行文件位于 dist\main.exe

echo 正在复制配置文件到dist目录...
REM 复制配置文件到dist目录
if not exist dist copy config.json dist\

REM 复制README.md到dist目录（如果存在）
if exist README.md copy README.md dist\

echo 打包完成！
pause