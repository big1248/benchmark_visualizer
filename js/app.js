/**
 * LLM Benchmark Visualizer - HTML/JS Version
 * 데이터 로딩, 필터링, 차트 생성을 담당하는 메인 스크립트
 */

// ============================================================
// 전역 상태
// ============================================================
const APP = {
    data: [],           // 전체 데이터
    filtered: [],       // 필터링된 데이터
    lang: 'ko',         // 현재 언어
    loading: true,      // 로딩 상태
    filters: {
        test: 'all',
        model: 'all',
        detail: 'all',
        prompting: 'all',
        problemType: 'all',
        law: 'all'
    }
};

// 다국어 지원
const I18N = {
    ko: {
        filters: '필터 옵션',
        testname: '테스트명',
        model: '모델',
        detail_type: '상세도',
        prompting: '프롬프팅',
        problem_type: '문제 유형',
        law_type: '법령 구분',
        current_data: '현재 표시 중인 데이터',
        problems: '개 문제',
        total_problems: '총 문제 수',
        accuracy: '평균 정확도',
        overview: '전체 요약',
        model_comparison: '모델별 비교',
        response_time_analysis: '응답시간 분석',
        law_analysis: '법령/비법령 분석',
        subject_analysis: '과목별 분석',
        year_analysis: '연도별 분석',
        incorrect_analysis: '오답 분석',
        difficulty_analysis: '난이도 분석',
        token_cost_analysis: '토큰/비용 분석',
        all: '전체',
        law: '법령',
        non_law: '비법령',
        text_only: '텍스트만',
        image_problem: '이미지 포함'
    },
    en: {
        filters: 'Filter Options',
        testname: 'Test Name',
        model: 'Model',
        detail_type: 'Detail Type',
        prompting: 'Prompting',
        problem_type: 'Problem Type',
        law_type: 'Law Type',
        current_data: 'Currently displayed',
        problems: ' problems',
        total_problems: 'Total Problems',
        accuracy: 'Avg Accuracy',
        overview: 'Overview',
        model_comparison: 'Model Comparison',
        response_time_analysis: 'Response Time',
        law_analysis: 'Law Analysis',
        subject_analysis: 'Subject Analysis',
        year_analysis: 'Year Analysis',
        incorrect_analysis: 'Error Analysis',
        difficulty_analysis: 'Difficulty',
        token_cost_analysis: 'Token & Cost',
        all: 'All',
        law: 'Law',
        non_law: 'Non-Law',
        text_only: 'Text Only',
        image_problem: 'With Image'
    }
};

// Plotly 기본 레이아웃
const PLOTLY_LAYOUT = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { color: '#e2e8f0', size: 12 },
    margin: { l: 60, r: 30, t: 50, b: 60 },
    xaxis: { gridcolor: 'rgba(255,255,255,0.1)', zerolinecolor: 'rgba(255,255,255,0.2)' },
    yaxis: { gridcolor: 'rgba(255,255,255,0.1)', zerolinecolor: 'rgba(255,255,255,0.2)' }
};

const PLOTLY_CONFIG = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'],
    displaylogo: false
};

// ============================================================
// 데이터 로딩
// ============================================================

async function loadData() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    const loadingProgress = document.getElementById('loadingProgress');
    const loadingPercent = document.getElementById('loadingPercent');
    
    try {
        // GitHub Releases에서 데이터 다운로드
        const repo = "big1248/benchmark_visualizer";
        const tag = "v2.2.0";
        const url = `https://github.com/${repo}/releases/download/${tag}/data.zip`;
        
        loadingText.textContent = 'GitHub에서 데이터 다운로드 중...';
        
        // CORS 프록시 사용 (필요시)
        const proxyUrl = `https://corsproxy.io/?${encodeURIComponent(url)}`;
        
        let response;
        try {
            response = await fetch(url);
            if (!response.ok) throw new Error('Direct fetch failed');
        } catch (e) {
            // CORS 프록시 시도
            loadingText.textContent = '프록시를 통해 다운로드 중...';
            response = await fetch(proxyUrl);
        }
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        // 다운로드 진행률 표시
        const contentLength = response.headers.get('content-length');
        const total = parseInt(contentLength, 10) || 0;
        let loaded = 0;
        
        const reader = response.body.getReader();
        const chunks = [];
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            chunks.push(value);
            loaded += value.length;
            
            if (total > 0) {
                const percent = Math.round((loaded / total) * 100);
                loadingProgress.style.width = `${percent}%`;
                loadingPercent.textContent = `${percent}%`;
            }
        }
        
        // ZIP 파일 처리
        loadingText.textContent = 'ZIP 파일 압축 해제 중...';
        loadingProgress.style.width = '100%';
        
        const blob = new Blob(chunks);
        const zip = await JSZip.loadAsync(blob);
        
        // CSV 파일 파싱
        loadingText.textContent = 'CSV 파일 파싱 중...';
        const csvFiles = Object.keys(zip.files).filter(name => name.endsWith('.csv'));
        
        let processedFiles = 0;
        const allData = [];
        
        for (const filename of csvFiles) {
            const content = await zip.files[filename].async('text');
            
            // 파일명에서 정보 추출
            const fileInfo = parseFilename(filename);
            
            // CSV 파싱
            const parsed = Papa.parse(content, {
                header: true,
                skipEmptyLines: true,
                dynamicTyping: true
            });
            
            // 각 행에 파일 정보 추가
            parsed.data.forEach(row => {
                if (row.Question || row.ID) {
                    row._model = fileInfo.model;
                    row._detail = fileInfo.detail;
                    row._prompting = fileInfo.prompting;
                    row._testname = fileInfo.testname;
                    
                    // 컬럼명 정규화
                    row.모델 = row.모델명 || fileInfo.model;
                    row.테스트명 = row['Test Name'] || fileInfo.testname;
                    row.정답여부 = row.정답여부 === true || row.정답여부 === 'True' || row.정답여부 === 1;
                    
                    allData.push(row);
                }
            });
            
            processedFiles++;
            const percent = Math.round((processedFiles / csvFiles.length) * 100);
            loadingProgress.style.width = `${percent}%`;
            loadingPercent.textContent = `파일 처리: ${processedFiles}/${csvFiles.length}`;
        }
        
        APP.data = allData;
        APP.filtered = [...allData];
        
        // UI 초기화
        initializeFilters();
        applyFilters();
        
        // 로딩 완료
        loadingOverlay.classList.add('hidden');
        APP.loading = false;
        
        document.getElementById('dataStatus').textContent = 
            `✅ ${allData.length.toLocaleString()}개 데이터 로드됨`;
        
    } catch (error) {
        console.error('데이터 로딩 실패:', error);
        loadingText.textContent = `❌ 오류: ${error.message}`;
        loadingPercent.textContent = '데이터 로딩에 실패했습니다. 페이지를 새로고침해주세요.';
        
        // 샘플 데이터로 대체 (개발용)
        loadSampleData();
    }
}

