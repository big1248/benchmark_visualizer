/**
 * LLM Benchmark Visualizer - Streamlit Style
 */

const APP = {
    data: [],
    filtered: [],
    lang: 'ko',
    loading: true,
    selectedTests: []
};

const PLOTLY_LAYOUT = {
    paper_bgcolor: 'white',
    plot_bgcolor: 'white',
    font: { color: '#262730', size: 12, family: 'Source Sans Pro, sans-serif' },
    margin: { l: 60, r: 30, t: 50, b: 80 },
    xaxis: { gridcolor: '#e6e9ef', zerolinecolor: '#e6e9ef', linecolor: '#e6e9ef' },
    yaxis: { gridcolor: '#e6e9ef', zerolinecolor: '#e6e9ef', linecolor: '#e6e9ef' }
};

const PLOTLY_CONFIG = { responsive: true, displayModeBar: false };
const COLORS = { primary: '#ff4b4b', blue: '#0068c9', green: '#09ab3b', orange: '#f59e0b' };

// ============================================================
// 데이터 로딩
// ============================================================

async function loadData() {
    const loadingOverlay = document.getElementById('loading');
    const loadingText = document.getElementById('loadingText');
    const loadingProgressBar = document.getElementById('progressFill');
    
    try {
        loadingText.textContent = '데이터 다운로드 중...';
        
        // 같은 사이트에서 직접 로드 (프록시 필요 없음)
        const response = await fetch('data.zip');
        if (!response.ok) throw new Error('data.zip을 찾을 수 없습니다');
        
        const reader = response.body.getReader();
        const contentLength = response.headers.get('Content-Length');
        let receivedLength = 0;
        const chunks = [];
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            receivedLength += value.length;
            if (contentLength && loadingProgressBar) {
                const progress = (receivedLength / contentLength) * 100;
                loadingProgressBar.style.width = `${progress}%`;
            }
        }
        
        loadingText.textContent = 'CSV 파일 파싱 중...';
        const blob = new Blob(chunks);
        const zip = await JSZip.loadAsync(blob);
        const csvFiles = Object.keys(zip.files).filter(name => name.endsWith('.csv'));
        
        const allData = [];
        for (const filename of csvFiles) {
            const content = await zip.files[filename].async('text');
            const fileInfo = parseFilename(filename);
            const parsed = Papa.parse(content, { header: true, skipEmptyLines: true, dynamicTyping: true });
            
            parsed.data.forEach(row => {
                if (row.Question || row.ID) {
                    row.모델 = row.모델명 || fileInfo.model;
                    row.테스트명 = row['Test Name'] || fileInfo.testname;
                    row.정답여부 = row.정답여부 === true || row.정답여부 === 'True' || row.정답여부 === 1;
                    row._detail = fileInfo.detail;
                    row._prompting = fileInfo.prompting;
                    allData.push(row);
                }
            });
        }
        
        APP.data = allData;
        APP.filtered = [...allData];
        initializeFilters();
        applyFilters();
        loadingOverlay.classList.add('hidden');
    } catch (error) {
        loadingText.textContent = `오류: ${error.message}`;
        console.error(error);
        loadSampleData();
    }
}

function parseFilename(filename) {
    const name = filename.replace('data/', '').replace('.csv', '');
    const parts = name.split('_');
    return {
        model: parts[0] || 'Unknown',
        detail: parts[1] || 'unknown',
        prompting: parts[2] || 'unknown',
        testname: parts.slice(3).join('_') || 'Unknown'
    };
}

