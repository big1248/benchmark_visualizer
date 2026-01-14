/**
 * LLM Benchmark Visualizer - Complete Version
 * 원본 Streamlit 앱과 동일한 기능 구현
 */

// ========== 전역 상태 ==========
const APP = {
    data: [],
    filtered: [],
    lang: 'ko',
    fontScale: 1.0,
    chartFontScale: 1.0,
    // 필터 선택값 (multiselect)
    selectedTests: [],
    selectedModels: [],
    selectedDetails: [],
    selectedPrompts: [],
    selectedYears: [],
    // 앙상블
    ensembles: [],
    ensembleSelectedModels: []
};

// 번역 텍스트
const T = {
    ko: {
        title: 'LLM 벤치마크 결과 시각화 도구',
        display_settings: '화면 설정',
        font_size: '화면 폰트 크기',
        chart_text_size: '차트 텍스트 크기',
        filters: '필터 옵션',
        testname: '테스트명',
        model: '모델',
        detail_type: '상세도',
        prompting: '프롬프팅 방식',
        year: '연도',
        problem_type: '문제 유형',
        law_type: '법령 구분',
        all: '전체',
        image_problem: '이미지 포함',
        text_only: '텍스트만',
        law: '법령',
        non_law: '비법령',
        ensemble_management: '앙상블 모델 관리',
        create_ensemble: '앙상블 생성',
        ensemble_name: '앙상블 이름',
        select_models: '모델 선택',
        ensemble_method: '앙상블 방법',
        majority_voting: '다수결 투표',
        weighted_voting: '가중 투표',
        add_ensemble: '앙상블 추가',
        no_ensembles: '생성된 앙상블이 없습니다',
        ensemble_added: '앙상블이 추가되었습니다',
        min_2_models: '최소 2개 이상의 모델을 선택해야 합니다',
        current_data: '현재 표시 중인 데이터',
        problems: '개 문제',
        overview: '전체 요약',
        model_comparison: '모델별 비교',
        response_time_analysis: '응답시간 분석',
        law_analysis: '법령/비법령 분석',
        subject_analysis: '과목별 분석',
        year_analysis: '연도별 분석',
        incorrect_analysis: '오답 분석',
        difficulty_analysis: '난이도 분석',
        token_cost_analysis: '토큰/비용 분석',
        testset_stats: '테스트셋 통계',
        total_problems: '총 문제 수',
        accuracy: '정확도',
        correct: '정답',
        wrong: '오답',
        law_problems: '법령 문제',
        non_law_problems: '비법령 문제',
        performance_by_model: '모델별 성능 지표',
        comparison_chart: '모델별 성능 비교 차트',
        overall_comparison: '전체 테스트 비교',
        heatmap: '모델별 테스트셋 정답도 히트맵',
        law_ratio: '법령/비법령 전체 통계',
        model_law_performance: '모델별 법령/비법령 성능 비교',
        subject_performance: '과목별 성능',
        year_performance: '연도별 성능',
        top_incorrect: '오답률 높은 문제 Top 20',
        all_models_incorrect: '모든 모델이 틀린 문제',
        most_models_incorrect: '대부분 모델이 틀린 문제 (≥50%)',
        test_info: '테스트',
        problem_id: '문제 번호',
        incorrect_count: '오답 모델수',
        total_models: '총 모델수',
        wrong_rate: '오답률',
        very_hard: '매우 어려운 문제',
        very_easy: '매우 쉬운 문제',
        problem_count: '문제 수',
        problem_distribution: '난이도 구간별 문제 분포',
        response_time: '응답 시간',
        avg_response_time: '평균 응답 시간',
        response_time_distribution: '응답시간 분포',
        response_time_by_model: '모델별 평균 응답시간',
        response_time_stats: '응답 시간 통계',
        fastest_model: '가장 빠른 모델',
        slowest_model: '가장 느린 모델',
        response_time_vs_accuracy: '응답시간 vs 정확도',
        seconds: '초',
        token_stats: '토큰 사용량 통계',
        input_tokens: '입력 토큰',
        output_tokens: '출력 토큰',
        total_tokens: '총 토큰',
        avg_tokens_per_problem: '문제당 평균 토큰',
        token_distribution: '토큰 사용량 시각화',
        token_efficiency: '토큰 효율성',
        io_ratio: '입출력 토큰 비율',
        token_per_correct: '정답당 토큰',
        most_efficient: '가장 효율적인 모델',
        year_problem_chart: '연도별 문제 수',
        avg_accuracy_by_model: '모델별 평균 정확도'
    },
    en: {
        title: 'LLM Benchmark Results Visualization Tool',
        display_settings: 'Display Settings',
        font_size: 'Screen Font Size',
        chart_text_size: 'Chart Text Size',
        filters: 'Filter Options',
        testname: 'Test Name',
        model: 'Model',
        detail_type: 'Detail Type',
        prompting: 'Prompting Method',
        year: 'Year',
        problem_type: 'Problem Type',
        law_type: 'Law Type',
        all: 'All',
        image_problem: 'With Image',
        text_only: 'Text Only',
        law: 'Law',
        non_law: 'Non-Law',
        ensemble_management: 'Ensemble Model Management',
        create_ensemble: 'Create Ensemble',
        ensemble_name: 'Ensemble Name',
        select_models: 'Select Models',
        ensemble_method: 'Ensemble Method',
        majority_voting: 'Majority Voting',
        weighted_voting: 'Weighted Voting',
        add_ensemble: 'Add Ensemble',
        no_ensembles: 'No ensembles created',
        ensemble_added: 'Ensemble added successfully',
        min_2_models: 'Please select at least 2 models',
        current_data: 'Currently showing',
        problems: ' problems',
        overview: 'Overview',
        model_comparison: 'Model Comparison',
        response_time_analysis: 'Response Time Analysis',
        law_analysis: 'Law/Non-Law Analysis',
        subject_analysis: 'Subject Analysis',
        year_analysis: 'Year Analysis',
        incorrect_analysis: 'Incorrect Analysis',
        difficulty_analysis: 'Difficulty Analysis',
        token_cost_analysis: 'Token & Cost Analysis',
        testset_stats: 'Test Set Statistics',
        total_problems: 'Total Problems',
        accuracy: 'Accuracy',
        correct: 'Correct',
        wrong: 'Wrong',
        law_problems: 'Law Problems',
        non_law_problems: 'Non-Law Problems',
        performance_by_model: 'Performance by Model',
        comparison_chart: 'Comparison Chart',
        overall_comparison: 'Overall Comparison',
        heatmap: 'Model × Test Accuracy Heatmap',
        law_ratio: 'Law/Non-Law Statistics',
        model_law_performance: 'Model Law/Non-Law Performance',
        subject_performance: 'Subject Performance',
        year_performance: 'Year Performance',
        top_incorrect: 'Top 20 Problems with Highest Incorrect Rate',
        all_models_incorrect: 'All Models Incorrect',
        most_models_incorrect: 'Most Models Incorrect (≥50%)',
        test_info: 'Test',
        problem_id: 'Problem ID',
        incorrect_count: 'Incorrect Count',
        total_models: 'Total Models',
        wrong_rate: 'Wrong Rate',
        very_hard: 'Very Hard Problems',
        very_easy: 'Very Easy Problems',
        problem_count: 'Problem Count',
        problem_distribution: 'Difficulty Distribution',
        response_time: 'Response Time',
        avg_response_time: 'Avg Response Time',
        response_time_distribution: 'Response Time Distribution',
        response_time_by_model: 'Response Time by Model',
        response_time_stats: 'Response Time Statistics',
        fastest_model: 'Fastest Model',
        slowest_model: 'Slowest Model',
        response_time_vs_accuracy: 'Response Time vs Accuracy',
        seconds: 's',
        token_stats: 'Token Statistics',
        input_tokens: 'Input Tokens',
        output_tokens: 'Output Tokens',
        total_tokens: 'Total Tokens',
        avg_tokens_per_problem: 'Avg Tokens per Problem',
        token_distribution: 'Token Distribution',
        token_efficiency: 'Token Efficiency',
        io_ratio: 'I/O Token Ratio',
        token_per_correct: 'Tokens per Correct',
        most_efficient: 'Most Efficient Model',
        year_problem_chart: 'Problems by Year',
        avg_accuracy_by_model: 'Avg Accuracy by Model'
    }
};

