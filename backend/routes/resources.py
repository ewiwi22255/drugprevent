"""
GET /api/resources
負責人：陳聖霖

Query params（皆為選用，可組合）：
  ?type=醫療|社福|輔導   篩選資源類型（不帶則回傳全部）
  ?city=台中市           篩選縣市（不帶則回傳全部）
  ?q=凱旋               依名稱／地址模糊搜尋（不分大小寫）

回傳：資源陣列，每筆含 name / type / city / address / phone / lat / lng。
查無資料時回傳空陣列 []（HTTP 200）。
"""
import re
from flask import Blueprint, jsonify, request
from backend.db import get_db

resources_bp = Blueprint("resources", __name__)


@resources_bp.route("/resources", methods=["GET"])
def get_resources():
    db    = get_db()
    query = {}

    res_type = request.args.get("type")
    city     = request.args.get("city")
    keyword  = request.args.get("q")

    if res_type:
        query["type"] = res_type
    if city:
        query["city"] = city
    if keyword:
        # 名稱或地址任一命中即可（大小寫不敏感）
        safe = re.escape(keyword)
        query["$or"] = [
            {"name":    {"$regex": safe, "$options": "i"}},
            {"address": {"$regex": safe, "$options": "i"}},
        ]

    docs = list(db.resources.find(query, {"_id": 0}).sort("city", 1))
    return jsonify(docs), 200