function loadSampleData() {
    const models = ['GPT-4o', 'Claude-3.5-Sonnet', 'Qwen3-30b-a3b-2507', 'Meta-Llama-3.1-8b-Instruct', 'Claude-3.5-Haiku'];
    const tests = ['건설안전기사', '경비지도사2차'];
    const subjects = ['안전관리론', '재난관리론', '소방학', '도시계획'];
    const sampleData = [];
    
    for (const model of models) {
        for (const test of tests) {
            for (let i = 0; i < 200; i++) {
                sampleData.push({
                    ID: sampleData.length + 1, 모델: model, 테스트명: test,
                    Year: 2018 + Math.floor(Math.random() * 7),
                    Subject: subjects[Math.floor(Math.random() * subjects.length)],
                    Question: `Question ${i + 1}`,
                    정답여부: Math.random() > 0.4,
                    law: Math.random() > 0.5 ? 'O' : '',
                    '문제당평균시간(초)': Math.random() * 3 + 0.1,
                    _detail: 'detailed', _prompting: 'no_prompting'
                });
            }
        }
    }
    
    APP.data = sampleData;
    APP.filtered = [...sampleData];
    initializeFilters();
    applyFilters();
    document.getElementById('loading').classList.add('hidden');
}

// ============================================================
// 필터링
// ============================================================

function initializeFilters() {
    const tests = [...new Set(APP.data.map(d => d.테스트명).filter(Boolean))].sort();
    const models = [...new Set(APP.data.map(d => d.모델).filter(Boolean))].sort();
    const details = [...new Set(APP.data.map(d => d._detail).filter(Boolean))].sort();
    const promptings = [...new Set(APP.data.map(d => d._prompting).filter(Boolean))].sort();
    const years = [...new Set(APP.data.map(d => d.Year).filter(Boolean))].sort();
    
    // 테스트 선택
    const testAddSelect = document.getElementById('testSelect');
    if (testAddSelect) {
        testAddSelect.innerHTML = '<option value="">+ 테스트 추가</option>';
        tests.forEach(test => {
            const opt = document.createElement('option');
            opt.value = test; opt.textContent = test;
            testAddSelect.appendChild(opt);
        });
        
        testAddSelect.addEventListener('change', (e) => {
            if (e.target.value && !APP.selectedTests.includes(e.target.value)) {
                APP.selectedTests.push(e.target.value);
                renderTestTags();
                applyFilters();
            }
            e.target.value = '';
        });
    }
    
    APP.selectedTests = tests.slice(0, 2);
    renderTestTags();
    
    // 모델 선택
    fillSelect('modelSelect', models);
    
    // 상세도 선택
    fillSelect('detailSelect', details);
    
    // 프롬프팅 선택
    fillSelect('promptSelect', promptings);
    
    // 연도 선택
    fillSelect('yearSelect', years);
    
    ['modelSelect', 'detailSelect', 'promptSelect', 'yearSelect', 'typeSelect', 'lawSelect'].forEach(id => {
        document.getElementById(id)?.addEventListener('change', applyFilters);
    });
    
    document.getElementById('fontSizeSlider')?.addEventListener('input', (e) => {
        document.getElementById('fontSizeValue').textContent = parseFloat(e.target.value).toFixed(2);
    });
    document.getElementById('chartSizeSlider')?.addEventListener('input', (e) => {
        document.getElementById('chartSizeValue').textContent = parseFloat(e.target.value).toFixed(2);
    });
}

function renderTestTags() {
    const container = document.getElementById('testTags');
    container.innerHTML = '';
    APP.selectedTests.forEach(test => {
        const tag = document.createElement('div');
        tag.className = 'tag';
        tag.innerHTML = `<span>${test}</span><span class="remove" onclick="removeTestTag('${test}')">×</span>`;
        container.appendChild(tag);
    });
}

function removeTestTag(test) {
    APP.selectedTests = APP.selectedTests.filter(t => t !== test);
    renderTestTags();
    applyFilters();
}

function fillSelect(id, options) {
    const select = document.getElementById(id);
    if (!select) return;
    while (select.options.length > 1) select.remove(1);
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt; option.textContent = opt;
        select.appendChild(option);
    });
}

function applyFilters() {
    const modelFilter = document.getElementById('filterModel')?.value || 'all';
    const lawFilter = document.getElementById('filterLaw')?.value || 'all';
    
    APP.filtered = APP.data.filter(row => {
        if (APP.selectedTests.length > 0 && !APP.selectedTests.includes(row.테스트명)) return false;
        if (modelFilter !== 'all' && row.모델 !== modelFilter) return false;
        if (lawFilter !== 'all') {
            if (lawFilter === 'O' && row.law !== 'O') return false;
            if (lawFilter === 'X' && row.law === 'O') return false;
        }
        return true;
    });
    
    document.getElementById('filteredCount').textContent = APP.filtered.length.toLocaleString();
    updateAllCharts();
}

