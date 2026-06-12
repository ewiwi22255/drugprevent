<template>
    <div class="chat-wrapper">
        <h4 class="mb-3">✨ Gemini 專業導覽助手</h4>
        
        <!-- API Key 和模型選擇已經藏在 Python 後端，這裡把舊的輸入框區塊拔掉，變得更美觀 -->

        <!-- 聊天紀錄清單 -->
        <TalkList :talk-contents="talk_contents"></TalkList>

        <!-- 這裡把 :disabled 裡面的 !apiKey 拿掉了，因為不需要再手動輸入 Key 囉！ -->
        <WordsInput 
            v-model="words" 
            :disabled="is_wait_response" 
            @send="handleSend"
        ></WordsInput>
        
        <!-- 等待回應的載入動畫 -->
        <div v-if="is_wait_response" class="text-center text-muted mt-2">
            <small>
                <span class="spinner-border spinner-border-sm me-1"></span>
                導覽員正在思考中...
            </small>
        </div>
    </div>
</template>

<script>
import TalkList from './components/TalkList.vue';
import WordsInput from './components/WordsInput.vue';

export default {
    name: 'App',
    components: {
        TalkList,
        WordsInput
    },
    data() {
        return {
            // 預設對話：一開機就給予親切的歡迎詞
            talk_contents: [
                { user: '導覽助手', content: '您好！我是『毒品防制資訊整合平台』的專業導覽員。請問今天有什麼我可以協助您的嗎？您可以詢問任何關於反毒防犯罪的資訊喔！', class: 'gemini' }
            ],
            words: '',
            is_wait_response: false
        };
    },
    methods: {
        // ★ 重大修改：不再直連 Google，改為連向你剛架好的 Python Flask 後端
        async sendRequestToBackend(text) {
            const url = 'http://127.0.0.1:5000/api/chat';
            
            // 準備送給 Python app.py 的 JSON 資料
            const payload = {
                message: text
            };

            try {
                const response = await axios.post(url, payload, {
                    headers: { 'Content-Type': 'application/json' }
                });
                
                // 讀取 Python 後端回傳的 jsonify({"reply": response.text})
                if (response.data && response.data.reply) {
                    return response.data.reply;
                }
                // 如果後端回傳的是錯誤訊息 jsonify({"error": ...})
                if (response.data && response.data.error) {
                    return `❌ 後端錯誤：${response.data.error}`;
                }
            } catch (error) {
                console.error("Backend Error:", error);
                return `系統連線失敗 (${error.message})，請確認後端 Python 伺服器是否開機中。`;
            }
            return "無回應";
        },

        async handleSend() {
            if (this.words.trim() === '') return;

            this.is_wait_response = true;
            const userMsg = this.words;

            // 1. 顯示使用者訊息
            this.talk_contents.push({
                class: 'user',
                user: '我',
                content: userMsg
            });

            this.words = '';

            // 2. 呼叫你的 Python 伺服器
            const reply = await this.sendRequestToBackend(userMsg);

            // 3. 顯示 AI 回應
            this.talk_contents.push({
                class: 'gemini',
                user: '導覽助手', 
                content: reply
            });

            this.is_wait_response = false;
        }
    }
}
</script>

<style scoped>
/* App.vue */
.chat-wrapper { 
    height: 100%;
    display: flex;
    flex-direction: column;
    background: white; 
    padding: 15px; 
    border-radius: 10px; 
}
</style>