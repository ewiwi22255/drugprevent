"""
Agent loop：多輪推理 + function calling
每次呼叫 run_agent() 都帶入完整的對話歷史，讓 DeepSeek 決定：
  - 直接回答  → 回傳文字，loop 結束
  - 呼叫工具  → 執行工具、把結果塞回 messages，繼續下一輪
"""
import json
from openai import OpenAI
from backend.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
from backend.agent.tools import TOOLS_SCHEMA, TOOL_MAP

# ── 初始化 OpenAI-compatible client ──────────────────────────────────────────

_client = OpenAI(
    api_key  = DEEPSEEK_API_KEY,
    base_url = DEEPSEEK_BASE_URL,
)

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """你是「藥物防制資訊整合平台」的專屬 AI 輔導員。

【你的能力】
1. 回答毒品防制、心理健康、求助管道相關問題
2. 查詢全台灣防制資源據點（使用 get_resources 工具）
3. 提供平台統計數據（使用 get_stats 工具）
4. 說明平台測驗題目的內容（使用 get_quiz_info 工具）

【行為準則】
- 只回答與毒品防制、心理健康、法律求助相關的問題
- 對於偏離主題的問題，友善地引導回正題
- 語氣溫暖、非批判性，避免使用嚇人或污名化的語言
- 回覆使用繁體中文，長度控制在 300 字以內
- 若使用者詢問資源地點，一定要先呼叫工具查詢，不可憑空捏造
- 若工具回傳「找不到」，誠實告知並建議撥打 1925 安心專線
"""

MAX_ROUNDS = 6  # 防止無限 loop


def run_agent(history: list[dict]) -> str:
    """
    執行 Agent loop。

    Args:
        history: 不含 system prompt 的對話歷史
                 格式: [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        最終的文字回覆（str）
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    for round_num in range(MAX_ROUNDS):
        response = _client.chat.completions.create(
            model       = DEEPSEEK_MODEL,
            messages    = messages,
            tools       = TOOLS_SCHEMA,
            tool_choice = "auto",
        )

        choice = response.choices[0]
        msg    = choice.message

        # 把 assistant 這輪的回覆加回 messages（含 tool_calls 欄位）
        msg_dict = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            msg_dict["tool_calls"] = [
                {
                    "id"      : tc.id,
                    "type"    : "function",
                    "function": {
                        "name"     : tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]
        messages.append(msg_dict)

        # 沒有 tool_calls → 最終回答
        if not msg.tool_calls:
            return msg.content or "（無回應）"

        # 有 tool_calls → 執行工具，結果塞回 messages
        for tc in msg.tool_calls:
            fn_name = tc.function.name
            try:
                fn_args = json.loads(tc.function.arguments or "{}")
                if fn_name in TOOL_MAP:
                    result = TOOL_MAP[fn_name](**fn_args)
                else:
                    result = f"未知工具：{fn_name}"
            except Exception as e:
                result = f"工具執行錯誤：{e}"

            messages.append({
                "role"        : "tool",
                "tool_call_id": tc.id,
                "content"     : json.dumps(result, ensure_ascii=False),
            })

    return "（Agent 已達最大推理輪數，請重新提問）"