// 파일명에서 정보 추출
function parseFilename(filename) {
    // 예: Claude-3-5-Haiku_detailed_no_prompting_방재안전직.csv
    const name = filename.replace('data/', '').replace('.csv', '');
    const parts = name.split('_');
    
    return {
        model: parts[0] || 'Unknown',
        detail: parts[1] || 'unknown',
        prompting: parts[2] || 'unknown',
        testname: parts.slice(3).join('_') || 'Unknown'
    };
}

// 샘플 데이터 로드 (개발/테스트용)
function loadSampleData() {
    console.log('샘플 데이터로 대체...');
    
    // 기본 샘플 데이터 생성
    const models = ['GPT-4o', 'Claude-3.5-Sonnet', 'Gemini-Pro', 'Llama-3.1-70b'];
    const tests = ['방재안전직', '건설안전기사', '소방설비기사', '산업안전기사'];
    const subjects = ['안전관리론', '재난관리론', '도시계획', '소방학'];
    
    const sampleData = [];
    
    for (const model of models) {
        for (const test of tests) {
            for (let i = 0; i < 50; i++) {
                sampleData.push({
                    ID: sampleData.length + 1,
                    모델: model,
                    테스트명: test,
                    Year: 2020 + Math.floor(Math.random() * 5),
                    Subject: subjects[Math.floor(Math.random() * subjects.length)],
                    Question: `Sample Question ${i + 1}`,
                    정답여부: Math.random() > 0.35,
                    law: Math.random() > 0.5 ? 'O' : '',
                    image: Math.random() > 0.8 ? 'image' : 'text_only',
                    '문제당평균시간(초)': Math.random() * 5 + 0.5,
                    '입력토큰': Math.floor(Math.random() * 500) + 100,
                    '출력토큰': Math.floor(Math.random() * 100) + 10,
                    '비용($)': Math.random() * 0.01,
                    _detail: 'detailed',
                    _prompting: 'no_prompting'
                });
            }
        }
    }
    
    APP.data = sampleData;
    APP.filtered = [...sampleData];
    
    initializeFilters();
    applyFilters();
    
    document.getElementById('loadingOverlay').classList.add('hidden');
    APP.loading = false;
    document.getElementById('dataStatus').textContent = '⚠️ 샘플 데이터 사용 중';
}

// ============================================================
// 필터링
// ============================================================

function initializeFilters() {
    const data = APP.data;
    
    // 고유값 추출
    const tests = [...new Set(data.map(d => d.테스트명).filter(Boolean))].sort();
    const models = [...new Set(data.map(d => d.모델).filter(Boolean))].sort();
    const details = [...new Set(data.map(d => d._detail).filter(Boolean))].sort();
    const promptings = [...new Set(data.map(d => d._prompting).filter(Boolean))].sort();
    
    // 필터 옵션 채우기
    fillSelect('filterTest', tests);
    fillSelect('filterModel', models);
    fillSelect('filterDetail', details);
    fillSelect('filterPrompting', promptings);
    
    // 이벤트 리스너 등록
    document.getElementById('filterTest').addEventListener('change', applyFilters);
    document.getElementById('filterModel').addEventListener('change', applyFilters);
    document.getElementById('filterDetail').addEventListener('change', applyFilters);
    document.getElementById('filterPrompting').addEventListener('change', applyFilters);
    document.getElementById('filterProblemType').addEventListener('change', applyFilters);
    document.getElementById('filterLaw').addEventListener('change', applyFilters);
    
    // 필터 초기화 버튼
    document.getElementById('resetFilters').addEventListener('click', resetFilters);
}

function fillSelect(id, options) {
    const select = document.getElementById(id);
    const currentValue = select.value;
    
    // 기존 옵션 유지 (전체)
    while (select.options.length > 1) {
        select.remove(1);
    }
    
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt;
        option.textContent = opt;
        select.appendChild(option);
    });
    
    select.value = currentValue;
}

