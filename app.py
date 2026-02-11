<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>COWAY Net-Zero 2050 Master Hub</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root { --mck-blue: #002d72; --mck-gold: #947b45; --bg: #f5f7fa; --white: #ffffff; --red: #d9534f; --blue: #4a90e2; --gray: #bdc3c7; --yellow: #f1c40f; }
        body { font-family: 'Noto Sans KR', sans-serif; background: var(--bg); margin: 0; display: flex; height: 100vh; overflow: hidden; color: #333; }
        
        /* Sidebar */
      .sidebar { width: 300px; background: var(--mck-blue); color: white; display: flex; flex-direction: column; padding: 45px 0; flex-shrink: 0; box-shadow: 4px 0 15px rgba(0,0,0,0.15); }
      .logo-box { padding: 0 35px; margin-bottom: 50px; border-left: 6px solid var(--mck-gold); margin-left: 25px; }
      .nav-item { padding: 22px 35px; cursor: pointer; transition: 0.3s; opacity: 0.6; font-size: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }
      .nav-item:hover { background: rgba(255,255,255,0.1); opacity: 1; }
      .nav-item.active { background: rgba(255,255,255,0.18); opacity: 1; font-weight: 700; border-right: 6px solid var(--mck-gold); }

        /* Content Area */
      .main { flex: 1; display: flex; flex-direction: column; overflow-y: auto; }
      .top-bar { background: white; padding: 20px 50px; border-bottom: 1px solid #dee2e6; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
      .page { display: none; padding: 30px 50px; }
      .page.active { display: block; animation: fadeIn 0.4s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* Control Panel */
      .control-panel { background: white; padding: 25px 50px; border-bottom: 1px solid #dee2e6; }
      .slider-wrap { display: flex; align-items: center; gap: 30px; }
      .year-label { font-size: 34px; font-weight: 700; color: var(--mck-blue); min-width: 100px; text-align: right; }
        input[type=range] { flex: 1; height: 12px; accent-color: var(--mck-blue); cursor: pointer; }

        /* KPI Cards */
      .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; margin-bottom: 30px; }
      .card { background: white; padding: 25px; border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid var(--mck-blue); }
      .card h4 { margin: 0 0 10px 0; font-size: 13px; color: #666; font-weight: 500; }
      .card.val { font-size: 30px; font-weight: 700; color: var(--mck-blue); }
      .card.unit { font-size: 14px; font-weight: 400; color: #999; margin-left: 5px; }

        /* Chart Container */
      .chart-box { background: white; padding: 35px; border-radius: 8px; box-shadow: 0 6px 20px rgba(0,0,0,0.06); }
        h3 { margin-top: 0; font-size: 22px; color: var(--mck-blue); margin-bottom: 30px; display: flex; align-items: center; }
        h3::before { content: '📊'; margin-right: 12px; }

        /* Data Table */
        table { width: 100%; border-collapse: collapse; }
        th { text-align: left; padding: 18px; background: #f8f9fa; border-bottom: 2.5px solid var(--mck-blue); font-size: 13px; }
        td { padding: 15px; border-bottom: 1px solid #eee; font-size: 14px; }
      .badge-on { background: #007a33; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 700; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo-box">
            <h2 style="margin:0; letter-spacing: 1px;">COWAY</h2>
            <div style="font-size:10px; color:var(--mck-gold); font-weight: 700;">NET-ZERO 2050 MASTER</div>
        </div>
        <div class="nav-item active" id="nav-summary" onclick="switchTab('summary')">1. 전사 넷제로 목표 관리</div>
        <div class="nav-item" id="nav-financial" onclick="switchTab('financial')">2. FINANCIAL IMPACT</div>
        <div class="nav-item" id="nav-sites" onclick="switchTab('sites')">3. SITE ANALYSIS</div>
        <div class="nav-item" id="nav-data" onclick="switchTab('data')">4. COMPLIANCE DATA</div>
        <div style="margin-top:auto; padding: 35px; font-size: 11px; opacity: 0.4;">© 2026 Coway Strategy Hub v7.0</div>
    </div>

    <div class="main">
        <div class="top-bar">
            <h2 id="tab-title" style="margin:0; font-weight: 700;">전사 넷제로 목표 관리</h2>
            <span class="badge-on">STRATEGY ALIGNED (SBTi)</span>
        </div>

        <div class="control-panel">
            <div style="margin-bottom: 10px; font-weight: 700; color: #555; font-size: 14px;">로드맵 시뮬레이션 연도 선택</div>
            <div class="slider-wrap">
                <input type="range" id="year-slider" min="2023" max="2050" value="2023" oninput="updateAll(this.value)">
                <span class="year-label" id="year-disp">2023</span>
            </div>
        </div>

        <div id="summary" class="page active">
            <div class="kpi-row">
                <div class="card"><h4>예상 배출량(BAU)</h4><div class="val" id="k-bau">18,041</div><span class="unit">tCO2eq</span></div>
                <div class="card"><h4>목표 배출량(Target)</h4><div class="val" id="k-target">18,000</div><span class="unit">tCO2eq</span></div>
                <div class="card"><h4>감축 필요 격차(Gap)</h4><div class="val" id="k-gap" style="color:var(--red)">41</div><span class="unit">tCO2eq</span></div>
                <div class="card"><h4>감축 이행률</h4><div class="val" id="k-rate">0.2</div><span class="unit">%</span></div>
            </div>
            <div class="chart-box">
                <h3>온실가스 감축 로드맵 분석</h3>
                <div style="height: 500px;"><canvas id="roadmapChart"></canvas></div>
            </div>
        </div>

        <div id="financial" class="page">
            <div class="kpi-row">
                <div class="card"><h4>당해 투자비</h4><div class="val" id="f-capex">0</div><span class="unit">억원</span></div>
                <div class="card"><h4>당해 절감액</h4><div class="val" id="f-opex">0</div><span class="unit">억원</span></div>
                <div class="card"><h4>누적 재무효과</h4><div class="val" id="f-net">0</div><span class="unit">억원</span></div>
                <div class="card"><h4>리스크 방어 추정</h4><div class="val" id="f-risk">0.2</div><span class="unit">억원</span></div>
            </div>
            <div class="chart-box">
                <h3>연도별 재무 투자 및 수익성 분석 (ROI)</h3>
                <div style="height: 400px;"><canvas id="finChart"></canvas></div>
            </div>
        </div>

        <div id="sites" class="page">
            <div class="chart-box">
                <h3>사업장별 전력 사용 및 태양광 설치 잠재량</h3>
                <table>
                    <thead><tr><th>사업장</th><th>계약전력(kW)</th><th>사용량(MWh)</th><th>전기요금(백만)</th><th>태양광 잠재(kW)</th></tr></thead>
                    <tbody>
                        <tr><td>환경기술연구소</td><td>3,200</td><td>3,937</td><td>726</td><td>109.0</td></tr>
                        <tr><td>유구물류센터</td><td>2,000</td><td>3,532</td><td>685</td><td>993.6</td></tr>
                        <tr><td>유구공장</td><td>2,050</td><td>3,316</td><td>724</td><td>774.2</td></tr>
                        <tr><td>인천공장</td><td>1,750</td><td>2,146</td><td>472</td><td>329.0</td></tr>
                        <tr><td>포천공장</td><td>800</td><td>614</td><td>163</td><td>78.4</td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div id="data" class="page">
            <div class="chart-box">
                <h3>이행 로드맵 통합 데이터 테이블 (2023-2050)</h3>
                <div id="table-render" style="max-height: 600px; overflow-y: auto;"></div>
            </div>
        </div>
    </div>

    <script>
        // 마스터 데이터 세팅 
        const dataSet = {
            yrs: Array.from({length: 28}, (_, i) => 2023 + i),
            target: ,
            bau: ,
            investReduc: ,
            recReduc: ,
            capex: [0, 0, 0, 13.6, 9.8, 0.5, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
            opex: [0, 0, 0, 1.2, 2.8, 7.1, 11.4, 15.7, 20.0, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4, 24.4]
        };

        // 옐로우 웨지(잔여 격차) 계산
        dataSet.gapWedge = dataSet.yrs.map((y, i) => Math.max(0, dataSet.bau[i] - dataSet.target[i] - dataSet.investReduc[i]));

        let roadmapChart, finChart;

        function switchTab(id) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            document.getElementById('nav-' + id).classList.add('active');
            
            const titleMap = {summary: '전사 넷제로 목표 관리', financial: '넷제로 투자 및 경제성 분석', sites: '사업장별 에너지 분석', data: '통합 이행 데이터 마스터'};
            document.getElementById('tab-title').innerText = titleMap[id];
            if(id === 'data') renderTable();
        }

        function initCharts() {
            const ctx1 = document.getElementById('roadmapChart').getContext('2d');
            roadmapChart = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: dataSet.yrs,
                    datasets:, borderDash: , pointRadius: 0, order: 1 },
                        { label: '넷제로 목표 배출량', data: dataSet.target, backgroundColor: '#bdc3c7', stack: 's1', order: 2 },
                        { label: '실제 감축량', data: dataSet.investReduc, backgroundColor: '#4a90e2', stack: 's1', order: 2 },
                        { label: '추가 감축 필요량(Gap)', data: dataSet.gapWedge, backgroundColor: '#f1c40f', stack: 's1', order: 2 }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { tooltip: { mode: 'index', intersect: false }, legend: { position: 'top' } },
                    scales: { x: { stacked: true }, y: { stacked: true, title: { display: true, text: '단위: 톤' } } }
                }
            });

            const ctx2 = document.getElementById('finChart').getContext('2d');
            finChart = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: dataSet.yrs,
                    datasets:
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        function updateAll(year) {
            const idx = year - 2023;
            document.getElementById('year-disp').innerText = year;
            
            // KPI 업데이트
            const b = dataSet.bau[idx];
            const t = dataSet.target[idx];
            const g = Math.max(0, b - t);
            document.getElementById('k-bau').innerText = b.toLocaleString();
            document.getElementById('k-target').innerText = t.toLocaleString();
            document.getElementById('k-gap').innerText = g.toLocaleString();
            document.getElementById('k-rate').innerText = ((1 - t/18000)*100).toFixed(1);

            // 재무 업데이트
            document.getElementById('f-capex').innerText = dataSet.capex[idx];
            document.getElementById('f-opex').innerText = dataSet.opex[idx];
            const net = (dataSet.opex.slice(0, idx+1).reduce((a,b)=>a+b, 0) - dataSet.capex.slice(0, idx+1).reduce((a,b)=>a+b, 0)).toFixed(1);
            document.getElementById('f-net').innerText = net;
            document.getElementById('f-risk').innerText = (g * 0.05).toFixed(1);
        }

        function renderTable() {
            let h = '<table><thead><tr><th>연도</th><th>BAU</th><th>Target</th><th>감축량</th><th>잔여격차</th><th>누적이익</th></tr></thead><tbody>';
            dataSet.yrs.forEach((y, i) => {
                const net = (dataSet.opex.slice(0, i+1).reduce((a,b)=>a+b, 0) - dataSet.capex.slice(0, i+1).reduce((a,b)=>a+b, 0)).toFixed(1);
                h += `<tr><td>${y}</td><td>${dataSet.bau[i].toLocaleString()}</td><td>${dataSet.target[i].toLocaleString()}</td><td>${dataSet.investReduc[i].toLocaleString()}</td><td style="color:red">${dataSet.gapWedge[i].toLocaleString()}</td><td>${net}억</td></tr>`;
            });
            document.getElementById('table-render').innerHTML = h + '</tbody></table>';
        }

        window.onload = () => { initCharts(); updateAll(2023); };
    </script>
</body>
</html>
