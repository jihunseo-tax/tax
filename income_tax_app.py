import streamlit as st

st.title("💰 대한민국 소득세 계산기 (2024 기준)")

# 사용자 입력
income = st.number_input("연간 소득을 입력하세요 (단위: 원)", min_value=0, step=1000000)

# 세율 계산
if income <= 12000000:
    tax_rate = 0.06; deduction = 0
elif income <= 46000000:
    tax_rate = 0.15; deduction = 1080000
elif income <= 88000000:
    tax_rate = 0.24; deduction = 5220000
elif income <= 150000000:
    tax_rate = 0.35; deduction = 14900000
elif income <= 300000000:
    tax_rate = 0.38; deduction = 19400000
elif income <= 500000000:
    tax_rate = 0.40; deduction = 25400000
elif income <= 1000000000:
    tax_rate = 0.42; deduction = 35400000
else:
    tax_rate = 0.45; deduction = 65400000

tax = int(income * tax_rate - deduction)

# 소득 수준 분류
if income >= 100000000:
    level = "고소득자"
elif income >= 40000000:
    level = "중간소득자"
else:
    level = "저소득자"

# 결과 표시
st.subheader("📊 계산 결과")
st.write(f"**총 소득:** {income:,} 원")
st.write(f"**적용 세율:** {tax_rate * 100:.1f}%")
st.write(f"**누진공제액:** {deduction:,} 원")
st.write(f"**산출 세금:** {tax:,} 원")
st.write(f"**소득 수준:** {level}")