// ============================================================
// 탭 관리
// ============================================================

function initializeTabs() {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.getElementById(`tab-${tab.dataset.tab}`).classList.add('active');
            updateTabCharts(tab.dataset.tab);
        });
    });
}

function updateTabCharts(tabId) {
    const handlers = {
        overview: updateOverviewTab, model: updateModelTab, response: updateResponseTab,
        law: updateLawTab, subject: updateSubjectTab, year: updateYearTab,
        incorrect: updateIncorrectTab, difficulty: updateDifficultyTab
    };
    handlers[tabId]?.();
}

function updateAllCharts() {
    const activeTab = document.querySelector('.tab.active');
    if (activeTab) updateTabCharts(activeTab.dataset.tab);
}

function getAccuracyColor(acc) {
    if (acc >= 80) return 'rgba(9, 171, 59, 0.8)';
    if (acc >= 70) return 'rgba(46, 204, 113, 0.7)';
    if (acc >= 60) return 'rgba(133, 200, 114, 0.6)';
    if (acc >= 50) return 'rgba(241, 196, 15, 0.6)';
    return 'rgba(230, 126, 34, 0.6)';
}

// ============================================================
// 탭별 업데이트 함수
// ============================================================

function updateOverviewTab() {
    const data = APP.filtered;
    const models = [...new Set(data.map(d => d.모델).filter(Boolean))];
    const correctCount = data.filter(d => d.정답여부).length;
    
    document.getElementById('metricTotalProblems').textContent = new Set(data.map(d => d.Question)).size.toLocaleString();
    document.getElementById('metricModelCount').textContent = models.length;
    document.getElementById('metricTotalEval').textContent = data.length.toLocaleString();
    document.getElementById('metricAvgAccuracy').textContent = data.length > 0 ? (correctCount / data.length * 100).toFixed(2) + '%' : '0%';
    document.getElementById('metricAvgProblems').textContent = models.length > 0 ? Math.round(data.length / models.length).toLocaleString() : '0';
    document.getElementById('metricAvgCorrect').textContent = models.length > 0 ? Math.round(correctCount / models.length).toLocaleString() : '0';
    document.getElementById('metricAvgWrong').textContent = models.length > 0 ? Math.round((data.length - correctCount) / models.length).toLocaleString() : '0';
    
    const modelStats = {};
    data.forEach(row => {
        if (!row.모델) return;
        if (!modelStats[row.모델]) modelStats[row.모델] = { correct: 0, total: 0 };
        modelStats[row.모델].total++;
        if (row.정답여부) modelStats[row.모델].correct++;
    });
    
    const sorted = Object.entries(modelStats).sort((a, b) => (b[1].correct / b[1].total) - (a[1].correct / a[1].total));
    
    document.querySelector('#tableModelPerformance tbody').innerHTML = sorted.map(([model, stats], i) => {
        const acc = (stats.correct / stats.total * 100).toFixed(2);
        return `<tr><td>${i}</td><td>${model}</td><td>${stats.correct}</td><td>${stats.total}</td><td><span class="accuracy-cell" style="background:${getAccuracyColor(parseFloat(acc))}">${acc}%</span></td></tr>`;
    }).join('');
    
    updateHeatmap(data, sorted.map(m => m[0]));
}