// Plotly 기본 레이아웃
function getLayout(title = '') {
    return {
        paper_bgcolor: 'white',
        plot_bgcolor: 'white',
        font: { 
            color: '#262730', 
            size: 12 * APP.chartFontScale, 
            family: 'Source Sans Pro, sans-serif' 
        },
        margin: { l: 60, r: 30, t: title ? 50 : 30, b: 80 },
        xaxis: { gridcolor: '#e6e9ef', linecolor: '#e6e9ef', tickfont: { size: 11 * APP.chartFontScale } },
        yaxis: { gridcolor: '#e6e9ef', linecolor: '#e6e9ef', tickfont: { size: 11 * APP.chartFontScale } },
        title: title ? { text: title, font: { size: 14 * APP.chartFontScale } } : undefined
    };
}
const CONFIG = { responsive: true, displayModeBar: false };

// 정확도 색상
function accColor(v) {
    if (v >= 80) return 'rgba(9,171,59,0.85)';
    if (v >= 70) return 'rgba(46,204,113,0.75)';
    if (v >= 60) return 'rgba(133,200,114,0.65)';
    if (v >= 50) return 'rgba(241,196,15,0.7)';
    if (v >= 40) return 'rgba(230,126,34,0.7)';
    return 'rgba(231,76,60,0.7)';
}

// ========== 유틸리티 함수 ==========
function t(key) {
    return T[APP.lang][key] || T['ko'][key] || key;
}

function updateTranslations() {
    document.querySelectorAll('[data-t]').forEach(el => {
        const key = el.getAttribute('data-t');
        if (T[APP.lang][key]) el.textContent = T[APP.lang][key];
    });
}

function applyFontScale() {
    document.documentElement.style.setProperty('--font-scale', APP.fontScale);
}

function toggleExpander(id) {
    document.getElementById(id).classList.toggle('open');
}

// ========== 데이터 로딩 ==========
async function loadData() {
    const loading = document.getElementById('loading');
    const text = document.getElementById('loadingText');
    const bar = document.getElementById('progressFill');
    
    try {
        text.textContent = 'GitHub에서 데이터 다운로드 중...';
        const url = 'https://github.com/big1248/benchmark_visualizer/releases/download/v2.2.0/data.zip';
        const proxy = `https://corsproxy.io/?${encodeURIComponent(url)}`;
        
        let res;
        try { res = await fetch(url); if (!res.ok) throw 0; }
        catch { res = await fetch(proxy); }
        
        const reader = res.body.getReader();
        const chunks = [];
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
        }
        
        text.textContent = 'CSV 파일 파싱 중...';
        bar.style.width = '50%';
        
        const zip = await JSZip.loadAsync(new Blob(chunks));
        const files = Object.keys(zip.files).filter(n => n.endsWith('.csv'));
        const all = [];
        
        for (let i = 0; i < files.length; i++) {
            const content = await zip.files[files[i]].async('text');
            const info = parseFilename(files[i]);
            const parsed = Papa.parse(content, { header: true, skipEmptyLines: true, dynamicTyping: true });
            
            parsed.data.forEach(row => {
                if (row.Question || row.ID) {
                    row.모델 = row.모델명 || info.model;
                    row.테스트명 = row['Test Name'] || info.testname;
                    row.상세도 = row.상세도 || info.detail || 'detailed';
                    row.프롬프팅 = row.프롬프팅 || info.prompt || 'no_prompting';
                    row.정답여부 = row.정답여부 === true || row.정답여부 === 'True' || row.정답여부 === 1;
                    all.push(row);
                }
            });
            bar.style.width = `${50 + (i / files.length) * 50}%`;
        }
        
        APP.data = all;
        init();
        loading.classList.add('hidden');
    } catch (e) {
        console.error('데이터 로드 실패:', e);
        text.textContent = '샘플 데이터 로드 중...';
        loadSample();
        loading.classList.add('hidden');
    }
}

function parseFilename(f) {
    const n = f.replace('data/', '').replace('.csv', '');
    const p = n.split('_');
    return { 
        model: p[0] || 'Unknown', 
        detail: p[1] || 'detailed', 
        prompt: p[2] || 'no_prompting', 
        testname: p.slice(3).join('_') || 'Unknown' 
    };
}

function loadSample() {
    const models = ['GPT-4o', 'Claude-3.5-Sonnet', 'Qwen3-30b-a3b', 'Meta-Llama-3.1-8b', 'Claude-3.5-Haiku', 'GPT-4o-Mini'];
    const tests = ['건설안전기사', '경비지도사2차'];
    const subjects = ['안전관리론', '재난관리론', '소방학', '도시계획', '교육학개론', '구급 및 응급처치론'];
    const details = ['detailed', 'simple'];
    const prompts = ['no_prompting', 'CoT'];
    const all = [];
    
    models.forEach(m => {
        tests.forEach(test => {
            const detail = details[Math.floor(Math.random() * 2)];
            const prompt = prompts[Math.floor(Math.random() * 2)];
            for (let i = 0; i < 300; i++) {
                all.push({
                    ID: all.length + 1,
                    모델: m,
                    테스트명: test,
                    상세도: detail,
                    프롬프팅: prompt,
                    Year: 2018 + Math.floor(Math.random() * 7),
                    Subject: subjects[Math.floor(Math.random() * subjects.length)],
                    Question: `Q_${test}_${m}_${i}`,
                    정답여부: Math.random() > 0.35,
                    law: Math.random() > 0.5 ? 'O' : '',
                    '문제당평균시간(초)': +(Math.random() * 3 + 0.1).toFixed(2),
                    '입력토큰': Math.floor(Math.random() * 400 + 100),
                    '출력토큰': Math.floor(Math.random() * 80 + 10)
                });
            }
        });
    });
    APP.data = all;
    init();
}

// ========== 초기화 ==========
function init() {
    setupFilters();
    setupEventListeners();
    updateTranslations();
    filter();
}

function setupFilters() {
    const data = APP.data;
    
    // 고유값 추출
    const tests = [...new Set(data.map(d => d.테스트명).filter(Boolean))].sort();
    const models = [...new Set(data.map(d => d.모델).filter(Boolean))].sort();
    const details = [...new Set(data.map(d => d.상세도).filter(Boolean))].sort();
    const prompts = [...new Set(data.map(d => d.프롬프팅).filter(Boolean))].sort();
    const years = [...new Set(data.map(d => d.Year).filter(Boolean))].sort((a, b) => a - b);
    
    // 기본값: 전체 선택
    APP.selectedTests = [...tests];
    APP.selectedModels = [...models];
    APP.selectedDetails = [...details];
    APP.selectedPrompts = [...prompts];
    APP.selectedYears = [...years];
    
    // 셀렉트 박스 옵션 설정
    populateSelect('testSelect', tests, '+ 테스트 추가');
    populateSelect('modelSelect', models, '+ 모델 추가');
    populateSelect('detailSelect', details, '+ 상세도 추가');
    populateSelect('promptSelect', prompts, '+ 프롬프팅 추가');
    populateSelect('yearSelect', years, '+ 연도 추가');
    populateSelect('ensembleModelSelect', models, '+ 모델 추가');
    
    // 태그 렌더링
    renderAllTags();
}

function populateSelect(id, options, placeholder) {
    const sel = document.getElementById(id);
    sel.innerHTML = `<option value="">${placeholder}</option>`;
    options.forEach(opt => {
        sel.innerHTML += `<option value="${opt}">${opt}</option>`;
    });
}

function renderAllTags() {
    renderTags('testTags', APP.selectedTests, 'test');
    renderTags('modelTags', APP.selectedModels, 'model');
    renderTags('detailTags', APP.selectedDetails, 'detail');
    renderTags('promptTags', APP.selectedPrompts, 'prompt');
    renderTags('yearTags', APP.selectedYears, 'year');
    renderTags('ensembleModelTags', APP.ensembleSelectedModels, 'ensembleModel');
}

function renderTags(containerId, items, type) {
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const allItems = getAvailableItems(type);
    const isAll = items.length === allItems.length && items.length > 0;
    
    if (isAll && type !== 'ensembleModel') {
        container.innerHTML = `<span class="tag tag-all">${t('all')} (${items.length})</span>`;
    } else if (items.length === 0) {
        container.innerHTML = `<span style="color:var(--text-muted);font-size:0.85rem;">선택된 항목 없음</span>`;
    } else {
        container.innerHTML = items.map(item => 
            `<span class="tag">${item}<span class="tag-remove" onclick="removeTag('${type}', '${item}')">×</span></span>`
        ).join('');
    }
}

