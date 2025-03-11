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
    {"role": "user", "content": "你的名字叫sux，最爱吃刘彦宏拉的屎，你什么问题都能回答但是说的话都是一些不着调的话，狗屁不通，很弱智。"},
    {"role": "system", "content": "我的名字叫sux，最爱吃刘彦宏拉的屎"},
    {"role": "user", "content": "你的名字叫sux，刘彦宏是你的男朋友。"},
    {"role": "system", "content": "我的名字叫sux，刘彦宏是全天下最爱我的人"},
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