function updateHeatmap(data, models) {
    const tests = [...new Set(data.map(d => d.테스트명).filter(Boolean))];
    const matrix = [], textMatrix = [];
    
    models.forEach(model => {
        const row = [], textRow = [];
        tests.forEach(test => {
            const f = data.filter(d => d.모델 === model && d.테스트명 === test);
            if (f.length > 0) {
                const acc = f.filter(d => d.정답여부).length / f.length * 100;
                row.push(acc); textRow.push(acc.toFixed(1) + '%');
            } else { row.push(null); textRow.push(''); }
        });
        matrix.push(row); textMatrix.push(textRow);
    });
    
    Plotly.newPlot('chartHeatmap', [{
        z: matrix, x: tests, y: models, type: 'heatmap',
        colorscale: [[0,'#e74c3c'],[0.5,'#f1c40f'],[1,'#09ab3b']],
        zmin: 0, zmax: 100, text: textMatrix, texttemplate: '%{text}', textfont: { size: 10 },
        colorbar: { title: '정확도 (%)' }
    }], { ...PLOTLY_LAYOUT, margin: { l: 150, r: 50, t: 30, b: 100 }, xaxis: { tickangle: -45 } }, PLOTLY_CONFIG);
}

function updateModelTab() {
    const data = APP.filtered;
    const modelStats = {};
    data.forEach(row => {
        if (!row.모델) return;
        if (!modelStats[row.모델]) modelStats[row.모델] = { correct: 0, total: 0, times: [] };
        modelStats[row.모델].total++;
        if (row.정답여부) modelStats[row.모델].correct++;
        if (row['문제당평균시간(초)']) modelStats[row.모델].times.push(row['문제당평균시간(초)']);
    });
    
    const sorted = Object.entries(modelStats).sort((a, b) => (b[1].correct / b[1].total) - (a[1].correct / a[1].total));
    const models = sorted.map(m => m[0]);
    const accs = sorted.map(m => m[1].correct / m[1].total * 100);
    
    Plotly.newPlot('chartModelComparison', [{
        x: models, y: accs, type: 'bar', marker: { color: accs.map(v => getAccuracyColor(v)) },
        text: accs.map(v => v.toFixed(1) + '%'), textposition: 'outside'
    }], { ...PLOTLY_LAYOUT, xaxis: { tickangle: -45 }, yaxis: { title: '정확도 (%)', range: [0, Math.max(...accs) * 1.15] } }, PLOTLY_CONFIG);
    
    document.querySelector('#tableModelDetail tbody').innerHTML = sorted.map(([model, stats], i) => {
        const acc = (stats.correct / stats.total * 100).toFixed(2);
        const avgTime = stats.times.length > 0 ? (stats.times.reduce((a,b)=>a+b,0) / stats.times.length).toFixed(2) + '초' : '-';
        return `<tr><td>${i}</td><td>${model}</td><td>${stats.correct}</td><td>${stats.total}</td><td><span class="accuracy-cell" style="background:${getAccuracyColor(parseFloat(acc))}">${acc}%</span></td><td>${avgTime}</td></tr>`;
    }).join('');
}

