from flask import Blueprint, request

anonymous_bp = Blueprint(
    "anonymous",
    __name__
)

anonymous_messages = []

@anonymous_bp.route(
    "/api/anonymous",
    methods=["POST"]
)
def submit_anonymous():

    data = request.json

    anonymous_messages.append(
        {
            "message":
            data.get("message")
        }
    )

    return {
        "success": True,
        "message": "送出成功"
    }