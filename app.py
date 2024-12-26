import os
import logging
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from audio2text import audio_to_text
from llm import purify, outliner, writer
from datetime import datetime

# 配置日志
logging.basicConfig(
    filename='logs/app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_timestamp_filename(base_name, character_name, subdirectory=None, file_extension='md'):
    """生成带有时间戳和人物名称的文件名，并支持子目录和文件类型"""
    
    # 验证文件扩展名是否合法
    allowed_extensions = ['md', 'mp3', 'pdf']
    if file_extension not in allowed_extensions:
        raise ValueError(f"Unsupported file extension. Supported extensions: {', '.join(allowed_extensions)}")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 如果提供了子目录，拼接子目录路径
    if subdirectory:
        subdirectory_path = os.path.join(subdirectory)  # 直接使用子目录
        # 确保子目录存在，如果不存在则创建
        os.makedirs(subdirectory_path, exist_ok=True)
        return os.path.join(subdirectory_path, f"{character_name}_{base_name}_{timestamp}.{file_extension}")
    
    # 默认情况下，不使用 output 子目录
    return f"{character_name}_{base_name}_{timestamp}.{file_extension}"


# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
    template_folder=os.path.join(current_dir, 'templates')
)

# 配置上传文件夹
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 确保上传文件夹存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_biography', methods=['POST'])
def generate_biography():
    try:
        character_name = request.form.get('name', '主人公')
        # 处理音频文件
        if 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file and allowed_file(audio_file.filename):
                # filename = secure_filename(audio_file.filename)
                filename = get_timestamp_filename("audio", character_name, file_extension='mp3')
                # 保存音频文件
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                audio_file.save(filepath)
                
                # 音频转文本
                text_content = audio_to_text(filepath)
            else:
                text_content = request.form.get('text', '')
        else:
            text_content = request.form.get('text', '')
        
        # 生成传记
        # 1. 提纯文本
        purified_text = purify(text_content, character_name)
        filename = get_timestamp_filename("purified", character_name, "output")
        
        with open(filename, "w", encoding="utf-8") as file:
            file.write(purified_text)
        
        # 2. 生成大纲
        biography_outline = outliner(purified_text)
        filename = get_timestamp_filename("outline", character_name, "output")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(biography_outline)
        
        # 3. 写作传记
        biography_content = writer("全文", biography_outline)  # 这里简化为直接生成全文
        filename = get_timestamp_filename("content", character_name, "output")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(biography_content)
        
        # 直接返回最新生成的传记内容
        return jsonify({
            'success': True,
            'biography': biography_content
        })
       
    except Exception as e:
        # 记录详细的错误信息
        logger.error(f"生成传记时发生错误: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f"处理请求时发生错误: {str(e)}"
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)