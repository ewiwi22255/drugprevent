// 頁面切換功能
function showPage(pageId, event) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
    }
    
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    if (pageId === 'map') {
        setTimeout(() => {
            if (!mapInstance && typeof L !== 'undefined') {
                initMap();
            } else if (typeof L === 'undefined') {
                const mapContainer = document.getElementById('map-container');
                if (mapContainer) {
                    mapContainer.innerHTML = '<div class="map-error"><p>地圖 API 載入中，請稍候...</p></div>';
                    const checkLeaflet = setInterval(() => {
                        if (typeof L !== 'undefined') {
                            clearInterval(checkLeaflet);
                            initMap();
                        }
                    }, 100);
                    setTimeout(() => clearInterval(checkLeaflet), 10000);
                }
            }
        }, 100);
    }
    
    if (pageId === 'analytics') {
        refreshAnalyticsDashboard();
    }
}

// 藥物迷思測驗資料
let quizQuestions = [
    {
        category: "成癮與生理機制",
        question: "偶爾使用毒品不會上癮？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！即使是偶爾使用，毒品仍可能造成身體和心理依賴，且每個人對藥物的反應不同，風險難以預測。"
    },
    {
        category: "藥物迷思辨析",
        question: "大麻是天然植物，所以比合成毒品安全？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！天然不代表安全。大麻仍會影響認知功能、記憶力和判斷力，長期使用可能導致心理依賴和相關健康問題。"
    },
    {
        category: "成癮與生理機制",
        question: "只要意志力夠強，就能自行戒除毒品？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！毒品成癮是複雜的生理和心理問題，需要專業醫療協助。自行戒除可能導致嚴重的戒斷症狀，甚至危及生命。"
    },
    {
        category: "誘因與環境辨識",
        question: "年輕人使用毒品是因為壓力太大？",
        options: ["正確", "錯誤"],
        correct: 0,
        explanation: "部分正確，但壓力只是其中一個因素。同儕影響、好奇心、錯誤認知、缺乏正確資訊等都是可能的原因。重要的是提供正確的資訊和支援管道。"
    },
    {
        category: "成癮與生理機制",
        question: "使用毒品可以提升學習或工作效率？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！毒品會損害大腦功能，長期使用會導致認知能力下降、記憶力減退、注意力不集中等問題，反而會降低學習和工作效率。"
    },
    {
        category: "誘因與環境辨識",
        question: "「新興毒品」包裝成糖果、咖啡包，看起來很時尚，所以比較安全？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！包裝再可愛、再時尚，本質仍是毒品，內含成分往往不明，濃度難以掌握，反而更容易造成急性中毒與猝死風險。"
    },
    {
        category: "誘因與環境辨識",
        question: "只在派對或夜店玩樂時使用毒品，不會影響日常生活？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！毒品的影響不會只停留在當下，可能造成睡眠、情緒、記憶與判斷力長期受損，也會增加交通事故與暴力事件的風險。"
    },
    {
        category: "誘因與環境辨識",
        question: "朋友說「這只是助興藥，不算毒品」，所以比較沒關係？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！所謂「助興藥」、「歡樂粉」等名稱只是包裝話術，多半仍屬於毒品或違法藥物，會對身心健康與人際關係造成嚴重傷害。"
    },
    {
        category: "藥物迷思辨析",
        question: "只要沒有被警察抓到，使用毒品就不算嚴重問題？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！法律責任只是其中一部分，更嚴重的是對大腦、心血管與心理健康的長期損害，還可能影響學業、工作與家庭關係。"
    },
    {
        category: "復健與心理觀念",
        question: "曾經使用過毒品的人，就一定無法回到正常生活？",
        options: ["正確", "錯誤"],
        correct: 1,
        explanation: "錯誤！只要願意面對問題並尋求專業協助，透過醫療、諮商與家人支持，很多人都能逐漸恢復生活功能，重新建立健康的人生。"
    }
];

let currentQuizIndex = 0;
let quizScore = 0;
let quizAnswers = [];

