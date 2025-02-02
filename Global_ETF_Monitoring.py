import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import altair as alt

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
    st.title("NH Amundi 글로벌 솔루션 본부")

# 첫 번째 행: 두 개의 컬럼
col1, col2 = st.columns(2)

# 두 번째 행: 세 개의 컬럼
col3, col4, col5 = st.columns(3)

# 파일 불러오기

file_path = "data/asset_index_df.csv"  # 로컬 또는 경로 수정
df_col1_1 = pd.read_csv(file_path, index_col=0)

# 색상 지정 (더 짙은 파란색 계열 적용)
colors = {
    "Stock": "#005BAC",  # 짙은 푸른색
    "Bond": "#FABF00",  # 중간 짙은 푸른색
    "Commodity": "#00AA4C"  # 더 깊은 푸른색
}

# 그래프 객체 생성
page1_col1 = go.Figure()

# 각 자산별로 선 추가
for asset in df_col1_1.columns:
    page1_col1.add_trace(go.Scatter(
        x=df_col1_1.index,
        y=df_col1_1[asset],
        mode="lines",
        name=asset,
        line=dict(color=colors.get(asset, "#80A1E9"), width=3),
        hoverinfo="x+y+name"
    ))

# 레이아웃 설정
page1_col1.update_layout(
    title="Asset Price Index",
    title_font=dict(size=30, family="Arial", color="#084594"),
    xaxis_title="",
    yaxis_title="Price Index (100 = 1 Year Ago)",
    template="plotly_white",
    hovermode="x unified",
    legend=dict(title="asset class", x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.5)'),
    margin=dict(l=10, r=10, t=60, b=10),
    transition=dict(duration=500, easing="linear"),
)

# col1에 선 그래프 추가
with col1:
    with st.container():
        st.plotly_chart(page1_col1, use_container_width=True)

with col2:


    # 데이터 로드 함수
    @st.cache_data
    def load_data_page1_col2():
        df = pd.read_csv("data/asset_return_weekly.csv", index_col=0, parse_dates=True)
        return df


    # 데이터 불러오기
    df_page1_col2 = load_data_page1_col2()
    df_page1_col2 = round(df_page1_col2, 2)

    # 최근 12주 데이터 필터링
    filtered_df_page1_col2 = df_page1_col2.tail(12).T
    filtered_df_page1_col2 = filtered_df_page1_col2.loc[["Stock", "Bond", "Commodity"], :]

    # 데이터 변환
    filtered_df_page1_col2 = filtered_df_page1_col2.reset_index().melt(id_vars="index", var_name="Date",
                                                                       value_name="Return")
    filtered_df_page1_col2.rename(columns={"index": "Asset"}, inplace=True)

    # Asset 컬럼을 Categorical 타입으로 변환하여 순서 유지
    asset_order = ["Commodity", "Bond", "Stock"]
    filtered_df_page1_col2["Asset"] = pd.Categorical(filtered_df_page1_col2["Asset"], categories=asset_order,
                                                     ordered=True)

    # Date 컬럼을 datetime 형식으로 변환
    filtered_df_page1_col2["Date"] = pd.to_datetime(filtered_df_page1_col2["Date"])

    # x축 정렬을 위한 순서값 추가
    filtered_df_page1_col2["DateOrder"] = range(len(filtered_df_page1_col2))
    filtered_df_page1_col2["FormattedDate"] = filtered_df_page1_col2["Date"].dt.strftime("%b %d")
    filtered_df_page1_col2["FormattedDate"] = pd.Categorical(
        filtered_df_page1_col2["FormattedDate"],
        categories=filtered_df_page1_col2.sort_values("DateOrder")["FormattedDate"].unique(),
        ordered=True
    )

    # 색상 설정
    colorscale = [[0, "#ffffff"], [0.5, "#c6dbef"], [1, "#084594"]]

    # 히트맵 데이터 정렬
    pivot_table = filtered_df_page1_col2.pivot(index="Asset", columns="FormattedDate", values="Return").loc[asset_order]

    # Plotly 히트맵 생성
    page1_col2 = go.Figure()
    page1_col2.add_trace(go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale=colorscale,
        showscale=True,
        colorbar=dict(title="Return(%)", tickfont=dict(size=10, family="Arial"), outlinewidth=0),
        hovertemplate="Date: %{x}<br>Asset: %{y}<br>Return: %{z:.2f}<extra></extra>",
    ))

    # 숫자 데이터 라벨 추가
    for i, row in enumerate(pivot_table.index):
        for j, col in enumerate(pivot_table.columns):
            page1_col2.add_trace(go.Scatter(
                x=[col],
                y=[row],
                text=[f"{pivot_table.loc[row, col]:.1f}"],
                mode="text",
                textfont=dict(size=12, family="Arial", color="#1C1C1C"),
                showlegend=False
            ))

    # 히트맵 레이아웃 조정
    page1_col2.update_layout(
        title="Asset Return(weekly)",
        title_font=dict(size=30, family="Arial", color="#084594"),
        xaxis=dict(title="", tickfont=dict(size=12, family="Arial")),
        yaxis=dict(title="", tickfont=dict(size=12, family="Arial")),
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=60, b=10),

    )
    with st.container():
        # col2에 히트맵 추가
        st.plotly_chart(page1_col2, use_container_width=True)




