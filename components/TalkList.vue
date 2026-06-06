<template>
    <div class="chat-window" ref="chatWindow">
        <div 
            class="chat-item" 
            v-for="(item, index) in talkContents" 
            :key="index" 
            :class="item.class"
        >
            <div class="avatar">{{ item.user }}</div>
            <div class="chat-content" v-html="renderMarkdown(item.content)"></div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TalkList',
    props: {
        talkContents: { type: Array, default: () => [] }
    },
    methods: {
        // 利用 marked.js 將 Markdown 轉為 HTML
        renderMarkdown(text) {
            if (!text) return '';
            return marked.parse(text); 
        }
    },
    watch: {
        talkContents: {
            handler() {
                this.$nextTick(() => {
                    // 自動捲動到底部
                    const box = this.$refs.chatWindow;
                    if(box) box.scrollTop = box.scrollHeight;
                    
                    // 核心：內容更新後，重新觸發代碼高亮
                    document.querySelectorAll('pre code').forEach((block) => {
                        hljs.highlightElement(block);
                    });
                });
            },
            deep: true
        }
    }
}
</script>

<style scoped>
/* 樣式美化：調整程式碼區塊背景與圓角 */
.chat-window { 
    height: 350px; /* 從 60vh 改為固定高度或彈性高度 */
    flex-grow: 1;  /* 讓對話區填滿空間 */
    border: 1px solid #dee2e6; 
    border-radius: 10px; 
    overflow-y: auto; 
    padding: 1rem; 
    background: #fff; 
    margin-bottom: 10px;
}
.chat-item { display: flex; margin-bottom: 1.5rem; }
.chat-item.user { flex-direction: row-reverse; }
.chat-content { max-width: 80%; padding: 0.8rem 1.2rem; border-radius: 15px; line-height: 1.6; }

/* AI 回應框樣式 */
.chat-item.gemini .chat-content { background-color: #f8f9fa; border: 1px solid #e9ecef; }
.chat-item.user .chat-content { background-color: #007bff; color: white; }

/* 針對程式碼區塊進行美化 */
:deep(pre) { background: #1e1e1e; padding: 1rem; border-radius: 8px; margin: 10px 0; overflow-x: auto; }
:deep(code) { font-family: 'Consolas', monospace; font-size: 0.9rem; }
:deep(ul), :deep(ol) { padding-left: 1.5rem; }
.avatar { font-size: 0.75rem; margin: 0 10px; color: #888; width: 60px; text-align: center; }
</style>