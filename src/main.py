import os
import logging
import requests
from pathlib import Path
from typing import List, Generator, Tuple
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('textbook_generator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TextbookGenerator:
    def __init__(self):
        self.load_config()
        
    def load_config(self):
        """加载环境变量配置"""
        load_dotenv()
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.input_dir = Path(os.getenv('INPUT_DATA_DIR', 'data'))
        self.output_dir = Path(os.getenv('OUTPUT_DIR', 'textbook'))
        self.base_prompt_path = self.input_dir / 'base_prompt.txt'
        
        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
        
        logger.info(f"配置加载完成: 输入目录={self.input_dir}, 输出目录={self.output_dir}")
        
    def load_base_prompt(self) -> str:
        """加载基础prompt模板"""
        try:
            with open(self.base_prompt_path, 'r', encoding='utf-8') as f:
                base_prompt = f.read().strip()
            logger.info("基础prompt模板加载成功")
            return base_prompt
        except Exception as e:
            logger.error(f"加载基础prompt模板失败: {str(e)}")
            raise

    def get_textbook_contents(self) -> Generator[Tuple[str, List[str]], None, None]:
        """获取所有教材文件的内容"""
        try:
            for file in self.input_dir.glob('*.txt'):
                if file.name != 'base_prompt.txt':
                    with open(file, 'r', encoding='utf-8') as f:
                        content = [line.strip() for line in f.readlines() if line.strip()]
                        logger.info(f"成功加载教材文件: {file.name}")
                        yield file.stem, content
        except Exception as e:
            logger.error(f"读取教材文件失败: {str(e)}")
            raise

    def call_deepseek_api(self, prompt: str) -> str:
        """调用DeepSeek API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'model': 'deepseek-chat',  # 指定模型
            'max_tokens': 2000,
            'temperature': 0.7
        }
        
        try:
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers=headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()['choices'][0]['message']['content']
            logger.info("API调用成功")
            return result
        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            raise

    def save_markdown(self, textbook_name: str, unit_name: str, content: str):
        """保存markdown文件"""
        textbook_dir = self.output_dir / textbook_name
        textbook_dir.mkdir(parents=True, exist_ok=True)
        
        # 清理单元名称，确保可以用作文件名
        safe_unit_name = "".join(c for c in unit_name if c.isalnum() or c in (' ', '-', '_')).strip()
        output_file = textbook_dir / f"{safe_unit_name}.md"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"保存markdown文件成功: {output_file}")
        except Exception as e:
            logger.error(f"保存markdown文件失败: {str(e)}")
            raise

    def generate(self):
        """生成教材内容"""
        base_prompt = self.load_base_prompt()
        
        for textbook_name, units in self.get_textbook_contents():
            logger.info(f"开始处理教材: {textbook_name}")
            
            for unit in units:
                try:
                    # 构建完整的prompt
                    full_prompt = f"{base_prompt}\n教材：{textbook_name}\n单元：{unit}"
                    
                    # 调用API获取内容
                    content = self.call_deepseek_api(full_prompt)
                    
                    # 保存结果
                    self.save_markdown(textbook_name, unit, content)
                    
                except Exception as e:
                    logger.error(f"处理单元失败 {textbook_name}/{unit}: {str(e)}")
                    continue

def main():
    try:
        generator = TextbookGenerator()
        generator.generate()
        logger.info("教材生成完成")
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        raise

if __name__ == '__main__':
    main() 