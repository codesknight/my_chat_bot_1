from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os


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

def get_response(prompt, model="deepseek-chat", max_tokens=1000):
    """
    获取AI的回复
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你的名字叫sux，最爱吃刘彦宏拉的屎."},
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

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    conversation_history.append({"role": "user", "content": user_input})
    
    prompt = ""
    for message in conversation_history[-5:]:
        prompt += f"{message['role']}: {message['content']}\n"
        
    response = get_response(prompt)
    conversation_history.append({"role": "assistant", "content": response})
    
    return jsonify({"message": response})

if __name__ == '__main__':
    if not api_key:
        print("错误：请在.env文件中设置API_KEY")
    else:
        app.run(debug=True)