function applyFilters() {
    const testFilter = document.getElementById('filterTest').value;
    const modelFilter = document.getElementById('filterModel').value;
    const detailFilter = document.getElementById('filterDetail').value;
    const promptingFilter = document.getElementById('filterPrompting').value;
    const problemTypeFilter = document.getElementById('filterProblemType').value;
    const lawFilter = document.getElementById('filterLaw').value;
    
    APP.filtered = APP.data.filter(row => {
        if (testFilter !== 'all' && row.테스트명 !== testFilter) return false;
        if (modelFilter !== 'all' && row.모델 !== modelFilter) return false;
        if (detailFilter !== 'all' && row._detail !== detailFilter) return false;
        if (promptingFilter !== 'all' && row._prompting !== promptingFilter) return false;
        
        if (problemTypeFilter !== 'all') {
            const isImage = row.image && row.image !== 'text_only';
            if (problemTypeFilter === 'text_only' && isImage) return false;
            if (problemTypeFilter === 'image' && !isImage) return false;
        }
        
        if (lawFilter !== 'all') {
            const isLaw = row.law === 'O';
            if (lawFilter === 'O' && !isLaw) return false;
            if (lawFilter === 'X' && isLaw) return false;
        }
        
        return true;
    });
    
    // 필터링된 데이터 수 업데이트
    document.getElementById('filteredCount').textContent = APP.filtered.length.toLocaleString();
    
    // 차트 업데이트
    updateAllCharts();
}

function resetFilters() {
    document.getElementById('filterTest').value = 'all';
    document.getElementById('filterModel').value = 'all';
    document.getElementById('filterDetail').value = 'all';
    document.getElementById('filterPrompting').value = 'all';
    document.getElementById('filterProblemType').value = 'all';
    document.getElementById('filterLaw').value = 'all';
    
    applyFilters();
}

// ============================================================
// 탭 관리
// ============================================================

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.dataset.tab;
            
            // 모든 탭 버튼 비활성화
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // 모든 탭 패널 숨기기
            document.querySelectorAll('.tab-panel').forEach(panel => {
                panel.classList.add('hidden');
            });
            
            // 선택된 탭 패널 표시
            document.getElementById(`tab-${tabId}`).classList.remove('hidden');
            
            // 해당 탭의 차트 업데이트
            updateTabCharts(tabId);
        });
    });
}

function updateTabCharts(tabId) {
    switch (tabId) {
        case 'overview':
            updateOverviewCharts();
            break;
        case 'model':
            updateModelCharts();
            break;
        case 'response':
            updateResponseCharts();
            break;
        case 'law':
            updateLawCharts();
            break;
        case 'subject':
            updateSubjectCharts();
            break;
        case 'year':
            updateYearCharts();
            break;
        case 'incorrect':
            updateIncorrectCharts();
            break;
        case 'difficulty':
            updateDifficultyCharts();
            break;
        case 'cost':
            updateCostCharts();
            break;
    }
}

function updateAllCharts() {
    // 메트릭 업데이트
    updateMetrics();
    
    // 현재 활성화된 탭 찾기
    const activeTab = document.querySelector('.tab-btn.active');
    if (activeTab) {
        updateTabCharts(activeTab.dataset.tab);
    }
}

// ============================================================
// 메트릭 업데이트
// ============================================================

function updateMetrics() {
    const data = APP.filtered;
    
    // 총 문제 수
    document.getElementById('metricTotal').textContent = data.length.toLocaleString();
    
    // 평균 정확도
    const correctCount = data.filter(d => d.정답여부).length;
    const accuracy = data.length > 0 ? (correctCount / data.length * 100).toFixed(1) : 0;
    document.getElementById('metricAccuracy').textContent = `${accuracy}%`;
    
    // 모델 수
    const models = new Set(data.map(d => d.모델).filter(Boolean));
    document.getElementById('metricModels').textContent = models.size;
    
    // 테스트 수
    const tests = new Set(data.map(d => d.테스트명).filter(Boolean));
    document.getElementById('metricTests').textContent = tests.size;
}

// ============================================================
// 차트: 전체 요약
// ============================================================

