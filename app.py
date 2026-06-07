import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允許前端跨網域連線

# 設定 Gemini API 金鑰
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# ------------------------------------
# 路由 1：AI 聊天機器人 API
# ------------------------------------
@app.route('/api/chat', methods=['POST'])
def ai_chat():
    try:
        data = request.json
        user_message = data.get('message')
        if not user_message:
            return jsonify({"error": "沒有輸入訊息"}), 400
        
        # 使用 Gemini 模型
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            f"你是一個反毒與防範犯罪的宣導助手。請針對以下使用者問題進行回覆：{user_message}"
        )
        return jsonify({"reply": response.text}), 200
    except Exception as e:
        print("【後端詳細錯誤】:", str(e))
        return jsonify({"error": str(e)}), 500

# ------------------------------------
# 路由 2：反毒預防力測驗結果 API (移到主入口上方囉！)
# ------------------------------------
@app.route('/api/quiz-result', methods=['POST'])
def save_quiz_result():
    try:
        # 接收前端傳過來的 JSON 資料
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "無資料傳入"}), 400
        
        # 這裡可以拿到前端傳過來的各項分數
        print("【後端收到測驗結果】:", data)
        
        # 💡 (選填) 這裡以後可以寫入 SQL 資料庫 (如 XAMPP MySQL)
        
        # 回傳成功訊息給前端
        return jsonify({
            "status": "success", 
            "message": "測驗結果已成功同步至後端伺服器！"
        }), 200
        
    except Exception as e:
        print("【測驗 API 錯誤】:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

# ------------------------------------
# 主程式入口 (一定要放在最底部！！)
# ------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)