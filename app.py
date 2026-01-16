import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import requests
import os

# --- [고급 폰트 설정: 파일 하나로 해결] ---
@st.cache_resource
def load_korean_font():
    # 폰트 파일 저장 경로 (나눔고딕)
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    
    # 폰트 파일이 없으면 다운로드
    if not os.path.exists(font_path):
        res = requests.get(font_url)
        with open(font_path, "wb") as f:
            f.write(res.content)
    
    # Matplotlib에 폰트 등록
    font_entry = fm.FontEntry(fname=font_path, name='NanumGothic')
    fm.fontManager.ttflist.insert(0, font_entry)
    plt.rcParams['font.family'] = font_entry.name
    plt.rcParams['axes.unicode_minus'] = False

# 폰트 적용
try:
    load_korean_font()
except Exception as e:
    st.warning(f"폰트 로드 중 오류 발생: {e}. 기본 폰트로 계속합니다.")

# --- [데이터 분석 앱 시작] ---
st.title("📊 국세청 근로소득 데이터 분석기")

# 파일 경로
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

try :
    # 자료 읽기
    df = pd.read_csv(file_path, encoding='euc-kr')
    st.success("✅ 파일 불러오기 성공")
    
    # 데이터 미리 보기
    st.subheader("🔎 데이터 미리 보기")
    st.dataframe(df.head())
    
    # 데이터 분석 그래프 그리기
    st.subheader("📈 근로소득 백분위 분포 그래프")
    
    # 숫자형 열만 선택 (문자열 열은 제외)
    column_options = df.select_dtypes(include=[np.number]).columns.tolist()
    if not column_options:
        column_options = df.columns.tolist()
        
    selected_column = st.selectbox("분석할 열을 선택하세요", column_options)

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # seaborn으로 히스토그램 그리기
    sns.histplot(df[selected_column], ax=ax, color="#87CEEB", kde=True)
    
    # 그래프 제목 및 축 설정 (한글 적용됨)
    ax.set_title(f"{selected_column} 분포 히스토그램", fontsize=16)
    ax.set_xlabel(selected_column, fontsize=12)
    ax.set_ylabel("빈도수", fontsize=12)
    
    # 스트림릿 웹 화면에 그래프 출력
    st.pyplot(fig)

except FileNotFoundError:
    st.error(f"❌ 파일을 찾을 수 없습니다: '{file_path}'")
except Exception as e:
    st.error(f"❌ 알 수 없는 오류 발생: {e}")