# DeepSeek 教材生成器

这个项目使用 DeepSeek API 自动生成教材内容，将生成的内容以 markdown 格式保存。

## 项目结构

```
.
├── data/               # 输入数据目录
│   ├── base_prompt.txt # 基础prompt模板
│   └── *.txt          # 教材目录文件
├── src/               # 源代码目录
│   └── main.py        # 主程序
├── textbook/          # 输出目录
├── pyproject.toml     # 项目配置
└── .env              # 环境变量配置
```

## 安装

1. 安装 uv（如果尚未安装）：
   ```bash
   pip install uv
   ```

2. 创建并激活虚拟环境：
   ```bash
   uv venv
   # Windows
   .venv/Scripts/activate
   # Linux/MacOS
   source .venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   uv pip install -r requirements.txt
   ```

4. 复制 `.env.example` 到 `.env` 并填写你的 DeepSeek API key

## 使用方法

1. 在 `data/base_prompt.txt` 中设置基础prompt模板

2. 在 `data/` 目录下创建教材文件，文件名即为教材名称，文件内容为教材单元列表（每行一个单元）

3. 运行程序：
   ```bash
   python src/main.py
   ```

4. 生成的markdown文件将保存在 `textbook/` 目录下，每本教材一个子目录

## 配置说明

在 `.env` 文件中可以配置以下参数：

- `DEEPSEEK_API_KEY`: DeepSeek API密钥（必需）
- `INPUT_DATA_DIR`: 输入数据目录（默认：data）
- `OUTPUT_DIR`: 输出目录（默认：textbook）

## 日志

程序运行日志保存在项目根目录下的 `textbook_generator.log` 文件中。

## 示例

1. 创建教材文件 `data/python_tutorial.txt`：
```
Python基础语法
变量与数据类型
控制流程
函数定义与调用
```

2. 运行程序后，将在 `textbook/python_tutorial/` 目录下生成对应的markdown文件。
