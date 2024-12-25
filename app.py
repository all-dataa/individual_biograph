import os
import logging
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from audio2text import audio_to_text
from llm import purify, outliner, writer

# 配置日志
logging.basicConfig(
    filename='logs/app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        # 处理音频文件
        if 'audio' in request.files:
            audio_file = request.files['audio']
            if audio_file and allowed_file(audio_file.filename):
                filename = secure_filename(audio_file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                audio_file.save(filepath)
                
                # 音频转文本
                text_content = audio_to_text(filepath)
            else:
                text_content = request.form.get('text', '')
        else:
            text_content = request.form.get('text', '')
        
        character_name = request.form.get('name', '主人公')
        
        # 生成传记
        # 1. 提纯文本
        purified_text = purify(text_content, character_name)
        
        # 2. 生成大纲
        biography_outline = outliner(purified_text)
        
        # 3. 写作传记
        writer("全文", biography_outline)  # 这里简化为直接生成全文
        
        # 读取生成的传记
        with open("output/biography.md", "r", encoding="utf-8") as file:
            biography = file.read()
            
        return jsonify({
            'success': True,
            'biography': biography
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