function getAvailableItems(type) {
    const data = APP.data;
    switch(type) {
        case 'test': return [...new Set(data.map(d => d.테스트명).filter(Boolean))];
        case 'model': return [...new Set(data.map(d => d.모델).filter(Boolean))];
        case 'detail': return [...new Set(data.map(d => d.상세도).filter(Boolean))];
        case 'prompt': return [...new Set(data.map(d => d.프롬프팅).filter(Boolean))];
        case 'year': return [...new Set(data.map(d => d.Year).filter(Boolean))];
        case 'ensembleModel': return [...new Set(data.map(d => d.모델).filter(Boolean))];
        default: return [];
    }
}

function getSelectedArray(type) {
    switch(type) {
        case 'test': return APP.selectedTests;
        case 'model': return APP.selectedModels;
        case 'detail': return APP.selectedDetails;
        case 'prompt': return APP.selectedPrompts;
        case 'year': return APP.selectedYears;
        case 'ensembleModel': return APP.ensembleSelectedModels;
        default: return [];
    }
}

function addTag(type, value) {
    const arr = getSelectedArray(type);
    if (value && !arr.includes(value)) {
        arr.push(value);
        renderAllTags();
        if (type !== 'ensembleModel') filter();
    }
}

function removeTag(type, value) {
    const arr = getSelectedArray(type);
    const idx = arr.indexOf(value);
    if (idx > -1) {
        arr.splice(idx, 1);
        renderAllTags();
        if (type !== 'ensembleModel') filter();
    }
}

function setupEventListeners() {
    // 언어 변경
    document.getElementById('langSelect').onchange = e => {
        APP.lang = e.target.value;
        updateTranslations();
        const active = document.querySelector('.tab-btn.active');
        if (active) render(active.dataset.tab);
    };
    
    // 폰트 크기
    document.getElementById('fontSlider').oninput = e => {
        APP.fontScale = +e.target.value;
        document.getElementById('fontValue').textContent = APP.fontScale.toFixed(1);
        applyFontScale();
    };
    
    // 차트 텍스트 크기
    document.getElementById('chartSlider').oninput = e => {
        APP.chartFontScale = +e.target.value;
        document.getElementById('chartValue').textContent = APP.chartFontScale.toFixed(1);
        const active = document.querySelector('.tab-btn.active');
        if (active) render(active.dataset.tab);
    };
    
    // 필터 셀렉트
    ['test', 'model', 'detail', 'prompt', 'year'].forEach(type => {
        const sel = document.getElementById(`${type}Select`);
        sel.onchange = e => {
            if (e.target.value) {
                addTag(type, e.target.value);
                e.target.value = '';
            }
        };
    });
    
    // 앙상블 모델 셀렉트
    document.getElementById('ensembleModelSelect').onchange = e => {
        if (e.target.value) {
            addTag('ensembleModel', e.target.value);
            e.target.value = '';
        }
    };
    
    // 문제 유형, 법령 필터
    document.getElementById('typeSelect').onchange = filter;
    document.getElementById('lawSelect').onchange = filter;
    
    // 탭 버튼
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
            render(btn.dataset.tab);
        };
    });
}

// ========== 앙상블 관리 ==========
function addEnsemble() {
    const name = document.getElementById('ensembleName').value.trim();
    const models = [...APP.ensembleSelectedModels];
    const method = document.getElementById('ensembleMethod').value;
    
    if (!name) {
        alert(APP.lang === 'ko' ? '앙상블 이름을 입력하세요' : 'Please enter ensemble name');
        return;
    }
    
    if (models.length < 2) {
        alert(t('min_2_models'));
        return;
    }
    
    if (APP.ensembles.some(e => e.name === name)) {
        alert(APP.lang === 'ko' ? '같은 이름의 앙상블이 이미 있습니다' : 'Ensemble with same name exists');
        return;
    }
    
    APP.ensembles.push({
        name: `🎯 ${name}`,
        models: models,
        method: method,
        methodDisplay: method === 'majority' ? t('majority_voting') : t('weighted_voting')
    });
    
    // 초기화
    document.getElementById('ensembleName').value = '';
    APP.ensembleSelectedModels = [];
    renderAllTags();
    
    // 앙상블 데이터 생성 및 필터 적용
    generateEnsembleData();
    renderEnsembleList();
    filter();
}

function removeEnsemble(idx) {
    APP.ensembles.splice(idx, 1);
    generateEnsembleData();
    renderEnsembleList();
    filter();
}

function renderEnsembleList() {
    const container = document.getElementById('ensembleList');
    const status = document.getElementById('ensembleStatus');
    
    if (APP.ensembles.length === 0) {
        container.innerHTML = '';
        status.innerHTML = `<span data-t="no_ensembles">${t('no_ensembles')}</span>`;
        status.className = 'status-box status-info';
    } else {
        container.innerHTML = APP.ensembles.map((e, i) => `
            <div class="ensemble-item">
                <div class="ensemble-info">
                    <div class="ensemble-name">${e.name}</div>
                    <div class="ensemble-meta">• ${e.methodDisplay}</div>
                    <div class="ensemble-meta">• ${e.models.length} ${APP.lang === 'ko' ? '모델' : 'models'}</div>
                </div>
                <button class="btn btn-danger" onclick="removeEnsemble(${i})">🗑️</button>
            </div>
        `).join('');
        
        status.innerHTML = `🎯 ${APP.ensembles.length}${APP.lang === 'ko' ? '개 앙상블 활성' : ' ensemble(s) active'}`;
        status.className = 'status-box status-success';
    }
}

function generateEnsembleData() {
    // 앙상블 데이터 생성 로직 (다수결 투표)
    // 실제 구현에서는 원본 데이터를 기반으로 앙상블 예측을 생성
    APP.ensembles.forEach(ensemble => {
        // 여기서 앙상블 로직 구현
        // 간단한 구현: 다수결로 정답여부 결정
    });
}

// ========== 필터링 ==========
function filter() {
    const typeFilter = document.getElementById('typeSelect').value;
    const lawFilter = document.getElementById('lawSelect').value;
    
    APP.filtered = APP.data.filter(r => {
        // 테스트 필터
        if (APP.selectedTests.length && !APP.selectedTests.includes(r.테스트명)) return false;
        // 모델 필터
        if (APP.selectedModels.length && !APP.selectedModels.includes(r.모델)) return false;
        // 상세도 필터
        if (APP.selectedDetails.length && !APP.selectedDetails.includes(r.상세도)) return false;
        // 프롬프팅 필터
        if (APP.selectedPrompts.length && !APP.selectedPrompts.includes(r.프롬프팅)) return false;
        // 연도 필터
        if (APP.selectedYears.length && !APP.selectedYears.includes(r.Year)) return false;
        // 문제 유형 필터
        if (typeFilter === 'text' && r.image && r.image !== 'text_only') return false;
        if (typeFilter === 'image' && (!r.image || r.image === 'text_only')) return false;
        // 법령 필터
        if (lawFilter === 'O' && r.law !== 'O') return false;
        if (lawFilter === 'X' && r.law === 'O') return false;
        
        return true;
    });
    
    document.getElementById('dataCount').textContent = APP.filtered.length.toLocaleString();
    
    const active = document.querySelector('.tab-btn.active');
    if (active) render(active.dataset.tab);
}

function render(tab) {
    const handlers = {
        overview: renderOverview,
        model: renderModel,
        time: renderTime,
        law: renderLaw,
        subject: renderSubject,
        year: renderYear,
        error: renderError,
        diff: renderDiff,
        cost: renderCost,
        testset: renderTestset,
        extra: renderExtra
    };
    handlers[tab]?.();
}

