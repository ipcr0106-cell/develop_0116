# 배포할 때 뭐를 메인 페이지로 열지 질문 -> 구분하게 명칭
# app.py를 메인으로

# streamlit은 flask(백엔드까지 알아야 함)와 달리배포가 쉬움
# css(스타일) : streamlit에서 지원 안함 -> 외부 라이브러리 사용해야함 -> gemini를 활용

import streamlit as st
import pandas as pd # 데이터프레임 다루기 편함(그래프 그리기)
import numpy as np # 다차원 수치계산
import matplotlib # 시각화
import matplotlib.pyplot as plt # 그래프 그리기
import seaborn as sns # 통계적 시각화

# --- 기존 폰트 설정 코드 삭제 후 아래로 대체 ---
import koreanize_matplotlib 

# 마이너스 기호 깨짐 방지 (이것만 남겨두세요)
plt.rcParams['axes.unicode_minus'] = False

# 운영체제별 폰트 설정
if platform.system() == 'Windows':
    # 윈도우의 경우 맑은 고딕 사용
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Darwin':
    # 맥(OS X)의 경우 AppleGothic 사용
    rc('font', family='AppleGothic')
else:
    # 리눅스(배포 서버 등)의 경우 나눔고딕 등 설치된 폰트 지정
    rc('font', family='NanumGothic')

# 마이너스 기호 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False
# --- 폰트 설정 추가 끝 ---

# 여러 가지 install 필요
    # pip install streamlit pandas numpy matplotlib seaborn

# 매번 라이브러리 설치하는 게 번거로우니
    # 필요한 라이브러리를 requirements.txt 파일 만들어서 관리
    # pip install -r requirements.txt


# 외부 데이터 불러오기
    # 공공데이터 포털에서 csv 파일 다운로드
        # 
    # 코트라 무역통계에서 엑셀 파일 다운로드
st.title("📊 국세청 근로소득 데이터 분석기") # 제목

# 데이터 불러오기
file_path="국세청_근로소득 백분위(천분위) 자료_20241231.csv" # 변수에 파일 경로 저장
    # 현재 위치보다 하위의 데이터 파일을 가져오려면           ./data/: ./ 현재 위치에서 data/파일을 찾아 들어가 가져오기
    # 현재 위치보다 상위의 데이터 파일을 가져오려면 ../data/파일명.csv: ../ 현재 위치에서 상위 폴더로 올라가 data/파일을 찾아 들어가 가져오기

# 오류 방지
try : # 오류가 없으면 이 방식으로 처리하고
    # 자료 읽기
    df=pd.read_csv(file_path, encoding='euc-kr') # csv 파일 불러오기 # 인코딩 방식 지정(한글 깨짐 방지)
    st.success("✅파일 불러오기 성공") # 성공 메시지 출력
    
    # 데이터 미리 보기
    st.subheader("🔎데이터 미리 보기") # 소제목
    st.dataframe(df.head()) # 데이터프레임의 표 상단 5줄 미리 보기
    
    # 데이터 분석 그래프 그리기
    st.subheader("📈근로소득 백분위 분포 그래프") # 소제목
    
    #분석하고 싶은 열(컬럼) 선택
        #예를 들어  급여나 인원 같은 숫자 데이터가 있는 칸을 골라야 한다
    column_options=df.columns.tolist() # 데이터프레임의 열 데이터를 첫번째 이름들로 리스트로 변환
    selected_column=st.selectbox("분석할 열을 선택하세요", column_options) # 드롭다운 메뉴로 열 선택

    # 그래프 그리기(seaborn 사용)
    fig, ax=plt.subplots(figsize=(10,5)) # 그래프 크기 지정 (가로10, 세로5)
        #fig=그래프 전체 사이즈 ax=그림 그려질 영역(제목, 축 등 포함)
    ax.set_title(f"{selected_column} 분포 히스토그램") # 그래프 제목 설정
        # seaborn(좀 더 예쁘게 그려줌)
    sns.histplot(df[selected_column],ax=ax, color="#87CFEB", kde=True)
        # histplot=막대 그래프(히스토그램)
        # ax=ax: 위에서 지정한 ax 영역에 그려라
        # color='#87CEEB': 막대 색상 지정
        # kde=True: 커널 밀도 추정 곡선(부드러운 곡선) 같이 그리기
    plt.title(f"{selected_column} 분포 히스토그램") # 그래프 제목 설정
    plt.xlabel(selected_column) # x축 제목 설정(예: "급여")
    plt.ylabel("빈도수") # y축 제목 설정
    
    # 스트림릿 웹 화면에 그래프 출력
    st.pyplot(fig) # streamlit에 그래프 출력

except FileNotFoundError: # 파일명이 잘못되었을 때
    st.error(f"❌파일 불러오기 실패. '{file_path}'파일이 존재하는지, 파일 경로와 이름을 확인하세요.") # 오류 메시지 출력
except Exception as e: # syntax error 등 다른 일반 오류가 발생했을 때
    st.error(f"❌알 수 없는 오류가 발생했습니다{e}") # 일반 오류 메시지 출력 # e: 오류 내용 변수