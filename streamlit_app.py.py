import streamlit as st
import pandas as pd
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="USD/KRW 환율 분석 대시보드", layout="wide")

# [필수 조건: 텍스트] st.title() 사용
st.title("📊 달러/원(USD/KRW) 환율 변동성 대시보드")
st.markdown("본 대시보드는 2025년부터 2026년까지의 월별 환율 데이터를 분석하여 시각화 정보를 제공합니다.")

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    # 데이터 생성 (2025-05 ~ 2026-05)
    dates = pd.date_range(start="2025-05-01", end="2026-05-01", freq="MS")
    prices = [1424.69, 1382.99, 1352.78, 1392.93, 1388.97, 1404.2, 1429.62, 1466.33, 1440.5, 1451.26, 1442.6, 1506.1, 1473.21]
    
    df = pd.DataFrame({"날짜": dates, "환율(원)": prices})
    # 등락률 계산: (현재가 - 이전가) / 이전가 * 100
    df["등락률(%)"] = df["환율(원)"].pct_change() * 100
    df["등락률(%)"] = df["등락률(%)"].fillna(0).round(2)
    return df

df = load_data()

# 3. 사이드바 - [필수 조건: 위젯] st.selectbox() 사용
st.sidebar.header("조회 설정")
view_option = st.sidebar.selectbox(
    "데이터 표시 방식 선택",
    ("전체 데이터 보기", "최근 6개월 보기")
)

# [필수 조건: 위젯-화면 연동] 위젯 값에 따른 데이터 필터링
display_df = df.copy()
if view_option == "최근 6개월 보기":
    display_df = df.tail(6)

# 4. 상단 지표 - [필수 조건: 데이터] st.metric() 사용
st.header("📌 주요 경제 지표")
m1, m2, m3 = st.columns(3)

latest_data = df.iloc[-1]
prev_data = df.iloc[-2]

m1.metric(label="현재 환율", value=f"{latest_data['환율(원)']} 원", 
          delta=f"{round(latest_data['환율(원)'] - prev_data['환율(원)'], 2)} 원")
m2.metric(label="전월 대비 등락률", value=f"{latest_data['등락률(%)']} %")
m3.metric(label="최고 환율 (기간 내)", value=f"{df['환율(원)'].max()} 원")

# 5. 차트 섹션 - [필수 조건: 차트] st.line_chart() 및 st.bar_chart() 사용
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 환율 추이 (Line Chart)")
    st.line_chart(display_df.set_index("날짜")["환율(원)"])

with col2:
    st.subheader("📊 월별 등락률 (Bar Chart)")
    st.bar_chart(display_df.set_index("날짜")["등락률(%)"])

# 6. 상세 분석 위젯 - [필수 조건: 위젯 & 위젯-화면 연동] st.slider() 사용
st.divider()
st.header("🔍 월별 상세 데이터 분석")

# 슬라이더를 통한 날짜 선택
selected_idx = st.slider(
    "분석할 시점을 선택하세요",
    min_value=0,
    max_value=len(df) - 1,
    value=len(df) - 1,
    format="월 index: %d"
)

target_row = df.iloc[selected_idx]

# [필수 조건: 데이터] st.table() 또는 st.dataframe() 사용
st.write(f"### {target_row['날짜'].strftime('%Y년 %m월')} 상세 지표")
st.table(pd.DataFrame([target_row]).set_index("날짜"))

# 7. 데이터 프레임 전체 출력
with st.expander("원본 데이터 프레임 확인"):
    st.dataframe(df, use_container_width=True)