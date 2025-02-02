import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 파일 불러오기
file_path = "../data/asset_index_df.csv"  # 로컬 또는 경로 수정
df_col1_1 = pd.read_csv(file_path, index_col=0)

# 색상 지정 (더 짙은 파란색 계열 적용)
colors = {
    "Stock": "#005BAC",  # 짙은 푸른색
    "Bond": "#FABF00",   # 중간 짙은 푸른색
    "Commodity": "#00AA4C"  # 더 깊은 푸른색
}

# 그래프 객체 생성
fig = go.Figure()

# 각 자산별로 선 추가
for asset in df_col1_1.columns:
    fig.add_trace(go.Scatter(
        x=df_col1_1.index,
        y=df_col1_1[asset],
        mode="lines",
        name=asset,
        line=dict(color=colors.get(asset, "#80A1E9"), width=3),
        hoverinfo="x+y+name"
    ))

# 레이아웃 설정
fig.update_layout(
    title="자산군별 가격 추이",
    xaxis_title="",
    yaxis_title="가격 (기준=100)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(title="자산군", x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.5)'),
    margin=dict(l=40, r=40, t=40, b=40)
)

# Streamlit 앱 설정
st.title("ETF Fund Flow Dashboard")

# 선 그래프 표시
st.plotly_chart(fig, use_container_width=True)
