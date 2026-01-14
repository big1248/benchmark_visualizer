/**
 * LLM Benchmark Visualizer - Complete Version (11 Tabs)
 */

const APP = { data: [], filtered: [], selectedTests: [], lang: 'ko' };

const LAYOUT = {
    paper_bgcolor: 'white', plot_bgcolor: 'white',
    font: { color: '#262730', size: 12, family: 'Source Sans Pro, sans-serif' },
    margin: { l: 60, r: 30, t: 50, b: 80 },
    xaxis: { gridcolor: '#e6e9ef', linecolor: '#e6e9ef' },
    yaxis: { gridcolor: '#e6e9ef', linecolor: '#e6e9ef' }
};
const CONFIG = { responsive: true, displayModeBar: false };

function accColor(v) {
    if (v >= 80) return 'rgba(9,171,59,0.85)';
    if (v >= 70) return 'rgba(46,204,113,0.75)';
    if (v >= 60) return 'rgba(133,200,114,0.65)';
    if (v >= 50) return 'rgba(241,196,15,0.7)';
    if (v >= 40) return 'rgba(230,126,34,0.7)';
    return 'rgba(231,76,60,0.7)';
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
                    row.정답여부 = row.정답여부 === true || row.정답여부 === 'True' || row.정답여부 === 1;
                    row._detail = info.detail;
                    row._prompt = info.prompt;
                    all.push(row);
                }
            });
            bar.style.width = `${50 + (i / files.length) * 50}%`;
        }
        
        APP.data = all;
        APP.filtered = [...all];
        init();
        loading.classList.add('hidden');
    } catch (e) {
        text.textContent = '샘플 데이터 로드 중...';
        loadSample();
        loading.classList.add('hidden');
    }
}

function parseFilename(f) {
    const n = f.replace('data/', '').replace('.csv', '');
    const p = n.split('_');
    return { model: p[0] || 'Unknown', detail: p[1] || '', prompt: p[2] || '', testname: p.slice(3).join('_') || 'Unknown' };
}

function loadSample() {
    const models = ['GPT-4o', 'Claude-3.5-Sonnet', 'Qwen3-30b-a3b-2507', 'Meta-Llama-3.1-8b-Instruct', 'Claude-3.5-Haiku', 'GPT-4o-Mini'];
    const tests = ['건설안전기사', '경비지도사2차'];
    const subjects = ['안전관리론', '재난관리론', '소방학', '도시계획', '교육학개론', '구급 및 응급처치론'];
    const all = [];
    
    models.forEach(m => {
        tests.forEach(t => {
            for (let i = 0; i < 300; i++) {
                all.push({
                    ID: all.length + 1, 모델: m, 테스트명: t,
                    Year: 2018 + Math.floor(Math.random() * 7),
                    Subject: subjects[Math.floor(Math.random() * subjects.length)],
                    Question: `Q_${t}_${i}`, 정답여부: Math.random() > 0.4,
                    law: Math.random() > 0.5 ? 'O' : '',
                    '문제당평균시간(초)': +(Math.random() * 3 + 0.1).toFixed(2),
                    '입력토큰': Math.floor(Math.random() * 400 + 100),
                    '출력토큰': Math.floor(Math.random() * 80 + 10),
                    '비용($)': +(Math.random() * 0.005).toFixed(5),
                    _detail: 'detailed', _prompt: 'no_prompting'
                });
            }
        });
    });
    APP.data = all;
    APP.filtered = [...all];
    init();
}

// ========== 초기화 ==========
function init() {
    const tests = [...new Set(APP.data.map(d => d.테스트명).filter(Boolean))].sort();
    const models = [...new Set(APP.data.map(d => d.모델).filter(Boolean))].sort();
    
    const sel = document.getElementById('testSelect');
    sel.innerHTML = '<option value="">+ 테스트 추가</option>';
    tests.forEach(t => sel.innerHTML += `<option value="${t}">${t}</option>`);
    APP.selectedTests = tests.slice(0, 2);
    renderTags();
    
    sel.onchange = e => {
        if (e.target.value && !APP.selectedTests.includes(e.target.value)) {
            APP.selectedTests.push(e.target.value);
            renderTags();
            filter();
        }
        e.target.value = '';
    };
    
    const msel = document.getElementById('modelSelect');
    msel.innerHTML = '<option value="all">전체</option>';
    models.forEach(m => msel.innerHTML += `<option value="${m}">${m}</option>`);
    
    ['modelSelect', 'detailSelect', 'promptSelect', 'typeSelect', 'lawSelect'].forEach(id => {
        document.getElementById(id).onchange = filter;
    });
    
    document.getElementById('fontSlider').oninput = e => {
        document.getElementById('fontValue').textContent = (+e.target.value).toFixed(2);
    };
    document.getElementById('chartSlider').oninput = e => {
        document.getElementById('chartValue').textContent = (+e.target.value).toFixed(2);
    };
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.onclick = () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
            render(btn.dataset.tab);
        };
    });
    
    filter();
}

