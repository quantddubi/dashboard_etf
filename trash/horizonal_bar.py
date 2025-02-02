import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# CSV 파일 불러오기
file_path = "../data/page2_ff,aum.csv"  # 실제 파일 경로 적용
df_page2 = pd.read_csv(file_path, index_col=0)

# 주식 데이터 필터링 (인덱스 필터링 또는 컬럼 기준 필터링)
df_stocks = df_page2[df_page2.index == '주식'].copy()  # 복사본 생성

# '대분류' 리스트 할당 (길이 검증 필요)
category_list = ['Country','Country','Country','Country','Country','Country','Country','Country','Country',
                 'Style','Style','Style','Style','Style',
                 'Sector','Sector','Sector','Sector','Sector','Sector','Sector','Sector','Sector','Sector']

# 리스트 길이 확인
if len(category_list) == len(df_stocks):
    df_stocks.loc[:, '대분류'] = category_list
else:
    st.warning(f"경고: '대분류' 리스트 길이({len(category_list)})가 데이터 길이({len(df_stocks)})와 맞지 않습니다.")

# 필요한 컬럼 선택
df_stocks = df_stocks[['대분류', '분류', 'ff/aum', 'return_1w', 'AUM']]

# AUM 기준 내림차순 정렬
df_stocks = df_stocks.sort_values(by='return_1w', ascending=False)

# 고유한 대분류별 색상 매핑
colors = {
    "Country": "#005BAC",
    "Style": "#FABF00",
    "Sector": "#00AA4C"
}
bar_colors = df_stocks['대분류'].map(colors)

# Streamlit 앱 구성
st.title("Filtered Stocks Data Dashboard")

# 데이터프레임 출력
st.write("### 필터링된 주식 데이터")
st.dataframe(df_stocks)

# 가로형 막대그래프 생성
fig = go.Figure()
for category in colors.keys():
    df_filtered = df_stocks[df_stocks['대분류'] == category]
    fig.add_trace(go.Bar(
        y=df_filtered['분류'],
        x=df_filtered['return_1w'],
        orientation='h',
        marker=dict(color=colors[category]),
        name=category  # 범례 추가
    ))

fig.update_layout(
    title='AUM 기준 가로형 막대그래프',
    xaxis_title='1week return',
    yaxis_title='',
    yaxis=dict(autorange='reversed'),  # 값이 높은 것부터 나오도록 정렬,
    bargap=0.05,
    margin=dict(l=10, r=10, t=60, b=10),
    legend_title="대분류",
    legend=dict(
        x=0.02,  # 그래프 내부 왼쪽 상단에 범례 배치
        y=0.98,
        bgcolor="rgba(255, 255, 255, 0.5)",
        bordercolor="lightgrey",
        borderwidth=1
    )
)

# Streamlit에 그래프 출력
st.plotly_chart(fig)