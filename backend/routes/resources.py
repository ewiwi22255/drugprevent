"""
GET /api/resources
負責人：陳聖霖

Query params:
  ?type=醫療|社福|輔導   (不帶則回傳全部)
  ?city=台中市           (不帶則回傳全部)
"""
from flask import Blueprint, jsonify, request
from backend.db import get_db

resources_bp = Blueprint("resources", __name__)


@resources_bp.route("/resources", methods=["GET"])
def get_resources():
    db    = get_db()
    query = {}

    res_type = request.args.get("type")
    city     = request.args.get("city")
    if res_type:
        query["type"] = res_type
    if city:
        query["city"] = city

    docs = list(db.resources.find(query, {"_id": 0}))
    return jsonify(docs), 200
