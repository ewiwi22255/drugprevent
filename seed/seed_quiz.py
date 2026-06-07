"""
執行方式（在 C:\drugprevent 下）：
    python seed/seed_quiz.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import get_db

QUIZ_QUESTIONS = [
    {"category": "成癮與生理機制", "question": "偶爾使用毒品不會上癮？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！即使是偶爾使用，毒品仍可能造成身體和心理依賴，且每個人對藥物的反應不同，風險難以預測。"},

    {"category": "藥物迷思辨析", "question": "大麻是天然植物，所以比合成毒品安全？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！天然不代表安全。大麻仍會影響認知功能、記憶力和判斷力，長期使用可能導致心理依賴和相關健康問題。"},

    {"category": "成癮與生理機制", "question": "只要意志力夠強，就能自行戒除毒品？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！毒品成癮是複雜的生理和心理問題，需要專業醫療協助。自行戒除可能導致嚴重的戒斷症狀，甚至危及生命。"},

    {"category": "誘因與環境辨識", "question": "年輕人使用毒品是因為壓力太大？",
     "options": ["正確", "錯誤"], "correct": 0,
     "explanation": "部分正確，但壓力只是其中一個因素。同儕影響、好奇心、錯誤認知、缺乏正確資訊等都是可能的原因。"},

    {"category": "成癮與生理機制", "question": "使用毒品可以提升學習或工作效率？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！毒品會損害大腦功能，長期使用會導致認知能力下降、記憶力減退，反而降低學習和工作效率。"},

    {"category": "誘因與環境辨識", "question": "「新興毒品」包裝成糖果、咖啡包，看起來很時尚，所以比較安全？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！包裝再可愛，本質仍是毒品，內含成分不明，反而更容易造成急性中毒與猝死風險。"},

    {"category": "誘因與環境辨識", "question": "只在派對或夜店玩樂時使用毒品，不會影響日常生活？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！毒品的影響不會只停留在當下，可能造成睡眠、情緒、記憶與判斷力長期受損。"},

    {"category": "誘因與環境辨識", "question": "朋友說「這只是助興藥，不算毒品」，所以比較沒關係？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！「助興藥」只是包裝話術，多半仍屬毒品或違法藥物，會對身心健康造成嚴重傷害。"},

    {"category": "藥物迷思辨析", "question": "只要沒有被警察抓到，使用毒品就不算嚴重問題？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！更嚴重的是對大腦、心血管與心理健康的長期損害，還可能影響學業、工作與家庭關係。"},

    {"category": "復健與心理觀念", "question": "曾經使用過毒品的人，就一定無法回到正常生活？",
     "options": ["正確", "錯誤"], "correct": 1,
     "explanation": "錯誤！透過醫療、諮商與家人支持，很多人都能逐漸恢復生活功能，重新建立健康的人生。"},
]


def seed():
    db = get_db()
    col = db.quizzes

    existing = col.count_documents({})
    if existing > 0:
        print(f"[seed] quizzes 已有 {existing} 筆資料，略過（如需重置請先手動清除 collection）")
        return

    result = col.insert_many(QUIZ_QUESTIONS)
    print(f"[seed] 成功匯入 {len(result.inserted_ids)} 題測驗題目")


if __name__ == "__main__":
    seed()
