import streamlit as st
import pandas as pd

# 웹 페이지 제목 설정
st.set_page_config(page_title="예산 및 상품 관리자", page_icon="🛒")
st.title("🛒 예산 맞춤 상품 관리 프로그램")

# 1. 세션 상태(Session State) 초기화
# Streamlit은 버튼을 누를 때마다 코드가 처음부터 다시 실행되므로, 
# 데이터를 유지하기 위해 st.session_state를 사용합니다.
if "il" not in st.session_state:
    st.session_state.il = []  # 제품명 리스트
if "pl" not in st.session_state:
    st.session_state.pl = []  # 제품 가격 리스트

# 2. 예산 설정 (Input 위젯)
budget = st.number_input("💵 총 예산을 입력하세요 (원):", min_value=0, value=50000, step=1000)

st.divider()

# 3. 상품 추가 섹션
st.subheader("➕ 새로운 상품 추가")
col1, col2 = st.columns(2)

with col1:
    name_input = st.text_input("제품명", placeholder="예: 키보드")
with col2:
    price_input = st.number_input("제품 가격 (원)", min_value=0, value=0, step=100)

if st.button("상품 추가하기", use_container_width=True):
    if name_input:
        # 리스트에 추가
        st.session_state.il.append(name_input)
        st.session_state.pl.append(price_input)
        st.success(f"✅ '{name_input}' 상품이 성공적으로 추가되었습니다.")
        
        # [핵심 로직] 가격이 예산을 초과하는지 체크
        if price_input > budget:
            st.warning(f"⚠️ 예산 초과임다! (입력한 가격: {price_input:,}원 / 예산: {budget:,}원)")
    else:
        st.error("제품명을 입력해주세요!")

st.divider()

# 4. 결과 출력 및 삭제 섹션
if st.session_state.il:
    st.subheader("📋 현재 상품 목록")
    
    # 데이터를 보기 좋게 데이터프레임(표)으로 변환
    df = pd.DataFrame({
        "제품명": st.session_state.il,
        "가격(원)": st.session_state.pl
    })
    
    # 웹 화면에 깔끔하게 표로 출력
    st.dataframe(df, use_container_width=True)
    
    # 총 합계 금액 표시
    total_price = sum(st.session_state.pl)
    st.metric(label="현재 총 합계 금액", value=f"{total_price:,} 원")

    st.divider()

    # 5. 상품 삭제 섹션 (기존 di, dp 입력 로직 개선)
    st.subheader("❌ 상품 삭제")
    
    # 기존 코드처럼 따로 입력하면 오차가 생기므로, 등록된 제품 목록을 선택 상자로 제공
    delete_options = [f"[{idx+1}] {st.session_state.il[idx]} ({st.session_state.pl[idx]}원)" for idx in range(len(st.session_state.il))]
    selected_delete = st.selectbox("삭제할 상품을 선택하세요:", delete_options)
    
    if st.button("선택한 상품 삭제하기", type="primary"):
        # 선택한 상품의 인덱스 찾기
        delete_idx = delete_options.index(selected_delete)
        
        # 리스트에서 삭제 진행
        removed_name = st.session_state.il.pop(delete_idx)
        removed_price = st.session_state.pl.pop(delete_idx)
        
        st.success(f"🗑️ '{removed_name}({removed_price}원)' 상품이 삭제되었습니다.")
        st.rerun() # 삭제 후 화면 즉시 갱신

else:
    st.info("현재 등록된 상품이 없습니다. 위의 입력창에서 상품을 추가해 주세요.")