function renderTags() {
    const c = document.getElementById('testTags');
    c.innerHTML = APP.selectedTests.map(t => 
        `<span class="tag">${t}<span class="tag-remove" onclick="removeTag('${t}')">×</span></span>`
    ).join('');
}

function removeTag(t) {
    APP.selectedTests = APP.selectedTests.filter(x => x !== t);
    renderTags();
    filter();
}

function filter() {
    const m = document.getElementById('modelSelect').value;
    const law = document.getElementById('lawSelect').value;
    const type = document.getElementById('typeSelect').value;
    
    APP.filtered = APP.data.filter(r => {
        if (APP.selectedTests.length && !APP.selectedTests.includes(r.테스트명)) return false;
        if (m !== 'all' && r.모델 !== m) return false;
        if (law === 'O' && r.law !== 'O') return false;
        if (law === 'X' && r.law === 'O') return false;
        if (type === 'text' && r.image && r.image !== 'text_only') return false;
        if (type === 'image' && (!r.image || r.image === 'text_only')) return false;
        return true;
    });
    
    document.getElementById('dataCount').textContent = APP.filtered.length.toLocaleString();
    const active = document.querySelector('.tab-btn.active');
    if (active) render(active.dataset.tab);
}

function render(tab) {
    const handlers = {
        overview: renderOverview, model: renderModel, time: renderTime,
        law: renderLaw, subject: renderSubject, year: renderYear,
        error: renderError, diff: renderDiff, cost: renderCost,
        testset: renderTestset, extra: renderExtra
    };
    handlers[tab]?.();
}

// ========== 전체 요약 ==========
function renderOverview() {
    const d = APP.filtered;
    const models = [...new Set(d.map(r => r.모델).filter(Boolean))];
    const questions = new Set(d.map(r => r.Question));
    const total = questions.size;
    const correct = d.filter(r => r.정답여부).length;
    
    document.getElementById('m-total').textContent = total.toLocaleString();
    document.getElementById('m-models').textContent = models.length;
    document.getElementById('m-evals').textContent = (total * models.length).toLocaleString();
    
    const accByModel = {};
    d.forEach(r => {
        if (!r.모델) return;
        if (!accByModel[r.모델]) accByModel[r.모델] = { c: 0, t: 0 };
        accByModel[r.모델].t++;
        if (r.정답여부) accByModel[r.모델].c++;
    });
    
    const avgAcc = Object.values(accByModel).reduce((s, v) => s + v.c / v.t, 0) / models.length * 100 || 0;
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
        marker: { color: mAccs.map(v => accColor(+v)), line: { color: '#000', width: 1 } },
        text: mAccs.map(v => v + '%'), textposition: 'outside'
    }], { ...LAYOUT, title: '모델별 평균 정확도', xaxis: { tickangle: -45 }, yaxis: { title: '정확도 (%)', range: [0, 100] } }, CONFIG);
    
    Plotly.newPlot('chart-lawcomp', [{
        x: ['법령', '비법령'], y: [lawAcc, nonLawAcc], type: 'bar',
        marker: { color: ['#FF6B6B', '#4ECDC4'], line: { color: '#000', width: 1.5 } },
        text: [lawAcc.toFixed(1) + '%', nonLawAcc.toFixed(1) + '%'], textposition: 'outside'
    }], { ...LAYOUT, title: '법령/비법령 정답률 비교', yaxis: { title: '정답률 (%)', range: [0, 100] } }, CONFIG);
    
    document.querySelector('#tbl-perf tbody').innerHTML = sorted.map(([m, s], i) => {
        const acc = (s.c / s.t * 100).toFixed(2);
        return `<tr><td>${i}</td><td>${m}</td><td>${s.c}</td><td>${s.t}</td><td><span class="acc-cell" style="background:${accColor(+acc)}">${acc}%</span></td><td>${s.t - s.c}</td></tr>`;
    }).join('');
    
    renderHeatmap('chart-heatmap', d, mNames);
    
    const tests = [...new Set(d.map(r => r.테스트명).filter(Boolean))];
    const testAcc = {};
    tests.forEach(t => {
        const td = d.filter(r => r.테스트명 === t);
        testAcc[t] = td.filter(r => r.정답여부).length / td.length * 100;
    });
    const hardest = Object.entries(testAcc).sort((a, b) => a[1] - b[1])[0];
    const easiest = Object.entries(testAcc).sort((a, b) => b[1] - a[1])[0];
    
    document.getElementById('heatmap-insight').innerHTML = `
        💡 <strong>히트맵 분석</strong>:<br>
        • <strong>가장 어려운 테스트</strong>: ${hardest?.[0] || '-'} (평균: ${hardest?.[1]?.toFixed(1) || 0}%)<br>
        • <strong>가장 쉬운 테스트</strong>: ${easiest?.[0] || '-'} (평균: ${easiest?.[1]?.toFixed(1) || 0}%)<br>
        • <strong>일관성</strong>: 모든 모델이 비슷한 성능 패턴을 보이는지 확인하세요<br>
        • <strong>특화 영역</strong>: 특정 모델이 특정 테스트에서 특히 우수한지 파악하세요
    `;
}

