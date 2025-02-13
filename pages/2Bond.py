import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정: 와이드 모드 활성화
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        /* 배경색 변경 */
        body, [data-testid="stAppViewContainer"] {
            background-color: #F5FAFF;
            color: white;
        }
        h1 {
            color: #084594 !important;  /* 타이틀 색상 */
            font-size: 40px !important; /* 타이틀 크기 */
            font-family: Arial, sans-serif !important; /* 폰트 스타일 */
            text-align: left !important; /* 왼쪽 정렬 */
        }
    </style>
    """,
    unsafe_allow_html=True
)
with st.container():
    st.title("Global Bond Market")

# 첫 번째 열
col1, col2, col3 = st.columns(3)


# CSV 파일 불러오기
df_page2 =  pd.read_csv('./data/asset_ff,aum,return.csv',index_col=0)

# 주식 데이터 필터링
df_stocks = df_page2[df_page2.index == '채권']

df_stocks['대분류'] =['Segmentation','Segmentation','Segmentation','Segmentation','Segmentation','Segmentation','Segmentation','Credit Rating','Credit Rating','Credit Rating','Maturity','Maturity','Maturity']
df_stocks = df_stocks[['대분류','분류','ff/aum','return_1w','AUM']]

# 고유한 대분류별 색상 매핑
categories = df_stocks['대분류'].unique()
colors = {
    "Segmentation": "#005BAC",
    "Credit Rating": "#FABF00",
    "Maturity": "#00AA4C"
}

# 점도표 생성
fig1 = go.Figure()

for category in categories:
    df_filtered = df_stocks[df_stocks['대분류'] == category]
    fig1.add_trace(go.Scatter(
        x=df_filtered['return_1w'],
        y=df_filtered['ff/aum'],
        mode='markers+text',
        marker=dict(
            size=20,
            color=colors.get(category, "gray"),
            opacity=0.8
        ),
        name=category,
        text=df_filtered['분류'],  # Hover text
        hoverinfo='text',  # 마우스 오버 시 '분류' 열 텍스트 표시
        textposition='top center'  # 라벨 위치 설정
    ))

# 중심축 및 주 눈금선 스타일 설정
fig1.update_layout(
    title="Weekly Return vs. Fund Flow/AUM",
    title_font=dict(size=30, family="Arial", color="#084594"),
    xaxis_title="Weekly Return (%)",
    yaxis_title="Fund Flow / AUM",
    template="plotly_white",
    margin=dict(l=10, r=10, t=60, b=10),
    legend=dict(
        x=0.02,  # 그래프 내부 왼쪽 상단에 범례 배치
        y=0.98,
        bgcolor="rgba(255, 255, 255, 0.5)",
        bordercolor="lightgrey",
        borderwidth=1
    ),
    xaxis=dict(
        zeroline=True, zerolinewidth=2, zerolinecolor='lightgray',
        showgrid=True, gridcolor='#F0F0F0', gridwidth=0.1
    ),
    yaxis=dict(
        zeroline=True, zerolinewidth=2, zerolinecolor='lightgray',
        showgrid=True, gridcolor='#F0F0F0', gridwidth=0.1
    ),
    height = 600
)

# col1에 점도표 표시
with col1:
    st.plotly_chart(fig1)

# AUM 기준 내림차순 정렬
df_stocks = df_stocks.sort_values(by='return_1w', ascending=False)

# 가로형 막대그래프 생성
fig2 = go.Figure()
for category in colors.keys():
    df_filtered = df_stocks[df_stocks['대분류'] == category]
    fig2.add_trace(go.Bar(
        y=df_filtered['분류'],
        x=df_filtered['return_1w'],
        orientation='h',
        marker=dict(color=colors[category]),
        name=category  # 범례 추가
    ))

fig2.update_layout(
    title="Weekly Return",
    title_font=dict(size=30, family="Arial", color="#084594"),
    xaxis_title='Weekly Return(%)(%)',
    yaxis_title='',
    yaxis=dict(autorange='reversed'),  # 값이 높은 것부터 나오도록 정렬
    bargap=0.05,
    margin=dict(l=10, r=10, t=60, b=10),
    legend=dict(
        x=0.02,  # 그래프 내부 왼쪽 상단에 범례 배치
        y=0.98,
        bgcolor="rgba(255, 255, 255, 0.5)",
        bordercolor="lightgrey",
        borderwidth=1
    ),
    height = 600
)

# col2에 막대그래프 표시
with col2:
    st.plotly_chart(fig2)

# 데이터프레임도 화면에 표시
# st.write("Filtered Data (Stocks Only):")
# st.dataframe(df_stocks)

# AUM 기준 내림차순 정렬
df_stocks_ff_aum = df_stocks.sort_values(by='ff/aum', ascending=False)

# 가로형 막대그래프 생성
fig2 = go.Figure()
for category in colors.keys():
    df_filtered_ff_aum = df_stocks_ff_aum[df_stocks_ff_aum['대분류'] == category]
    fig2.add_trace(go.Bar(
        y=df_filtered_ff_aum['분류'],
        x=df_filtered_ff_aum['ff/aum'],
        orientation='h',
        marker=dict(color=colors[category]),
        name=category  # 범례 추가
    ))

fig2.update_layout(
    title='Weekly Fund Flow/AUM',
    title_font=dict(size=30, family="Arial", color="#084594"),
    xaxis_title='Fund Flow/AUM(%)',
    yaxis_title='',
    yaxis=dict(autorange='reversed'),  # 값이 높은 것부터 나오도록 정렬
    bargap=0.05,
    margin=dict(l=10, r=10, t=60, b=10),
    legend=dict(
        x=0.98,  # 그래프 내부 왼쪽 상단에 범례 배치
        y=0.02,
        bgcolor="rgba(255, 255, 255, 0.5)",
        bordercolor="lightgrey",
        borderwidth=1
    ),
    height = 600
)
with col3:
    st.plotly_chart(fig2)


# AUM 기준 내림차순 정렬
df_stocks_ff_aum = df_stocks.sort_values(by='ff/aum', ascending=False)

# 가로형 막대그래프 생성
fig2 = go.Figure()
for category in colors.keys():
    df_filtered_ff_aum = df_stocks_ff_aum[df_stocks_ff_aum['대분류'] == category]
    fig2.add_trace(go.Bar(
        y=df_filtered_ff_aum['분류'],
        x=df_filtered_ff_aum['ff/aum'],
        orientation='h',
        marker=dict(color=colors[category]),
        name=category  # 범례 추가
    ))

fig2.update_layout(
    title='AUM 기준 가로형 막대그래프',
    xaxis_title='Fund Flow/AUM(%)',
    yaxis_title='',
    yaxis=dict(autorange='reversed'),  # 값이 높은 것부터 나오도록 정렬
    bargap=0.05,
    margin=dict(l=10, r=10, t=60, b=10),
    legend_title="Classification",
    legend=dict(
        x=0.02,  # 그래프 내부 왼쪽 상단에 범례 배치
        y=0.98,
        bgcolor="rgba(255, 255, 255, 0.5)",
        bordercolor="lightgrey",
        borderwidth=1
    )
)
