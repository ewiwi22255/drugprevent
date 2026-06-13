"""
POST /api/chat
負責人：洪邑閩

Body: { "message": "使用者輸入文字" }
回傳: { "reply": "DeepSeek 回應" }
"""
from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from backend.db import get_db
from backend.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
from openai import OpenAI

chat_bp = Blueprint("chat", __name__)

# DeepSeek (OpenCode Go) 初始化（Key 在後端，不暴露給前端）
_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

SYSTEM_PROMPT = (
    "你是一位專業的毒品防制輔導員，只回答與毒品防制、心理健康、求助資源相關的問題。"
    "語氣友善、非批判性，回答請使用繁體中文，長度控制在 200 字以內。"
)


@chat_bp.route("/chat", methods=["POST"])
def chat():
    db = get_db()
    data = request.get_json()

    if not data or not data.get("message"):
        return jsonify({"error": "message 不能為空"}), 400

    user_message = data["message"]

    try:
        response = _client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("【DeepSeek 錯誤】:", str(e))
        return jsonify({"error": str(e)}), 500

    # 記錄對話至 MongoDB
    db.chat_logs.insert_one({
        "user_message": user_message,
        "bot_reply"   : reply,
        "created_at"  : datetime.now(timezone.utc),
    })

    return jsonify({"reply": reply}), 200