async function loadQuizQuestions() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/quiz');
        quizQuestions = await response.json();
        console.log('Quiz 題庫已從後端載入', quizQuestions);
    } catch (error) {
        console.error('載入 Quiz 題庫失敗，使用前端預設題庫:', error);
    }
}

async function startQuiz() {
    await loadQuizQuestions();
    
    currentQuizIndex = 0;
    quizScore = 0;
    quizAnswers = [];
    document.getElementById('quiz-start').style.display = 'none';
    document.getElementById('quiz-content').style.display = 'block';
    document.getElementById('quiz-complete').style.display = 'none';
    showQuizQuestion();
    trackEvent('quiz_started');
}
// 1. 定義顏色映射表 (使用 Tailwind 類名)
const categoryColorMap = {
    "成癮與生理機制": "bg-red-100 text-red-700 border-red-200",
    "藥物迷思辨析": "bg-blue-100 text-blue-700 border-blue-200",
    "誘因與環境辨識": "bg-purple-100 text-purple-700 border-purple-200",
    "復健與心理觀念": "bg-green-100 text-green-700 border-green-200"
};

function showQuizQuestion() {
    const question = quizQuestions[currentQuizIndex];
    document.getElementById('quiz-question').textContent = question.question;
    document.getElementById('quiz-progress').textContent = `${currentQuizIndex + 1} / ${quizQuestions.length}`;
    document.getElementById('quiz-progress-bar').style.width = `${((currentQuizIndex + 1) / quizQuestions.length) * 100}%`;
    // 更新維度標籤
    const tagEl = document.getElementById('quiz-category-tag');
    const category = question.category || "一般資訊";
    tagEl.textContent = category;

    // 移除舊顏色並加上對應新顏色
    tagEl.className = "px-3 py-1 rounded-full text-xs font-bold border " + 
                     (categoryColorMap[category] || "bg-gray-100 text-gray-700 border-gray-200");

    document.getElementById('quiz-question').textContent = question.question;
    const optionsContainer = document.getElementById('quiz-options');
    optionsContainer.innerHTML = '';
    question.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'quiz-option w-full p-4 text-left border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50';
        button.textContent = option;
        button.onclick = () => selectQuizAnswer(index);
        optionsContainer.appendChild(button);
    });
    
    



    document.getElementById('quiz-result').classList.add('hidden');
}

function selectQuizAnswer(selectedIndex) {
    const question = quizQuestions[currentQuizIndex];
    const isCorrect = selectedIndex === question.correct;
    
    // 避免重複點擊（鎖定選項）
    const options = document.querySelectorAll('.quiz-option');
    options.forEach(opt => opt.disabled = true);

    if (isCorrect) quizScore++;
    
    quizAnswers.push({
        question: question.question,
        selected: selectedIndex,
        correct: question.correct,
        isCorrect: isCorrect
    });
    
    const resultDiv = document.getElementById('quiz-result');
    resultDiv.classList.remove('hidden');
    resultDiv.className = `mt-6 p-4 rounded-lg ${isCorrect ? 'bg-green-50 border border-green-200 text-green-800' : 'bg-red-50 border border-red-200 text-red-800'}`;
    
    // 插入科普知識內容及「下一題」按鈕
    resultDiv.innerHTML = `
        <p class="font-semibold mb-2">${isCorrect ? '✓ 答對了！' : '✗ 答錯了'}</p>
        <p class="mb-4">${question.explanation}</p>
        <div class="flex flex-wrap gap-2 justify-end">
            <button onclick="askAIAbout('${question.question}')" class="bg-purple-100 text-purple-700 px-4 py-2 rounded-lg hover:bg-purple-200 text-sm font-medium transition">
                ✨ 讓 AI 解釋更多
            </button>
            <button onclick="goToNextQuestion()" class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-medium transition shadow-md">
                ${currentQuizIndex === quizQuestions.length - 1 ? '查看結果' : '下一題 →'}
            </button>
        </div>
    `;
    
    trackEvent('quiz_answered', { question: currentQuizIndex, correct: isCorrect });
}