function updateOverviewCharts() {
    const data = APP.filtered;
    
    // 모델별 정확도
    const modelStats = {};
    data.forEach(row => {
        const model = row.모델;
        if (!model) return;
        
        if (!modelStats[model]) {
            modelStats[model] = { correct: 0, total: 0 };
        }
        modelStats[model].total++;
        if (row.정답여부) modelStats[model].correct++;
    });
    
    const modelNames = Object.keys(modelStats).sort((a, b) => {
        const accA = modelStats[a].correct / modelStats[a].total;
        const accB = modelStats[b].correct / modelStats[b].total;
        return accB - accA;
    });
    
    const modelAccuracies = modelNames.map(m => (modelStats[m].correct / modelStats[m].total * 100).toFixed(1));
    
    Plotly.newPlot('chartModelAccuracy', [{
        x: modelNames,
        y: modelAccuracies,
        type: 'bar',
        marker: {
            color: modelAccuracies.map(v => `rgba(59, 130, 246, ${0.3 + parseFloat(v) / 150})`),
            line: { color: 'rgba(59, 130, 246, 1)', width: 1 }
        },
        text: modelAccuracies.map(v => `${v}%`),
        textposition: 'outside'
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '모델별 정확도', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정확도 (%)', range: [0, 100] }
    }, PLOTLY_CONFIG);
    
    // 테스트셋별 정확도
    const testStats = {};
    data.forEach(row => {
        const test = row.테스트명;
        if (!test) return;
        
        if (!testStats[test]) {
            testStats[test] = { correct: 0, total: 0 };
        }
        testStats[test].total++;
        if (row.정답여부) testStats[test].correct++;
    });
    
    const testNames = Object.keys(testStats).sort((a, b) => {
        const accA = testStats[a].correct / testStats[a].total;
        const accB = testStats[b].correct / testStats[b].total;
        return accB - accA;
    });
    
    const testAccuracies = testNames.map(t => (testStats[t].correct / testStats[t].total * 100).toFixed(1));
    
    Plotly.newPlot('chartTestAccuracy', [{
        x: testNames,
        y: testAccuracies,
        type: 'bar',
        marker: {
            color: testAccuracies.map(v => `rgba(16, 185, 129, ${0.3 + parseFloat(v) / 150})`),
            line: { color: 'rgba(16, 185, 129, 1)', width: 1 }
        },
        text: testAccuracies.map(v => `${v}%`),
        textposition: 'outside'
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '테스트셋별 정확도', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정확도 (%)', range: [0, 100] }
    }, PLOTLY_CONFIG);
    
    // 히트맵
    updateHeatmap(data, modelNames, testNames);
}

function updateHeatmap(data, models, tests) {
    // 모델 × 테스트 정확도 매트릭스 계산
    const matrix = [];
    const annotations = [];
    
    models.forEach((model, i) => {
        const row = [];
        tests.forEach((test, j) => {
            const filtered = data.filter(d => d.모델 === model && d.테스트명 === test);
            if (filtered.length > 0) {
                const acc = (filtered.filter(d => d.정답여부).length / filtered.length * 100);
                row.push(acc);
                annotations.push({
                    x: test,
                    y: model,
                    text: acc.toFixed(1),
                    font: { color: acc > 50 ? 'white' : 'black', size: 10 },
                    showarrow: false
                });
            } else {
                row.push(null);
            }
        });
        matrix.push(row);
    });
    
    Plotly.newPlot('chartHeatmap', [{
        z: matrix,
        x: tests,
        y: models,
        type: 'heatmap',
        colorscale: 'RdYlGn',
        zmin: 0,
        zmax: 100,
        colorbar: { title: '정확도 (%)' }
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '모델 × 테스트셋 정답률 히트맵', font: { size: 16 } },
        annotations: annotations,
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        margin: { l: 150, r: 50, t: 80, b: 150 }
    }, PLOTLY_CONFIG);
}

// ============================================================
// 차트: 모델별 비교
// ============================================================

function updateModelCharts() {
    const data = APP.filtered;
    
    // 모델별 상세 통계 계산
    const modelStats = {};
    data.forEach(row => {
        const model = row.모델;
        if (!model) return;
        
        if (!modelStats[model]) {
            modelStats[model] = {
                total: 0,
                correct: 0,
                responseTime: [],
                inputTokens: [],
                outputTokens: [],
                cost: []
            };
        }
        
        modelStats[model].total++;
        if (row.정답여부) modelStats[model].correct++;
        
        if (row['문제당평균시간(초)']) modelStats[model].responseTime.push(row['문제당평균시간(초)']);
        if (row['입력토큰']) modelStats[model].inputTokens.push(row['입력토큰']);
        if (row['출력토큰']) modelStats[model].outputTokens.push(row['출력토큰']);
        if (row['비용($)']) modelStats[model].cost.push(row['비용($)']);
    });
    
    const models = Object.keys(modelStats).sort((a, b) => {
        return (modelStats[b].correct / modelStats[b].total) - (modelStats[a].correct / modelStats[a].total);
    });
    
    // 레이더 차트용 데이터
    const accuracies = models.map(m => modelStats[m].correct / modelStats[m].total * 100);
    
    // 막대 차트
    Plotly.newPlot('chartModelComparison', [{
        x: models,
        y: accuracies,
        type: 'bar',
        marker: {
            color: accuracies.map((v, i) => {
                const colors = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4'];
                return colors[i % colors.length];
            })
        },
        text: accuracies.map(v => `${v.toFixed(1)}%`),
        textposition: 'outside'
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '모델별 정확도 비교', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정확도 (%)', range: [0, Math.max(...accuracies) * 1.1] }
    }, PLOTLY_CONFIG);
    
    // 테이블 생성
    createModelStatsTable(modelStats, models);
}

function createModelStatsTable(stats, models) {
    const tableHtml = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>모델</th>
                    <th>총 문제</th>
                    <th>정답</th>
                    <th>정확도 (%)</th>
                    <th>평균 응답시간 (초)</th>
                    <th>평균 토큰</th>
                </tr>
            </thead>
            <tbody>
                ${models.map(model => {
                    const s = stats[model];
                    const acc = (s.correct / s.total * 100).toFixed(2);
                    const avgTime = s.responseTime.length > 0 
                        ? (s.responseTime.reduce((a, b) => a + b, 0) / s.responseTime.length).toFixed(2)
                        : '-';
                    const avgTokens = s.inputTokens.length > 0
                        ? Math.round((s.inputTokens.reduce((a, b) => a + b, 0) + s.outputTokens.reduce((a, b) => a + b, 0)) / s.inputTokens.length)
                        : '-';
                    
                    return `
                        <tr>
                            <td class="font-medium">${model}</td>
                            <td>${s.total.toLocaleString()}</td>
                            <td>${s.correct.toLocaleString()}</td>
                            <td class="text-blue-400 font-semibold">${acc}%</td>
                            <td>${avgTime}</td>
                            <td>${avgTokens}</td>
                        </tr>
                    `;
                }).join('')}
            </tbody>
        </table>
    `;
    
    document.getElementById('tableModelStats').innerHTML = tableHtml;
}

// ============================================================
// 차트: 응답시간 분석
// ============================================================

function updateResponseCharts() {
    const data = APP.filtered.filter(d => d['문제당평균시간(초)']);
    
    // 모델별 평균 응답시간
    const modelTimes = {};
    data.forEach(row => {
        const model = row.모델;
        if (!model) return;
        
        if (!modelTimes[model]) modelTimes[model] = [];
        modelTimes[model].push(row['문제당평균시간(초)']);
    });
    
    const models = Object.keys(modelTimes).sort((a, b) => {
        const avgA = modelTimes[a].reduce((s, v) => s + v, 0) / modelTimes[a].length;
        const avgB = modelTimes[b].reduce((s, v) => s + v, 0) / modelTimes[b].length;
        return avgA - avgB;
    });
    
    const avgTimes = models.map(m => {
        const times = modelTimes[m];
        return (times.reduce((s, v) => s + v, 0) / times.length).toFixed(2);
    });
    
    Plotly.newPlot('chartResponseTime', [{
        x: models,
        y: avgTimes,
        type: 'bar',
        marker: {
            color: avgTimes.map((v, i) => `rgba(245, 158, 11, ${0.4 + i * 0.05})`),
            line: { color: 'rgba(245, 158, 11, 1)', width: 1 }
        },
        text: avgTimes.map(v => `${v}초`),
        textposition: 'outside'
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '모델별 평균 응답시간', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '응답시간 (초)' }
    }, PLOTLY_CONFIG);
    
    // 응답시간 vs 정확도
    const scatterData = models.map(m => {
        const times = modelTimes[m];
        const avgTime = times.reduce((s, v) => s + v, 0) / times.length;
        const modelData = APP.filtered.filter(d => d.모델 === m);
        const accuracy = modelData.filter(d => d.정답여부).length / modelData.length * 100;
        return { model: m, time: avgTime, accuracy: accuracy };
    });
    
    Plotly.newPlot('chartTimeVsAccuracy', [{
        x: scatterData.map(d => d.time),
        y: scatterData.map(d => d.accuracy),
        mode: 'markers+text',
        type: 'scatter',
        text: scatterData.map(d => d.model),
        textposition: 'top center',
        marker: { size: 15, color: '#3b82f6' }
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '응답시간 vs 정확도', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, title: '평균 응답시간 (초)' },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정확도 (%)' }
    }, PLOTLY_CONFIG);
    
    // 응답시간 분포
    const allTimes = data.map(d => d['문제당평균시간(초)']);
    
    Plotly.newPlot('chartResponseDistribution', [{
        x: allTimes,
        type: 'histogram',
        nbinsx: 30,
        marker: { color: 'rgba(59, 130, 246, 0.7)' }
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '응답시간 분포', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, title: '응답시간 (초)' },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '빈도' }
    }, PLOTLY_CONFIG);
}

// ============================================================
// 차트: 법령/비법령 분석
// ============================================================

function updateLawCharts() {
    const data = APP.filtered;
    
    // 법령/비법령 분포
    const lawCount = data.filter(d => d.law === 'O').length;
    const nonLawCount = data.length - lawCount;
    
    Plotly.newPlot('chartLawDistribution', [{
        values: [lawCount, nonLawCount],
        labels: ['법령', '비법령'],
        type: 'pie',
        marker: {
            colors: ['#3b82f6', '#10b981']
        },
        textinfo: 'label+percent',
        textfont: { size: 14 }
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '법령/비법령 문제 분포', font: { size: 16 } }
    }, PLOTLY_CONFIG);
    
    // 법령/비법령 정답률
    const lawCorrect = data.filter(d => d.law === 'O' && d.정답여부).length;
    const nonLawCorrect = data.filter(d => d.law !== 'O' && d.정답여부).length;
    
    const lawAcc = lawCount > 0 ? (lawCorrect / lawCount * 100).toFixed(1) : 0;
    const nonLawAcc = nonLawCount > 0 ? (nonLawCorrect / nonLawCount * 100).toFixed(1) : 0;
    
    Plotly.newPlot('chartLawAccuracy', [{
        x: ['법령', '비법령'],
        y: [lawAcc, nonLawAcc],
        type: 'bar',
        marker: {
            color: ['#3b82f6', '#10b981']
        },
        text: [`${lawAcc}%`, `${nonLawAcc}%`],
        textposition: 'outside'
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '법령/비법령 정답률 비교', font: { size: 16 } },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정답률 (%)', range: [0, 100] }
    }, PLOTLY_CONFIG);
    
    // 모델별 법령/비법령 성능
    const modelLawStats = {};
    data.forEach(row => {
        const model = row.모델;
        if (!model) return;
        
        if (!modelLawStats[model]) {
            modelLawStats[model] = {
                lawTotal: 0, lawCorrect: 0,
                nonLawTotal: 0, nonLawCorrect: 0
            };
        }
        
        if (row.law === 'O') {
            modelLawStats[model].lawTotal++;
            if (row.정답여부) modelLawStats[model].lawCorrect++;
        } else {
            modelLawStats[model].nonLawTotal++;
            if (row.정답여부) modelLawStats[model].nonLawCorrect++;
        }
    });
    
    const models = Object.keys(modelLawStats);
    const lawAccuracies = models.map(m => {
        const s = modelLawStats[m];
        return s.lawTotal > 0 ? (s.lawCorrect / s.lawTotal * 100) : 0;
    });
    const nonLawAccuracies = models.map(m => {
        const s = modelLawStats[m];
        return s.nonLawTotal > 0 ? (s.nonLawCorrect / s.nonLawTotal * 100) : 0;
    });
    
    Plotly.newPlot('chartModelLawPerformance', [
        {
            x: models,
            y: lawAccuracies,
            name: '법령',
            type: 'bar',
            marker: { color: '#3b82f6' }
        },
        {
            x: models,
            y: nonLawAccuracies,
            name: '비법령',
            type: 'bar',
            marker: { color: '#10b981' }
        }
    ], {
        ...PLOTLY_LAYOUT,
        title: { text: '모델별 법령/비법령 성능', font: { size: 16 } },
        barmode: 'group',
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정답률 (%)', range: [0, 100] },
        legend: { x: 1, y: 1, xanchor: 'right' }
    }, PLOTLY_CONFIG);
}

// ============================================================
// 차트: 과목별 분석
// ============================================================

function updateSubjectCharts() {
    const data = APP.filtered;
    
    // 과목별 통계
    const subjectStats = {};
    data.forEach(row => {
        const subject = row.Subject;
        if (!subject) return;
        
        if (!subjectStats[subject]) {
            subjectStats[subject] = { total: 0, correct: 0 };
        }
        subjectStats[subject].total++;
        if (row.정답여부) subjectStats[subject].correct++;
    });
    
    const subjects = Object.keys(subjectStats).sort((a, b) => {
        const accA = subjectStats[a].correct / subjectStats[a].total;
        const accB = subjectStats[b].correct / subjectStats[b].total;
        return accB - accA;
    });
    
    const accuracies = subjects.map(s => (subjectStats[s].correct / subjectStats[s].total * 100).toFixed(1));
    const counts = subjects.map(s => subjectStats[s].total);
    
    Plotly.newPlot('chartSubjectAccuracy', [{
        x: subjects,
        y: accuracies,
        type: 'bar',
        marker: {
            color: accuracies.map(v => `rgba(139, 92, 246, ${0.3 + parseFloat(v) / 150})`),
            line: { color: 'rgba(139, 92, 246, 1)', width: 1 }
        },
        text: accuracies.map(v => `${v}%`),
        textposition: 'outside'
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '과목별 정답률', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정답률 (%)', range: [0, 100] }
    }, PLOTLY_CONFIG);
    
    // 테이블 생성
    const tableHtml = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>과목</th>
                    <th>문제 수</th>
                    <th>정답 수</th>
                    <th>정답률 (%)</th>
                </tr>
            </thead>
            <tbody>
                ${subjects.map((subject, i) => {
                    const s = subjectStats[subject];
                    return `
                        <tr>
                            <td class="font-medium">${subject}</td>
                            <td>${s.total.toLocaleString()}</td>
                            <td>${s.correct.toLocaleString()}</td>
                            <td class="text-purple-400 font-semibold">${accuracies[i]}%</td>
                        </tr>
                    `;
                }).join('')}
            </tbody>
        </table>
    `;
    
    document.getElementById('tableSubjectStats').innerHTML = tableHtml;
}

// ============================================================
// 차트: 연도별 분석
// ============================================================

function updateYearCharts() {
    const data = APP.filtered;
    
    // 연도별 통계
    const yearStats = {};
    data.forEach(row => {
        const year = row.Year;
        if (!year) return;
        
        if (!yearStats[year]) {
            yearStats[year] = { total: 0, correct: 0 };
        }
        yearStats[year].total++;
        if (row.정답여부) yearStats[year].correct++;
    });
    
    const years = Object.keys(yearStats).sort();
    const counts = years.map(y => yearStats[y].total);
    const accuracies = years.map(y => (yearStats[y].correct / yearStats[y].total * 100).toFixed(1));
    
    // 연도별 문제 수
    Plotly.newPlot('chartYearCount', [{
        x: years,
        y: counts,
        type: 'bar',
        marker: { color: '#3b82f6' }
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '연도별 문제 수', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, title: '연도' },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '문제 수' }
    }, PLOTLY_CONFIG);
    
    // 연도별 정답률 추이
    Plotly.newPlot('chartYearAccuracy', [{
        x: years,
        y: accuracies,
        type: 'scatter',
        mode: 'lines+markers',
        marker: { size: 10, color: '#10b981' },
        line: { color: '#10b981', width: 2 }
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '연도별 정답률 추이', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, title: '연도' },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정답률 (%)', range: [0, 100] }
    }, PLOTLY_CONFIG);
}

// ============================================================
// 차트: 오답 분석
// ============================================================

function updateIncorrectCharts() {
    const data = APP.filtered;
    
    // 문제별 오답률 계산
    const questionStats = {};
    data.forEach(row => {
        const question = row.Question;
        if (!question) return;
        
        if (!questionStats[question]) {
            questionStats[question] = {
                total: 0,
                incorrect: 0,
                testName: row.테스트명,
                subject: row.Subject,
                year: row.Year,
                models: []
            };
        }
        questionStats[question].total++;
        if (!row.정답여부) {
            questionStats[question].incorrect++;
            questionStats[question].models.push(row.모델);
        }
    });
    
    // 오답률 높은 문제 Top 20
    const sortedQuestions = Object.entries(questionStats)
        .filter(([q, s]) => s.total >= 2) // 최소 2번 이상 시도된 문제
        .sort((a, b) => (b[1].incorrect / b[1].total) - (a[1].incorrect / a[1].total))
        .slice(0, 20);
    
    const tableHtml = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>순위</th>
                    <th>테스트</th>
                    <th>과목</th>
                    <th>연도</th>
                    <th>오답 모델수</th>
                    <th>총 시도</th>
                    <th>오답률 (%)</th>
                </tr>
            </thead>
            <tbody>
                ${sortedQuestions.map(([question, stats], i) => {
                    const errorRate = (stats.incorrect / stats.total * 100).toFixed(1);
                    return `
                        <tr>
                            <td>${i + 1}</td>
                            <td>${stats.testName || '-'}</td>
                            <td>${stats.subject || '-'}</td>
                            <td>${stats.year || '-'}</td>
                            <td class="text-red-400">${stats.incorrect}</td>
                            <td>${stats.total}</td>
                            <td class="text-red-400 font-semibold">${errorRate}%</td>
                        </tr>
                    `;
                }).join('')}
            </tbody>
        </table>
    `;
    
    document.getElementById('tableTopIncorrect').innerHTML = tableHtml;
    
    // 모델 간 오답 일치도 히트맵
    updateErrorAgreementHeatmap(data);
}

function updateErrorAgreementHeatmap(data) {
    const models = [...new Set(data.map(d => d.모델).filter(Boolean))];
    
    if (models.length < 2) {
        document.getElementById('chartErrorAgreement').innerHTML = 
            '<p class="text-center text-gray-400 py-8">모델이 2개 이상 필요합니다.</p>';
        return;
    }
    
    // 모델별 오답 문제 세트
    const modelErrors = {};
    models.forEach(model => {
        modelErrors[model] = new Set(
            data.filter(d => d.모델 === model && !d.정답여부)
                .map(d => d.Question)
        );
    });
    
    // 일치도 매트릭스 계산
    const matrix = [];
    const annotations = [];
    
    models.forEach((model1, i) => {
        const row = [];
        models.forEach((model2, j) => {
            if (model1 === model2) {
                row.push(100);
                annotations.push({
                    x: model2, y: model1,
                    text: '100', font: { color: 'white', size: 10 },
                    showarrow: false
                });
            } else {
                const errors1 = modelErrors[model1];
                const errors2 = modelErrors[model2];
                const intersection = new Set([...errors1].filter(x => errors2.has(x)));
                const union = new Set([...errors1, ...errors2]);
                const agreement = union.size > 0 ? (intersection.size / union.size * 100) : 0;
                
                row.push(agreement);
                annotations.push({
                    x: model2, y: model1,
                    text: agreement.toFixed(0),
                    font: { color: agreement > 50 ? 'white' : 'black', size: 10 },
                    showarrow: false
                });
            }
        });
        matrix.push(row);
    });
    
    Plotly.newPlot('chartErrorAgreement', [{
        z: matrix,
        x: models,
        y: models,
        type: 'heatmap',
        colorscale: 'Reds',
        colorbar: { title: '일치도 (%)' }
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '모델 간 오답 일치도', font: { size: 16 } },
        annotations: annotations,
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        margin: { l: 150, r: 50, t: 80, b: 150 }
    }, PLOTLY_CONFIG);
}

// ============================================================
// 차트: 난이도 분석
// ============================================================

function updateDifficultyCharts() {
    const data = APP.filtered;
    
    // 문제별 난이도(정답률) 계산
    const questionDifficulty = {};
    data.forEach(row => {
        const question = row.Question;
        if (!question) return;
        
        if (!questionDifficulty[question]) {
            questionDifficulty[question] = { total: 0, correct: 0 };
        }
        questionDifficulty[question].total++;
        if (row.정답여부) questionDifficulty[question].correct++;
    });
    
    // 난이도 구간 분류
    const difficultyRanges = {
        '매우 어려움 (0-20%)': { min: 0, max: 20, count: 0 },
        '어려움 (20-40%)': { min: 20, max: 40, count: 0 },
        '보통 (40-60%)': { min: 40, max: 60, count: 0 },
        '쉬움 (60-80%)': { min: 60, max: 80, count: 0 },
        '매우 쉬움 (80-100%)': { min: 80, max: 100, count: 0 }
    };
    
    Object.values(questionDifficulty).forEach(q => {
        const accuracy = q.correct / q.total * 100;
        for (const [range, info] of Object.entries(difficultyRanges)) {
            if (accuracy >= info.min && accuracy < info.max) {
                info.count++;
                break;
            }
            if (accuracy === 100 && range === '매우 쉬움 (80-100%)') {
                info.count++;
            }
        }
    });
    
    const ranges = Object.keys(difficultyRanges);
    const counts = ranges.map(r => difficultyRanges[r].count);
    
    Plotly.newPlot('chartDifficultyDistribution', [{
        x: ranges,
        y: counts,
        type: 'bar',
        marker: {
            color: ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e']
        },
        text: counts,
        textposition: 'outside'
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '난이도 구간별 문제 분포', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -30 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '문제 수' }
    }, PLOTLY_CONFIG);
    
    // 모델별 난이도 구간 성능
    const modelDifficultyStats = {};
    data.forEach(row => {
        const model = row.모델;
        const question = row.Question;
        if (!model || !question || !questionDifficulty[question]) return;
        
        const accuracy = questionDifficulty[question].correct / questionDifficulty[question].total * 100;
        let range;
        if (accuracy < 20) range = '매우 어려움';
        else if (accuracy < 40) range = '어려움';
        else if (accuracy < 60) range = '보통';
        else if (accuracy < 80) range = '쉬움';
        else range = '매우 쉬움';
        
        if (!modelDifficultyStats[model]) {
            modelDifficultyStats[model] = {};
        }
        if (!modelDifficultyStats[model][range]) {
            modelDifficultyStats[model][range] = { total: 0, correct: 0 };
        }
        modelDifficultyStats[model][range].total++;
        if (row.정답여부) modelDifficultyStats[model][range].correct++;
    });
    
    const models = Object.keys(modelDifficultyStats);
    const diffRanges = ['매우 어려움', '어려움', '보통', '쉬움', '매우 쉬움'];
    const traces = diffRanges.map((range, i) => ({
        x: models,
        y: models.map(m => {
            const s = modelDifficultyStats[m][range];
            return s ? (s.correct / s.total * 100) : 0;
        }),
        name: range,
        type: 'bar',
        marker: { color: ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e'][i] }
    }));
    
    Plotly.newPlot('chartModelDifficulty', traces, {
        ...PLOTLY_LAYOUT,
        title: { text: '모델별 난이도 구간 성능', font: { size: 16 } },
        barmode: 'group',
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정답률 (%)', range: [0, 100] },
        legend: { x: 1, y: 1, xanchor: 'right' }
    }, PLOTLY_CONFIG);
}

// ============================================================
// 차트: 토큰/비용 분석
// ============================================================

function updateCostCharts() {
    const data = APP.filtered.filter(d => d['입력토큰'] || d['출력토큰']);
    
    // 모델별 토큰 사용량
    const modelTokens = {};
    data.forEach(row => {
        const model = row.모델;
        if (!model) return;
        
        if (!modelTokens[model]) {
            modelTokens[model] = { input: 0, output: 0, count: 0, cost: 0, correct: 0 };
        }
        modelTokens[model].input += row['입력토큰'] || 0;
        modelTokens[model].output += row['출력토큰'] || 0;
        modelTokens[model].cost += row['비용($)'] || 0;
        modelTokens[model].count++;
        if (row.정답여부) modelTokens[model].correct++;
    });
    
    const models = Object.keys(modelTokens);
    
    Plotly.newPlot('chartTokenUsage', [
        {
            x: models,
            y: models.map(m => Math.round(modelTokens[m].input / modelTokens[m].count)),
            name: '입력 토큰',
            type: 'bar',
            marker: { color: '#3b82f6' }
        },
        {
            x: models,
            y: models.map(m => Math.round(modelTokens[m].output / modelTokens[m].count)),
            name: '출력 토큰',
            type: 'bar',
            marker: { color: '#10b981' }
        }
    ], {
        ...PLOTLY_LAYOUT,
        title: { text: '모델별 평균 토큰 사용량', font: { size: 16 } },
        barmode: 'stack',
        xaxis: { ...PLOTLY_LAYOUT.xaxis, tickangle: -45 },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '토큰 수' },
        legend: { x: 1, y: 1, xanchor: 'right' }
    }, PLOTLY_CONFIG);
    
    // 비용 vs 정확도
    const scatterData = models.map(m => ({
        model: m,
        cost: modelTokens[m].cost / modelTokens[m].count * 1000, // 1000문제당 비용
        accuracy: modelTokens[m].correct / modelTokens[m].count * 100
    }));
    
    Plotly.newPlot('chartCostVsAccuracy', [{
        x: scatterData.map(d => d.cost),
        y: scatterData.map(d => d.accuracy),
        mode: 'markers+text',
        type: 'scatter',
        text: scatterData.map(d => d.model),
        textposition: 'top center',
        marker: { size: 15, color: '#f59e0b' }
    }], {
        ...PLOTLY_LAYOUT,
        title: { text: '비용 vs 정확도', font: { size: 16 } },
        xaxis: { ...PLOTLY_LAYOUT.xaxis, title: '1000문제당 비용 ($)' },
        yaxis: { ...PLOTLY_LAYOUT.yaxis, title: '정확도 (%)' }
    }, PLOTLY_CONFIG);
    
    // 비용 효율성 테이블
    const tableHtml = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>모델</th>
                    <th>평균 입력 토큰</th>
                    <th>평균 출력 토큰</th>
                    <th>문제당 평균 비용 ($)</th>
                    <th>정확도 (%)</th>
                    <th>비용 효율성</th>
                </tr>
            </thead>
            <tbody>
                ${models.map(model => {
                    const s = modelTokens[model];
                    const avgInput = Math.round(s.input / s.count);
                    const avgOutput = Math.round(s.output / s.count);
                    const avgCost = (s.cost / s.count).toFixed(6);
                    const accuracy = (s.correct / s.count * 100).toFixed(1);
                    const efficiency = s.cost > 0 ? (s.correct / s.cost).toFixed(0) : '-';
                    
                    return `
                        <tr>
                            <td class="font-medium">${model}</td>
                            <td>${avgInput.toLocaleString()}</td>
                            <td>${avgOutput.toLocaleString()}</td>
                            <td>$${avgCost}</td>
                            <td class="text-blue-400">${accuracy}%</td>
                            <td class="text-green-400">${efficiency}</td>
                        </tr>
                    `;
                }).join('')}
            </tbody>
        </table>
        <p class="text-sm text-gray-400 mt-2">※ 비용 효율성 = 정답 수 / 총 비용 (높을수록 좋음)</p>
    `;
    
    document.getElementById('tableCostEfficiency').innerHTML = tableHtml;
}

// ============================================================
// 언어 변경
// ============================================================

function updateLanguage(lang) {
    APP.lang = lang;
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (I18N[lang][key]) {
            el.textContent = I18N[lang][key];
        }
    });
    
    // 차트 제목 등도 업데이트 (재렌더링)
    updateAllCharts();
}

// ============================================================
// 초기화
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    // 탭 초기화
    initializeTabs();
    
    // 언어 변경 이벤트
    document.getElementById('langSelect').addEventListener('change', (e) => {
        updateLanguage(e.target.value);
    });
    
    // 데이터 로드
    loadData();
});