function renderHeatmap(id, data, models) {
    const tests = [...new Set(data.map(r => r.테스트명).filter(Boolean))];
    const z = [], txt = [];
    
    models.forEach(m => {
        const row = [], trow = [];
        tests.forEach(t => {
            const f = data.filter(r => r.모델 === m && r.테스트명 === t);
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
        text: txt, texttemplate: '%{text}', textfont: { size: 10 },
        colorbar: { title: '정확도 (%)' }, xgap: 2, ygap: 2
    }], { ...LAYOUT, margin: { l: 150, r: 50, t: 30, b: 100 }, xaxis: { tickangle: -45 } }, CONFIG);
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
    const wrongs = sorted.map(x => x[1].t - x[1].c);
    const corrects = sorted.map(x => x[1].c);
    
    document.querySelector('#tbl-model tbody').innerHTML = sorted.map(([m, s], i) => {
        const acc = (s.c / s.t * 100).toFixed(2);
        return `<tr><td>${i}</td><td>${m}</td><td>${s.c}</td><td>${s.t}</td><td><span class="acc-cell" style="background:${accColor(+acc)}">${acc}%</span></td><td>${s.t - s.c}</td></tr>`;
    }).join('');
    
    Plotly.newPlot('chart-modelbar', [{
        x: models, y: accs, type: 'bar',
        marker: { color: accs.map(v => accColor(v)), line: { color: '#000', width: 1 } },
        text: accs.map(v => v.toFixed(1) + '%'), textposition: 'outside'
    }], { ...LAYOUT, title: '전체 테스트 비교', xaxis: { tickangle: -45 }, yaxis: { title: '정확도 (%)', range: [0, Math.max(...accs) * 1.15] } }, CONFIG);
    
    Plotly.newPlot('chart-modelstack', [
        { x: models, y: corrects, name: '정답', type: 'bar', marker: { color: 'lightgreen', line: { color: '#000', width: 1 } } },
        { x: models, y: wrongs, name: '오답', type: 'bar', marker: { color: 'lightcoral', line: { color: '#000', width: 1 } } }
    ], { ...LAYOUT, barmode: 'stack', title: '정답/오답 비교 차트', xaxis: { tickangle: -45 }, yaxis: { title: '문제 수' } }, CONFIG);
    
    renderHeatmap('chart-heatmap2', d, models);
}

// ========== 응답시간 ==========
function renderTime() {
    const d = APP.filtered.filter(r => r['문제당평균시간(초)']);
    if (!d.length) return;
    
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
        const std = Math.sqrt(times.reduce((s, t) => s + (t - avg) ** 2, 0) / times.length);
        return { model: m, avg, median, std, min: Math.min(...times), max: Math.max(...times), count: s.t, acc: s.c / s.t * 100, times };
    }).sort((a, b) => a.avg - b.avg);
    
    const fastest = rows[0];
    const slowest = rows[rows.length - 1];
    const avgAll = rows.reduce((s, r) => s + r.avg, 0) / rows.length;
    
    document.getElementById('m-fastest').textContent = fastest?.model || '-';
    document.getElementById('m-fastestT').textContent = `↑ ${fastest?.avg.toFixed(2) || 0}초`;
    document.getElementById('m-slowest').textContent = slowest?.model || '-';
    document.getElementById('m-slowestT').textContent = `↑ ${slowest?.avg.toFixed(2) || 0}초`;
    document.getElementById('m-avgtime').textContent = avgAll.toFixed(2) + '초';
    
    document.querySelector('#tbl-time tbody').innerHTML = rows.map((r, i) => 
        `<tr><td>${i}</td><td>${r.model}</td><td><span class="acc-cell" style="background:${accColor(100 - r.avg * 30)}">${r.avg.toFixed(2)}</span></td><td>${r.median.toFixed(2)}</td><td>${r.std.toFixed(2)}</td><td>${r.min.toFixed(2)}</td><td>${r.max.toFixed(2)}</td><td>${r.count}</td><td>${r.acc.toFixed(2)}%</td></tr>`
    ).join('');
    
    Plotly.newPlot('chart-timebar', [{
        x: rows.map(r => r.model), y: rows.map(r => r.avg), type: 'bar',
        marker: { color: rows.map(r => `rgba(${Math.min(255, r.avg * 80)}, ${Math.max(0, 200 - r.avg * 60)}, 100, 0.8)`), line: { color: '#000', width: 1 } },
        text: rows.map(r => r.avg.toFixed(2) + '초'), textposition: 'outside'
    }], { ...LAYOUT, title: '모델별 평균 응답시간', xaxis: { tickangle: -45 }, yaxis: { title: '응답시간 (초)' } }, CONFIG);
    
    Plotly.newPlot('chart-timebox', rows.map(r => ({
        y: r.times, type: 'box', name: r.model, boxpoints: false
    })), { ...LAYOUT, title: '응답시간 분포', showlegend: false, yaxis: { title: '응답시간 (초)' } }, CONFIG);
    
    Plotly.newPlot('chart-timescatter', [{
        x: rows.map(r => r.avg), y: rows.map(r => r.acc),
        mode: 'markers+text', type: 'scatter',
        text: rows.map(r => r.model), textposition: 'top center',
        marker: { size: 14, color: '#0068c9', line: { width: 2, color: '#000' } }
    }], { ...LAYOUT, title: '응답시간 vs 정확도', xaxis: { title: '평균 응답시간 (초)' }, yaxis: { title: '정확도 (%)' } }, CONFIG);
    
    const timeRatio = slowest.avg / fastest.avg;
    const accRatio = fastest.acc / slowest.acc;
    document.getElementById('time-insight').innerHTML = `
        💡 <strong>속도 vs 정확도 트레이드오프 분석</strong>:<br><br>
        🏃 <strong>속도</strong>:<br>
        • <strong>최고속</strong>: ${fastest.model} (${fastest.avg.toFixed(2)}초, 정확도 ${fastest.acc.toFixed(1)}%)<br>
        • <strong>최저속</strong>: ${slowest.model} (${slowest.avg.toFixed(2)}초, 정확도 ${slowest.acc.toFixed(1)}%)<br>
        • <strong>속도 차이</strong>: ${timeRatio.toFixed(1)}x<br><br>
        🎯 <strong>효율성 분석</strong>:<br>
        • 빠른 모델이 ${accRatio.toFixed(2)}x의 정확도를 가짐<br>
        • <strong>권장사항</strong>: 실시간 처리가 중요하면 ${fastest.model}, 정확도가 중요하면 ${slowest.acc > fastest.acc ? slowest.model : fastest.model}
    `;
}