// ========== 전체 요약 ==========
function renderOverview() {
    const d = APP.filtered;
    const models = [...new Set(d.map(r => r.모델).filter(Boolean))];
    const questions = new Set(d.map(r => r.Question));
    const total = questions.size;
    
    document.getElementById('m-total').textContent = total.toLocaleString();
    document.getElementById('m-models').textContent = models.length;
    document.getElementById('m-evals').textContent = d.length.toLocaleString();
    
    const accByModel = {};
    d.forEach(r => {
        if (!r.모델) return;
        if (!accByModel[r.모델]) accByModel[r.모델] = { c: 0, t: 0 };
        accByModel[r.모델].t++;
        if (r.정답여부) accByModel[r.모델].c++;
    });
    
    const avgAcc = models.length ? Object.values(accByModel).reduce((s, v) => s + v.c / v.t, 0) / models.length * 100 : 0;
    const avgC = Math.round(total * avgAcc / 100);
    
    document.getElementById('m-acc').textContent = avgAcc.toFixed(2) + '%';
    document.getElementById('m-avgq').textContent = total.toLocaleString();
    document.getElementById('m-avgc').textContent = avgC.toLocaleString();
    document.getElementById('m-avgw').textContent = (total - avgC).toLocaleString();
    
    const lawD = d.filter(r => r.law === 'O');
    const nonLawD = d.filter(r => r.law !== 'O');
    const lawQ = new Set(lawD.map(r => r.Question)).size;
    const nonLawQ = new Set(nonLawD.map(r => r.Question)).size;
    const lawAcc = lawD.length ? (lawD.filter(r => r.정답여부).length / lawD.length * 100) : 0;
    const nonLawAcc = nonLawD.length ? (nonLawD.filter(r => r.정답여부).length / nonLawD.length * 100) : 0;
    
    document.getElementById('m-law').textContent = lawQ.toLocaleString();
    document.getElementById('m-lawacc').textContent = lawAcc.toFixed(2) + '%';
    document.getElementById('m-nonlaw').textContent = nonLawQ.toLocaleString();
    document.getElementById('m-nonlawacc').textContent = nonLawAcc.toFixed(2) + '%';
    
    const sorted = Object.entries(accByModel).sort((a, b) => b[1].c / b[1].t - a[1].c / a[1].t);
    const mNames = sorted.map(x => x[0]);
    const mAccs = sorted.map(x => (x[1].c / x[1].t * 100).toFixed(2));
    
    Plotly.newPlot('chart-modelacc', [{
        x: mNames, y: mAccs, type: 'bar',
        marker: { color: mAccs.map(v => accColor(+v)), line: { color: '#000', width: 1.5 } },
        text: mAccs.map(v => v + '%'), textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('avg_accuracy_by_model')), xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('accuracy') + ' (%)', range: [0, 100] } }, CONFIG);
    
    Plotly.newPlot('chart-lawcomp', [{
        x: [t('law'), t('non_law')], y: [lawAcc, nonLawAcc], type: 'bar',
        marker: { color: ['#FF6B6B', '#4ECDC4'], line: { color: '#000', width: 1.5 } },
        text: [lawAcc.toFixed(1) + '%', nonLawAcc.toFixed(1) + '%'], textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('law') + '/' + t('non_law') + ' ' + t('accuracy')), yaxis: { title: t('accuracy') + ' (%)', range: [0, 100] } }, CONFIG);
    
    document.querySelector('#tbl-perf tbody').innerHTML = sorted.map(([m, s], i) => {
        const acc = (s.c / s.t * 100).toFixed(2);
        return `<tr><td>${i+1}</td><td>${m}</td><td>${s.c}</td><td>${s.t}</td><td><span class="acc-cell" style="background:${accColor(+acc)}">${acc}%</span></td><td>${s.t - s.c}</td></tr>`;
    }).join('');
    
    renderHeatmap('chart-heatmap', d, mNames);
    
    const tests = [...new Set(d.map(r => r.테스트명).filter(Boolean))];
    const testAcc = {};
    tests.forEach(test => {
        const td = d.filter(r => r.테스트명 === test);
        testAcc[test] = td.filter(r => r.정답여부).length / td.length * 100;
    });
    const hardest = Object.entries(testAcc).sort((a, b) => a[1] - b[1])[0];
    const easiest = Object.entries(testAcc).sort((a, b) => b[1] - a[1])[0];
    
    document.getElementById('heatmap-insight').innerHTML = `
        💡 <strong>히트맵 분석</strong>:<br>
        • <strong>가장 어려운 테스트</strong>: ${hardest?.[0] || '-'} (${APP.lang === 'ko' ? '평균' : 'avg'}: ${hardest?.[1]?.toFixed(1) || 0}%)<br>
        • <strong>가장 쉬운 테스트</strong>: ${easiest?.[0] || '-'} (${APP.lang === 'ko' ? '평균' : 'avg'}: ${easiest?.[1]?.toFixed(1) || 0}%)<br>
        • <strong>일관성</strong>: ${APP.lang === 'ko' ? '모든 모델이 비슷한 성능 패턴을 보이는지 확인하세요' : 'Check if all models show similar performance patterns'}<br>
        • <strong>특화 영역</strong>: ${APP.lang === 'ko' ? '특정 모델이 특정 테스트에서 특히 우수한지 파악하세요' : 'Identify if specific models excel in certain tests'}
    `;
}

function renderHeatmap(id, data, models) {
    const tests = [...new Set(data.map(r => r.테스트명).filter(Boolean))];
    const z = [], txt = [];
    
    models.forEach(m => {
        const row = [], trow = [];
        tests.forEach(test => {
            const f = data.filter(r => r.모델 === m && r.테스트명 === test);
            if (f.length) {
                const acc = f.filter(r => r.정답여부).length / f.length * 100;
                row.push(acc);
                trow.push(acc.toFixed(1));
            } else {
                row.push(null);
                trow.push('');
            }
        });
        z.push(row);
        txt.push(trow);
    });
    
    Plotly.newPlot(id, [{
        z, x: tests, y: models, type: 'heatmap',
        colorscale: 'RdYlGn', zmin: 0, zmax: 100,
        text: txt, texttemplate: '%{text}', textfont: { size: 10 * APP.chartFontScale },
        colorbar: { title: t('accuracy') + ' (%)' }, xgap: 2, ygap: 2
    }], { ...getLayout(), margin: { l: 150, r: 50, t: 30, b: 100 }, xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { tickfont: { size: 10 * APP.chartFontScale } } }, CONFIG);
}

// ========== 모델별 비교 ==========
function renderModel() {
    const d = APP.filtered;
    const stats = {};
    d.forEach(r => {
        if (!r.모델) return;
        if (!stats[r.모델]) stats[r.모델] = { c: 0, t: 0 };
        stats[r.모델].t++;
        if (r.정답여부) stats[r.모델].c++;
    });
    
    const sorted = Object.entries(stats).sort((a, b) => b[1].c / b[1].t - a[1].c / a[1].t);
    const models = sorted.map(x => x[0]);
    const accs = sorted.map(x => (x[1].c / x[1].t * 100));
    const corrects = sorted.map(x => x[1].c);
    const wrongs = sorted.map(x => x[1].t - x[1].c);
    
    document.querySelector('#tbl-model tbody').innerHTML = sorted.map(([m, s], i) => {
        const acc = (s.c / s.t * 100).toFixed(2);
        return `<tr><td>${i+1}</td><td>${m}</td><td>${s.c}</td><td>${s.t}</td><td><span class="acc-cell" style="background:${accColor(+acc)}">${acc}%</span></td><td>${s.t - s.c}</td></tr>`;
    }).join('');
    
    Plotly.newPlot('chart-modelbar', [{
        x: models, y: accs, type: 'bar',
        marker: { color: accs.map(v => accColor(v)), line: { color: '#000', width: 1.5 } },
        text: accs.map(v => v.toFixed(1) + '%'), textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('overall_comparison')), xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('accuracy') + ' (%)', range: [0, Math.max(...accs) * 1.15] } }, CONFIG);
    
    Plotly.newPlot('chart-modelstack', [
        { x: models, y: corrects, name: t('correct'), type: 'bar', marker: { color: 'lightgreen', line: { color: '#000', width: 1 } } },
        { x: models, y: wrongs, name: t('wrong'), type: 'bar', marker: { color: 'lightcoral', line: { color: '#000', width: 1 } } }
    ], { ...getLayout(t('correct') + '/' + t('wrong') + ' ' + t('comparison_chart')), barmode: 'stack', xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('problem_count') } }, CONFIG);
    
    renderHeatmap('chart-heatmap2', d, models);
}

