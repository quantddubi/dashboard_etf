import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정: 와이드 모드 활성화
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        /* 전체 배경색 변경 */
        [data-testid="stAppViewContainer"] {
            background-color: #F5FAFF;
        }

        /* 제목 스타일 */
        h1 {
            color: #084594 !important;  /* 타이틀 색상 */
            font-size: 40px !important; /* 타이틀 크기 */
            font-family: Arial, sans-serif !important; /* 폰트 스타일 */
            text-align: left !important; /* 왼쪽 정렬 */
        }

        /* 커스텀 메트릭 박스 */
        .ehvl34q0 {
            background-color: #FFFFFF; /* 배경색 */
            padding: 5px;
            border-radius: 15px;
            text-align: left;
            color: white;
            font-size: 20px;
            font-weight: bold;
        }

    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.title("NH Amundi 글로벌솔루션본부")

###########
# Metrics #
###########
df_metrics = pd.read_csv('./data/page1_metrics_data.csv', index_col=0)
df_metrics_index1 = df_metrics.loc[1,['US','Europe','Japan','China','Korea','Energy&Fuel','fx']].round(1)
df_metrics_index2 = df_metrics.loc[1,['Unnamed: 49','Unnamed: 50']].round(2)
df_metrics_index = pd.concat([df_metrics_index1,df_metrics_index2])
formatted_values = df_metrics_index.apply(lambda x: f"{x:,}")

df_metrics_chg = round(df_metrics.iloc[0,:],2)


col1_1, col1_2, col1_3, col1_4, col1_5, col1_6, col1_7, col1_8, col1_9 = st.columns(9)

col1_1.metric(label="S&P500", value=f"{formatted_values.iloc[0]} pt",
              delta=f"{df_metrics_chg.iloc[0]} %", label_visibility='visible', border=True)
col1_2.metric(label="Euro Stoxx", value=f"{formatted_values.iloc[1]} pt",
              delta=f"{df_metrics_chg.iloc[1]} %", label_visibility='visible', border=True)
col1_3.metric(label="Nikkei", value=f"{formatted_values.iloc[2]} pt",
              delta=f"{df_metrics_chg.iloc[2]} %", label_visibility='visible', border=True)
col1_4.metric(label="CSI300", value=f"{formatted_values.iloc[3]} pt",
              delta=f"{df_metrics_chg.iloc[3]} %", label_visibility='visible', border=True)
col1_5.metric(label="KOSPI", value=f"{formatted_values.iloc[4]} pt",
              delta=f"{df_metrics_chg.iloc[4]} %", label_visibility='visible', border=True)
col1_6.metric(label="US_2y", value=f"{formatted_values.iloc[8]} %",
              delta=f"{df_metrics_chg.iloc[6]} %p", label_visibility='visible', border=True)
col1_7.metric(label="US_10y", value=f"{formatted_values.iloc[7]} %",
              delta=f"{df_metrics_chg.iloc[5]} %p", label_visibility='visible', border=True)
col1_8.metric(label="Commodity", value=f"{formatted_values.iloc[5]} USD",
              delta=f"{df_metrics_chg.iloc[7]} %", label_visibility='visible', border=True)
col1_9.metric(label="USD/KRW", value=f"{formatted_values.iloc[6]} WON",
              delta=f"{df_metrics_chg.iloc[8]} WON", label_visibility='visible', border=True)

# 첫 번째 행: 두 개의 컬럼
col1, col2 = st.columns(2)

# 두 번째 행: 세 개의 컬럼
col3, col4, col5 = st.columns(3)

# 파일 불러오기

file_path = "./data/asset_index_df.csv"  # 로컬 또는 경로 수정
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
        df = pd.read_csv("./data/asset_return_weekly.csv", index_col=0, parse_dates=True)
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


##############################
# Bottom_4주 누적 순유입액/AUM  #
##############################

# 데이터 불러오기
df_page1_bottom = pd.read_csv('./data/page1_ff,aum_4w_cul.csv', index_col=0, parse_dates=True).iloc[3:]
df_page1_bottom = round(df_page1_bottom,2)

# 전처리
df_page1_bottom = df_page1_bottom.T
df_page1_bottom_processing = df_page1_bottom.reset_index().melt(id_vars="index", var_name="Date",
                                                             value_name="ff/aum")
df_page1_bottom_processing.rename(columns={"index": "Asset"}, inplace=True)


# Asset 컬럼을 Categorical 타입으로 변환하여 순서 유지
asset_order = ["Commodity", "Bond", "Stock"]
df_page1_bottom_processing["Asset"] = pd.Categorical(df_page1_bottom_processing["Asset"], categories=asset_order,
                                                 ordered=True)

# Date 컬럼을 datetime 형식으로 변환
df_page1_bottom_processing["Date"] = pd.to_datetime(df_page1_bottom_processing["Date"])

 # x축 정렬을 위한 순서값 추가
df_page1_bottom_processing["DateOrder"] = range(len(df_page1_bottom_processing))
df_page1_bottom_processing["FormattedDate"] = df_page1_bottom_processing["Date"].dt.strftime("%b %d")
df_page1_bottom_processing["FormattedDate"] = pd.Categorical(
    df_page1_bottom_processing["FormattedDate"],
    categories=df_page1_bottom_processing.sort_values("DateOrder")["FormattedDate"].unique(),
    ordered=True
)

# 색상 설정
colorscale = [[0, "#ffffff"], [0.5, "#c6dbef"], [1, "#084594"]]

pivot_table_4w = df_page1_bottom_processing.pivot(index="Asset", columns="FormattedDate", values="ff/aum").loc[asset_order]

# Plotly 히트맵 생성
page1_bottom = go.Figure()
page1_bottom.add_trace(go.Heatmap(
    z=pivot_table_4w.values,
    x=pivot_table_4w.columns,
    y=pivot_table_4w.index,
    colorscale=colorscale,
    showscale=True,
    colorbar=dict(title="FF/AUM(%)", tickfont=dict(size=10, family="Arial"), outlinewidth=0),
    hovertemplate="Date: %{x}<br>Asset: %{y}<br>FF/AUM(%): %{z:.2f}<extra></extra>",
))

# 숫자 데이터 라벨 추가
for i, row in enumerate(pivot_table_4w.index):
    for j, col in enumerate(pivot_table_4w.columns):
        page1_col2.add_trace(go.Scatter(
            x=[col],
            y=[row],
            text=[f"{pivot_table_4w.loc[row, col]:.1f}"],
            mode="text",
            textfont=dict(size=12, family="Arial", color="#1C1C1C"),
            showlegend=False
        ))

# 히트맵 레이아웃 조정
page1_bottom.update_layout(
    title="FundFlow(4-week cumulative)/AUM(%)",
    title_font=dict(size=30, family="Arial", color="#084594"),
    xaxis=dict(title="", tickfont=dict(size=12, family="Arial")),
    yaxis=dict(title="", tickfont=dict(size=12, family="Arial")),
    plot_bgcolor="white",
    margin=dict(l=5, r=5, t=60, b=10),

)
with st.container():
    # col2에 히트맵 추가
    st.plotly_chart(page1_bottom, use_container_width=True)