// ========== 법령/비법령 ==========
function renderLaw() {
    const d = APP.filtered;
    const lawD = d.filter(r => r.law === 'O');
    const nonD = d.filter(r => r.law !== 'O');
    const lawQ = new Set(lawD.map(r => r.Question)).size;
    const nonQ = new Set(nonD.map(r => r.Question)).size;
    
    document.getElementById('m-law2').textContent = `${lawQ} (${(lawQ / (lawQ + nonQ) * 100).toFixed(1)}%)`;
    document.getElementById('m-nonlaw2').textContent = `${nonQ} (${(nonQ / (lawQ + nonQ) * 100).toFixed(1)}%)`;
    
    Plotly.newPlot('chart-lawpie', [{
        values: [lawQ, nonQ], labels: ['법령', '비법령'], type: 'pie',
        marker: { colors: ['#FF6B6B', '#4ECDC4'], line: { color: '#000', width: 2 } },
        hole: 0.3
    }], { ...LAYOUT, title: '법령/비법령 문제 분포' }, CONFIG);
    
    const stats = {};
    d.forEach(r => {
        if (!r.모델) return;
        if (!stats[r.모델]) stats[r.모델] = { lc: 0, lt: 0, nc: 0, nt: 0 };
        if (r.law === 'O') { stats[r.모델].lt++; if (r.정답여부) stats[r.모델].lc++; }
        else { stats[r.모델].nt++; if (r.정답여부) stats[r.모델].nc++; }
    });
    
    const models = Object.keys(stats);
    Plotly.newPlot('chart-lawmodel', [
        { x: models, y: models.map(m => stats[m].lt ? stats[m].lc / stats[m].lt * 100 : 0), name: '법령', type: 'bar', marker: { color: '#FF6B6B', line: { color: '#000', width: 1 } } },
        { x: models, y: models.map(m => stats[m].nt ? stats[m].nc / stats[m].nt * 100 : 0), name: '비법령', type: 'bar', marker: { color: '#4ECDC4', line: { color: '#000', width: 1 } } }
    ], { ...LAYOUT, barmode: 'group', title: '모델별 법령/비법령 성능', xaxis: { tickangle: -45 }, yaxis: { title: '정답률 (%)', range: [0, 100] } }, CONFIG);
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
        return `<tr><td>${i}</td><td>${s}</td><td>${v.c}</td><td>${v.t}</td><td><span class="acc-cell" style="background:${accColor(+acc)}">${acc}%</span></td></tr>`;
    }).join('');
    
    Plotly.newPlot('chart-subject', [{
        y: sorted.map(x => x[0]), x: sorted.map(x => x[1].c / x[1].t * 100),
        type: 'bar', orientation: 'h',
        marker: { color: sorted.map(x => accColor(x[1].c / x[1].t * 100)), line: { color: '#000', width: 1 } },
        text: sorted.map(x => (x[1].c / x[1].t * 100).toFixed(1) + '%'), textposition: 'outside'
    }], { ...LAYOUT, margin: { l: 180 }, xaxis: { title: '정확도 (%)', range: [0, 100] } }, CONFIG);
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
        text: years.map(y => stats[y].t), textposition: 'outside'
    }], { ...LAYOUT, title: '연도별 문제 수', xaxis: { title: '연도' }, yaxis: { title: '문제 수' } }, CONFIG);
    
    Plotly.newPlot('chart-yearacc', [{
        x: years, y: years.map(y => stats[y].c / stats[y].t * 100),
        type: 'scatter', mode: 'lines+markers+text',
        marker: { size: 10, color: '#09ab3b', line: { width: 2, color: '#000' } },
        line: { color: '#09ab3b', width: 3 },
        text: years.map(y => (stats[y].c / stats[y].t * 100).toFixed(1) + '%'),
        textposition: 'top center'
    }], { ...LAYOUT, title: '연도별 정답률 추이', xaxis: { title: '연도' }, yaxis: { title: '정확도 (%)', range: [0, 100] } }, CONFIG);
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
        alert.innerHTML = `<div class="alert alert-error">⚠️ <strong>심각한 공통 오답 발견: ${allWrong.length}개 문제</strong><br>이 문제들은 <strong>모든 평가 모델이 틀렸습니다</strong>. 현재 LLM들이 공통적으로 해당 지식 영역을 제대로 이해하지 못하고 있음을 의미합니다.</div>`;
        document.querySelector('#tbl-allwrong tbody').innerHTML = allWrong.slice(0, 15).map(([q, s]) => 
            `<tr><td>${q.substring(0, 30)}...</td><td>${s.test || '-'}</td><td>${s.subj || '-'}</td><td>${s.year || '-'}</td><td>${s.c}</td></tr>`
        ).join('');
    } else {
        alert.innerHTML = '<div class="alert alert-success">✅ 모든 모델이 틀린 문제가 없습니다!</div>';
        document.querySelector('#tbl-allwrong tbody').innerHTML = '';
    }
    
    const mostWrong = sorted.filter(([q, s]) => s.c / s.t >= 0.5);
    document.getElementById('most-wrong-alert').innerHTML = mostWrong.length
        ? `<div class="alert alert-warning">⚠️ <strong>주요 공통 오답: ${mostWrong.length}개 문제</strong><br>이 문제들은 <strong>50% 이상의 모델이 틀렸습니다</strong>.</div>`
        : '<div class="alert alert-success">✅ 대부분 모델이 틀린 문제가 없습니다!</div>';
    
    // 오답률 Top 10 차트
    const top10 = sorted.slice(0, 10);
    Plotly.newPlot('chart-errortop10', [{
        x: top10.map(([q]) => q.substring(0, 20) + '...'),
        y: top10.map(([q, s]) => s.c / s.t * 100),
        type: 'bar',
        marker: { color: top10.map(([q, s]) => `rgba(231, 76, 60, ${s.c / s.t})`), line: { color: '#000', width: 1 } },
        text: top10.map(([q, s]) => (s.c / s.t * 100).toFixed(0) + '%'),
        textposition: 'outside'
    }], { ...LAYOUT, title: '오답률 높은 문제 Top 10', xaxis: { tickangle: -45 }, yaxis: { title: '오답률 (%)', range: [0, 100] } }, CONFIG);
    
    // 오답 일치도 히트맵
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
            colorbar: { title: '일치도 (%)' }, xgap: 2, ygap: 2,
            text: z.map(row => row.map(v => v.toFixed(0))), texttemplate: '%{text}%', textfont: { size: 10 }
        }], { ...LAYOUT, title: '모델 간 오답 일치도', margin: { l: 150, r: 50, t: 50, b: 100 }, xaxis: { tickangle: -45 } }, CONFIG);
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
    
    const ranges = { '매우 어려움 (0-20%)': 0, '어려움 (20-40%)': 0, '보통 (40-60%)': 0, '쉬움 (60-80%)': 0, '매우 쉬움 (80-100%)': 0 };
    const questions = Object.values(qDiff);
    
    questions.forEach(q => {
        const acc = q.c / q.t * 100;
        if (acc < 20) ranges['매우 어려움 (0-20%)']++;
        else if (acc < 40) ranges['어려움 (20-40%)']++;
        else if (acc < 60) ranges['보통 (40-60%)']++;
        else if (acc < 80) ranges['쉬움 (60-80%)']++;
        else ranges['매우 쉬움 (80-100%)']++;
    });
    
    Plotly.newPlot('chart-diffdist', [{
        x: Object.keys(ranges), y: Object.values(ranges), type: 'bar',
        marker: { color: ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#09ab3b'], line: { color: '#000', width: 1 } },
        text: Object.values(ranges), textposition: 'outside'
    }], { ...LAYOUT, title: '난이도 구간별 문제 분포', xaxis: { tickangle: -30 }, yaxis: { title: '문제 수' } }, CONFIG);
    
    // 모델별 난이도
    const modelDiff = {};
    d.forEach(r => {
        if (!r.모델 || !r.Question || !qDiff[r.Question]) return;
        const acc = qDiff[r.Question].c / qDiff[r.Question].t * 100;
        const range = acc < 20 ? '매우 어려움' : acc < 40 ? '어려움' : acc < 60 ? '보통' : acc < 80 ? '쉬움' : '매우 쉬움';
        if (!modelDiff[r.모델]) modelDiff[r.모델] = {};
        if (!modelDiff[r.모델][range]) modelDiff[r.모델][range] = { c: 0, t: 0 };
        modelDiff[r.모델][range].t++;
        if (r.정답여부) modelDiff[r.모델][range].c++;
    });
    
    const models = Object.keys(modelDiff);
    const diffNames = ['매우 어려움', '어려움', '보통', '쉬움', '매우 쉬움'];
    const colors = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#09ab3b'];
    
    Plotly.newPlot('chart-diffmodel', diffNames.map((r, i) => ({
        x: models, y: models.map(m => modelDiff[m][r] ? modelDiff[m][r].c / modelDiff[m][r].t * 100 : 0),
        name: r, type: 'bar', marker: { color: colors[i] }
    })), { ...LAYOUT, barmode: 'group', title: '모델별 난이도 구간 성능', xaxis: { tickangle: -45 }, yaxis: { title: '정확도 (%)', range: [0, 100] } }, CONFIG);
    
    // 어려운/쉬운 문제 통계
    const veryHard = questions.filter(q => q.c / q.t < 0.2);
    const veryEasy = questions.filter(q => q.c / q.t > 0.8);
    
    document.getElementById('m-veryhard').textContent = veryHard.length;
    document.getElementById('m-veryhardacc').textContent = veryHard.length ? (veryHard.reduce((s, q) => s + q.c / q.t, 0) / veryHard.length * 100).toFixed(1) + '%' : '0%';
    document.getElementById('m-veryeasy').textContent = veryEasy.length;
    document.getElementById('m-veryeasyacc').textContent = veryEasy.length ? (veryEasy.reduce((s, q) => s + q.c / q.t, 0) / veryEasy.length * 100).toFixed(1) + '%' : '0%';
    
    // 과목별 난이도
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
        text: subjSorted.map(x => x.avg.toFixed(1) + '%'), textposition: 'outside'
    }], { ...LAYOUT, title: '과목별 평균 난이도 (정답률)', xaxis: { tickangle: -45 }, yaxis: { title: '평균 정답률 (%)', range: [0, 100] } }, CONFIG);
    
    const total = questions.length;
    document.getElementById('diff-insight').innerHTML = `
        💡 <strong>난이도 분포 종합 분석</strong>:<br><br>
        📊 <strong>문제 난이도 구성</strong>:<br>
        • <strong>매우 어려움</strong>: ${(ranges['매우 어려움 (0-20%)'] / total * 100).toFixed(1)}% (${ranges['매우 어려움 (0-20%)']}개)<br>
        • <strong>어려움</strong>: ${(ranges['어려움 (20-40%)'] / total * 100).toFixed(1)}% (${ranges['어려움 (20-40%)']}개)<br>
        • <strong>보통</strong>: ${(ranges['보통 (40-60%)'] / total * 100).toFixed(1)}% (${ranges['보통 (40-60%)']}개)<br>
        • <strong>쉬움</strong>: ${(ranges['쉬움 (60-80%)'] / total * 100).toFixed(1)}% (${ranges['쉬움 (60-80%)']}개)<br>
        • <strong>매우 쉬움</strong>: ${(ranges['매우 쉬움 (80-100%)'] / total * 100).toFixed(1)}% (${ranges['매우 쉬움 (80-100%)']}개)
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
    const avgIn = models.reduce((s, m) => s + stats[m].inT / stats[m].t, 0) / models.length;
    const avgOut = models.reduce((s, m) => s + stats[m].outT / stats[m].t, 0) / models.length;
    const ioRatio = avgOut > 0 ? (avgIn / avgOut).toFixed(2) : 0;
    
    document.getElementById('m-totaltoken').textContent = totalToken.toLocaleString();
    document.getElementById('m-intoken').textContent = Math.round(avgIn).toLocaleString();
    document.getElementById('m-outtoken').textContent = Math.round(avgOut).toLocaleString();
    document.getElementById('m-ioratio').textContent = `${ioRatio}:1`;
    
    // 테이블
    const rows = models.map(m => {
        const s = stats[m];
        const total = s.inT + s.outT;
        const avg = total / s.t;
        const acc = s.c / s.t * 100;
        const perCorrect = s.c > 0 ? total / s.c : 0;
        return { model: m, inT: s.inT, outT: s.outT, total, avg, count: s.t, acc, perCorrect };
    }).sort((a, b) => b.total - a.total);
    
    document.querySelector('#tbl-cost tbody').innerHTML = rows.map((r, i) => 
        `<tr><td>${i}</td><td>${r.model}</td><td>${r.inT.toLocaleString()}</td><td>${r.outT.toLocaleString()}</td><td>${r.total.toLocaleString()}</td><td>${Math.round(r.avg).toLocaleString()}</td><td>${r.acc.toFixed(2)}%</td><td style="color:${r.perCorrect < avgIn + avgOut ? '#09ab3b' : '#dc3545'}">${Math.round(r.perCorrect).toLocaleString()}</td></tr>`
    ).join('');
    
    // 차트들
    Plotly.newPlot('chart-token', [{
        x: rows.map(r => r.model), y: rows.map(r => r.total), type: 'bar',
        marker: { color: '#0068c9', line: { color: '#000', width: 1 } },
        text: rows.map(r => (r.total / 1000).toFixed(0) + 'K'), textposition: 'outside'
    }], { ...LAYOUT, title: '총 토큰 (모델별)', xaxis: { tickangle: -45 }, yaxis: { title: '총 토큰' } }, CONFIG);
    
    Plotly.newPlot('chart-tokenstack', [
        { x: rows.map(r => r.model), y: rows.map(r => r.inT), name: '입력 토큰', type: 'bar', marker: { color: 'lightblue', line: { color: '#000', width: 1 } } },
        { x: rows.map(r => r.model), y: rows.map(r => r.outT), name: '출력 토큰', type: 'bar', marker: { color: 'lightgreen', line: { color: '#000', width: 1 } } }
    ], { ...LAYOUT, barmode: 'stack', title: '입출력 토큰 비교', xaxis: { tickangle: -45 }, yaxis: { title: '토큰' } }, CONFIG);
    
    Plotly.newPlot('chart-tokenscatter', [{
        x: rows.map(r => r.perCorrect), y: rows.map(r => r.acc),
        mode: 'markers+text', type: 'scatter',
        text: rows.map(r => r.model), textposition: 'top center',
        marker: { size: 14, color: '#f59e0b', line: { width: 2, color: '#000' } }
    }], { ...LAYOUT, title: '토큰 효율성 vs 정확도', xaxis: { title: '정답당 토큰' }, yaxis: { title: '정확도 (%)' } }, CONFIG);
}

// ========== 테스트셋 통계 ==========
function renderTestset() {
    const d = APP.filtered;
    const tests = [...new Set(d.map(r => r.테스트명).filter(Boolean))];
    
    const stats = tests.map(t => {
        const td = d.filter(r => r.테스트명 === t);
        const total = new Set(td.map(r => r.Question)).size;
        const law = new Set(td.filter(r => r.law === 'O').map(r => r.Question)).size;
        const acc = td.filter(r => r.정답여부).length / td.length * 100;
        return { test: t, total, law, nonLaw: total - law, acc };
    });
    
    document.querySelector('#tbl-testset tbody').innerHTML = stats.map(s => 
        `<tr><td>${s.test}</td><td>${s.total}</td><td>${s.law}</td><td>${s.nonLaw}</td><td><span class="acc-cell" style="background:${accColor(s.acc)}">${s.acc.toFixed(2)}%</span></td></tr>`
    ).join('');
    
    Plotly.newPlot('chart-testsetacc', [{
        x: stats.map(s => s.test), y: stats.map(s => s.acc), type: 'bar',
        marker: { color: stats.map(s => accColor(s.acc)), line: { color: '#000', width: 1 } },
        text: stats.map(s => s.acc.toFixed(1) + '%'), textposition: 'outside'
    }], { ...LAYOUT, title: '테스트셋별 평균 정답률', xaxis: { tickangle: -45 }, yaxis: { title: '정답률 (%)', range: [0, 100] } }, CONFIG);
    
    Plotly.newPlot('chart-testsetdist', [
        { x: stats.map(s => s.test), y: stats.map(s => s.law), name: '법령', type: 'bar', marker: { color: '#FF6B6B' } },
        { x: stats.map(s => s.test), y: stats.map(s => s.nonLaw), name: '비법령', type: 'bar', marker: { color: '#4ECDC4' } }
    ], { ...LAYOUT, barmode: 'stack', title: '테스트셋별 문제 분포', xaxis: { tickangle: -45 }, yaxis: { title: '문제 수' } }, CONFIG);
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
        `<tr><td>${i + 1}</td><td>${r.model}</td><td>${r.acc.toFixed(2)}%</td><td>${r.time ? r.time.toFixed(2) + '초' : '-'}</td><td>${r.efficiency ? Math.round(r.efficiency).toLocaleString() : '-'}</td></tr>`
    ).join('');
    
    // 레이더 차트
    const top5 = rows.slice(0, 5);
    const maxAcc = Math.max(...top5.map(r => r.acc));
    const maxTime = Math.max(...top5.filter(r => r.time).map(r => r.time)) || 1;
    const maxEff = Math.max(...top5.filter(r => r.efficiency).map(r => r.efficiency)) || 1;
    
    Plotly.newPlot('chart-radar', top5.map(r => ({
        type: 'scatterpolar',
        r: [r.acc / maxAcc * 100, r.time ? (1 - r.time / maxTime) * 100 : 50, r.efficiency ? (1 - r.efficiency / maxEff) * 100 : 50, r.acc / maxAcc * 100],
        theta: ['정확도', '속도', '효율성', '정확도'],
        fill: 'toself',
        name: r.model
    })), { ...LAYOUT, polar: { radialaxis: { visible: true, range: [0, 100] } }, title: '모델 성능 비교 (Top 5)' }, CONFIG);
    
    // 인사이트
    const best = rows[0];
    const fastest = rows.filter(r => r.time).sort((a, b) => a.time - b.time)[0];
    const efficient = rows.filter(r => r.efficiency).sort((a, b) => a.efficiency - b.efficiency)[0];
    
    document.getElementById('extra-insight').innerHTML = `
        💡 <strong>종합 분석 결과</strong>:<br><br>
        🏆 <strong>최고 정확도</strong>: ${best.model} (${best.acc.toFixed(2)}%)<br>
        ⚡ <strong>최고 속도</strong>: ${fastest?.model || '-'} (${fastest?.time?.toFixed(2) || '-'}초)<br>
        💰 <strong>최고 효율</strong>: ${efficient?.model || '-'} (정답당 ${efficient?.efficiency ? Math.round(efficient.efficiency) : '-'}토큰)<br><br>
        📊 <strong>권장사항</strong>:<br>
        • 정확도 우선: ${best.model}<br>
        • 속도 우선: ${fastest?.model || best.model}<br>
        • 비용 효율 우선: ${efficient?.model || best.model}
    `;
}

// 시작
document.addEventListener('DOMContentLoaded', loadData);