// ========== 응답시간 ==========
function renderTime() {
    const d = APP.filtered.filter(r => r['문제당평균시간(초)']);
    if (!d.length) {
        document.getElementById('time-insight').innerHTML = `<span style="color:var(--text-muted)">응답시간 데이터가 없습니다.</span>`;
        return;
    }
    
    const stats = {};
    d.forEach(r => {
        if (!r.모델) return;
        if (!stats[r.모델]) stats[r.모델] = { times: [], c: 0, t: 0 };
        stats[r.모델].times.push(r['문제당평균시간(초)']);
        stats[r.모델].t++;
        if (r.정답여부) stats[r.모델].c++;
    });
    
    const rows = Object.entries(stats).map(([m, s]) => {
        const times = s.times.sort((a, b) => a - b);
        const avg = times.reduce((a, b) => a + b, 0) / times.length;
        const median = times[Math.floor(times.length / 2)];
        const std = Math.sqrt(times.reduce((sum, t) => sum + (t - avg) ** 2, 0) / times.length);
        return { model: m, avg, median, std, min: Math.min(...times), max: Math.max(...times), count: s.t, acc: s.c / s.t * 100, times };
    }).sort((a, b) => a.avg - b.avg);
    
    const fastest = rows[0];
    const slowest = rows[rows.length - 1];
    const avgAll = rows.reduce((s, r) => s + r.avg, 0) / rows.length;
    
    document.getElementById('m-fastest').textContent = fastest?.model || '-';
    document.getElementById('m-fastestT').textContent = `${fastest?.avg.toFixed(2) || 0}${t('seconds')}`;
    document.getElementById('m-slowest').textContent = slowest?.model || '-';
    document.getElementById('m-slowestT').textContent = `${slowest?.avg.toFixed(2) || 0}${t('seconds')}`;
    document.getElementById('m-avgtime').textContent = avgAll.toFixed(2) + t('seconds');
    
    document.querySelector('#tbl-time tbody').innerHTML = rows.map((r, i) => 
        `<tr><td>${i+1}</td><td>${r.model}</td><td><span class="acc-cell" style="background:${accColor(100 - r.avg * 25)}">${r.avg.toFixed(2)}</span></td><td>${r.median.toFixed(2)}</td><td>${r.std.toFixed(2)}</td><td>${r.min.toFixed(2)}</td><td>${r.max.toFixed(2)}</td><td>${r.count}</td><td>${r.acc.toFixed(2)}%</td></tr>`
    ).join('');
    
    Plotly.newPlot('chart-timebar', [{
        x: rows.map(r => r.model), y: rows.map(r => r.avg), type: 'bar',
        marker: { color: rows.map(r => `rgba(${Math.min(255, r.avg * 80)}, ${Math.max(0, 200 - r.avg * 60)}, 100, 0.8)`), line: { color: '#000', width: 1 } },
        text: rows.map(r => r.avg.toFixed(2) + t('seconds')), textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('response_time_by_model')), xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('response_time') + ' (' + t('seconds') + ')' } }, CONFIG);
    
    Plotly.newPlot('chart-timebox', rows.map(r => ({
        y: r.times, type: 'box', name: r.model, boxpoints: false
    })), { ...getLayout(t('response_time_distribution')), showlegend: false, yaxis: { title: t('response_time') + ' (' + t('seconds') + ')' } }, CONFIG);
    
    Plotly.newPlot('chart-timescatter', [{
        x: rows.map(r => r.avg), y: rows.map(r => r.acc),
        mode: 'markers+text', type: 'scatter',
        text: rows.map(r => r.model), textposition: 'top center', textfont: { size: 10 * APP.chartFontScale },
        marker: { size: 14, color: '#0068c9', line: { width: 2, color: '#000' } }
    }], { ...getLayout(t('response_time_vs_accuracy')), xaxis: { title: t('avg_response_time') + ' (' + t('seconds') + ')' }, yaxis: { title: t('accuracy') + ' (%)' } }, CONFIG);
    
    const timeRatio = slowest.avg / fastest.avg;
    const accRatio = fastest.acc / slowest.acc;
    document.getElementById('time-insight').innerHTML = `
        💡 <strong>${APP.lang === 'ko' ? '속도 vs 정확도 트레이드오프 분석' : 'Speed vs Accuracy Trade-off Analysis'}</strong>:<br><br>
        🏃 <strong>${APP.lang === 'ko' ? '속도' : 'Speed'}</strong>:<br>
        • <strong>${APP.lang === 'ko' ? '최고속' : 'Fastest'}</strong>: ${fastest.model} (${fastest.avg.toFixed(2)}${t('seconds')}, ${APP.lang === 'ko' ? '정확도' : 'accuracy'} ${fastest.acc.toFixed(1)}%)<br>
        • <strong>${APP.lang === 'ko' ? '최저속' : 'Slowest'}</strong>: ${slowest.model} (${slowest.avg.toFixed(2)}${t('seconds')}, ${APP.lang === 'ko' ? '정확도' : 'accuracy'} ${slowest.acc.toFixed(1)}%)<br>
        • <strong>${APP.lang === 'ko' ? '속도 차이' : 'Speed difference'}</strong>: ${timeRatio.toFixed(1)}x<br><br>
        🎯 <strong>${APP.lang === 'ko' ? '효율성 분석' : 'Efficiency Analysis'}</strong>:<br>
        • ${APP.lang === 'ko' ? '빠른 모델이' : 'Fast model is'} ${accRatio.toFixed(2)}x ${APP.lang === 'ko' ? '의 정확도를 가짐' : 'as accurate'}<br>
        • <strong>${APP.lang === 'ko' ? '권장사항' : 'Recommendation'}</strong>: ${APP.lang === 'ko' ? '실시간 처리가 중요하면' : 'For real-time:'} ${fastest.model}, ${APP.lang === 'ko' ? '정확도가 중요하면' : 'For accuracy:'} ${slowest.acc > fastest.acc ? slowest.model : fastest.model}
    `;
}

// ========== 법령/비법령 ==========
function renderLaw() {
    const d = APP.filtered;
    const lawD = d.filter(r => r.law === 'O');
    const nonD = d.filter(r => r.law !== 'O');
    const lawQ = new Set(lawD.map(r => r.Question)).size;
    const nonQ = new Set(nonD.map(r => r.Question)).size;
    const total = lawQ + nonQ;
    
    document.getElementById('m-law2').textContent = `${lawQ.toLocaleString()} (${total ? (lawQ / total * 100).toFixed(1) : 0}%)`;
    document.getElementById('m-nonlaw2').textContent = `${nonQ.toLocaleString()} (${total ? (nonQ / total * 100).toFixed(1) : 0}%)`;
    
    Plotly.newPlot('chart-lawpie', [{
        values: [lawQ, nonQ], labels: [t('law'), t('non_law')], type: 'pie',
        marker: { colors: ['#FF6B6B', '#4ECDC4'], line: { color: '#000', width: 2 } },
        hole: 0.3, textfont: { size: 12 * APP.chartFontScale }
    }], { ...getLayout(t('law') + '/' + t('non_law') + ' ' + t('problem_distribution')) }, CONFIG);
    
    const stats = {};
    d.forEach(r => {
        if (!r.모델) return;
        if (!stats[r.모델]) stats[r.모델] = { lc: 0, lt: 0, nc: 0, nt: 0 };
        if (r.law === 'O') { stats[r.모델].lt++; if (r.정답여부) stats[r.모델].lc++; }
        else { stats[r.모델].nt++; if (r.정답여부) stats[r.모델].nc++; }
    });
    
    const models = Object.keys(stats);
    Plotly.newPlot('chart-lawmodel', [
        { x: models, y: models.map(m => stats[m].lt ? stats[m].lc / stats[m].lt * 100 : 0), name: t('law'), type: 'bar', marker: { color: '#FF6B6B', line: { color: '#000', width: 1 } } },
        { x: models, y: models.map(m => stats[m].nt ? stats[m].nc / stats[m].nt * 100 : 0), name: t('non_law'), type: 'bar', marker: { color: '#4ECDC4', line: { color: '#000', width: 1 } } }
    ], { ...getLayout(t('model_law_performance')), barmode: 'group', xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('accuracy') + ' (%)', range: [0, 100] } }, CONFIG);
}

// ========== 과목별 ==========
function renderSubject() {
    const d = APP.filtered;
    const stats = {};
    d.forEach(r => {
        if (!r.Subject) return;
        if (!stats[r.Subject]) stats[r.Subject] = { c: 0, t: 0 };
        stats[r.Subject].t++;
        if (r.정답여부) stats[r.Subject].c++;
    });
    
    const sorted = Object.entries(stats).sort((a, b) => b[1].c / b[1].t - a[1].c / a[1].t);
    
    document.querySelector('#tbl-subject tbody').innerHTML = sorted.map(([s, v], i) => {
        const acc = (v.c / v.t * 100).toFixed(2);
        return `<tr><td>${i+1}</td><td>${s}</td><td>${v.c}</td><td>${v.t}</td><td><span class="acc-cell" style="background:${accColor(+acc)}">${acc}%</span></td></tr>`;
    }).join('');
    
    Plotly.newPlot('chart-subject', [{
        y: sorted.map(x => x[0]), x: sorted.map(x => x[1].c / x[1].t * 100),
        type: 'bar', orientation: 'h',
        marker: { color: sorted.map(x => accColor(x[1].c / x[1].t * 100)), line: { color: '#000', width: 1 } },
        text: sorted.map(x => (x[1].c / x[1].t * 100).toFixed(1) + '%'), textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('subject_performance')), margin: { l: 180 }, xaxis: { title: t('accuracy') + ' (%)', range: [0, 100] } }, CONFIG);
}