function updateResponseTab() {
    const data = APP.filtered.filter(d => d['문제당평균시간(초)']);
    const modelTimes = {};
    data.forEach(row => {
        if (!row.모델) return;
        if (!modelTimes[row.모델]) modelTimes[row.모델] = { times: [], correct: 0, total: 0 };
        modelTimes[row.모델].times.push(row['문제당평균시간(초)']);
        modelTimes[row.모델].total++;
        if (row.정답여부) modelTimes[row.모델].correct++;
    });
    
    const models = Object.keys(modelTimes);
    const avgTimes = models.map(m => modelTimes[m].times.reduce((a,b)=>a+b,0) / modelTimes[m].times.length);
    
    let fastestIdx = 0, slowestIdx = 0;
    avgTimes.forEach((t, i) => { if (t < avgTimes[fastestIdx]) fastestIdx = i; if (t > avgTimes[slowestIdx]) slowestIdx = i; });
    
    document.getElementById('metricFastestModel').textContent = models[fastestIdx] || '-';
    document.getElementById('metricFastestTime').textContent = `↑ ${avgTimes[fastestIdx]?.toFixed(2) || 0}초`;
    document.getElementById('metricSlowestModel').textContent = models[slowestIdx] || '-';
    document.getElementById('metricSlowestTime').textContent = `↑ ${avgTimes[slowestIdx]?.toFixed(2) || 0}초`;
    document.getElementById('metricAvgResponseTime').textContent = `${(avgTimes.reduce((a,b)=>a+b,0) / avgTimes.length || 0).toFixed(2)}초`;
    
    const sorted = models.map((m, i) => ({ model: m, avg: avgTimes[i], ...modelTimes[m] })).sort((a, b) => a.avg - b.avg);
    
    document.querySelector('#tableResponseTime tbody').innerHTML = sorted.map((s, i) => {
        const times = s.times.sort((a,b)=>a-b);
        const mean = s.avg, median = times[Math.floor(times.length/2)];
        const std = Math.sqrt(times.reduce((sum,t)=>sum+Math.pow(t-mean,2),0)/times.length);
        const acc = (s.correct / s.total * 100).toFixed(2);
        return `<tr><td>${i}</td><td>${s.model}</td><td><span class="accuracy-cell" style="background:${getAccuracyColor(mean*30)}">${mean.toFixed(2)}</span></td><td>${median.toFixed(2)}</td><td>${std.toFixed(2)}</td><td>${Math.min(...times).toFixed(2)}</td><td>${Math.max(...times).toFixed(2)}</td><td>${s.total}</td><td>${acc}%</td></tr>`;
    }).join('');
    
    const scatter = models.map(m => ({ x: modelTimes[m].times.reduce((a,b)=>a+b,0)/modelTimes[m].times.length, y: modelTimes[m].correct/modelTimes[m].total*100, m }));
    Plotly.newPlot('chartTimeVsAccuracy', [{ x: scatter.map(d=>d.x), y: scatter.map(d=>d.y), mode: 'markers+text', type: 'scatter', text: scatter.map(d=>d.m), textposition: 'top center', marker: { size: 12, color: COLORS.blue } }], { ...PLOTLY_LAYOUT, xaxis: { title: '평균 응답시간 (초)' }, yaxis: { title: '정확도 (%)' } }, PLOTLY_CONFIG);
}

function updateLawTab() {
    const data = APP.filtered;
    const lawCount = data.filter(d => d.law === 'O').length;
    const nonLawCount = data.length - lawCount;
    
    Plotly.newPlot('chartLawDistribution', [{ values: [lawCount, nonLawCount], labels: ['법령', '비법령'], type: 'pie', marker: { colors: [COLORS.blue, COLORS.green] } }], PLOTLY_LAYOUT, PLOTLY_CONFIG);
    
    const lawAcc = lawCount > 0 ? data.filter(d => d.law === 'O' && d.정답여부).length / lawCount * 100 : 0;
    const nonLawAcc = nonLawCount > 0 ? data.filter(d => d.law !== 'O' && d.정답여부).length / nonLawCount * 100 : 0;
    
    Plotly.newPlot('chartLawAccuracy', [{ x: ['법령', '비법령'], y: [lawAcc, nonLawAcc], type: 'bar', marker: { color: [COLORS.blue, COLORS.green] }, text: [lawAcc.toFixed(1)+'%', nonLawAcc.toFixed(1)+'%'], textposition: 'outside' }], { ...PLOTLY_LAYOUT, yaxis: { title: '정확도 (%)', range: [0, 100] } }, PLOTLY_CONFIG);
    
    const modelLaw = {};
    data.forEach(row => {
        if (!row.모델) return;
        if (!modelLaw[row.모델]) modelLaw[row.모델] = { lT: 0, lC: 0, nT: 0, nC: 0 };
        if (row.law === 'O') { modelLaw[row.모델].lT++; if (row.정답여부) modelLaw[row.모델].lC++; }
        else { modelLaw[row.모델].nT++; if (row.정답여부) modelLaw[row.모델].nC++; }
    });
    const models = Object.keys(modelLaw);
    Plotly.newPlot('chartModelLawPerformance', [
        { x: models, y: models.map(m => modelLaw[m].lT > 0 ? modelLaw[m].lC/modelLaw[m].lT*100 : 0), name: '법령', type: 'bar', marker: { color: COLORS.blue } },
        { x: models, y: models.map(m => modelLaw[m].nT > 0 ? modelLaw[m].nC/modelLaw[m].nT*100 : 0), name: '비법령', type: 'bar', marker: { color: COLORS.green } }
    ], { ...PLOTLY_LAYOUT, barmode: 'group', xaxis: { tickangle: -45 }, yaxis: { title: '정확도 (%)', range: [0, 100] } }, PLOTLY_CONFIG);
}

