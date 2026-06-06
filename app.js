// app.js
const options = {
    moduleCache: {
        vue: Vue
    },
    // 告訴 loader 怎麼讀取檔案
    async getFile(url) {
        const res = await fetch(url);
        if ( !res.ok )
            throw Object.assign(new Error(res.statusText + ' ' + url), { res });
        return {
            getContentData: asBinary => asBinary ? res.arrayBuffer() : res.text(),
        }
    },
    // 讓 .vue 檔案可以使用 <style>
    addStyle(textContent) {
        const style = document.createElement('style');
        style.textContent = textContent;
        const ref = document.head.getElementsByTagName('style')[0] || null;
        document.head.insertBefore(style, ref);
    },
}

const { loadModule } = window['vue3-sfc-loader'];

const app = Vue.createApp({
    components: {
        // 動態載入 App.vue
        'App': Vue.defineAsyncComponent(() => loadModule('./App.vue', options))
    },
    template: '<App></App>'
});

app.mount('#app');