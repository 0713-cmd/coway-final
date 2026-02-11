import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Coway Net-Zero 2050", layout="wide")

# 2. HTML/JS/CSS 통합 마스터 코드
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>COWAY Net-Zero Master Hub</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        :root { --mck-blue: #002d72; --mck-gold: #947b45; --bg: #f8f9fa; --red: #d9534f; --blue: #4a90e2; --gray: #bdc3c7; --yellow: #f1c40f; }
        body { font-family: 'Noto Sans KR', sans-serif; background: var(--bg); margin: 0; padding: 0; overflow-x: hidden; color: #333; }
        
       .sidebar { width: 280px; background: var(--mck-blue); color: white; height: 100vh; position: fixed; padding: 40px 0; }
       .logo { padding: 0 30px; margin-bottom: 50px; border-left: 5px solid var(--mck-gold); margin-left: 20px; }
       .nav-item { padding: 20px 30px; cursor: pointer; transition: 0.3s; opacity: 0.7; font-size: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }
       .nav-item.active { background: rgba(255,255,255,0.15); opacity: 1; font-weight: 700; border-right: 6px solid var(--mck-gold); }

       .main { margin-left: 280px; padding: 40px; }
       .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid #ddd; padding-bottom: 20px; }
        
       .control-panel { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 30px; }
       .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
       .year-label { font-size: 32px; font-weight: 700; color: var(--mck-blue); }
        input[type=range] { width: 100%; accent-color: var(--mck-blue); }

       .kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
       .card { background: white; padding: 25px; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-top: 5px solid var(--mck-blue); }
       .card h4 { margin: 0 0 10px 0; font-size: 13px; color: #666; font-weight: 500; }
       .card.val { font-size: 28px; font-weight: 700; color: var(--mck-blue); }
       .unit { font-size: 14px; font-weight: 400; color: #999; margin-left: 5px; }

       .chart-box { background: white; padding: 35px; border-radius: 8px; box-shadow: 0 6px 20px rgba(0,0,0,0.06); }
        h3 { margin-top: 0; font-size: 22px; color: var(--mck-blue); display: flex; align-items: center; }
        h3::before { content: ''; width: 6px; height: 24px; background: var(--mck-gold); margin-right: 15px; display: inline-block; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo"><h2>COWAY</h2><div style="font-size:10px; color:var(--mck-gold);">NET-ZERO MASTER</div></div>
        <div class="nav-item active">1. 전사 넷제로 목표 관리</div>
        <div class="nav-item" style="opacity:0.4">2. FINANCIAL IMPACT</div>
        <div class="nav-item" style="opacity:0.4">3. SITE ANALYSIS</div>
        <div class="nav-item" style="opacity:0.4">4. COMPLIANCE DATA</div>
    </div>

    <div class="main">
        <div class="top-bar">
            <h2 style="margin:0">전사 넷제로 목표 관리</h2>
            <div style="background:#007a33; color:white; padding:6px 15px; border-radius:20px; font-size:12px; font-weight:700">STRATEGY ALIGNED</div>
        </div>

        <div class="control-panel">
            <div class="slider-header">
                <span style="font-weight:700; color:#555">시뮬레이션 연도 선택 (2023 - 2050)</span>
                <span class="year-label" id="y-disp">2023</span>
            </div>
            <input type="range" id="y-slider" min="2023" max="2050" value="2023" oninput="updateDashboard(this.value)">
        </div>

        <div class="kpi-row">
            <div class="card"><h4>예상 배출량 (BAU)</h4><div class="val" id="v-bau">18,041</div><span class="unit">tCO2eq</span></div>
            <div class="card"><h4>목표 배출량 (Target)</h4><div class="val" id="v-target">18,000</div><span class="unit">tCO2eq</span></div>
            <div class="card"><h4>감축 필요량 (Gap)</h4><div class="val" id="v-gap" style="color:var(--red)">41</div><span class="unit">tCO2eq</span></div>
            <div class="card"><h4>감축 이행률</h4><div class="val" id="v-rate">0.2</div><span class="unit">%</span></div>
        </div>

        <div class="chart-box">
            <h3>온실가스 감축 로드맵 분석</h3>
            <div style="height: 500px;"><canvas id="wChart"></canvas></div>
        </div>
    </div>

    <script>
        const nzData = {
            yrs: Array.from({length: 28}, (_, i) => 2023 + i),
            target: ,
            bau: Array(28).fill(20000).map((v, i) => i === 0? 18041 : (i === 1? 17811 : 20000)),
            invest: 
        };
        nzData.gap = nzData.yrs.map((y, i) => Math.max(0, nzData.bau[i] - nzData.target[i] - nzData.invest[i]));

        let wChart;
        function init() {
            wChart = new Chart(document.getElementById('wChart').getContext('2d'), {
                type: 'bar',
                data: {
                    labels: nzData.yrs,
                    datasets:, fill: false, pointRadius: 0, order: 1 },
                        { label: '목표 배출량', data: nzData.target, backgroundColor: '#bdc3c7', stack: 's1', order: 2 },
                        { label: '실제 감축량', data: nzData.invest, backgroundColor: '#4a90e2', stack: 's1', order: 2 },
                        { label: '추가 필요량(Gap)', data: nzData.gap, backgroundColor: '#f1c40f', stack: 's1', order: 2 }
                    ]
                },
                options: { 
                    responsive: true, maintainAspectRatio: false,
                    plugins: { tooltip: { mode: 'index', intersect: false } },
                    scales: { x: { stacked: true }, y: { stacked: true } }
                }
            });
        }

        function updateDashboard(year) {
            const idx = year - 2023;
            document.getElementById('y-disp').innerText = year;
            const b = nzData.bau[idx];
            const t = nzData.target[idx];
            document.getElementById('v-bau').innerText = b.toLocaleString();
            document.getElementById('v-target').innerText = t.toLocaleString();
            document.getElementById('v-gap').innerText = Math.max(0, b - t).toLocaleString();
            document.getElementById('v-rate').innerText = ((1 - t/18000)*100).toFixed(1);
        }

        window.onload = () => { init(); updateDashboard(2023); };
    </script>
</body>
</html>
"""

# 3. Streamlit으로 HTML 렌더링
components.html(html_code, height=1000, scrolling=True)