// 新增詢問 AI 的邏輯
function askAIAbout(questionText) {
    // 1. 打開 Chatbot 視窗
    const window = document.getElementById('chatbot-window');
    if (window.classList.contains('chatbot-hidden')) {
        toggleChatbot();
    }
    
    // 2. 這裡可以透過簡單的提示詞，引導使用者去 Chatbot 貼上問題
    alert("已為您開啟 AI 助手！您可以直接輸入：『請跟我解釋為什麼：\"" + questionText + "\" 是錯誤的觀念？』");
}


// 處理點擊確認按鈕後的前往邏輯
function goToNextQuestion() {
    currentQuizIndex++;
    if (currentQuizIndex < quizQuestions.length) {
        showQuizQuestion();
    } else {
        completeQuiz();
    }
}
// 在 completeQuiz 內更新呼叫方式
function completeQuiz() {
    document.getElementById('quiz-content').style.display = 'none';
    document.getElementById('quiz-complete').style.display = 'block';
    const percentage = Math.round((quizScore / quizQuestions.length) * 100);
    document.getElementById('quiz-score').textContent = `您答對了 ${quizScore} / ${quizQuestions.length} 題 (${percentage}%)`;
    
    quizAnswers.forEach(answer => {
        if (!answer.isCorrect) {
            // 找到該題的維度標籤並記錄
            const original = quizQuestions.find(q => q.question === answer.question);
            trackMythError(original.category);
        }
    });
    
    trackEvent('quiz_completed', { score: quizScore, total: quizQuestions.length });
}

function resetQuiz() {
    document.getElementById('quiz-start').style.display = 'block';
    document.getElementById('quiz-content').style.display = 'none';
    document.getElementById('quiz-complete').style.display = 'none';
}

// 修改 script.js 中的 preventionQuestions
const preventionQuestions = [
    { category: '成癮與生理機制', question: '當你聽說某種藥物可以「快速提神且不傷身」時，你的反應是？', options: ['非常有興趣', '半信半疑', '完全不信', '查證醫學資訊'], scores: [0, 1, 3, 4] },
    { category: '成癮與生理機制', question: '面對壓力時，你是否曾想過依賴某種物質來獲得短暫逃避？', options: ['經常', '偶爾', '極少', '從不'], scores: [0, 1, 3, 4] },
    
    { category: '藥物迷思辨析', question: '當好朋友告訴你「這只是助興藥，不是毒品」時，你會？', options: ['相信朋友', '猶豫不決', '直接拒絕', '勸導朋友'], scores: [0, 1, 3, 4] },
    { category: '藥物迷思辨析', question: '對於網路流傳的「藥物減肥」或「聰明藥」，你的看法是？', options: ['想試試看', '視為普通藥品', '保持戒心', '認定其危險性'], scores: [0, 1, 3, 4] },
    
    { category: '誘因與環境辨識', question: '如果你身處的聚會中有人提供不明來源的糖果或飲料，你會？', options: ['直接食用', '觀察別人後再拿', '禮貌婉拒', '堅決不拿並離開'], scores: [0, 1, 3, 4] },
    { category: '誘因與環境辨識', question: '當你發現身邊的朋友開始接觸奇怪的包裝粉末時，你會？', options: ['一起嘗試', '裝作沒看到', '提醒其風險', '尋求長輩協助'], scores: [0, 1, 3, 4] },
    
    { category: '復健與心理觀念', question: '若你身邊有親友曾誤入歧途，你對他們的回歸社會抱持？', options: ['排斥與歧視', '不予置評', '抱持希望', '願意提供支持'], scores: [0, 1, 2, 4] },
    { category: '復健與心理觀念', question: '當你遇到無法獨自解決的心理情緒問題時，你會？', options: ['獨自承受', '尋求偏方', '與親友傾訴', '尋求專業諮商'], scores: [0, 1, 3, 4] }
];

