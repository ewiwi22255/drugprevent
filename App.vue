<template>
    <div class="chat-wrapper">
        <div class="chat-header">
            <span class="chat-title">AI 防治輔導員</span>
            <button class="clear-btn" @click="clearSession" title="清除對話">
                🗑 清除
            </button>
        </div>

        <!-- 聊天紀錄 -->
        <div class="chat-messages" ref="messagesEl">
            <div
                v-for="(msg, i) in messages"
                :key="i"
                :class="['message', msg.role === 'user' ? 'message-user' : 'message-bot']"
            >
                <div class="bubble" v-html="renderContent(msg.content)"></div>
            </div>
            <div v-if="loading" class="message message-bot">
                <div class="bubble typing">
                    <span></span><span></span><span></span>
                </div>
            </div>
        </div>

        <!-- 輸入列 -->
        <div class="chat-input-row">
            <textarea
                v-model="input"
                :disabled="loading"
                placeholder="輸入問題…（Enter 送出，Shift+Enter 換行）"
                rows="1"
                @keydown.enter.exact.prevent="send"
            ></textarea>
            <button :disabled="loading || !input.trim()" @click="send" class="send-btn">
                ➤
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'App',
    data() {
        const SESSION_KEY = 'drugprevent_session_id';
        return {
            SESSION_KEY,
            session_id: localStorage.getItem(SESSION_KEY) || null,
            messages: [
                {
                    role: 'assistant',
                    content:
                        '你好！我是毒品防制資訊整合平台的 AI 輔導員。\n\n' +
                        '我可以：\n- 回答毒品防制相關問題\n- 查詢全台防制資源據點\n- 提供平台統計資料\n\n' +
                        '有什麼我可以幫你的嗎？',
                },
            ],
            input: '',
            loading: false,
        };
    },
    methods: {
        renderContent(text) {
            if (typeof marked !== 'undefined') {
                return marked.parse(text || '');
            }
            return (text || '').replace(/\n/g, '<br>');
        },

        async send() {
            const text = this.input.trim();
            if (!text || this.loading) return;

            this.messages.push({ role: 'user', content: text });
            this.input   = '';
            this.loading = true;
            this.$nextTick(() => this.scrollToBottom());

            try {
                const payload = { message: text };
                if (this.session_id) payload.session_id = this.session_id;

                const res = await axios.post('/api/chat', payload, {
                    headers: { 'Content-Type': 'application/json' },
                });

                if (res.data.session_id) {
                    this.session_id = res.data.session_id;
                    localStorage.setItem(this.SESSION_KEY, this.session_id);
                }

                this.messages.push({
                    role: 'assistant',
                    content: res.data.reply || '（無回應）',
                });
            } catch (err) {
                const msg =
                    err.response?.data?.error ||
                    `連線失敗：${err.message}`;
                this.messages.push({ role: 'assistant', content: `❌ ${msg}` });
            } finally {
                this.loading = false;
                this.$nextTick(() => this.scrollToBottom());
            }
        },

        async clearSession() {
            if (this.session_id) {
                try {
                    await axios.delete(`/api/chat/${this.session_id}`);
                } catch (_) { /* 忽略 404 */ }
                localStorage.removeItem(this.SESSION_KEY);
                this.session_id = null;
            }
            this.messages = [
                {
                    role: 'assistant',
                    content: '對話已清除！有什麼新問題嗎？',
                },
            ];
        },

        scrollToBottom() {
            const el = this.$refs.messagesEl;
            if (el) el.scrollTop = el.scrollHeight;
        },
    },
};
</script>

<style scoped>
.chat-wrapper {
    height: 100%;
    display: flex;
    flex-direction: column;
    background: #f3f6f4;
    font-family: 'Noto Sans TC', sans-serif;
}

.chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    background: #0a2623;
    color: #fff;
    font-size: 0.9rem;
    font-weight: 600;
    flex-shrink: 0;
}

.chat-title { letter-spacing: 0.02em; }

.clear-btn {
    background: transparent;
    border: 1px solid rgba(255,255,255,0.3);
    color: rgba(255,255,255,0.8);
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 0.75rem;
    cursor: pointer;
    transition: background 0.15s;
}
.clear-btn:hover { background: rgba(255,255,255,0.1); }

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 14px 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.message { display: flex; }
.message-user  { justify-content: flex-end; }
.message-bot   { justify-content: flex-start; }

.bubble {
    max-width: 80%;
    padding: 10px 14px;
    border-radius: 16px;
    font-size: 0.88rem;
    line-height: 1.6;
    word-break: break-word;
}
.message-user .bubble {
    background: #228577;
    color: #fff;
    border-bottom-right-radius: 4px;
}
.message-bot .bubble {
    background: #fff;
    color: #0a2623;
    border: 1px solid #c9e6e2;
    border-bottom-left-radius: 4px;
}

/* Markdown 樣式 */
.bubble :deep(p)  { margin: 0 0 0.5em; }
.bubble :deep(p:last-child) { margin-bottom: 0; }
.bubble :deep(ul), .bubble :deep(ol) { margin: 0.4em 0 0.4em 1.2em; }
.bubble :deep(table) {
    border-collapse: collapse;
    font-size: 0.82rem;
    margin: 0.5em 0;
    width: 100%;
}
.bubble :deep(th), .bubble :deep(td) {
    border: 1px solid #c9e6e2;
    padding: 4px 8px;
    text-align: left;
}
.bubble :deep(th) { background: #e8f4f2; }
.bubble :deep(code) {
    background: #f0f0f0;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 0.82em;
}
.bubble :deep(strong) { color: #156b5f; }

/* 打字動畫 */
.typing { display: flex; gap: 5px; align-items: center; padding: 12px 16px; }
.typing span {
    width: 7px; height: 7px;
    background: #43a093;
    border-radius: 50%;
    animation: bounce 1.2s infinite;
}
.typing span:nth-child(2) { animation-delay: 0.2s; }
.typing span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); }
    30%            { transform: translateY(-6px); }
}

/* 輸入列 */
.chat-input-row {
    display: flex;
    gap: 8px;
    padding: 10px 12px;
    border-top: 1px solid #c9e6e2;
    background: #fff;
    flex-shrink: 0;
}
.chat-input-row textarea {
    flex: 1;
    resize: none;
    border: 1px solid #c9e6e2;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 0.88rem;
    font-family: inherit;
    line-height: 1.5;
    outline: none;
    background: #f3f6f4;
    color: #0a2623;
    transition: border 0.15s;
}
.chat-input-row textarea:focus { border-color: #228577; }

.send-btn {
    background: #228577;
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 0 14px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background 0.15s;
    flex-shrink: 0;
}
.send-btn:hover:not(:disabled) { background: #156b5f; }
.send-btn:disabled { background: #a0d3cc; cursor: not-allowed; }
</style>