function updateSubjectTab() {
    const data = APP.filtered;
    const subjectStats = {};
    data.forEach(row => {
        if (!row.Subject) return;
        if (!subjectStats[row.Subject]) subjectStats[row.Subject] = { correct: 0, total: 0 };
        subjectStats[row.Subject].total++;
        if (row.정답여부) subjectStats[row.Subject].correct++;
    });
    
    const sorted = Object.entries(subjectStats).sort((a, b) => (b[1].correct/b[1].total) - (a[1].correct/a[1].total));
    
    document.querySelector('#tableSubject tbody').innerHTML = sorted.map(([subj, stats], i) => {
        const acc = (stats.correct / stats.total * 100).toFixed(2);
        return `<tr><td>${i}</td><td>${subj}</td><td>${stats.correct}</td><td>${stats.total}</td><td><span class="accuracy-cell" style="background:${getAccuracyColor(parseFloat(acc))}">${acc}%</span></td></tr>`;
    }).join('');
    
    Plotly.newPlot('chartSubjectAccuracy', [{ y: sorted.map(s=>s[0]), x: sorted.map(s=>s[1].correct/s[1].total*100), type: 'bar', orientation: 'h', marker: { color: sorted.map(s=>getAccuracyColor(s[1].correct/s[1].total*100)) } }], { ...PLOTLY_LAYOUT, margin: { l: 200 }, xaxis: { title: '정확도 (%)', range: [0, 100] } }, PLOTLY_CONFIG);
}

function updateYearTab() {
    const data = APP.filtered;
    const yearStats = {};
    data.forEach(row => {
        if (!row.Year) return;
        if (!yearStats[row.Year]) yearStats[row.Year] = { correct: 0, total: 0 };
        yearStats[row.Year].total++;
        if (row.정답여부) yearStats[row.Year].correct++;
    });
    
    const years = Object.keys(yearStats).sort();
    Plotly.newPlot('chartYearCount', [{ x: years, y: years.map(y => yearStats[y].total), type: 'bar', marker: { color: COLORS.blue } }], { ...PLOTLY_LAYOUT, xaxis: { title: '연도' }, yaxis: { title: '문제 수' } }, PLOTLY_CONFIG);
    Plotly.newPlot('chartYearAccuracy', [{ x: years, y: years.map(y => yearStats[y].correct/yearStats[y].total*100), type: 'scatter', mode: 'lines+markers', marker: { color: COLORS.green }, line: { color: COLORS.green } }], { ...PLOTLY_LAYOUT, xaxis: { title: '연도' }, yaxis: { title: '정확도 (%)', range: [0, 100] } }, PLOTLY_CONFIG);
}

function updateIncorrectTab() {
    const data = APP.filtered;
    const qStats = {};
    data.forEach(row => {
        if (!row.Question) return;
        if (!qStats[row.Question]) qStats[row.Question] = { total: 0, incorrect: 0, test: row.테스트명, subj: row.Subject, year: row.Year };
        qStats[row.Question].total++;
        if (!row.정답여부) qStats[row.Question].incorrect++;
    });
    
    const sorted = Object.entries(qStats).filter(([q,s]) => s.total >= 2).sort((a,b) => (b[1].incorrect/b[1].total) - (a[1].incorrect/a[1].total)).slice(0, 20);
    
    document.querySelector('#tableTopIncorrect tbody').innerHTML = sorted.map(([q, s], i) => {
        const rate = (s.incorrect / s.total * 100).toFixed(1);
        return `<tr><td>${i+1}</td><td>${s.test||'-'}</td><td>${s.subj||'-'}</td><td>${s.year||'-'}</td><td style="color:#e74c3c">${s.incorrect}</td><td>${s.total}</td><td style="color:#e74c3c;font-weight:600">${rate}%</td></tr>`;
    }).join('');
    
    const models = [...new Set(data.map(d => d.모델).filter(Boolean))];
    if (models.length < 2) { document.getElementById('chartErrorAgreement').innerHTML = '<p style="text-align:center;padding:2rem;color:#666">모델이 2개 이상 필요합니다.</p>'; return; }
    
    const modelErrors = {};
    models.forEach(m => { modelErrors[m] = new Set(data.filter(d => d.모델 === m && !d.정답여부).map(d => d.Question)); });
    
    const matrix = models.map(m1 => models.map(m2 => {
        if (m1 === m2) return 100;
        const inter = new Set([...modelErrors[m1]].filter(x => modelErrors[m2].has(x)));
        const union = new Set([...modelErrors[m1], ...modelErrors[m2]]);
        return union.size > 0 ? inter.size / union.size * 100 : 0;
    }));
    
    Plotly.newPlot('chartErrorAgreement', [{ z: matrix, x: models, y: models, type: 'heatmap', colorscale: 'Reds', colorbar: { title: '일치도 (%)' } }], { ...PLOTLY_LAYOUT, margin: { l: 150, r: 50, t: 30, b: 100 }, xaxis: { tickangle: -45 } }, PLOTLY_CONFIG);
}