let currentPreventionIndex = 0;
let preventionScores = { 
    '成癮與生理機制': 0, 
    '藥物迷思辨析': 0, 
    '誘因與環境辨識': 0, 
    '復健與心理觀念': 0 
};

// 修改 script.js 中的 startPreventionTest
function startPreventionTest() {
    currentPreventionIndex = 0;
    // 初始化為 4 個維度標籤
    preventionScores = { 
        '成癮與生理機制': 0, 
        '藥物迷思辨析': 0, 
        '誘因與環境辨識': 0, 
        '復健與心理觀念': 0 
    };
    document.getElementById('prevention-start').style.display = 'none';
    document.getElementById('prevention-content').style.display = 'block';
    document.getElementById('prevention-results').style.display = 'none';
    showPreventionQuestion();
}

function showPreventionQuestion() {
    const question = preventionQuestions[currentPreventionIndex];
    document.getElementById('prevention-question').textContent = question.question;
    document.getElementById('prevention-category').textContent = `面向：${question.category}`;
    document.getElementById('prevention-progress').textContent = `${currentPreventionIndex + 1} / ${preventionQuestions.length}`;
    document.getElementById('prevention-progress-bar').style.width = `${((currentPreventionIndex + 1) / preventionQuestions.length) * 100}%`;
    
    const optionsContainer = document.getElementById('prevention-options');
    optionsContainer.innerHTML = '';
    question.options.forEach((option, index) => {
        const button = document.createElement('button');
        button.className = 'quiz-option w-full p-4 text-left border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50';
        button.textContent = option;
        button.onclick = () => selectPreventionAnswer(index);
        optionsContainer.appendChild(button);
    });
}

function selectPreventionAnswer(selectedIndex) {
    const question = preventionQuestions[currentPreventionIndex];
    const score = question.scores[selectedIndex];
    preventionScores[question.category] += score;
    
    trackEvent('prevention_answered', { category: question.category, question: currentPreventionIndex, score: score });
    
    currentPreventionIndex++;
    if (currentPreventionIndex < preventionQuestions.length) {
        showPreventionQuestion();
    } else {
        showPreventionResults();
    }
}

function showPreventionResults() {
    document.getElementById('prevention-content').style.display = 'none';
    document.getElementById('prevention-results').style.display = 'block';
    const scoresContainer = document.getElementById('prevention-scores');
    scoresContainer.innerHTML = '';
    const maxScore = 8;
    Object.keys(preventionScores).forEach(category => {
        const score = preventionScores[category];
        const percentage = Math.round((score / maxScore) * 100);
        const level = percentage >= 70 ? '高' : percentage >= 40 ? '中' : '低';
        const color = percentage >= 70 ? 'green' : percentage >= 40 ? 'yellow' : 'red';
        const scoreDiv = document.createElement('div');
        scoreDiv.className = 'bg-gray-50 p-4 rounded-lg border border-gray-200';
        scoreDiv.innerHTML = `
            <div class="flex justify-between items-center mb-2">
                <h4 class="font-semibold">${category}</h4>
                <span class="text-lg font-bold text-${color}-600">${level} (${percentage}%)</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-${color}-500 h-2 rounded-full transition-all duration-300" style="width: ${percentage}%"></div>
            </div>
        `;
        scoresContainer.appendChild(scoreDiv);
    });
    const interpretation = generateInterpretation(preventionScores);
    document.getElementById('prevention-interpretation').innerHTML = `
        <h4 class="font-semibold text-blue-900 mb-3">評估說明</h4>
        <p class="text-gray-700 leading-relaxed">${interpretation}</p>
    `;
    console.log('showPreventionResults: preventionScores =', preventionScores);
    trackEvent('prevention_test_completed', preventionScores);
    trackPreventionScore(preventionScores);
}

