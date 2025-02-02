import plotly.graph_objects as go
import numpy as np

# 샘플 데이터 (12x3 행렬)
np.random.seed(42)
data = np.random.randint(1, 100, size=(3, 12))  # 1~100 사이의 랜덤 숫자

# 히트맵 생성
fig = go.Figure(data=go.Heatmap(
    z=data,  # 데이터
    x=[f'Month {i+1}' for i in range(12)],  # 가로축 라벨
    y=['Row 1', 'Row 2', 'Row 3'],  # 세로축 라벨
    colorscale='Viridis',  # 색상 스케일 (Plasma, Cividis 등 변경 가능)
    text=data,  # 히트맵 안에 들어갈 숫자
    texttemplate="%{text}",  # 숫자 표시 형식
    showscale=True  # 컬러바 표시
))

# 레이아웃 설정
fig.update_layout(
    title="12x3 Heatmap with Annotations",
    xaxis=dict(title="Months", tickmode="array", tickvals=list(range(12))),
    yaxis=dict(title="Categories", tickmode="array", tickvals=list(range(3))),
    plot_bgcolor='white'
)

# 그래프 출력
fig.show()