# CSV 파일 불러오기
df_col1_2 = pd.read_csv('data/asset_ff_aum.csv', index_col=0)

# 날짜 형식 변경
if isinstance(df_col1_2.index, pd.DatetimeIndex):
    df_col1_2.index = df_col1_2.index.strftime('%b %d')
else:
    df_col1_2.index = pd.to_datetime(df_col1_2.index).strftime('%b %d')

# 몇 주
i_col1_2 = 24


with col3:
    df_col3 = df_col1_2[['Stock']].iloc[-i_col1_2:, :]
    colors_col3 = ['#D3D3D3'] * (len(df_col3) - 1) + ['#084594']
    fig_col3 = go.Figure()
    fig_col3.add_trace(go.Bar(
        x=df_col3.index,
        y=df_col3['Stock'],
        marker=dict(color=colors_col3),
        name='Stock Values'
    ))
    fig_col3.update_layout(
        title="Stock Fund Flow/AUM",
        title_font=dict(size=30, family="Arial", color="#084594"),
        bargap=0.01,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    with st.container():
        st.plotly_chart(fig_col3, use_container_width=True)
    st.subheader("첫 번째 컬럼 (두 번째 행)")

with col4:
    df_col4 = df_col1_2[['Bond']].iloc[-i_col1_2:, :]
    colors_col4 = ['#D3D3D3'] * (len(df_col4) - 1) + ['#084594']
    fig_col4 = go.Figure()
    fig_col4.add_trace(go.Bar(
        x=df_col4.index,
        y=df_col4['Bond'],
        marker=dict(color=colors_col4),
        name='Bond Values'
    ))
    fig_col4.update_layout(
        title="Bond Fund Flow/AUM",
        title_font=dict(size=30, family="Arial", color="#084594"),
        bargap=0.01,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    with st.container():
        st.plotly_chart(fig_col4, use_container_width=True)
    st.subheader("두 번째 컬럼 (두 번째 행)")

with col5:
    df_col5 = df_col1_2[['Commodity']].iloc[-i_col1_2:, :]
    colors_col5 = ['#D3D3D3'] * (len(df_col5) - 1) + ['#084594']
    fig_col5 = go.Figure()
    fig_col5.add_trace(go.Bar(
        x=df_col5.index,
        y=df_col5['Commodity'],
        marker=dict(color=colors_col5),
        name='Commodity Fund Flow/AUM'
    ))
    fig_col5.update_layout(
        title="Commodity Fund Flow/AUM",
        title_font=dict(size=30, family="Arial", color="#084594"),
        bargap=0.01,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    with st.container():
        st.plotly_chart(fig_col5, use_container_width=True)
    st.subheader("세 번째 컬럼 (두 번째 행)")
