import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(layout="wide")

# 데이터 로드 함수
@st.cache_data
def load_data_col1_1():
    df = pd.read_csv("../data/asset_return_weekly.csv", index_col=0, parse_dates=True)
    return df

# 데이터 불러오기
df_col1_1 = load_data_col1_1()
df_col1_1 = round(df_col1_1, 2)  # 소수점 두 자리 반올림

# 최근 12주 데이터 필터링 (모든 자산 포함)
filtered_df_col1_1 = df_col1_1.tail(24).T
filtered_df_col1_1 = filtered_df_col1_1.loc[["Stock", "Bond", "Commodity"], :]

# 데이터 변환: Plotly를 위한 DataFrame 구조 변경
filtered_df_col1_1 = filtered_df_col1_1.reset_index().melt(id_vars="index", var_name="Date", value_name="Return")
filtered_df_col1_1.rename(columns={"index": "Asset"}, inplace=True)

# "Asset" 컬럼을 Categorical 타입으로 변환하여 순서 유지
asset_order = ["Commodity", "Bond", "Stock"]
filtered_df_col1_1["Asset"] = pd.Categorical(filtered_df_col1_1["Asset"], categories=asset_order, ordered=True)

# Date 컬럼을 datetime 형식으로 변환
filtered_df_col1_1["Date"] = pd.to_datetime(filtered_df_col1_1["Date"])

# x축 정렬을 위한 순서값 추가
filtered_df_col1_1["DateOrder"] = range(len(filtered_df_col1_1))
filtered_df_col1_1["FormattedDate"] = filtered_df_col1_1["Date"].dt.strftime("%b %d")
filtered_df_col1_1["FormattedDate"] = pd.Categorical(
    filtered_df_col1_1["FormattedDate"],
    categories=filtered_df_col1_1.sort_values("DateOrder")["FormattedDate"].unique(),
    ordered=True
)


# 폰트 크기 및 스타일 설정
font_size = 12
font_family = "Arial"

# 색상 설정 (값의 크기에 따라 색상 조정)
colorscale = [[0, "#ffffff"], [0.5, "#c6dbef"], [1, "#084594"]]

# 히트맵 데이터를 올바른 순서로 정렬
pivot_table = filtered_df_col1_1.pivot(index="Asset", columns="FormattedDate", values="Return").loc[asset_order]

# Plotly 히트맵 생성
fig_col1_1 = go.Figure()
fig_col1_1.add_trace(go.Heatmap(
    z=pivot_table.values,
    x=pivot_table.columns,
    y=pivot_table.index,
    colorscale=colorscale,
    showscale=True,
    colorbar=dict(title="Return", tickfont=dict(size=font_size, family=font_family), outlinewidth=0),
    hovertemplate="Date: %{x}<br>Asset: %{y}<br>Return: %{z:.2f}<extra></extra>",
))

# 숫자 데이터 라벨 추가
for i, row in enumerate(pivot_table.index):
    for j, col in enumerate(pivot_table.columns):
        fig_col1_1.add_trace(go.Scatter(
            x=[col],
            y=[row],
            text=[f"{pivot_table.loc[row, col]:.1f}"],
            mode="text",
            textfont=dict(size=font_size, family=font_family, color="#1C1C1C"),
            showlegend=False
        ))

# 히트맵 레이아웃 조정
fig_col1_1.update_layout(
    title="Asset Return Heatmap",
    title_font=dict(size=font_size + 2, family=font_family),
    xaxis=dict(title="", tickfont=dict(size=font_size, family=font_family)),
    yaxis=dict(title="", tickfont=dict(size=font_size, family=font_family)),
    plot_bgcolor="white"
)


# Streamlit 레이아웃 설정
col1, col2 = st.columns([2, 2])

with col1:
    st.plotly_chart(fig_col1_1, use_container_width=True)
