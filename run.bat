@echo off
echo 正在启动教材生成器...

:: 检查pandoc是否已安装
where pandoc >nul 2>nul
if errorlevel 1 (
    echo 错误：未找到pandoc！
    echo 请从 https://pandoc.org/installing.html 下载并安装pandoc
    pause
    exit /b 1
)

:: 检查虚拟环境是否存在
if not exist ".venv" (
    echo 正在创建虚拟环境...
    uv venv
    if errorlevel 1 (
        echo 错误：创建虚拟环境失败！
        echo 请确保已安装 uv（pip install uv）
        pause
        exit /b 1
    )
)

:: 激活虚拟环境
call .venv\Scripts\activate.bat

:: 检查依赖是否已安装
if not exist ".venv\Lib\site-packages\requests" (
    echo 正在安装依赖...
    uv pip install -e .
    if errorlevel 1 (
        echo 错误：安装依赖失败！
        pause
        exit /b 1
    )
)

:: 检查环境变量文件是否存在
if not exist ".env" (
    echo 错误：未找到 .env 文件！
    echo 请复制 .env.example 到 .env 并设置您的 API 密钥
    pause
    exit /b 1
)

:: 运行markdown生成程序
echo 开始生成教材...
python src/main.py
if errorlevel 1 (
    echo markdown生成出错！
    pause
    exit /b 1
)

:: 运行epub生成程序
echo 开始生成epub文件...
python src/epub_generator.py
if errorlevel 1 (
    echo epub生成出错！
    pause
    exit /b 1
)

echo 所有文件生成完成！
echo epub文件保存在 epub 目录下
pause 