function generateInterpretation(scores) {
    let interpretation = "根據您的評估結果：\n\n";
    Object.keys(scores).forEach(category => {
        const score = scores[category];
        const percentage = Math.round((score / 8) * 100);
        if (percentage >= 70) {
            interpretation += `• ${category}：您的預防力表現良好，能夠有效判斷資訊、管理情緒或維護界線。\n`;
        } else if (percentage >= 40) {
            interpretation += `• ${category}：您的預防力處於中等水平，建議加強相關能力的培養。\n`;
        } else {
            interpretation += `• ${category}：建議您尋求專業協助，學習相關的預防技能。\n`;
        }
    });
    interpretation += "\n請記住，這只是參考評估，如有需要請尋求專業協助。";
    return interpretation;
}

function resetPreventionTest() {
    document.getElementById('prevention-start').style.display = 'block';
    document.getElementById('prevention-content').style.display = 'none';
    document.getElementById('prevention-results').style.display = 'none';
}

let mapInstance = null;
let markers = [];
const resources = [
    // 北部地區
    { name: "基隆市毒品危害防制中心", type: "輔導", city: "基隆市", lat: 25.1276, lng: 121.7391, phone: "02-2456-5515", address: "基隆市七堵區明德一路169號" },
    { name: "台北市立聯合醫院松德院區", type: "醫療", city: "台北市", lat: 25.0245, lng: 121.5775, phone: "02-2726-3141", address: "台北市信義區松德路309號" },
    { name: "台北市毒品危害防制中心", type: "輔導", city: "台北市", lat: 25.0422, lng: 121.5065, phone: "02-2370-1244", address: "台北市萬華區昆明街100號" },
    { name: "新北市藥癮防制中心", type: "社福", city: "新北市", lat: 25.0116, lng: 121.4663, phone: "02-2257-7155", address: "新北市板橋區文化路一段188巷57號" },
    { name: "桃園市毒品危害防制中心", type: "輔導", city: "桃園市", lat: 24.9936, lng: 121.3010, phone: "03-332-2600", address: "桃園市桃園區縣府路1號" },
    { name: "新竹市毒品危害防制中心", type: "輔導", city: "新竹市", lat: 24.8143, lng: 120.9610, phone: "03-535-5191", address: "新竹市北區中央路241號" },
    { name: "新竹縣毒品危害防制中心", type: "輔導", city: "新竹縣", lat: 24.8287, lng: 121.0177, phone: "03-551-8101", address: "新竹縣竹北市光明五街10號" },
    { name: "宜蘭縣毒品危害防制中心", type: "輔導", city: "宜蘭縣", lat: 24.7516, lng: 121.7517, phone: "03-936-7885", address: "宜蘭縣宜蘭市女中路二段287號" },

    // 中部地區
    { name: "苗栗縣毒品危害防制中心", type: "輔導", city: "苗栗縣", lat: 24.5649, lng: 120.8208, phone: "037-558-208", address: "苗栗縣苗栗市府前路1號" },
    { name: "台中榮民總醫院精神部", type: "醫療", city: "台中市", lat: 24.1777, lng: 120.6415, phone: "04-2359-2525", address: "台中市西屯區台灣大道四段1650號" },
    { name: "台中市毒品危害防制中心", type: "輔導", city: "台中市", lat: 24.2435, lng: 120.7188, phone: "04-2526-1170", address: "台中市豐原區中興路136號" },
    { name: "彰化縣毒品危害防制中心", type: "社福", city: "彰化縣", lat: 24.0770, lng: 120.5417, phone: "04-722-2151", address: "彰化縣彰化市中山路二段416號" },
    { name: "南投縣毒品危害防制中心", type: "輔導", city: "南投縣", lat: 23.9028, lng: 120.6905, phone: "049-220-9595", address: "南投縣南投市復興路6號" },
    { name: "雲林縣毒品危害防制中心", type: "輔導", city: "雲林縣", lat: 23.7093, lng: 120.4313, phone: "05-533-6136", address: "雲林縣斗六市府前街34號" },

    // 南部地區
    { name: "嘉義市毒品危害防制中心", type: "輔導", city: "嘉義市", lat: 23.4755, lng: 120.4473, phone: "05-233-8066", address: "嘉義市西區德明路1號" },
    { name: "嘉義縣毒品危害防制中心", type: "輔導", city: "嘉義縣", lat: 23.4589, lng: 120.2930, phone: "05-362-0600", address: "嘉義縣太保市祥和二路東段5號" },
    { name: "台南毒品危害防制中心", type: "輔導", city: "台南市", lat: 23.3117, lng: 120.3159, phone: "06-635-7716", address: "台南市新營區民治路36號" },
    { name: "高雄市立凱旋醫院", type: "醫療", city: "高雄市", lat: 22.6099, lng: 120.3139, phone: "07-751-3171", address: "高雄市苓雅區凱旋二路130號" },
    { name: "高雄市毒品危害防制中心", type: "輔導", city: "高雄市", lat: 22.6273, lng: 120.3014, phone: "07-211-1311", address: "高雄市前金區中正四路261號" },
    { name: "屏東縣毒品危害防制中心", type: "輔導", city: "屏東縣", lat: 22.6732, lng: 120.4862, phone: "08-737-0123", address: "屏東縣屏東市自由路272號" },

    // 東部及離島
    { name: "花蓮縣毒品危害防制中心", type: "輔導", city: "花蓮縣", lat: 23.9872, lng: 121.6176, phone: "03-822-7141", address: "花蓮縣花蓮市新興路200號" },
    { name: "台東縣毒品危害防制中心", type: "輔導", city: "台東縣", lat: 22.7554, lng: 121.1495, phone: "089-325-250", address: "台東縣台東市博愛路336號" },
    { name: "澎湖縣毒品危害防制中心", type: "輔導", city: "澎湖縣", lat: 23.5658, lng: 119.5665, phone: "06-927-2162", address: "澎湖縣馬公市中正路115號" },
    { name: "金門縣毒品危害防制中心", type: "輔導", city: "金門縣", lat: 24.4484, lng: 118.3785, phone: "082-330-697", address: "金門縣金湖鎮復興路1-12號" },
    { name: "連江縣毒品危害防制中心", type: "輔導", city: "連江縣", lat: 26.1511, lng: 119.9392, phone: "0836-22095", address: "連江縣南竿鄉介壽村256號" }
];

