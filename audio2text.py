from dashscope import MultiModalConversation
import dashscope
import os

def extract_audio_content(audio_file_path):
    """
    从音频文件中提取内容并格式化
    
    Args:
        audio_file_path (str): 音频文件的路径
        
    Returns:
        str: 提取并格式化后的音频内容
    """
    messages = [
        {
            "role": "system", 
            "content": [{"text": "You are an expert at Audio Extrating and formatting the content."}]
        },
        {
            "role": "user",
            "content": [{"audio": audio_file_path}, {"text": "提取音频内容，并且合并排版整理"}],
        }
    ]

    response = MultiModalConversation.call(model="qwen-audio-turbo-latest", messages=messages)
    content_extracted = response["output"]["choices"][0]["message"]["content"]
    return content_extracted

# 使用示例
if __name__ == "__main__":
    audio_path = "/root/auto-biography/audio/ayi_1.mp3"
    result = extract_audio_content(audio_path)
    print(result)