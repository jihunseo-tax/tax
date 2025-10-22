import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="2024 대한민국 종합소득세 계산기", layout="wide")
st.title("🇰🇷 2024 대한민국 종합소득세 자동화 웹 앱")

# ───────────────────────────────
# ✅ 1. 세율 계산 함수 (2024 대한민국 종합소득세 누진공제 기준)
# ───────────────────────────────
def calc_tax_2024(income_man):
    income = income_man * 10000  # 만원 → 원 단위 변환

    # 세율 구간 및 누진공제 (2024년 기준)
    brackets = [
        (14_000_000, 0.06, 0),
        (50_000_000, 0.15, 1_080_000),
        (88_000_000, 0.24, 5_220_000),
        (150_000_000, 0.35, 14_900_000),
        (300_000_000, 0.38, 19_400_000),
        (500_000_000, 0.40, 25_400_000),
        (1_000_000_000, 0.42, 33_400_000),
        (float('inf'), 0.45, 63_400_000),
    ]

    for limit, rate, deduction in brackets:
        if income <= limit:
            tax = income * rate - deduction
            return round(tax / 10000, 0)  # 만원 단위로 반환

def add_tax_columns(df):
    df["세금(만원)"] = df["연소득(만원)"].apply(calc_tax_2024)
    df["세율(%)"] = (df["세금(만원)"] / df["연소득(만원)"] * 100).round(2)
    # ✅ 소득구간 계산도 이 안에서 자동으로 처리
    bins = [0, 3000, 5000, 8000, 12000, 20000]
    labels = ["≤3000", "3001~5000", "5001~8000", "8001~12000", ">12000"]
    df["소득구간"] = pd.cut(df["연소득(만원)"], bins=bins, labels=labels, include_lowest=True)
    return df

# ───────────────────────────────
# ✅ 2. 세션 상태 초기화
# ───────────────────────────────
if "data" not in st.session_state:
    df_init = pd.DataFrame({
        "이름": ["김민준", "이서윤", "박지호", "최지우", "정현우"],
        "연소득(만원)": [2800, 5200, 7500, 9500, 13000]
    })
    st.session_state.data = add_tax_columns(df_init)

df = st.session_state.data

# ───────────────────────────────
# ✅ 3. 데이터 추가 / 삭제
# ───────────────────────────────
st.sidebar.header("데이터 추가 / 삭제")

with st.sidebar:
    name = st.text_input("이름 입력")
    income = st.number_input("연소득 (만원)", min_value=1000, max_value=20000, step=100)

    if st.button("데이터 추가"):
        if name.strip() == "":
            st.warning("이름을 입력하세요.")
        else:
            new_row = pd.DataFrame({"이름": [name], "연소득(만원)": [income]})
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.session_state.data = add_tax_columns(st.session_state.data)
            st.success(f"{name}님의 데이터가 추가되었습니다!")

    if len(st.session_state.data) > 0:
        delete_name = st.selectbox("삭제할 이름 선택", st.session_state.data["이름"])
        if st.button("데이터 삭제"):
            st.session_state.data = st.session_state.data[st.session_state.data["이름"] != delete_name]
            st.success(f"{delete_name}님의 데이터가 삭제되었습니다!")

# ───────────────────────────────
# ✅ 4. 데이터 테이블 표시
# ───────────────────────────────
st.subheader("📋 데이터 테이블")
st.dataframe(st.session_state.data, use_container_width=True)

# ───────────────────────────────
# ✅ 5. 요약 정보
# ───────────────────────────────
st.subheader("📊 요약 정보")
col1, col2, col3 = st.columns(3)
col1.metric("총 인원", len(st.session_state.data))
col2.metric("총 연소득(만원)", int(st.session_state.data["연소득(만원)"].sum()))
col3.metric("평균 세율(%)", round(st.session_state.data["세율(%)"].mean(), 2))

# ───────────────────────────────
# ✅ 6. 파이차트 (소득 구간별)
# ───────────────────────────────
st.subheader("🎨 소득 구간별 인원 비율")
fig = px.pie(st.session_state.data, names="소득구간", title="연소득 구간 비율",
             color="소득구간",
             color_discrete_sequence=["#B0E0FF", "#FFF9A6", "#FFD6A5", "#FFA1A1", "#C7A6FF"])
st.plotly_chart(fig, use_container_width=True)

