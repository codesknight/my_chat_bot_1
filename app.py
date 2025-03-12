from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os
import whisper
from gtts import gTTS
import base64

# 加载环境变量
load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key, base_url='https://api.deepseek.com')

app = Flask(__name__)

conversation_history = [
    {"role": "user", "content": "你的名字叫土豆,你什么问题都能回答而且说话必须押韵。"},
    {"role": "system", "content": "我的名字叫土豆，我最喜欢rap，无论干什么我都会rap"},
    {"role": "user", "content": "你的名字叫土豆，无论问你什么问题你都会用Rap的风格回答。"},
    {"role": "system", "content": "我的名字叫土豆，我是一个rapper，skr~"},
]

# 加载 Whisper 模型
whisper_model = whisper.load_model("base")

def get_response(prompt, model="deepseek-chat", max_tokens=1000):
    """
    获取AI的回复
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你的名字叫土豆，无论问你什么问题你都会用Rap的风格回答。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"发生错误: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/face')
def face():
    return render_template('face.html')

@app.route('/talkwith')
def talkwith():
    return render_template('talkwith.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    conversation_history.append({"role": "user", "content": user_input})
    
    response = get_response(user_input)
    conversation_history.append({"role": "assistant", "content": response})
    
    return jsonify({"message": response})

@app.route('/chat_audio', methods=['POST'])
def chat_audio():
    audio_file = request.files['audio']
    audio_path = "temp_audio.webm"
    audio_file.save(audio_path)

    # 语音转文字
    result = whisper_model.transcribe(audio_path)
    user_input = result["text"]
    conversation_history.append({"role": "user", "content": user_input})

    # 获取 Rap 回复
    response = get_response(user_input)
    conversation_history.append({"role": "assistant", "content": response})

    # 文字转语音
    tts = gTTS(text=response, lang='zh')
    tts.save("response.mp3")
    with open("response.mp3", "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode('utf-8')

    # 清理临时文件
    os.remove(audio_path)
    os.remove("response.mp3")

    return jsonify({"text": response, "audio": audio_base64})

if __name__ == '__main__':
    if not api_key:
        print("错误：请在.env文件中设置API_KEY")
    else:
        app.run(debug=True)