"""
Agent 可呼叫的工具函式（對應 function calling schema）
每個函式直接查 MongoDB，回傳可序列化的 Python 物件。
"""
from backend.db import get_db


def get_resources(city: str = None, resource_type: str = None) -> list | str:
    """查詢全台毒品防制資源據點，可依城市或類型過濾。"""
    db    = get_db()
    query = {}

    if city:
        query["city"] = {"$regex": city, "$options": "i"}
    if resource_type:
        query["type"] = {"$regex": resource_type, "$options": "i"}

    results = list(db.resources.find(query, {"_id": 0}).limit(6))

    if not results:
        return "找不到符合條件的資源據點，請試試不同的城市或類型。"

    return results


def get_stats() -> dict:
    """取得平台目前的統計數字。"""
    db = get_db()
    return {
        "total_quizzes"  : db.quiz_results.count_documents({}),
        "total_anonymous": db.anonymous_messages.count_documents({}),
        "total_chats"    : db.chat_sessions.count_documents({}),
        "total_resources": db.resources.count_documents({}),
    }


def get_quiz_info() -> dict:
    """取得現有測驗題目的基本資訊（題數、類別分布）。"""
    db         = get_db()
    questions  = list(db.quizzes.find({}, {"_id": 0, "category": 1, "question": 1}))
    categories = {}
    for q in questions:
        cat = q.get("category", "未分類")
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "total_questions": len(questions),
        "categories"     : categories,
        "sample_questions": [q["question"] for q in questions[:3]],
    }


# ── Schema（送給 DeepSeek 的 function calling 定義）──────────────────────────

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name"       : "get_resources",
            "description": (
                "查詢毒品防制資源據點（醫療、諮商、戒治、法律等），"
                "可依城市（例如台北市、高雄市）或類型過濾。"
                "使用者詢問附近資源、戒毒機構、諮商管道時請呼叫此工具。"
            ),
            "parameters": {
                "type"      : "object",
                "properties": {
                    "city": {
                        "type"       : "string",
                        "description": "城市名稱，例如：台北市、新北市、台中市、高雄市",
                    },
                    "resource_type": {
                        "type"       : "string",
                        "description": "資源類型，例如：醫療、諮商、戒治、法律、社福",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name"       : "get_stats",
            "description": (
                "取得本平台的統計數字，包含累計測驗次數、匿名留言數、"
                "諮詢對話數、資源據點總數。"
                "使用者詢問平台資料或成效時請呼叫此工具。"
            ),
            "parameters": {
                "type"      : "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name"       : "get_quiz_info",
            "description": (
                "取得平台測驗題目的資訊，包含題數、類別分布及範例題目。"
                "使用者詢問測驗內容、有哪些題目時請呼叫此工具。"
            ),
            "parameters": {
                "type"      : "object",
                "properties": {},
            },
        },
    },
]

# ── 工具名稱 → 函式的對照表 ────────────────────────────────────────────────

TOOL_MAP = {
    "get_resources": get_resources,
    "get_stats"    : get_stats,
    "get_quiz_info": get_quiz_info,
}
