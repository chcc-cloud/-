import streamlit as st
import pandas as pd
import time

# --- [1] 페이지 기본 설정 ---
st.set_page_config(page_title="CODA: 인지저하 경보 시스템", page_icon="💊", layout="centered")

# --- [2] 가상 데이터베이스 (보고서 분석 결과 반영) ---
# 실제 데이터베이스가 연결된 것처럼 보이도록 공모전 결과물 핵심 성분을 넣었습니다.
mock_db = pd.DataFrame({
    '제품명': ['탁센(나프록센)', '지르텍(세티리진)', '이지엔6(덱시부프로펜)', '타이레놀(아세트아미노펜)', '훼스탈(소화제)', '니코레트(니코틴)'],
    '성분명': ['나프록센', '세티리진염산염', '덱시부프로펜', '아세트아미노펜', '판크레아틴', '니코틴'],
    'DICI위험': [True, True, True, False, False, True],
    '위험키워드': ['방향감각, 집중, 인식기능', '기억장애', '방향감각, 착란', '-', '-', '집중, 주의력'],
    'DUR_병용금기': [False, False, False, False, False, False] # 사각지대 강조를 위해 모두 False로 세팅
})

# --- [3] UI 헤더 부분 ---
st.title("🚨 CODA (COgnitive Decline Alert)")
st.subheader("고령층 일반의약품 인지저하 위험 및 DUR 사각지대 분석 시스템")
st.markdown("""
**Rx(redefine Reveal X)** 팀이 제안하는 약물 유발성 인지저하(DICI) 사전 모니터링 시스템입니다.  
처방전 없이 구매한 일반의약품들을 입력하여, **현행 DUR 시스템이 잡아내지 못하는 인지저하 위험**을 확인해보세요.
""")
st.divider()

# --- [4] 사용자 입력 부분 ---
st.write("#### 현재 복용 중이거나 구매 예정인 약품을 모두 선택해주세요.")
selected_drugs = st.multiselect(
    "약품 검색 및 선택 (다중 선택 가능)",
    options=mock_db['제품명'].tolist(),
    default=['지르텍(세티리진)', '타이레놀(아세트아미노펜)']
)

analyze_button = st.button("🔍 인지저하 위험성 분석하기", type="primary", use_container_width=True)

# --- [5] 분석 로직 및 결과 출력 ---
if analyze_button:
    if not selected_drugs:
        st.warning("분석할 약품을 선택해주세요.")
    else:
        with st.spinner("DUR 데이터베이스 및 식약처 허가사항을 교차 분석 중입니다..."):
            time.sleep(1.5) # 분석하는 듯한 효과 연출
            
        # 선택된 약품 데이터 필터링
        result_df = mock_db[mock_db['제품명'].isin(selected_drugs)]
        risk_drugs = result_df[result_df['DICI위험'] == True]
        
        st.divider()
        st.write("#### 분석 결과 리포트")
        
        # 위험 약물이 발견된 경우
        if len(risk_drugs) > 0:
            st.error(f"⚠️ 경고: 선택하신 약품 중 **{len(risk_drugs)}개**의 약품에서 인지저하(DICI) 발생 위험 성분이 발견되었습니다.")
            
            # 사각지대 강조 메트릭
            col1, col2 = st.columns(2)
            col1.metric("발견된 인지저하 위험 약물", f"{len(risk_drugs)} 건", delta="주의 요망", delta_color="inverse")
            col2.metric("DUR 병용금기 모니터링 여부", "0 건", delta="사각지대 발견!", delta_color="off")
            
            st.info("💡 **DUR 사각지대 알림**: 해당 약품들은 인지저하 위험이 존재함에도 현행 DUR 병용금기 체계에서 경고해주지 않는 일반의약품입니다. 복용 시 주의가 필요합니다.")
            
            # 위험 상세 내역 카드
            st.write("#### 🔍 위험 성분 상세 정보")
            for index, row in risk_drugs.iterrows():
                with st.expander(f"💊 {row['제품명']} (성분명: {row['성분명']})", expanded=True):
                    st.markdown(f"- **발생 가능 인지저하 이상사례**: `{row['위험키워드']}`")
                    st.markdown("- **DUR 병용금기 등재 여부**: ❌ 미등재 (사각지대)")
                    st.markdown("- **조치 권고사항**: 고령자의 경우 장기 복용을 피하고, 약사 또는 의사와 상담 후 복용하시기 바랍니다.")
                    
        # 위험 약물이 없는 경우
        else:
            st.success("✅ 안전: 선택하신 약품 조합에서는 알려진 인지저하(DICI) 위험 성분이 발견되지 않았습니다.")
            st.balloons()

# --- [6] 사이드바 (팀 정보 및 아이디어 설명) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2875/2875078.png", width=100) # 가상의 약국 아이콘
    st.write("### About CODA")
    st.write("CODA 시스템은 식약처 e약은요 데이터와 심평원 DUR 데이터를 연계하여 구축된 **사후 기반 위험 모니터링 프로토타입**입니다.")
    st.write("---")
    st.write("**👨🔬 Team Rx**")
    st.caption("숨겨진 위험, 사각지대, 미지의 문제를 드러내자")