function initMap() {
    if (mapInstance) return;
    const mapContainer = document.getElementById('map-container');
    if (!mapContainer) return;
    if (typeof L === 'undefined') return;
    try {
        mapContainer.innerHTML = '';
        mapInstance = L.map('map-container').setView([23.8, 121], 7);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(mapInstance);
        renderResources('all');
    } catch (e) { console.error(e); }
}

function renderResources(filterType) {
    if (!mapInstance) return;
    const filteredResources = filterType === 'all' ? resources : resources.filter(r => r.type === filterType);
    markers.forEach(m => mapInstance.removeLayer(m));
    markers = [];
    const listContainer = document.getElementById('resource-list');
    if (listContainer) listContainer.innerHTML = '';
    filteredResources.forEach(res => {
        const marker = L.marker([res.lat, res.lng]).addTo(mapInstance);
        marker.bindPopup(`<b>${res.name}</b><br>${res.type}<br>${res.phone}`);
        markers.push(marker);
        if (listContainer) {
            const card = document.createElement('div');
            card.className = "p-3 border rounded-lg hover:bg-blue-50 cursor-pointer transition text-sm";
            card.innerHTML = `<h3 class="font-bold">${res.name}</h3><p class="text-xs text-gray-500">${res.city}</p>`;
            card.onclick = () => { mapInstance.setView([res.lat, res.lng], 15); marker.openPopup(); };
            listContainer.appendChild(card);
        }
    });
}

// 修正：原本代碼中這裡是遞迴呼叫自己，會導致無窮迴圈，已改為呼叫 renderResources
function filterResources(type) { 
    renderResources(type); 
    
    // 更新按鈕狀態
    document.querySelectorAll('.filter-btn').forEach(btn => {
        if(btn.dataset.filter === type) {
            btn.classList.remove('bg-gray-200', 'text-gray-700');
            btn.classList.add('bg-blue-600', 'text-white');
        } else {
            btn.classList.remove('bg-blue-600', 'text-white');
            btn.classList.add('bg-gray-200', 'text-gray-700');
        }
    });
}

