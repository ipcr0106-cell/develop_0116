import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib  # ✨ 이 줄만 추가하면 폰트 설정 코드가 필요 없습니다!

st.title("📊 국세청 근로소득 데이터 분석기")

# 파일 경로 설정 (데이터 파일이 스크립트와 같은 위치에 있다고 가정)
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try:
    # 데이터 읽기 (euc-kr 또는 cp949)
    df = pd.read_csv(file_path, encoding='euc-kr')
    st.success("✅ 파일 불러오기 성공")
    
    st.subheader("🔎 데이터 미리 보기")
    st.dataframe(df.head())
    
    st.subheader("📈 근로소득 백분위 분포 그래프")
    
    # 숫자형 데이터만 선택할 수 있도록 필터링 (그래프 오류 방지)
    column_options = df.select_dtypes(include=[np.number]).columns.tolist()
    if not column_options:
        column_options = df.columns.tolist()
        
    selected_column = st.selectbox("분석할 열을 선택하세요", column_options)

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Seaborn 히스토그램
    sns.histplot(df[selected_column], ax=ax, color="#87CEEB", kde=True)
    
    # 제목 및 라벨 설정 (koreanize-matplotlib 덕분에 한글이 깨지지 않음)
    ax.set_title(f"[{selected_column}] 분포 히스토그램", fontsize=15)
    ax.set_xlabel(selected_column)
    ax.set_ylabel("빈도수")
    
    st.pyplot(fig)

except FileNotFoundError:
    st.error(f"❌ '{file_path}' 파일을 찾을 수 없습니다.")
except Exception as e:
    st.error(f"❌ 오류 발생: {e}")