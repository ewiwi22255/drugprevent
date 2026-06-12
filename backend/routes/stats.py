"""
GET /api/stats
負責人：陳聖霖

回傳儀表板所需統計資料：
  - 總參與人數
  - 累計測驗次數
  - 各迷思類別答錯次數
  - 預防力各維度平均分
  - 防制資源總數與各類型數量（供地圖頁顯示）
"""
from flask import Blueprint, jsonify
from backend.db import get_db

stats_bp = Blueprint("stats", __name__)


@stats_bp.route("/stats", methods=["GET"])
def get_stats():
    db = get_db()

    total_quizzes = db.quiz_results.count_documents({})

    # 防制資源統計：總數 + 依類型分組
    resource_counts: dict = {}
    for row in db.resources.aggregate([
        {"$group": {"_id": "$type", "count": {"$sum": 1}}}
    ]):
        resource_counts[row["_id"] or "其他"] = row["count"]
    total_resources = sum(resource_counts.values())

    # 各類別答錯統計
    myth_errors: dict = {}
    for result in db.quiz_results.find({}, {"answers": 1}):
        for ans in result.get("answers", []):
            if not ans["is_correct"]:
                cat = ans.get("category", "其他")
                myth_errors[cat] = myth_errors.get(cat, 0) + 1

    # 預防力各維度平均
    categories     = ["成癮與生理機制", "藥物迷思辨析", "誘因與環境辨識", "復健與心理觀念"]
    prevention_avg = {c: 0 for c in categories}
    total_prev     = db.prevention_results.count_documents({})
    if total_prev:
        for doc in db.prevention_results.find({}, {"scores": 1}):
            for c in categories:
                prevention_avg[c] += doc.get("scores", {}).get(c, 0)
        for c in categories:
            prevention_avg[c] = round(prevention_avg[c] / total_prev, 1)

    return jsonify({
        "total_quizzes"   : total_quizzes,
        "myth_errors"     : myth_errors,
        "prevention_avg"  : prevention_avg,
        "total_resources" : total_resources,
        "resource_counts" : resource_counts,
    }), 200