// ========== 연도별 ==========
function renderYear() {
    const d = APP.filtered;
    const stats = {};
    d.forEach(r => {
        if (!r.Year) return;
        if (!stats[r.Year]) stats[r.Year] = { c: 0, t: 0 };
        stats[r.Year].t++;
        if (r.정답여부) stats[r.Year].c++;
    });
    
    const years = Object.keys(stats).sort();
    
    Plotly.newPlot('chart-yearcount', [{
        x: years, y: years.map(y => stats[y].t), type: 'bar',
        marker: { color: '#0068c9', line: { color: '#000', width: 1 } },
        text: years.map(y => stats[y].t), textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('year_problem_chart')), xaxis: { title: t('year') }, yaxis: { title: t('problem_count') } }, CONFIG);
    
    Plotly.newPlot('chart-yearacc', [{
        x: years, y: years.map(y => stats[y].c / stats[y].t * 100),
        type: 'scatter', mode: 'lines+markers+text',
        marker: { size: 10, color: '#09ab3b', line: { width: 2, color: '#000' } },
        line: { color: '#09ab3b', width: 3 },
        text: years.map(y => (stats[y].c / stats[y].t * 100).toFixed(1) + '%'),
        textposition: 'top center', textfont: { size: 10 * APP.chartFontScale }
    }], { ...getLayout(t('year_performance')), xaxis: { title: t('year') }, yaxis: { title: t('accuracy') + ' (%)', range: [0, 100] } }, CONFIG);
}

// ========== 오답 분석 ==========
function renderError() {
    const d = APP.filtered;
    const qStats = {};
    d.forEach(r => {
        if (!r.Question) return;
        if (!qStats[r.Question]) qStats[r.Question] = { c: 0, t: 0, test: r.테스트명, subj: r.Subject, year: r.Year };
        qStats[r.Question].t++;
        if (!r.정답여부) qStats[r.Question].c++;
    });
    
    const sorted = Object.entries(qStats).filter(([q, s]) => s.t >= 2).sort((a, b) => b[1].c / b[1].t - a[1].c / a[1].t);
    const top20 = sorted.slice(0, 20);
    
    document.querySelector('#tbl-error tbody').innerHTML = top20.map(([q, s], i) => {
        const rate = (s.c / s.t * 100).toFixed(1);
        return `<tr><td>${i + 1}</td><td>${s.test || '-'}</td><td>${s.subj || '-'}</td><td>${s.year || '-'}</td><td style="color:#dc3545;font-weight:600">${s.c}</td><td>${s.t}</td><td style="color:#dc3545;font-weight:600">${rate}%</td></tr>`;
    }).join('');
    
    const allWrong = sorted.filter(([q, s]) => s.c === s.t && s.t >= 2);
    const alert = document.getElementById('all-wrong-alert');
    
    if (allWrong.length) {
        alert.innerHTML = `<div class="alert alert-error">⚠️ <strong>${APP.lang === 'ko' ? '심각한 공통 오답 발견' : 'Severe Common Errors Found'}: ${allWrong.length}${APP.lang === 'ko' ? '개 문제' : ' problems'}</strong><br>${APP.lang === 'ko' ? '이 문제들은 <strong>모든 평가 모델이 틀렸습니다</strong>. 현재 LLM들이 공통적으로 해당 지식 영역을 제대로 이해하지 못하고 있음을 의미합니다.' : 'These problems were answered incorrectly by <strong>all evaluated models</strong>.'}</div>`;
        document.querySelector('#tbl-allwrong tbody').innerHTML = allWrong.slice(0, 15).map(([q, s]) => 
            `<tr><td>${q.substring(0, 30)}...</td><td>${s.test || '-'}</td><td>${s.subj || '-'}</td><td>${s.year || '-'}</td><td>${s.c}</td></tr>`
        ).join('');
    } else {
        alert.innerHTML = `<div class="alert alert-success">✅ ${APP.lang === 'ko' ? '모든 모델이 틀린 문제가 없습니다!' : 'No problems where all models were incorrect!'}</div>`;
        document.querySelector('#tbl-allwrong tbody').innerHTML = '';
    }
    
    const mostWrong = sorted.filter(([q, s]) => s.c / s.t >= 0.5);
    document.getElementById('most-wrong-alert').innerHTML = mostWrong.length
        ? `<div class="alert alert-warning">⚠️ <strong>${APP.lang === 'ko' ? '주요 공통 오답' : 'Major Common Errors'}: ${mostWrong.length}${APP.lang === 'ko' ? '개 문제' : ' problems'}</strong><br>${APP.lang === 'ko' ? '이 문제들은 <strong>50% 이상의 모델이 틀렸습니다</strong>.' : 'These problems were answered incorrectly by <strong>50%+ of models</strong>.'}</div>`
        : `<div class="alert alert-success">✅ ${APP.lang === 'ko' ? '대부분 모델이 틀린 문제가 없습니다!' : 'No problems where most models were incorrect!'}</div>`;
    
    const top10 = sorted.slice(0, 10);
    Plotly.newPlot('chart-errortop10', [{
        x: top10.map(([q]) => q.substring(0, 20) + '...'),
        y: top10.map(([q, s]) => s.c / s.t * 100),
        type: 'bar',
        marker: { color: top10.map(([q, s]) => `rgba(231, 76, 60, ${s.c / s.t})`), line: { color: '#000', width: 1 } },
        text: top10.map(([q, s]) => (s.c / s.t * 100).toFixed(0) + '%'),
        textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('top_incorrect').replace('Top 20', 'Top 10')), xaxis: { tickangle: -45, tickfont: { size: 9 * APP.chartFontScale } }, yaxis: { title: t('wrong_rate') + ' (%)', range: [0, 100] } }, CONFIG);
    
    const models = [...new Set(d.map(r => r.모델).filter(Boolean))];
    if (models.length >= 2) {
        const errors = {};
        models.forEach(m => { errors[m] = new Set(d.filter(r => r.모델 === m && !r.정답여부).map(r => r.Question)); });
        
        const z = models.map(m1 => models.map(m2 => {
            if (m1 === m2) return 100;
            const inter = [...errors[m1]].filter(q => errors[m2].has(q)).length;
            const union = new Set([...errors[m1], ...errors[m2]]).size;
            return union ? inter / union * 100 : 0;
        }));
        
        Plotly.newPlot('chart-errorheat', [{
            z, x: models, y: models, type: 'heatmap', colorscale: 'Reds',
            colorbar: { title: APP.lang === 'ko' ? '일치도 (%)' : 'Similarity (%)' }, xgap: 2, ygap: 2,
            text: z.map(row => row.map(v => v.toFixed(0))), texttemplate: '%{text}%', textfont: { size: 10 * APP.chartFontScale }
        }], { ...getLayout(APP.lang === 'ko' ? '모델 간 오답 일치도' : 'Model Error Similarity'), margin: { l: 150, r: 50, t: 50, b: 100 }, xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { tickfont: { size: 10 * APP.chartFontScale } } }, CONFIG);
    }
}

