import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 삼성/SK 스타일 프리미엄 테마 설정
st.set_page_config(page_title="코웨이 넷제로 관리 시스템", layout="wide")

st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
    
    .main { background-color: #ffffff; padding-top: 2rem; }
    .title-container { border-bottom: 3px solid #000000; margin-bottom: 3rem; padding-bottom: 1rem; }
    .main-title { font-size: 2.8rem; font-weight: 700; color: #111; letter-spacing: -0.05rem; }
    
    .premium-card {
        background: #f8fafc; padding: 2.5rem; border-radius: 12px;
        border: 1px solid #e2e8f0; min-height: 240px; margin-bottom: 2rem;
    }
    .card-title { font-size: 1.2rem; font-weight: 700; color: #1e293b; margin-bottom: 1.5rem; border-left: 5px solid #1e293b; padding-left: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터베이스 재구축 (차장님 엑셀 100% 동기화)
years = list(range(2023, 2051))

# [수정] 예상 배출량 (BAU): 20,000톤 절대 고정 (넘지 않음)
expected_emissions = [20000] * 28 

# 목표 배출량 (3행): 2050년 0달성 로직
target_emissions = [18000, 17139, 16237, 15335, 14433, 13531, 12629, 11727, 10824, 9922, 9000, 
                    7747, 7543, 7305, 7062, 6807, 6542, 6268, 5980, 5678, 5362, 5026, 4670, 4293, 3892, 3467, 3014, 0]

# 실제 감축량 (투자 및 REC 합계)
actual_reductions = [0, 1135.9, 2312.6, 3489.3, 4666, 5842.7, 7019.4, 8196.1, 9372.8, 10549.5, 11726, 
                     13274, 13753, 14265, 14782, 15312, 15852, 16401, 16963, 17540, 18131, 18741, 19372, 20024, 20698, 21399, 22127, 25415]

# 비용 데이터 (백만원 단위)
invest_costs = [6.4, 194.8, 585.4, 546.8, 612.9, 382.2, 286.7, 209.3, 131.8, 36.0, 179.5] + [374 + 10*i for i in range(17)]
save_costs = [0, 21.3, 60.5, 105.8, 155.5, 209.2, 266.5, 327.1, 368.7, 373.2, 379.2] + [400 for _ in range(17)]

df = pd.DataFrame({
    '연도': years, '넷제로 목표 배출량': target_emissions, '예상 배출량': expected_emissions,
    '실제 감축량': actual_reductions, '투자 비용': invest_costs, '감축 비용': save_costs
})

# 계산 로직
df['감축 필요량'] = df['예상 배출량'] - df['넷제로 목표 배출량']
df['연도별 비용'] = df['감축 비용'] - df['투자 비용']

# 3. 화면 구성
st.markdown('<div class="title-container"><span class="main-title">코웨이 넷제로 관리 시스템</span></div>', unsafe_allow_html=True)

g_col1, g_col2 = st.columns(2, gap="large")

with g_col1:
    st.markdown("### 📈 온실가스 감축 로드맵 (1. 넷제로 로드맵)")
    fig1 = go.Figure()
    
    # 20,000톤 BAU 점선
    fig1.add_trace(go.Scatter(x=df['연도'], y=df['예상 배출량'], name='BAU (20,000톤 고정)', 
                               line=dict(color='#94a3b8', width=2, dash='dash')))
    
    # 실제 감축 현황 (막대)
    fig1.add_trace(go.Bar(x=df['연도'], y=df['실제 감축량'], name='누적 감축량', marker_color='#3b82f6'))
    
    # 목표선 (Red Line)
    fig1.add_trace(go.Scatter(x=df['연도'], y=df['넷제로 목표 배출량'], name='목표 배출량', 
                               line=dict(color='#ef4444', width=3)))
    
    fig1.update_layout(height=450, hovermode="x unified", template="none",
                      yaxis=dict(title="단위: 톤", range=[0, 25000]))
    st.plotly_chart(fig1, use_container_width=True)

with g_col2:
    st.markdown("### 💰 투자 및 감축비용 분석")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=df['연도'], y=df['투자 비용'], name='투자 비용', marker_color='#1d4ed8'))
    fig2.add_trace(go.Scatter(x=df['연도'], y=df['감축 비용'], name='감축 비용', line=dict(color='#047857', width=3)))
    
    fig2.update_layout(height=450, hovermode="x unified", template="none", yaxis_title="단위: 억 원")
    st.plotly_chart(fig2, use_container_width=True)

# 연도 선택 슬라이더
st.markdown('---')
selected_year = st.select_slider("📅 분석 연도 선택", options=years, value=2030)
curr = df[df['연도'] == selected_year].iloc[0]

# 하단 정보 카드
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"""<div class="premium-card">
        <div class="card-title">📉 {selected_year}년 온실가스 요약</div>
        - 예상 배출량: <b>{curr['예상 배출량']:,.0f} 톤</b><br>
        - 목표 배출량: <b>{curr['넷제로 목표 배출량']:,.0f} 톤</b><br>
        - 실제 감축량: <b>{curr['실제 감축량']:,.0f} 톤</b>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="premium-card">
        <div class="card-title">💵 {selected_year}년 재무 요약</div>
        - 투자 비용: <b>{curr['투자 비용']:.1f} 억 원</b><br>
        - 감축 비용: <b>{curr['감축 비용']:.1f} 억 원</b><br>
        - 순 비용: <b>{curr['연도별 비용']:.1f} 억 원</b>
    </div>""", unsafe_allow_html=True)