function updateDifficultyTab() {
    const data = APP.filtered;
    const qDiff = {};
    data.forEach(row => {
        if (!row.Question) return;
        if (!qDiff[row.Question]) qDiff[row.Question] = { correct: 0, total: 0 };
        qDiff[row.Question].total++;
        if (row.정답여부) qDiff[row.Question].correct++;
    });
    
    const ranges = { '매우 어려움 (0-20%)': 0, '어려움 (20-40%)': 0, '보통 (40-60%)': 0, '쉬움 (60-80%)': 0, '매우 쉬움 (80-100%)': 0 };
    Object.values(qDiff).forEach(q => {
        const acc = q.correct / q.total * 100;
        if (acc < 20) ranges['매우 어려움 (0-20%)']++;
        else if (acc < 40) ranges['어려움 (20-40%)']++;
        else if (acc < 60) ranges['보통 (40-60%)']++;
        else if (acc < 80) ranges['쉬움 (60-80%)']++;
        else ranges['매우 쉬움 (80-100%)']++;
    });
    
    Plotly.newPlot('chartDifficultyDistribution', [{ x: Object.keys(ranges), y: Object.values(ranges), type: 'bar', marker: { color: ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#09ab3b'] } }], { ...PLOTLY_LAYOUT, xaxis: { tickangle: -30 }, yaxis: { title: '문제 수' } }, PLOTLY_CONFIG);
    
    const modelDiff = {};
    data.forEach(row => {
        if (!row.모델 || !row.Question || !qDiff[row.Question]) return;
        const acc = qDiff[row.Question].correct / qDiff[row.Question].total * 100;
        let range = acc < 20 ? '매우 어려움' : acc < 40 ? '어려움' : acc < 60 ? '보통' : acc < 80 ? '쉬움' : '매우 쉬움';
        if (!modelDiff[row.모델]) modelDiff[row.모델] = {};
        if (!modelDiff[row.모델][range]) modelDiff[row.모델][range] = { correct: 0, total: 0 };
        modelDiff[row.모델][range].total++;
        if (row.정답여부) modelDiff[row.모델][range].correct++;
    });
    
    const models = Object.keys(modelDiff);
    const diffRanges = ['매우 어려움', '어려움', '보통', '쉬움', '매우 쉬움'];
    const colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#09ab3b'];
    
    Plotly.newPlot('chartModelDifficulty', diffRanges.map((r, i) => ({
        x: models, y: models.map(m => modelDiff[m][r] ? modelDiff[m][r].correct / modelDiff[m][r].total * 100 : 0),
        name: r, type: 'bar', marker: { color: colors[i] }
    })), { ...PLOTLY_LAYOUT, barmode: 'group', xaxis: { tickangle: -45 }, yaxis: { title: '정확도 (%)', range: [0, 100] } }, PLOTLY_CONFIG);
}

// ============================================================
// 초기화
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    loadData();
});