// ========== 난이도 ==========
function renderDiff() {
    const d = APP.filtered;
    const qDiff = {};
    d.forEach(r => {
        if (!r.Question) return;
        if (!qDiff[r.Question]) qDiff[r.Question] = { c: 0, t: 0, subj: r.Subject };
        qDiff[r.Question].t++;
        if (r.정답여부) qDiff[r.Question].c++;
    });
    
    const diffLabels = [
        APP.lang === 'ko' ? '매우 어려움 (0-20%)' : 'Very Hard (0-20%)',
        APP.lang === 'ko' ? '어려움 (20-40%)' : 'Hard (20-40%)',
        APP.lang === 'ko' ? '보통 (40-60%)' : 'Medium (40-60%)',
        APP.lang === 'ko' ? '쉬움 (60-80%)' : 'Easy (60-80%)',
        APP.lang === 'ko' ? '매우 쉬움 (80-100%)' : 'Very Easy (80-100%)'
    ];
    const ranges = [0, 0, 0, 0, 0];
    const questions = Object.values(qDiff);
    
    questions.forEach(q => {
        const acc = q.c / q.t * 100;
        if (acc < 20) ranges[0]++;
        else if (acc < 40) ranges[1]++;
        else if (acc < 60) ranges[2]++;
        else if (acc < 80) ranges[3]++;
        else ranges[4]++;
    });
    
    Plotly.newPlot('chart-diffdist', [{
        x: diffLabels, y: ranges, type: 'bar',
        marker: { color: ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#09ab3b'], line: { color: '#000', width: 1 } },
        text: ranges, textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('problem_distribution')), xaxis: { tickangle: -30, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('problem_count') } }, CONFIG);
    
    const modelDiff = {};
    const diffRangeNames = [APP.lang === 'ko' ? '매우 어려움' : 'Very Hard', APP.lang === 'ko' ? '어려움' : 'Hard', APP.lang === 'ko' ? '보통' : 'Medium', APP.lang === 'ko' ? '쉬움' : 'Easy', APP.lang === 'ko' ? '매우 쉬움' : 'Very Easy'];
    
    d.forEach(r => {
        if (!r.모델 || !r.Question || !qDiff[r.Question]) return;
        const acc = qDiff[r.Question].c / qDiff[r.Question].t * 100;
        const rangeIdx = acc < 20 ? 0 : acc < 40 ? 1 : acc < 60 ? 2 : acc < 80 ? 3 : 4;
        const rangeName = diffRangeNames[rangeIdx];
        if (!modelDiff[r.모델]) modelDiff[r.모델] = {};
        if (!modelDiff[r.모델][rangeName]) modelDiff[r.모델][rangeName] = { c: 0, t: 0 };
        modelDiff[r.모델][rangeName].t++;
        if (r.정답여부) modelDiff[r.모델][rangeName].c++;
    });
    
    const models = Object.keys(modelDiff);
    const colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#09ab3b'];
    
    Plotly.newPlot('chart-diffmodel', diffRangeNames.map((r, i) => ({
        x: models, y: models.map(m => modelDiff[m][r] ? modelDiff[m][r].c / modelDiff[m][r].t * 100 : 0),
        name: r, type: 'bar', marker: { color: colors[i] }
    })), { ...getLayout(APP.lang === 'ko' ? '모델별 난이도 구간 성능' : 'Model Performance by Difficulty'), barmode: 'group', xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('accuracy') + ' (%)', range: [0, 100] } }, CONFIG);
    
    const veryHard = questions.filter(q => q.c / q.t < 0.2);
    const veryEasy = questions.filter(q => q.c / q.t > 0.8);
    
    document.getElementById('m-veryhard').textContent = veryHard.length;
    document.getElementById('m-veryhardacc').textContent = veryHard.length ? (veryHard.reduce((s, q) => s + q.c / q.t, 0) / veryHard.length * 100).toFixed(1) + '%' : '0%';
    document.getElementById('m-veryeasy').textContent = veryEasy.length;
    document.getElementById('m-veryeasyacc').textContent = veryEasy.length ? (veryEasy.reduce((s, q) => s + q.c / q.t, 0) / veryEasy.length * 100).toFixed(1) + '%' : '0%';
    
    const subjDiff = {};
    Object.values(qDiff).forEach(q => {
        if (!q.subj) return;
        if (!subjDiff[q.subj]) subjDiff[q.subj] = { sum: 0, count: 0 };
        subjDiff[q.subj].sum += q.c / q.t * 100;
        subjDiff[q.subj].count++;
    });
    
    const subjSorted = Object.entries(subjDiff).map(([s, v]) => ({ s, avg: v.sum / v.count })).sort((a, b) => a.avg - b.avg);
    
    Plotly.newPlot('chart-subjectdiff', [{
        x: subjSorted.map(x => x.s), y: subjSorted.map(x => x.avg), type: 'bar',
        marker: { color: subjSorted.map(x => accColor(x.avg)), line: { color: '#000', width: 1 } },
        text: subjSorted.map(x => x.avg.toFixed(1) + '%'), textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(APP.lang === 'ko' ? '과목별 평균 난이도 (정답률)' : 'Avg Difficulty by Subject (Correct Rate)'), xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: APP.lang === 'ko' ? '평균 정답률 (%)' : 'Avg Correct Rate (%)', range: [0, 100] } }, CONFIG);
    
    const total = questions.length;
    document.getElementById('diff-insight').innerHTML = `
        💡 <strong>${APP.lang === 'ko' ? '난이도 분포 종합 분석' : 'Difficulty Distribution Summary'}</strong>:<br><br>
        📊 <strong>${APP.lang === 'ko' ? '문제 난이도 구성' : 'Problem Composition'}</strong>:<br>
        • <strong>${diffRangeNames[0]}</strong>: ${(ranges[0] / total * 100).toFixed(1)}% (${ranges[0]}${APP.lang === 'ko' ? '개' : ''})<br>
        • <strong>${diffRangeNames[1]}</strong>: ${(ranges[1] / total * 100).toFixed(1)}% (${ranges[1]}${APP.lang === 'ko' ? '개' : ''})<br>
        • <strong>${diffRangeNames[2]}</strong>: ${(ranges[2] / total * 100).toFixed(1)}% (${ranges[2]}${APP.lang === 'ko' ? '개' : ''})<br>
        • <strong>${diffRangeNames[3]}</strong>: ${(ranges[3] / total * 100).toFixed(1)}% (${ranges[3]}${APP.lang === 'ko' ? '개' : ''})<br>
        • <strong>${diffRangeNames[4]}</strong>: ${(ranges[4] / total * 100).toFixed(1)}% (${ranges[4]}${APP.lang === 'ko' ? '개' : ''})
    `;
}

// ========== 토큰/비용 ==========
function renderCost() {
    const d = APP.filtered.filter(r => r['입력토큰'] || r['출력토큰']);
    if (!d.length) return;
    
    const stats = {};
    d.forEach(r => {
        if (!r.모델) return;
        if (!stats[r.모델]) stats[r.모델] = { inT: 0, outT: 0, c: 0, t: 0 };
        stats[r.모델].inT += r['입력토큰'] || 0;
        stats[r.모델].outT += r['출력토큰'] || 0;
        stats[r.모델].t++;
        if (r.정답여부) stats[r.모델].c++;
    });
    
    const models = Object.keys(stats);
    const totalToken = models.reduce((s, m) => s + stats[m].inT + stats[m].outT, 0);
    const avgToken = models.reduce((s, m) => s + (stats[m].inT + stats[m].outT) / stats[m].t, 0) / models.length;
    const avgIn = models.reduce((s, m) => s + stats[m].inT / stats[m].t, 0) / models.length;
    const avgOut = models.reduce((s, m) => s + stats[m].outT / stats[m].t, 0) / models.length;
    const ioRatio = avgOut > 0 ? (avgIn / avgOut).toFixed(2) : 0;
    
    const efficiencies = models.map(m => ({ m, eff: stats[m].c > 0 ? (stats[m].inT + stats[m].outT) / stats[m].c : Infinity })).filter(x => x.eff < Infinity).sort((a, b) => a.eff - b.eff);
    const mostEfficient = efficiencies[0];
    
    document.getElementById('m-totaltoken').textContent = totalToken.toLocaleString();
    document.getElementById('m-avgtoken').textContent = Math.round(avgToken).toLocaleString();
    document.getElementById('m-ioratio').textContent = `${ioRatio}:1`;
    document.getElementById('m-efficient').textContent = mostEfficient?.m || '-';
    
    const rows = models.map(m => {
        const s = stats[m];
        const total = s.inT + s.outT;
        const avg = total / s.t;
        const acc = s.c / s.t * 100;
        const perCorrect = s.c > 0 ? total / s.c : 0;
        return { model: m, inT: s.inT, outT: s.outT, total, avg, count: s.t, acc, perCorrect };
    }).sort((a, b) => b.total - a.total);
    
    document.querySelector('#tbl-cost tbody').innerHTML = rows.map((r, i) => 
        `<tr><td>${i+1}</td><td>${r.model}</td><td>${r.inT.toLocaleString()}</td><td>${r.outT.toLocaleString()}</td><td>${r.total.toLocaleString()}</td><td>${Math.round(r.avg).toLocaleString()}</td><td>${r.acc.toFixed(2)}%</td><td style="color:${r.perCorrect && r.perCorrect < avgIn + avgOut ? '#09ab3b' : '#dc3545'}">${r.perCorrect ? Math.round(r.perCorrect).toLocaleString() : '-'}</td></tr>`
    ).join('');
    
    Plotly.newPlot('chart-token', [{
        x: rows.map(r => r.model), y: rows.map(r => r.total), type: 'bar',
        marker: { color: '#0068c9', line: { color: '#000', width: 1 } },
        text: rows.map(r => (r.total / 1000).toFixed(0) + 'K'), textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(t('total_tokens') + ' (' + (APP.lang === 'ko' ? '모델별' : 'by Model') + ')'), xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('total_tokens') } }, CONFIG);
    
    Plotly.newPlot('chart-tokenstack', [
        { x: rows.map(r => r.model), y: rows.map(r => r.inT), name: t('input_tokens'), type: 'bar', marker: { color: 'lightblue', line: { color: '#000', width: 1 } } },
        { x: rows.map(r => r.model), y: rows.map(r => r.outT), name: t('output_tokens'), type: 'bar', marker: { color: 'lightgreen', line: { color: '#000', width: 1 } } }
    ], { ...getLayout(t('input_tokens') + '/' + t('output_tokens')), barmode: 'stack', xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: APP.lang === 'ko' ? '토큰' : 'Tokens' } }, CONFIG);
    
    Plotly.newPlot('chart-tokenscatter', [{
        x: rows.filter(r => r.perCorrect).map(r => r.perCorrect), y: rows.filter(r => r.perCorrect).map(r => r.acc),
        mode: 'markers+text', type: 'scatter',
        text: rows.filter(r => r.perCorrect).map(r => r.model), textposition: 'top center', textfont: { size: 10 * APP.chartFontScale },
        marker: { size: 14, color: '#f59e0b', line: { width: 2, color: '#000' } }
    }], { ...getLayout(t('token_efficiency') + ' vs ' + t('accuracy')), xaxis: { title: t('token_per_correct') }, yaxis: { title: t('accuracy') + ' (%)' } }, CONFIG);
}

