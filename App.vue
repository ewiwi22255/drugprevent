<template>
    <div class="chat-wrapper">
        <h4 class="mb-3">✨ Gemini 多模型對話助手</h4>
        
        <div class="card p-3 mb-3 bg-light border-0">
            <div class="row g-2">
                <div class="col-md-7">
                    <label class="form-label text-muted small mb-1">Gemini API Key</label>
                    <input 
                        type="password" 
                        class="form-control" 
                        v-model="apiKey" 
                        placeholder="貼上您的 Google API Key"
                    >
                </div>

                <div class="col-md-5">
                    <label class="form-label text-muted small mb-1">選擇模型</label>
                    <select class="form-select" v-model="selectedModel">
                        <option 
                            v-for="model in modelList" 
                            :key="model.value" 
                            :value="model.value"
                        >
                            {{ model.name }}
                        </option>
                    </select>
                </div>
            </div>
        </div>

        <TalkList :talk-contents="talk_contents"></TalkList>

        <WordsInput 
            v-model="words" 
            :disabled="is_wait_response || !apiKey" 
            @send="handleSend"
        ></WordsInput>
        
        <div v-if="is_wait_response" class="text-center text-muted mt-2">
            <small>
                <span class="spinner-border spinner-border-sm me-1"></span>
                正在使用 <b>{{ getModelName(selectedModel) }}</b> 思考中...
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
            apiKey: '', 
            // 預設對話
            talk_contents: [
                { user: 'System', content: '請輸入 API Key 並選擇模型開始對話。', class: 'gemini' }
            ],
            words: '',
            is_wait_response: false,
            
            // ★ 新增：目前選中的模型 (預設值)
            // 注意：這裡的 value 必須是 Google API 真實認得的 ID
            selectedModel: 'gemini-2.5-flash-lite', 

            // ★ 新增：模型清單
            modelList: [
                { 
                    name: 'Gemini 2.5 Flash-Lite (預設)', 
                    value: 'gemini-2.5-flash-lite'  // 若 API 尚未開放，請暫時改回 'gemini-1.5-flash' 測試
                },
                { 
                    name: 'Gemini 2.5 Flash', 
                    value: 'gemini-2.5-flash' 
                },
                { 
                    name: 'Gemini 3 Flash', 
                    value: 'gemini-3.0-flash' 
                },

            ]
        };
    },
    methods: {
        // 輔助函式：透過 value 找 name (顯示用)
        getModelName(value) {
            const m = this.modelList.find(item => item.value === value);
            return m ? m.name : value;
        },

        async sendRequestToGemini(text) {
            // ★ 修改重點：將 URL 中的模型名稱變成動態變數
            const model = this.selectedModel;
            const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${this.apiKey}`;
            
            const payload = {
    contents: [{
        parts: [{ 
            text: `你現在是一位『毒品防制資訊整合平台』的專業導覽員。
            請用親切、專業且不帶批判的口吻回答。
            如果使用者感到困惑，可以引導他們去玩平台的『藥物迷思測驗』或查看『資源地圖』。
            
            使用者訊息：${text}` 
        }]
    }]
};

            try {
                const response = await axios.post(url, payload, {
                    headers: { 'Content-Type': 'application/json' }
                });
                
                if (response.data && response.data.candidates) {
                    return response.data.candidates[0].content.parts[0].text;
                }
            } catch (error) {
                console.error("API Error:", error);
                
                // 針對 404 錯誤提供更精準的提示
                if (error.response && error.response.status === 404) {
                    return `❌ 錯誤 404：模型 "${model}" 不存在或是名稱錯誤。\nGoogle 可能尚未開放此模型 ID，請切換回「穩定版」測試。`;
                }
                
                return `發生錯誤 (${error.message})，請檢查 API Key 或網路。`;
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

            // 2. 呼叫 API (內部會使用 selectedModel)
            const reply = await this.sendRequestToGemini(userMsg);

            // 3. 顯示 AI 回應
            this.talk_contents.push({
                class: 'gemini',
                user: this.getModelName(this.selectedModel), // 顯示目前是哪個模型回的
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
    /* 移除 margin: 0 auto 和 box-shadow，因為父層已經有了 */
}
.card {
    border-radius: 8px;
}
</style>