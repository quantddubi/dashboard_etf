import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(layout="wide")


# CSV 파일 불러오기
df_col1_2 = pd.read_csv('../data/asset_ff_aum.csv', index_col=0)

# 날짜 형식 변경
if isinstance(df_col1_2.index, pd.DatetimeIndex):
    df_col1_2.index = df_col1_2.index.strftime('%b %d')
else:
    df_col1_2.index = pd.to_datetime(df_col1_2.index).strftime('%b %d')

# 몇 주
i_col1_2 = 12

# 개별 자산 데이터 추출
df_col2 = df_col1_2[['Stock']].iloc[-i_col1_2:, :]
df_col3 = df_col1_2[['Bond']].iloc[-i_col1_2:, :]
df_col4 = df_col1_2[['Commodity']].iloc[-i_col1_2:, :]

# 색상 설정
colors_col1_2 = ['#D3D3D3'] * (len(df_col2) - 1) + ['#084594']
colors_col2 = ['#D3D3D3'] * (len(df_col3) - 1) + ['#084594']
colors_col3 = ['#D3D3D3'] * (len(df_col4) - 1) + ['#084594']

# 막대그래프 간격 설정
gap_value = 0.01  # 원하는 막대 간격 조정 값

# 막대그래프 생성
fig_col1_2 = go.Figure()
fig_col1_2.add_trace(go.Bar(
    x=df_col2.index,
    y=df_col2['Stock'],
    marker=dict(color=colors_col1_2),
    name='Stock Values'
))
fig_col1_2.update_layout(bargap=gap_value)

fig_col2 = go.Figure()
fig_col2.add_trace(go.Bar(
    x=df_col3.index,
    y=df_col3['Bond'],
    marker=dict(color=colors_col2),
    name='Bond Values'
))
fig_col2.update_layout(bargap=gap_value)

fig_col3 = go.Figure()
fig_col3.add_trace(go.Bar(
    x=df_col4.index,
    y=df_col4['Commodity'],
    marker=dict(color=colors_col3),
    name='Commodity Values'
))
fig_col3.update_layout(bargap=gap_value)

# Streamlit 레이아웃 설정
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(fig_col1_2, use_container_width=True)

with col2:
    st.plotly_chart(fig_col2, use_container_width=True)

with col3:
    st.plotly_chart(fig_col3, use_container_width=True)