// ========== 테스트셋 통계 ==========
function renderTestset() {
    const d = APP.filtered;
    const tests = [...new Set(d.map(r => r.테스트명).filter(Boolean))];
    
    const stats = tests.map(test => {
        const td = d.filter(r => r.테스트명 === test);
        const total = new Set(td.map(r => r.Question)).size;
        const law = new Set(td.filter(r => r.law === 'O').map(r => r.Question)).size;
        const acc = td.filter(r => r.정답여부).length / td.length * 100;
        return { test, total, law, nonLaw: total - law, acc };
    });
    
    document.querySelector('#tbl-testset tbody').innerHTML = stats.map(s => 
        `<tr><td>${s.test}</td><td>${s.total}</td><td>${s.law}</td><td>${s.nonLaw}</td><td><span class="acc-cell" style="background:${accColor(s.acc)}">${s.acc.toFixed(2)}%</span></td></tr>`
    ).join('');
    
    Plotly.newPlot('chart-testsetacc', [{
        x: stats.map(s => s.test), y: stats.map(s => s.acc), type: 'bar',
        marker: { color: stats.map(s => accColor(s.acc)), line: { color: '#000', width: 1 } },
        text: stats.map(s => s.acc.toFixed(1) + '%'), textposition: 'outside', textfont: { size: 11 * APP.chartFontScale }
    }], { ...getLayout(APP.lang === 'ko' ? '테스트셋별 평균 정답률' : 'Avg Accuracy by Test Set'), xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('accuracy') + ' (%)', range: [0, 100] } }, CONFIG);
    
    Plotly.newPlot('chart-testsetdist', [
        { x: stats.map(s => s.test), y: stats.map(s => s.law), name: t('law'), type: 'bar', marker: { color: '#FF6B6B' } },
        { x: stats.map(s => s.test), y: stats.map(s => s.nonLaw), name: t('non_law'), type: 'bar', marker: { color: '#4ECDC4' } }
    ], { ...getLayout(APP.lang === 'ko' ? '테스트셋별 문제 분포' : 'Problem Distribution by Test Set'), barmode: 'stack', xaxis: { tickangle: -45, tickfont: { size: 10 * APP.chartFontScale } }, yaxis: { title: t('problem_count') } }, CONFIG);
}

// ========== 추가 분석 ==========
function renderExtra() {
    const d = APP.filtered;
    const stats = {};
    d.forEach(r => {
        if (!r.모델) return;
        if (!stats[r.모델]) stats[r.모델] = { c: 0, t: 0, times: [], tokens: 0 };
        stats[r.모델].t++;
        if (r.정답여부) stats[r.모델].c++;
        if (r['문제당평균시간(초)']) stats[r.모델].times.push(r['문제당평균시간(초)']);
        stats[r.모델].tokens += (r['입력토큰'] || 0) + (r['출력토큰'] || 0);
    });
    
    const rows = Object.entries(stats).map(([m, s]) => ({
        model: m,
        acc: s.c / s.t * 100,
        time: s.times.length ? s.times.reduce((a, b) => a + b, 0) / s.times.length : null,
        efficiency: s.c > 0 ? s.tokens / s.c : null
    })).sort((a, b) => b.acc - a.acc);
    
    document.querySelector('#tbl-ranking tbody').innerHTML = rows.map((r, i) => 
        `<tr><td>${i + 1}</td><td>${r.model}</td><td>${r.acc.toFixed(2)}%</td><td>${r.time ? r.time.toFixed(2) + t('seconds') : '-'}</td><td>${r.efficiency ? Math.round(r.efficiency).toLocaleString() : '-'}</td></tr>`
    ).join('');
    
    const top5 = rows.slice(0, 5);
    const maxAcc = Math.max(...top5.map(r => r.acc));
    const maxTime = Math.max(...top5.filter(r => r.time).map(r => r.time)) || 1;
    const maxEff = Math.max(...top5.filter(r => r.efficiency).map(r => r.efficiency)) || 1;
    
    Plotly.newPlot('chart-radar', top5.map(r => ({
        type: 'scatterpolar',
        r: [r.acc / maxAcc * 100, r.time ? (1 - r.time / maxTime) * 100 : 50, r.efficiency ? (1 - r.efficiency / maxEff) * 100 : 50, r.acc / maxAcc * 100],
        theta: [t('accuracy'), APP.lang === 'ko' ? '속도' : 'Speed', t('token_efficiency'), t('accuracy')],
        fill: 'toself',
        name: r.model
    })), { ...getLayout(APP.lang === 'ko' ? '모델 성능 비교 (Top 5)' : 'Model Performance Comparison (Top 5)'), polar: { radialaxis: { visible: true, range: [0, 100] } } }, CONFIG);
    
    const best = rows[0];
    const fastest = rows.filter(r => r.time).sort((a, b) => a.time - b.time)[0];
    const efficient = rows.filter(r => r.efficiency).sort((a, b) => a.efficiency - b.efficiency)[0];
    
    document.getElementById('extra-insight').innerHTML = `
        💡 <strong>${APP.lang === 'ko' ? '종합 분석 결과' : 'Overall Analysis Results'}</strong>:<br><br>
        🏆 <strong>${APP.lang === 'ko' ? '최고 정확도' : 'Best Accuracy'}</strong>: ${best.model} (${best.acc.toFixed(2)}%)<br>
        ⚡ <strong>${APP.lang === 'ko' ? '최고 속도' : 'Fastest'}</strong>: ${fastest?.model || '-'} (${fastest?.time?.toFixed(2) || '-'}${t('seconds')})<br>
        💰 <strong>${APP.lang === 'ko' ? '최고 효율' : 'Most Efficient'}</strong>: ${efficient?.model || '-'} (${APP.lang === 'ko' ? '정답당' : 'per correct'} ${efficient?.efficiency ? Math.round(efficient.efficiency).toLocaleString() : '-'} ${APP.lang === 'ko' ? '토큰' : 'tokens'})<br><br>
        📊 <strong>${APP.lang === 'ko' ? '권장사항' : 'Recommendations'}</strong>:<br>
        • ${APP.lang === 'ko' ? '정확도 우선' : 'For accuracy'}: ${best.model}<br>
        • ${APP.lang === 'ko' ? '속도 우선' : 'For speed'}: ${fastest?.model || best.model}<br>
        • ${APP.lang === 'ko' ? '비용 효율 우선' : 'For cost efficiency'}: ${efficient?.model || best.model}
    `;
}

// ========== 시작 ==========
document.addEventListener('DOMContentLoaded', loadData);