// 修改 script.js 中的求助表單監聽器
document.getElementById('help-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const helpType = document.getElementById('help-type').value;
    const helpMessage = document.getElementById('help-message').value;
    const successMsg = document.getElementById('help-success');

    if (!helpMessage.trim()) {
        alert('請輸入求助內容');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/anonymous', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                type: helpType,
                message: helpMessage
            })
        });

        const result = await response.json();

        if (result.success) {
            successMsg.classList.remove('hidden');
            document.getElementById('help-form').reset();
        } else {
            alert('送出失敗，請稍後再試');
        }
    } catch (error) {
        console.error('匿名求助送出錯誤:', error);
        alert('無法連接後端，請確認 Flask 是否正在執行');
    }
});

function updateAnalytics() {
    const participants = JSON.parse(localStorage.getItem('afp_participants') || '[]');
    const quizzes = localStorage.getItem('afp_totalQuizzes') || '0';
    document.getElementById('total-users').textContent = participants.length;
    document.getElementById('total-quizzes').textContent = quizzes;
}

// Chart.js 圖表實例
let mythChartInstance = null;
let preventionChartInstance = null;

function renderMythChart() {
    const ctxEl = document.getElementById('myth-chart');
    if (!ctxEl) return;
    const ctx = ctxEl.getContext && ctxEl.getContext('2d') || ctxEl;
    const categoryErrors = JSON.parse(localStorage.getItem('mythErrorsByCategory') || '{}');
    const labels = Object.keys(categoryErrors);
    const data = Object.values(categoryErrors);

    if (mythChartInstance) { mythChartInstance.destroy(); }

    mythChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels, // 現在顯示的是「生理成癮」、「辨識防範」等簡潔標籤
            datasets: [{
                label: '該領域答錯次數',
                data: data,
                backgroundColor: 'rgba(59, 130, 246, 0.6)',
                borderColor: 'rgba(37, 99, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });
}

// 修改 script.js 中的 renderPreventionChart — 將 4 維度合併為 3 個群組：資訊判斷、情緒管理、人際界線
function renderPreventionChart() {
    const ctxEl = document.getElementById('prevention-chart');
    if (!ctxEl) return;
    const ctx = ctxEl.getContext && ctxEl.getContext('2d') || ctxEl;

    const history = JSON.parse(localStorage.getItem('preventionScores') || '[]');
    if (!history.length) return;

    // 新的三個群組及其對應的原始欄位
    const groups = [
        { label: '📚 資訊判斷', keys: ['藥物迷思辨析'] },
        { label: '🧘 情緒管理', keys: ['成癮與生理機制', '復健與心理觀念'] },
        { label: '🔒 人際界線', keys: ['誘因與環境辨識'] }
    ];
    const maxPerCategory = 8; // 原始每類最大分

    // 計算平台平均（以百分比表示）
    const sumsByGroup = groups.map(g => 0);
    history.forEach(entry => {
        groups.forEach((g, gi) => {
            g.keys.forEach(k => { sumsByGroup[gi] += (entry[k] || 0); });
        });
    });
    const averageData = groups.map((g, gi) => {
        const groupMax = g.keys.length * maxPerCategory;
        return Math.round((sumsByGroup[gi] / history.length / groupMax) * 100);
    });

    // 取最新一筆使用者資料並計算百分比
    const latest = history[history.length - 1] || {};
    const userData = groups.map(g => {
        const total = g.keys.reduce((sum, k) => sum + (latest[k] || 0), 0);
        const groupMax = g.keys.length * maxPerCategory;
        return Math.round((total / groupMax) * 100);
    });

    console.log('renderPreventionChart: groups labels =', groups.map(g=>g.label));
    console.log('renderPreventionChart: averageData =', averageData, 'userData =', userData);

    // 分析最強/最弱（保護性檢查 DOM 節點存在性）
    const analysis = groups.map((g, i) => ({ label: g.label, score: userData[i] }));
    analysis.sort((a, b) => b.score - a.score);
    const topEl = document.getElementById('top-strength');
    const weakEl = document.getElementById('top-weakness');
    if (topEl) topEl.textContent = `「${analysis[0].label}」表現優異，顯示您具備正確的防衛觀念。`;
    if (weakEl) weakEl.textContent = `「${analysis[analysis.length-1].label}」仍有提升空間，建議多閱讀相關科普資訊。`;

    if (preventionChartInstance) { preventionChartInstance.destroy(); }

    preventionChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: groups.map(g => g.label),
            datasets: [
                {
                    label: '您的表現 (%)',
                    data: userData,
                    backgroundColor: 'rgba(37, 99, 235, 0.3)',
                    borderColor: '#2563eb',
                    pointBackgroundColor: '#2563eb',
                    pointBorderColor: '#fff',
                    pointHoverRadius: 6,
                    borderWidth: 3,
                    tension: 0.1
                },
                {
                    label: '平台平均 (%)',
                    data: averageData,
                    backgroundColor: 'rgba(156, 163, 175, 0.1)',
                    borderColor: '#9ca3af',
                    borderDash: [5, 5],
                    pointRadius: 0,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: '#e5e7eb' },
                    grid: { color: '#f3f4f6' },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: { display: false, stepSize: 20 },
                    pointLabels: {
                        font: { size: 12, weight: 'bold' },
                        color: '#4b5563'
                    }
                }
            },
            plugins: {
                legend: { position: 'bottom', labels: { usePointStyle: true, boxWidth: 6 } }
            }
        }
    });
}

// 更新儀表板數值 + 圖表
function refreshAnalyticsDashboard() {
    console.log('refreshAnalyticsDashboard called');
    updateAnalytics();
    renderMythChart();
    renderPreventionChart();
}

function trackEvent(name, data) {
    if (name === 'quiz_completed') {
        const count = parseInt(localStorage.getItem('afp_totalQuizzes') || '0') + 1;
        localStorage.setItem('afp_totalQuizzes', count);
    }
    const userId = localStorage.getItem('afp_userId') || 'u_'+Date.now();
    localStorage.setItem('afp_userId', userId);
    const participants = new Set(JSON.parse(localStorage.getItem('afp_participants') || '[]'));
    participants.add(userId);
    localStorage.setItem('afp_participants', JSON.stringify([...participants]));
}

// 修改：改為紀錄維度名稱
function trackMythError(category) {
    const errs = JSON.parse(localStorage.getItem('mythErrorsByCategory') || '{}');
    errs[category] = (errs[category] || 0) + 1;
    localStorage.setItem('mythErrorsByCategory', JSON.stringify(errs));
}

function trackPreventionScore(s) {
    console.log('trackPreventionScore called with:', s);
    const history = JSON.parse(localStorage.getItem('preventionScores') || '[]');
    // push a deep copy to avoid accidental later mutation
    history.push(JSON.parse(JSON.stringify(s)));
    localStorage.setItem('preventionScores', JSON.stringify(history));
    console.log('trackPreventionScore: saved history length =', history.length);
    // 如果目前已在 analytics 頁面，立即刷新儀表板（讓圖表即時更新）
    const analyticsPage = document.getElementById('analytics');
    if (analyticsPage && analyticsPage.classList.contains('active')) {
        try { refreshAnalyticsDashboard(); } catch (e) { console.error('refreshAnalyticsDashboard error', e); }
    }
}

document.addEventListener('DOMContentLoaded', () => showPage('home'));


// 在 script.js 最下方加入
function toggleChatbot() {
    const window = document.getElementById('chatbot-window');
    const btn = document.getElementById('chatbot-toggle');
    
    window.classList.toggle('chatbot-hidden');
    btn.classList.toggle('active');
    
    // 如果打開時需要自動對焦輸入框，可以在這裡處理
    if (!window.classList.contains('chatbot-hidden')) {
        trackEvent('chatbot_opened');
    }
}
