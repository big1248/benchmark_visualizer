import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import glob
from pathlib import Path
import numpy as np
from scipy import stats

import streamlit as st
import requests
import zipfile
import os

@st.cache_data(ttl=86400)
def download_data_from_github():
    """GitHub Releases에서 데이터 다운로드"""
    
    data_dir = Path('./data')
    
    # 이미 있으면 스킵
    if data_dir.exists() and len(list(data_dir.glob('*.csv'))) > 0:
        return
    
    try:
        # 기존 data 폴더 삭제
        if data_dir.exists():
            import shutil
            shutil.rmtree(data_dir)
        
        repo = "kjs9964/benchmark_visualizer"
        tag = "v2.2.0"
        url = f"https://github.com/{repo}/releases/download/{tag}/data.zip"
        
        # 다운로드
        st.info("📥 데이터 다운로드 중...")
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        # 저장 및 압축 해제
        with open('data.zip', 'wb') as f:
            f.write(response.content)
        
        with zipfile.ZipFile('data.zip', 'r') as zip_ref:
            zip_ref.extractall('.')
        
        os.remove('data.zip')
        
        # 검증
        if not data_dir.exists():
            raise Exception("data 폴더가 생성되지 않았습니다")
        
        csv_count = len(list(data_dir.glob('*.csv')))
        if csv_count == 0:
            raise Exception("CSV 파일이 없습니다")
        
        st.success(f"✅ 데이터 로드 완료 ({csv_count}개 파일)")
        
    except Exception as e:
        st.error(f"❌ 데이터 다운로드 실패: {str(e)}")
        st.error("GitHub Release 확인: https://github.com/kjs9964/benchmark_visualizer/releases")
        st.stop()

# 페이지 설정
st.set_page_config(
    page_title="LLM 벤치마크 시각화",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 다국어 지원 설정
LANGUAGES = {
    'ko': {
        'title': 'LLM 벤치마크 결과 시각화 도구',
        'data_dir': '데이터 디렉토리',
        'filters': '필터 옵션',
        'testname': '테스트명',
        'all': '전체',
        'model': '모델',
        'detail_type': '상세도',
        'prompting': '프롬프팅 방식',
        'session': '세션',
        'problem_type': '문제 유형',
        'image_problem': '이미지 문제',
        'text_only': '텍스트만',
        'year': '연도',
        'law_type': '법령 구분',
        'law': '법령',
        'non_law': '비법령',
        'overview': '전체 요약',
        'model_comparison': '모델별 비교',
        'law_analysis': '법령/비법령 분석',
        'subject_analysis': '과목별 분석',
        'year_analysis': '연도별 분석',
        'incorrect_analysis': '오답 분석',
        'difficulty_analysis': '난이도 분석',
        'testset_stats': '테스트셋 통계',
        'total_problems': '총 문제 수',
        'accuracy': '정확도',
        'correct': '정답',
        'wrong': '오답',
        'law_problems': '법령 문제',
        'non_law_problems': '비법령 문제',
        'correct_rate': '정답률',
        'wrong_rate': '오답률',
        'performance_by_model': '모델별 성능 지표',
        'comparison_chart': '모델별 성능 비교 차트',
        'overall_comparison': '전체 테스트 비교',
        'heatmap': '모델별 테스트셋 정답도 히트맵',
        'law_ratio': '법령/비법령 전체 통계',
        'model_law_performance': '모델별 법령/비법령 성능 비교',
        'law_distribution': '모델별 법령/비법령 정답도',
        'subject_performance': '과목별 성능',
        'year_performance': '연도별 성능',
        'top_incorrect': '오답률 높은 문제 Top 20',
        'all_models_incorrect': '모든 모델이 틀린 문제',
        'most_models_incorrect': '대부분 모델이 틀린 문제 (≥20%)',
        'test_info': '테스트',
        'problem_id': '문제번호',
        'incorrect_count': '오답 모델수',
        'correct_count': '정답 모델수',
        'total_models': '총 모델수',
        'attempted_models': '시도한 모델',
        'question': '문제',
        'difficulty_score': '난이도 점수',
        'by_session': '세션별',
        'by_subject': '과목별',
        'by_year': '연도별',
        'problem_count': '문제 수',
        'session_distribution': '세션별 문제 분포',
        'subject_distribution': '과목별 문제 분포',
        'year_distribution': '연도별 문제 분포',
        'law_distribution_stat': '법령/비법령 문제 분포',
        'basic_stats': '기본 통계',
        'help': '도움말',
        'new_features': '새로운 기능',
        'existing_features': '기존 기능',
        'current_data': '현재 표시 중인 데이터',
        'problems': '개 문제',
        'session_filter': '특정 세션의 결과만 분석',
        'incorrect_pattern': '어려운 문제와 오답 패턴 분석',
        'difficulty_comparison': '문제 난이도별 모델 성능 비교',
        'problem_type_filter': '이미지/텍스트 문제 구분',
        'basic_filters': '테스트명, 모델, 상세도, 프롬프팅 방식으로 필터링',
        'law_analysis_desc': '법령/비법령 구분 분석',
        'detail_analysis': '과목별, 연도별 상세 분석',
        'font_size': '폰트 크기',
    },
    'en': {
        'title': 'LLM Benchmark Results Visualization Tool',
        'data_dir': 'Data Directory',
        'filters': 'Filter Options',
        'testname': 'Test Name',
        'all': 'All',
        'model': 'Model',
        'detail_type': 'Detail Type',
        'prompting': 'Prompting Method',
        'session': 'Session',
        'problem_type': 'Problem Type',
        'image_problem': 'Image Problem',
        'text_only': 'Text Only',
        'year': 'Year',
        'law_type': 'Law Type',
        'law': 'Law',
        'non_law': 'Non-Law',
        'overview': 'Overview',
        'model_comparison': 'Model Comparison',
        'law_analysis': 'Law/Non-Law Analysis',
        'subject_analysis': 'Subject Analysis',
        'year_analysis': 'Year Analysis',
        'incorrect_analysis': 'Incorrect Answer Analysis',
        'difficulty_analysis': 'Difficulty Analysis',
        'testset_stats': 'Test Set Statistics',
        'total_problems': 'Total Problems',
        'accuracy': 'Accuracy',
        'correct': 'Correct',
        'wrong': 'Wrong',
        'law_problems': 'Law Problems',
        'non_law_problems': 'Non-Law Problems',
        'correct_rate': 'Correct Rate',
        'wrong_rate': 'Wrong Rate',
        'performance_by_model': 'Performance Metrics by Model',
        'comparison_chart': 'Model Performance Comparison Chart',
        'overall_comparison': 'Overall Test Comparison',
        'heatmap': 'Model × Test Set Accuracy Heatmap',
        'law_ratio': 'Law/Non-Law Overall Statistics',
        'model_law_performance': 'Model Law/Non-Law Performance Comparison',
        'law_distribution': 'Law/Non-Law Accuracy by Model',
        'subject_performance': 'Performance by Subject',
        'year_performance': 'Performance by Year',
        'top_incorrect': 'Top 20 Problems with Highest Incorrect Rate',
        'all_models_incorrect': 'Problems All Models Got Wrong',
        'most_models_incorrect': 'Problems Most Models Got Wrong (≥20%)',
        'test_info': 'Test',
        'problem_id': 'Problem ID',
        'incorrect_count': 'Incorrect Models',
        'correct_count': 'Correct Models',
        'total_models': 'Total Models',
        'attempted_models': 'Attempted Models',
        'question': 'Question',
        'difficulty_score': 'Difficulty Score',
        'by_session': 'By Session',
        'by_subject': 'By Subject',
        'by_year': 'By Year',
        'problem_count': 'Problem Count',
        'session_distribution': 'Problem Distribution by Session',
        'subject_distribution': 'Problem Distribution by Subject',
        'year_distribution': 'Problem Distribution by Year',
        'law_distribution_stat': 'Law/Non-Law Problem Distribution',
        'basic_stats': 'Basic Statistics',
        'help': 'Help',
        'new_features': 'New Features',
        'existing_features': 'Existing Features',
        'current_data': 'Currently Displayed Data',
        'problems': ' problems',
        'session_filter': 'Analyze specific session results only',
        'incorrect_pattern': 'Analyze difficult problems and incorrect patterns',
        'difficulty_comparison': 'Compare model performance by problem difficulty',
        'problem_type_filter': 'Distinguish image/text problems',
        'basic_filters': 'Filter by test name, model, detail type, prompting method',
        'law_analysis_desc': 'Analyze law/non-law distinction',
        'detail_analysis': 'Detailed analysis by subject and year',
        'font_size': 'Font Size',
    }
}

# 커스텀 CSS - 폰트 크기 및 레이아웃 조정
def apply_custom_css(font_size_multiplier=1.0):
    base_font = int(16 * font_size_multiplier)
    metric_value = int(32 * font_size_multiplier)
    metric_label = int(18 * font_size_multiplier)
    h1_size = f"{3 * font_size_multiplier}rem"
    h2_size = f"{2.2 * font_size_multiplier}rem"
    h3_size = f"{1.8 * font_size_multiplier}rem"
    
    st.markdown(f"""
    <style>
        /* 전체 폰트 크기 증가 */
        html, body, [class*="css"] {{
            font-size: {base_font}px;
        }}
        
        /* 메트릭 카드 폰트 크기 */
        [data-testid="stMetricValue"] {{
            font-size: {metric_value}px !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: {metric_label}px !important;
        }}
        
        /* 헤더 폰트 크기 */
        h1 {{
            font-size: {h1_size} !important;
            font-weight: 700 !important;
        }}
        
        h2 {{
            font-size: {h2_size} !important;
            font-weight: 600 !important;
            margin-top: 1.5rem !important;
        }}
        
        h3 {{
            font-size: {h3_size} !important;
            font-weight: 600 !important;
        }}
        
        /* 테이블 폰트 크기 */
        .dataframe {{
            font-size: {int(15 * font_size_multiplier)}px !important;
        }}
        
        /* 사이드바 폰트 크기 */
        .css-1d391kg, [data-testid="stSidebar"] {{
            font-size: {int(15 * font_size_multiplier)}px !important;
        }}
        
        /* 탭 폰트 크기 */
        .stTabs [data-baseweb="tab-list"] button {{
            font-size: {int(18 * font_size_multiplier)}px !important;
            padding: 12px 20px !important;
        }}
        
        /* 버튼 폰트 크기 */
        .stButton>button {{
            font-size: {base_font}px !important;
            padding: 0.5rem 1rem !important;
        }}
        
        /* 셀렉트박스 폰트 크기 */
        .stSelectbox label, .stMultiSelect label {{
            font-size: {base_font}px !important;
            font-weight: 600 !important;
        }}
        
        /* 차트 여백 조정 */
        .js-plotly-plot {{
            margin: 1rem 0 !important;
        }}
        
        /* 컨테이너 패딩 */
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# 안전한 정렬 함수 (타입 혼합 대응)
def safe_sort(values):
    """문자열과 숫자가 섞여있어도 안전하게 정렬"""
    try:
        # 타입별로 그룹화하여 정렬: 숫자 먼저, 그 다음 문자열
        return sorted(values, key=lambda x: (isinstance(x, str), x))
    except:
        # 실패하면 모두 문자열로 변환하여 정렬
        return sorted(values, key=str)

# 데이터 로드 함수
@st.cache_data
def load_data(data_dir):
    """모든 CSV 파일을 로드하고 통합"""
    
    # testset 파일들 로드
    testset_files = glob.glob(os.path.join(data_dir, "testset_*.csv"))
    testsets = {}
    for file in testset_files:
        test_name = os.path.basename(file).replace("testset_", "").replace(".csv", "")
        try:
            df = pd.read_csv(file, encoding='utf-8')
            testsets[test_name] = df
        except:
            try:
                df = pd.read_csv(file, encoding='cp949')
                testsets[test_name] = df
            except:
                continue
    
    # 결과 파일들 로드
    result_files = glob.glob(os.path.join(data_dir, "*_detailed_*.csv")) + \
                   glob.glob(os.path.join(data_dir, "*_summary_*.csv"))
    
    results = []
    for file in result_files:
        filename = os.path.basename(file)
        
        try:
            # 파일명 파싱 개선
            model = None
            detail_type = None
            prompt_type = None
            test_name = None
            
            # Claude 모델 파싱
            if "Claude" in filename:
                if "Claude-3-5-Sonnet" in filename or "Claude-3.5-Sonnet" in filename:
                    model = "Claude-3.5-Sonnet"
                elif "Claude-3-5-Haiku" in filename or "Claude-3.5-Haiku" in filename:
                    model = "Claude-3.5-Haiku"
                elif "Claude-Sonnet-4" in filename:
                    model = "Claude-Sonnet-4"
                
                if "detailed" in filename:
                    detail_type = "detailed"
                elif "summary" in filename:
                    detail_type = "summary"
            
            # GPT 모델 파싱
            elif "GPT" in filename:
                if "GPT-4o-Mini" in filename:
                    model = "GPT-4o-Mini"
                elif "GPT-4o" in filename:
                    model = "GPT-4o"
                
                if "detailed" in filename:
                    detail_type = "detailed"
                elif "summary" in filename:
                    detail_type = "summary"
            
            # 모델을 찾지 못한 경우 건너뛰기
            if model is None or detail_type is None:
                continue
            
            # 프롬프팅 방식 찾기 - 개선된 파싱
            if "noprompting" in filename or "no-prompting" in filename or "no_prompting" in filename:
                prompt_type = "no-prompting"
            elif "few-shot" in filename or "few_shot" in filename or "fewshot" in filename:
                prompt_type = "few-shot"
            elif "cot" in filename.lower() or "chain-of-thought" in filename:
                prompt_type = "cot"
            else:
                prompt_type = "unknown"
            
            # 테스트명 찾기
            test_names = ["산업안전기사", "방재기사", "건설안전기사", "방재안전직"]
            for tn in test_names:
                if tn in filename:
                    test_name = tn
                    break
            
            if test_name is None:
                continue
            
            # CSV 파일 읽기
            try:
                df = pd.read_csv(file, encoding='utf-8')
            except:
                try:
                    df = pd.read_csv(file, encoding='cp949')
                except:
                    continue
            
            # 메타데이터 추가
            df['모델'] = model
            df['상세도'] = detail_type
            df['프롬프팅'] = prompt_type
            df['테스트명'] = test_name
            
            results.append(df)
            
        except Exception as e:
            st.sidebar.warning(f"파일 로드 실패: {os.path.basename(file)}")
            continue
    
    if results:
        results_df = pd.concat(results, ignore_index=True)
    else:
        results_df = pd.DataFrame()
    
    return testsets, results_df

def safe_convert_to_int(value):
    """안전하게 값을 정수로 변환 - 쉼표 구분자 처리 개선"""
    try:
        # None이나 NaN 처리
        if pd.isna(value):
            return None
            
        # 문자열인 경우 쉼표 제거 (천 단위 구분자)
        if isinstance(value, str):
            # 쉼표는 천 단위 구분자이므로 그냥 제거
            value = value.replace(',', '')
        
        # float로 변환 후 int로 변환
        return int(float(value))
    except (ValueError, TypeError):
        return None

def get_available_sessions(df, test_names):
    """특정 테스트들에서 사용 가능한 세션 목록 반환 (문자열과 숫자 모두 지원)"""
    if df is None or len(df) == 0:
        return []
    
    # 여러 테스트 선택 시 필터링
    if test_names:
        test_df = df[df['테스트명'].isin(test_names)] if '테스트명' in df.columns else df
    else:
        test_df = df
    
    if 'Session' in test_df.columns:
        sessions_raw = test_df['Session'].dropna().unique().tolist()
        sessions_clean = []
        
        for s in sessions_raw:
            # 숫자로 변환 가능한지 먼저 시도
            s_int = safe_convert_to_int(s)
            if s_int is not None:
                # 숫자로 변환 가능하면 정수로 저장
                if s_int not in sessions_clean:
                    sessions_clean.append(s_int)
            else:
                # 숫자로 변환 불가능하면 문자열로 저장
                if isinstance(s, str):
                    s_clean = s.strip()
                    if s_clean and s_clean not in sessions_clean:
                        sessions_clean.append(s_clean)
        
        # 정렬: 숫자 먼저, 그 다음 문자열
        return sorted(sessions_clean, key=lambda x: (isinstance(x, str), x))
    return []

def create_problem_identifier(row, lang='ko'):
    """문제 식별자 생성 (테스트명/연도/세션/과목/문제번호)"""
    parts = []
    
    if 'Test Name' in row and pd.notna(row['Test Name']):
        parts.append(str(row['Test Name']))
    elif '테스트명' in row and pd.notna(row['테스트명']):
        parts.append(str(row['테스트명']))
    
    if 'Year' in row and pd.notna(row['Year']):
        year_int = safe_convert_to_int(row['Year'])
        if year_int:
            parts.append(str(year_int))
    
    if 'Session' in row and pd.notna(row['Session']):
        session_int = safe_convert_to_int(row['Session'])
        if session_int:
            parts.append(f"S{session_int}")
    
    if 'Subject' in row and pd.notna(row['Subject']):
        parts.append(str(row['Subject']))
    
    if 'Number' in row and pd.notna(row['Number']):
        number_int = safe_convert_to_int(row['Number'])
        if number_int:
            parts.append(f"Q{number_int}")
    
    return " / ".join(parts) if parts else "Unknown"

def get_testset_statistics(testsets, test_name, lang='ko'):
    """테스트셋의 기초 통계 반환"""
    t = LANGUAGES[lang]
    
    if test_name not in testsets:
        return None
    
    df = testsets[test_name]
    stats = {}
    
    # 총 문제 수
    stats['total_problems'] = len(df)
    
    # 법령/비법령 문제 수
    if 'law' in df.columns:
        stats['law_problems'] = len(df[df['law'] == 'O'])
        stats['non_law_problems'] = len(df[df['law'] != 'O'])
    
    # 과목별 문제 수
    if 'Subject' in df.columns:
        stats['by_subject'] = df['Subject'].value_counts().to_dict()
    
    # 연도별 문제 수
    if 'Year' in df.columns:
        stats['by_year'] = df['Year'].value_counts().sort_index().to_dict()
    
    # 세션별 문제 수
    if 'Session' in df.columns:
        stats['by_session'] = df['Session'].value_counts().sort_index().to_dict()
    
    return stats

# 메인 실행
def main():
    # 🔥 GitHub에서 데이터 다운로드 (최초 1회)
    download_data_from_github()
    
    # 언어 선택 (사이드바 상단에 배치)
    st.sidebar.selectbox(
        "Language / 언어",
        options=['ko', 'en'],
        format_func=lambda x: "한국어" if x == 'ko' else "English",
        key='language'
    )
    
    lang = st.session_state.language
    t = LANGUAGES[lang]
    
    # 폰트 크기 조정
    st.sidebar.markdown("---")
    font_size = st.sidebar.slider(
        t['font_size'],
        min_value=0.8,
        max_value=1.5,
        value=1.0,
        step=0.1
    )
    apply_custom_css(font_size)
    
    # 제목
    st.title(f"🎯 {t['title']}")
    st.markdown("---")
    
    # 데이터 디렉토리는 항상 ./data (GitHub에서 다운로드한 폴더)
    data_dir = "./data"
    
    if not os.path.exists(data_dir):
        st.error(f"Directory not found: {data_dir}")
        return
    
    # 데이터 로드
    testsets, results_df = load_data(data_dir)
    
    if results_df.empty:
        st.warning("No data files found in the specified directory.")
        return
    
    # 정답여부 컬럼 생성
    if 'Answer' in results_df.columns and '예측답' in results_df.columns:
        results_df['정답여부'] = results_df.apply(
            lambda row: row['Answer'] == row['예측답'] if pd.notna(row['Answer']) and pd.notna(row['예측답']) else False,
            axis=1
        )
    
    # 사이드바 필터
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"## {t['filters']}")
    
    # 테스트명 필터 (multiselect로 변경)
    test_names = sorted(results_df['테스트명'].unique().tolist())
    selected_tests = st.sidebar.multiselect(
        t['testname'],
        options=test_names,
        default=test_names,
        help="여러 테스트를 선택할 수 있습니다"
    )
    
    # 테스트 선택에 따른 데이터 필터링
    if selected_tests:
        filtered_df = results_df[results_df['테스트명'].isin(selected_tests)].copy()
    else:
        filtered_df = results_df.copy()
    
    # 모델 필터
    models = sorted(filtered_df['모델'].unique().tolist())
    selected_models = st.sidebar.multiselect(
        t['model'],
        options=models,
        default=models
    )
    
    if selected_models:
        filtered_df = filtered_df[filtered_df['모델'].isin(selected_models)]
    
    # 상세도 필터 (multiselect로 변경)
    details = sorted(filtered_df['상세도'].unique().tolist())
    selected_details = st.sidebar.multiselect(
        t['detail_type'],
        options=details,
        default=details,
        help="여러 상세도를 선택할 수 있습니다"
    )
    
    if selected_details:
        filtered_df = filtered_df[filtered_df['상세도'].isin(selected_details)]
    
    # 프롬프팅 방식 필터 (multiselect로 변경)
    prompts = sorted(filtered_df['프롬프팅'].unique().tolist())
    selected_prompts = st.sidebar.multiselect(
        t['prompting'],
        options=prompts,
        default=prompts,
        help="여러 프롬프팅 방식을 선택할 수 있습니다"
    )
    
    if selected_prompts:
        filtered_df = filtered_df[filtered_df['프롬프팅'].isin(selected_prompts)]
    
    # 세션 필터 (원본 데이터에서 추출, multiselect로 변경)
    if selected_tests:
        # 선택된 테스트들의 원본 데이터에서 세션 추출
        available_sessions = get_available_sessions(results_df, selected_tests)
        if available_sessions:
            selected_sessions = st.sidebar.multiselect(
                t['session'],
                options=available_sessions,
                default=available_sessions,
                help="여러 세션을 선택할 수 있습니다"
            )
            
            if selected_sessions:
                # 선택된 세션과 매칭 (문자열과 숫자 모두 지원)
                def match_session(x):
                    if pd.isna(x):
                        return False
                    
                    # x를 정수로 변환 시도
                    x_int = safe_convert_to_int(x)
                    
                    # 선택된 세션에 정수로 변환된 값이 있는지 확인
                    if x_int is not None and x_int in selected_sessions:
                        return True
                    
                    # 문자열로 직접 비교
                    if isinstance(x, str):
                        x_clean = x.strip()
                        return x_clean in selected_sessions
                    
                    return False
                
                filtered_df = filtered_df[filtered_df['Session'].apply(match_session)]
    
    # 문제 유형 필터
    if 'image' in filtered_df.columns:
        problem_types = [t['all'], t['image_problem'], t['text_only']]
        selected_problem_type = st.sidebar.selectbox(
            t['problem_type'],
            options=problem_types
        )
        
        if selected_problem_type == t['image_problem']:
            filtered_df = filtered_df[filtered_df['image'] != 'text_only']
        elif selected_problem_type == t['text_only']:
            filtered_df = filtered_df[filtered_df['image'] == 'text_only']
    
    # 연도 필터 (원본 데이터에서 추출하여 모든 연도 표시)
    if 'Year' in results_df.columns:
        # 선택된 테스트들의 연도만 표시
        if selected_tests:
            year_source_df = results_df[results_df['테스트명'].isin(selected_tests)]
        else:
            year_source_df = results_df
        
        # 연도를 정수로 변환하여 표시
        years_raw = year_source_df['Year'].dropna().unique().tolist()
        years_int = []
        for y in years_raw:
            y_int = safe_convert_to_int(y)
            if y_int and y_int not in years_int:
                years_int.append(y_int)
        years = safe_sort(years_int)
        
        if years:
            selected_years = st.sidebar.multiselect(
                t['year'],
                options=years,
                default=years
            )
            
            if selected_years:
                # 선택된 연도와 매칭되는 원본 데이터 필터링
                filtered_df = filtered_df[filtered_df['Year'].apply(
                    lambda x: safe_convert_to_int(x) in selected_years if pd.notna(x) else False
                )]
    
    # 법령 구분 필터
    if 'law' in filtered_df.columns:
        law_options = [t['all'], t['law'], t['non_law']]
        selected_law = st.sidebar.selectbox(
            t['law_type'],
            options=law_options
        )
        
        if selected_law == t['law']:
            filtered_df = filtered_df[filtered_df['law'] == 'O']
        elif selected_law == t['non_law']:
            filtered_df = filtered_df[filtered_df['law'] != 'O']
    
    # 필터링된 데이터가 없는 경우
    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        return
    
    # 탭 생성
    tabs = st.tabs([
        f"📊 {t['overview']}",
        f"🔍 {t['model_comparison']}",
        f"⚖️ {t['law_analysis']}",
        f"📚 {t['subject_analysis']}",
        f"📅 {t['year_analysis']}",
        f"❌ {t['incorrect_analysis']}",
        f"📈 {t['difficulty_analysis']}",
        f"📋 {t['testset_stats']}"
    ])
    
    # 탭 1: 전체 요약
    with tabs[0]:
        st.header(f"📊 {t['overview']}")
        
        # 테스트셋 기반으로 실제 문제 수 계산
        total_problems = 0
        if selected_tests:
            for test_name in selected_tests:
                if test_name in testsets:
                    total_problems += len(testsets[test_name])
        
        # 고유 문제 수는 filtered_df에서 중복 제거 (백업용)
        unique_questions = filtered_df['Question'].nunique()
        num_models = filtered_df['모델'].nunique()
        
        # 테스트셋 기본 정보
        st.subheader("📋 테스트셋 정보")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 테스트셋 파일의 실제 문제 수 사용
            display_problems = total_problems if total_problems > 0 else unique_questions
            st.metric("총 문제 수", f"{display_problems:,}")
        with col2:
            st.metric("평가 모델 수", f"{num_models}")
        with col3:
            # 수정: 총 평가 횟수 = 총 문제 수 × 모델 수
            actual_eval_count = display_problems * num_models
            st.metric("총 평가 횟수", f"{actual_eval_count:,}")
        
        st.markdown("---")
        
        # 모델 평균 성능
        st.subheader("🎯 모델 평균 성능")
        col1, col2, col3, col4 = st.columns(4)
        
        # 모델별 정확도 계산 후 평균
        model_accuracies = filtered_df.groupby('모델')['정답여부'].mean()
        avg_accuracy = model_accuracies.mean() * 100
        
        # 평균 정답/오답 수 (모델당)
        avg_problems_per_model = display_problems  # 모델당 평가한 문제 수 (테스트셋 기준)
        avg_correct = (avg_problems_per_model * avg_accuracy / 100) if avg_problems_per_model > 0 else 0
        avg_wrong = avg_problems_per_model - avg_correct
        
        with col1:
            st.metric("평균 정확도", f"{avg_accuracy:.2f}%")
        with col2:
            st.metric("모델당 평균 문제 수", f"{avg_problems_per_model:.0f}")
        with col3:
            st.metric("평균 정답 수", f"{avg_correct:.0f}")
        with col4:
            st.metric("평균 오답 수", f"{avg_wrong:.0f}")
        
        # 법령/비법령 통계
        if 'law' in filtered_df.columns:
            st.markdown("---")
            st.subheader("⚖️ 법령/비법령 분석")
            
            # 테스트셋 기반으로 법령/비법령 문제 수 계산
            law_count_testset = 0
            non_law_count_testset = 0
            
            if selected_tests:
                for test_name in selected_tests:
                    if test_name in testsets and 'law' in testsets[test_name].columns:
                        test_df = testsets[test_name]
                        law_count_testset += len(test_df[test_df['law'] == 'O'])
                        non_law_count_testset += len(test_df[test_df['law'] != 'O'])
            
            # 백업: filtered_df에서 계산 (테스트셋이 없는 경우)
            unique_problems = filtered_df[['Question', 'law']].drop_duplicates()
            law_count_backup = len(unique_problems[unique_problems['law'] == 'O'])
            non_law_count_backup = len(unique_problems[unique_problems['law'] != 'O'])
            
            # 테스트셋 값이 있으면 사용, 없으면 백업 사용
            law_count = law_count_testset if law_count_testset > 0 else law_count_backup
            non_law_count = non_law_count_testset if non_law_count_testset > 0 else non_law_count_backup
            
            # 법령/비법령 정답률 (모든 모델 평균)
            law_df = filtered_df[filtered_df['law'] == 'O']
            non_law_df = filtered_df[filtered_df['law'] != 'O']
            
            law_accuracy = (law_df['정답여부'].mean() * 100) if len(law_df) > 0 else 0
            non_law_accuracy = (non_law_df['정답여부'].mean() * 100) if len(non_law_df) > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(t['law_problems'], f"{law_count:,}")
            with col2:
                st.metric(f"{t['law']} {t['correct_rate']}", f"{law_accuracy:.2f}%")
            with col3:
                st.metric(t['non_law_problems'], f"{non_law_count:,}")
            with col4:
                st.metric(f"{t['non_law']} {t['correct_rate']}", f"{non_law_accuracy:.2f}%")
        
        # 시각화 차트 추가
        st.markdown("---")
        st.subheader("📊 주요 지표 시각화")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 모델별 평균 정확도 바 차트
            model_acc_df = filtered_df.groupby('모델')['정답여부'].mean().reset_index()
            model_acc_df.columns = ['모델', '정확도']
            model_acc_df['정확도'] = model_acc_df['정확도'] * 100
            model_acc_df = model_acc_df.sort_values('정확도', ascending=False)
            
            fig = px.bar(
                model_acc_df,
                x='모델',
                y='정확도',
                title='모델별 평균 정확도',
                text='정확도',
                color='정확도',
                color_continuous_scale='RdYlGn'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                height=400,
                showlegend=False,
                yaxis_title='정확도 (%)',
                xaxis_title='모델',
                yaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 법령/비법령 정답률 비교 차트
            if 'law' in filtered_df.columns:
                law_comparison = pd.DataFrame({
                    '구분': ['법령', '비법령'],
                    '정답률': [law_accuracy, non_law_accuracy],
                    '문제수': [law_count, non_law_count]
                })
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='정답률',
                    x=law_comparison['구분'],
                    y=law_comparison['정답률'],
                    text=law_comparison['정답률'].round(1),
                    texttemplate='%{text}%',
                    textposition='outside',
                    marker_color=['#FF6B6B', '#4ECDC4'],
                    yaxis='y'
                ))
                
                fig.add_trace(go.Scatter(
                    name='문제 수',
                    x=law_comparison['구분'],
                    y=law_comparison['문제수'],
                    text=law_comparison['문제수'],
                    texttemplate='%{text}개',
                    textposition='top center',
                    mode='lines+markers+text',
                    marker=dict(size=10, color='orange'),
                    line=dict(width=2, color='orange'),
                    yaxis='y2'
                ))
                
                fig.update_layout(
                    title='법령/비법령 정답률 및 문제 수 비교',
                    height=400,
                    yaxis=dict(
                        title='정답률 (%)',
                        range=[0, 100]
                    ),
                    yaxis2=dict(
                        title='문제 수',
                        overlaying='y',
                        side='right',
                        range=[0, max(law_count, non_law_count) * 1.2]
                    ),
                    hovermode='x unified',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                # 법령 정보가 없을 때 - 모델별 정답/오답 수 차트
                model_correct_wrong = filtered_df.groupby('모델')['정답여부'].agg(['sum', 'count']).reset_index()
                model_correct_wrong.columns = ['모델', '정답', '총문제']
                model_correct_wrong['오답'] = model_correct_wrong['총문제'] - model_correct_wrong['정답']
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='정답',
                    x=model_correct_wrong['모델'],
                    y=model_correct_wrong['정답'],
                    marker_color='lightgreen'
                ))
                fig.add_trace(go.Bar(
                    name='오답',
                    x=model_correct_wrong['모델'],
                    y=model_correct_wrong['오답'],
                    marker_color='lightcoral'
                ))
                
                fig.update_layout(
                    barmode='stack',
                    title='모델별 정답/오답 수',
                    height=400,
                    yaxis_title='문제 수',
                    xaxis_title='모델'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # 테스트셋별 분포 (여러 테스트가 있을 경우)
        if '테스트명' in filtered_df.columns and filtered_df['테스트명'].nunique() > 1:
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 테스트셋별 문제 수
                test_problem_count = filtered_df.groupby('테스트명')['Question'].nunique().reset_index()
                test_problem_count.columns = ['테스트명', '문제수']
                test_problem_count = test_problem_count.sort_values('문제수', ascending=False)
                
                fig = px.bar(
                    test_problem_count,
                    x='테스트명',
                    y='문제수',
                    title='테스트셋별 문제 수',
                    text='문제수',
                    color='문제수',
                    color_continuous_scale='Blues'
                )
                fig.update_traces(textposition='outside')
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    yaxis_title='문제 수',
                    xaxis_title='테스트명'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # 테스트셋별 평균 정확도
                test_accuracy = filtered_df.groupby('테스트명')['정답여부'].mean().reset_index()
                test_accuracy.columns = ['테스트명', '정확도']
                test_accuracy['정확도'] = test_accuracy['정확도'] * 100
                test_accuracy = test_accuracy.sort_values('정확도', ascending=False)
                
                fig = px.bar(
                    test_accuracy,
                    x='테스트명',
                    y='정확도',
                    title='테스트셋별 평균 정확도',
                    text='정확도',
                    color='정확도',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    yaxis_title='정확도 (%)',
                    xaxis_title='테스트명',
                    yaxis=dict(range=[0, 100])
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
    
    # 탭 2: 모델별 비교
    with tabs[1]:
        st.header(f"🔍 {t['model_comparison']}")
        
        # 모델별 성능 계산
        model_stats = filtered_df.groupby('모델').agg({
            '정답여부': ['sum', 'count', 'mean']
        }).reset_index()
        model_stats.columns = ['모델', '정답', '총문제', '정확도']
        model_stats['정확도'] = model_stats['정확도'] * 100
        model_stats['오답'] = model_stats['총문제'] - model_stats['정답']
        model_stats = model_stats.sort_values('정확도', ascending=False)
        
        # 성능 지표 테이블
        st.subheader(t['performance_by_model'])
        
        # 테이블 컬럼명 변경
        display_stats = model_stats.copy()
        if lang == 'en':
            display_stats.columns = ['Model', 'Correct', 'Total', 'Accuracy', 'Wrong']
        
        st.dataframe(
            display_stats.style.format({
                '정확도' if lang == 'ko' else 'Accuracy': '{:.2f}%'
            }).background_gradient(subset=['정확도' if lang == 'ko' else 'Accuracy'], cmap='RdYlGn'),
            use_container_width=True
        )
        
        # 비교 차트
        st.markdown("---")
        st.subheader(t['comparison_chart'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 정확도 바 차트
            fig = px.bar(
                model_stats,
                x='모델',
                y='정확도',
                title=t['overall_comparison'],
                text='정확도',
                color='정확도',
                color_continuous_scale='RdYlGn'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                height=400,
                showlegend=False,
                yaxis_title=t['accuracy'] + ' (%)',
                xaxis_title=t['model']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 정답/오답 스택 바 차트
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=t['correct'],
                x=model_stats['모델'],
                y=model_stats['정답'],
                marker_color='lightgreen'
            ))
            fig.add_trace(go.Bar(
                name=t['wrong'],
                x=model_stats['모델'],
                y=model_stats['오답'],
                marker_color='lightcoral'
            ))
            
            fig.update_layout(
                barmode='stack',
                title=f"{t['correct']}/{t['wrong']} {t['comparison_chart']}",
                height=400,
                yaxis_title=t['problem_count'],
                xaxis_title=t['model']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 히트맵
        if '테스트명' in filtered_df.columns:
            st.markdown("---")
            st.subheader(t['heatmap'])
            
            # 모델별, 테스트별 정확도 계산
            heatmap_data = filtered_df.groupby(['모델', '테스트명'])['정답여부'].mean() * 100
            heatmap_pivot = heatmap_data.unstack(fill_value=0)
            
            # 히트맵 생성 (숫자 표시 추가)
            fig = px.imshow(
                heatmap_pivot,
                labels=dict(x=t['testname'], y=t['model'], color=t['accuracy'] + " (%)"),
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index,
                color_continuous_scale='RdYlGn',
                aspect="auto",
                text_auto='.1f'  # 숫자 표시 추가
            )
            
            fig.update_layout(height=400)
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # 탭 3: 법령/비법령 분석
    with tabs[2]:
        if 'law' not in filtered_df.columns:
            st.info("Law classification data not available.")
        else:
            st.header(f"⚖️ {t['law_analysis']}")
            
            # 전체 법령/비법령 비율
            st.subheader(t['law_ratio'])
            
            # 중복 제거한 문제로 계산
            unique_problems = filtered_df.drop_duplicates(subset=['Question', 'law'])
            law_count = len(unique_problems[unique_problems['law'] == 'O'])
            non_law_count = len(unique_problems[unique_problems['law'] != 'O'])
            total_unique = law_count + non_law_count
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 파이 차트
                fig = go.Figure(data=[go.Pie(
                    labels=[t['law'], t['non_law']],
                    values=[law_count, non_law_count],
                    hole=0.3
                )])
                fig.update_layout(
                    title=t['law_distribution_stat'],
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # 수치 표시
                st.metric(t['law_problems'], f"{law_count} ({law_count/total_unique*100:.1f}%)")
                st.metric(t['non_law_problems'], f"{non_law_count} ({non_law_count/total_unique*100:.1f}%)")
            
            # 모델별 법령/비법령 성능
            st.markdown("---")
            st.subheader(t['model_law_performance'])
            
            law_performance = []
            for model in filtered_df['모델'].unique():
                model_df = filtered_df[filtered_df['모델'] == model]
                
                law_model = model_df[model_df['law'] == 'O']
                non_law_model = model_df[model_df['law'] != 'O']
                
                law_acc = (law_model['정답여부'].sum() / len(law_model) * 100) if len(law_model) > 0 else 0
                non_law_acc = (non_law_model['정답여부'].sum() / len(non_law_model) * 100) if len(non_law_model) > 0 else 0
                
                law_performance.append({
                    '모델': model,
                    '법령': law_acc,
                    '비법령': non_law_acc
                })
            
            law_perf_df = pd.DataFrame(law_performance)
            
            # 그룹 바 차트
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=t['law'],
                x=law_perf_df['모델'],
                y=law_perf_df['법령'],
                marker_color='skyblue'
            ))
            fig.add_trace(go.Bar(
                name=t['non_law'],
                x=law_perf_df['모델'],
                y=law_perf_df['비법령'],
                marker_color='lightcoral'
            ))
            
            fig.update_layout(
                barmode='group',
                title=t['law_distribution'],
                height=500,
                yaxis_title=t['accuracy'] + ' (%)',
                xaxis_title=t['model']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 탭 4: 과목별 분석
    with tabs[3]:
        if 'Subject' not in filtered_df.columns:
            st.info("Subject data not available.")
        else:
            st.header(f"📚 {t['subject_analysis']}")
            
            # 과목별 성능
            subject_stats = filtered_df.groupby('Subject').agg({
                '정답여부': ['sum', 'count', 'mean']
            }).reset_index()
            subject_stats.columns = ['과목', '정답', '총문제', '정확도']
            subject_stats['정확도'] = subject_stats['정확도'] * 100
            subject_stats = subject_stats.sort_values('정확도', ascending=False)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # 테이블
                st.dataframe(
                    subject_stats.style.format({'정확도': '{:.2f}%'})
                    .background_gradient(subset=['정확도'], cmap='RdYlGn'),
                    use_container_width=True
                )
            
            with col2:
                # 바 차트
                fig = px.bar(
                    subject_stats,
                    x='과목',
                    y='정확도',
                    title=t['subject_performance'],
                    text='정확도',
                    color='정확도',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    yaxis_title=t['accuracy'] + ' (%)'
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            # 모델별 과목 성능 히트맵
            st.markdown("---")
            subject_model = filtered_df.groupby(['모델', 'Subject'])['정답여부'].mean() * 100
            subject_model_pivot = subject_model.unstack(fill_value=0)
            
            fig = px.imshow(
                subject_model_pivot,
                labels=dict(x=t['by_subject'], y=t['model'], color=t['accuracy'] + " (%)"),
                x=subject_model_pivot.columns,
                y=subject_model_pivot.index,
                color_continuous_scale='RdYlGn',
                aspect="auto",
                text_auto='.1f'  # 숫자 표시 추가
            )
            fig.update_layout(height=400)
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # 탭 5: 연도별 분석
    with tabs[4]:
        if 'Year' not in filtered_df.columns:
            st.info("Year data not available.")
        else:
            st.header(f"📅 {t['year_analysis']}")
            
            # 디버깅 정보 표시
            with st.expander("🔍 디버깅 정보 (클릭하여 펼치기)"):
                st.write("**필터링 전 원본 데이터:**")
                st.write(f"- 전체 데이터 행 수: {len(results_df):,}")
                st.write(f"- 원본 Year 고유값: {sorted([str(y) for y in results_df['Year'].dropna().unique().tolist()])}")
                
                st.write("**필터링 후 데이터:**")
                st.write(f"- 필터링된 데이터 행 수: {len(filtered_df):,}")
                st.write(f"- 필터링된 Year 고유값: {sorted([str(y) for y in filtered_df['Year'].dropna().unique().tolist()])}")
                
                st.write("**현재 필터 설정:**")
                st.write(f"- 선택된 테스트: {selected_tests}")
                st.write(f"- 선택된 모델: {selected_models}")
                st.write(f"- 선택된 연도: {selected_years if 'selected_years' in locals() else '전체'}")
            
            # Year를 정수로 변환
            filtered_df['Year_Int'] = filtered_df['Year'].apply(safe_convert_to_int)
            year_df = filtered_df[filtered_df['Year_Int'].notna()].copy()
            
            if not year_df.empty:
                # 연도별 성능
                year_stats = year_df.groupby('Year_Int').agg({
                    '정답여부': ['sum', 'count', 'mean']
                }).reset_index()
                year_stats.columns = ['연도', '정답', '총문제', '정확도']
                year_stats['정확도'] = year_stats['정확도'] * 100
                year_stats = year_stats.sort_values('연도')
                
                # 연도를 정수로 표시
                year_stats['연도'] = year_stats['연도'].astype(int)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # 테이블 (소수점 없이 표시)
                    st.dataframe(
                        year_stats.style.format({
                            '연도': '{:.0f}',
                            '정답': '{:.0f}',
                            '총문제': '{:.0f}',
                            '정확도': '{:.2f}%'
                        })
                        .background_gradient(subset=['정확도'], cmap='RdYlGn'),
                        use_container_width=True
                    )
                
                with col2:
                    # 라인 차트
                    fig = px.line(
                        year_stats,
                        x='연도',
                        y='정확도',
                        title=t['year_performance'],
                        markers=True,
                        text='정확도'
                    )
                    fig.update_traces(texttemplate='%{text:.1f}%', textposition='top center')
                    fig.update_layout(
                        height=400,
                        yaxis_title=t['accuracy'] + ' (%)',
                        xaxis_title=t['year']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # 연도별 문제 수 차트 추가
                st.markdown("---")
                st.subheader("📊 연도별 문제 수 분포")
                
                # 테스트셋에서 실제 문제 수 계산 (중복 제거)
                if selected_tests:
                    year_problem_count = []
                    for test_name in selected_tests:
                        if test_name in testsets and 'Year' in testsets[test_name].columns:
                            test_year_counts = testsets[test_name].groupby('Year').size()
                            for year, count in test_year_counts.items():
                                year_int = safe_convert_to_int(year)
                                if year_int:
                                    year_problem_count.append({'연도': year_int, '문제수': count})
                    
                    if year_problem_count:
                        year_problem_df = pd.DataFrame(year_problem_count)
                        year_problem_df = year_problem_df.groupby('연도')['문제수'].sum().reset_index()
                        year_problem_df = year_problem_df.sort_values('연도')
                    else:
                        # 백업: filtered_df에서 고유 문제 수 계산
                        year_problem_df = year_df.groupby('Year_Int')['Question'].nunique().reset_index()
                        year_problem_df.columns = ['연도', '문제수']
                        year_problem_df['연도'] = year_problem_df['연도'].astype(int)
                        year_problem_df = year_problem_df.sort_values('연도')
                else:
                    # 테스트 선택 안 됨: filtered_df에서 계산
                    year_problem_df = year_df.groupby('Year_Int')['Question'].nunique().reset_index()
                    year_problem_df.columns = ['연도', '문제수']
                    year_problem_df['연도'] = year_problem_df['연도'].astype(int)
                    year_problem_df = year_problem_df.sort_values('연도')
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # 연도별 문제 수 테이블
                    st.dataframe(
                        year_problem_df.style.format({
                            '연도': '{:.0f}',
                            '문제수': '{:.0f}'
                        })
                        .background_gradient(subset=['문제수'], cmap='Blues'),
                        use_container_width=True
                    )
                    
                    # 총 문제 수 표시
                    st.metric("총 문제 수", f"{year_problem_df['문제수'].sum():,.0f}개")
                
                with col2:
                    # 바 차트
                    fig = px.bar(
                        year_problem_df,
                        x='연도',
                        y='문제수',
                        title='연도별 문제 수',
                        text='문제수',
                        color='문제수',
                        color_continuous_scale='Blues'
                    )
                    fig.update_traces(texttemplate='%{text}', textposition='outside')
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        yaxis_title='문제 수',
                        xaxis_title='연도',
                        xaxis=dict(tickmode='linear')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # 모델별 연도 성능 히트맵
                st.markdown("---")
                year_model = year_df.groupby(['모델', 'Year_Int'])['정답여부'].mean() * 100
                year_model_pivot = year_model.unstack(fill_value=0)
                
                # 컬럼명을 정수로 변환
                year_model_pivot.columns = year_model_pivot.columns.astype(int)
                
                fig = px.imshow(
                    year_model_pivot,
                    labels=dict(x=t['year'], y=t['model'], color=t['accuracy'] + " (%)"),
                    x=year_model_pivot.columns,
                    y=year_model_pivot.index,
                    color_continuous_scale='RdYlGn',
                    aspect="auto",
                    text_auto='.1f'  # 숫자 표시 추가
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("연도 정보가 있는 데이터가 없습니다.")
    
    # 탭 6: 오답 분석
    with tabs[5]:
        st.header(f"❌ {t['incorrect_analysis']}")
        
        # 문제별 오답률 계산
        problem_analysis = filtered_df.groupby('Question').agg({
            '정답여부': ['sum', 'count', 'mean']
        }).reset_index()
        problem_analysis.columns = ['Question', 'correct_count', 'total_count', 'correct_rate']
        problem_analysis['incorrect_rate'] = 1 - problem_analysis['correct_rate']
        problem_analysis['incorrect_count'] = problem_analysis['total_count'] - problem_analysis['correct_count']
        
        # 문제 식별자 추가
        problem_ids = []
        for question in problem_analysis['Question']:
            matching_rows = filtered_df[filtered_df['Question'] == question]
            if len(matching_rows) > 0:
                problem_id = create_problem_identifier(matching_rows.iloc[0], lang)
                problem_ids.append(problem_id)
            else:
                problem_ids.append("Unknown")
        
        problem_analysis['problem_id'] = problem_ids
        
        # 오답률 순으로 정렬 (동일한 오답률이면 문제 ID로 정렬)
        problem_analysis = problem_analysis.sort_values(
            by=['incorrect_rate', 'problem_id'],
            ascending=[False, True]
        )
        
        # 시도한 모델 목록 추가
        attempted_models = []
        for question in problem_analysis['Question']:
            models = filtered_df[filtered_df['Question'] == question]['모델'].unique().tolist()
            attempted_models.append(', '.join(sorted(models)))
        
        problem_analysis['attempted_models'] = attempted_models
        
        # 모델별 정오답 정보 추가
        correct_models_list = []
        incorrect_models_list = []
        
        for question in problem_analysis['Question']:
            q_df = filtered_df[filtered_df['Question'] == question]
            correct_models = q_df[q_df['정답여부'] == True]['모델'].unique().tolist()
            incorrect_models = q_df[q_df['정답여부'] == False]['모델'].unique().tolist()
            
            correct_models_list.append('✓ ' + ', '.join(sorted(correct_models)) if correct_models else '-')
            incorrect_models_list.append('✗ ' + ', '.join(sorted(incorrect_models)) if incorrect_models else '-')
        
        problem_analysis['correct_models'] = correct_models_list
        problem_analysis['incorrect_models'] = incorrect_models_list
        
        # Top 20 오답률 높은 문제
        st.subheader(t['top_incorrect'])
        
        top_20 = problem_analysis.head(20)
        
        # 디스플레이용 데이터프레임
        display_top_20 = pd.DataFrame({
            t['problem_id']: top_20['problem_id'],
            t['incorrect_count']: top_20['incorrect_count'].astype(int),
            t['correct_count']: top_20['correct_count'].astype(int),
            t['total_models']: top_20['total_count'].astype(int),
            t['wrong_rate']: (top_20['incorrect_rate'] * 100).round(2),
            '정답 모델' if lang == 'ko' else 'Correct Models': top_20['correct_models'],
            '오답 모델' if lang == 'ko' else 'Incorrect Models': top_20['incorrect_models']
        })
        
        st.dataframe(
            display_top_20.style.background_gradient(
                subset=[t['wrong_rate']],
                cmap='Reds',
                vmin=0,
                vmax=100
            ),
            use_container_width=True,
            height=600
        )
        
        # 모든 모델이 틀린 문제
        st.markdown("---")
        st.subheader(t['all_models_incorrect'])
        
        all_wrong = problem_analysis[problem_analysis['correct_count'] == 0]
        
        if len(all_wrong) > 0:
            display_all_wrong = pd.DataFrame({
                t['problem_id']: all_wrong['problem_id'],
                t['incorrect_count']: all_wrong['incorrect_count'].astype(int),
                t['correct_count']: all_wrong['correct_count'].astype(int),
                t['total_models']: all_wrong['total_count'].astype(int),
                '오답 모델' if lang == 'ko' else 'Incorrect Models': all_wrong['incorrect_models']
            })
            
            st.dataframe(display_all_wrong, use_container_width=True)
            
            # 문제 상세 보기 옵션
            if st.checkbox('문제 내용 보기' if lang == 'ko' else 'Show Question Details'):
                for idx, row in all_wrong.iterrows():
                    with st.expander(f"{row['problem_id']}"):
                        q_detail = filtered_df[filtered_df['Question'] == row['Question']].iloc[0]
                        st.write(f"**{t['question']}:** {q_detail['Question']}")
                        if 'Subject' in q_detail and pd.notna(q_detail['Subject']):
                            st.write(f"**과목/Subject:** {q_detail['Subject']}")
                        
                        # 선택지 표시
                        if all(['Option 1' in q_detail, 'Option 2' in q_detail, 'Option 3' in q_detail, 'Option 4' in q_detail]):
                            st.write("**선택지/Options:**")
                            for i in range(1, 5):
                                option_key = f'Option {i}'
                                if option_key in q_detail and pd.notna(q_detail[option_key]):
                                    st.write(f"  {i}. {q_detail[option_key]}")
                        
                        # 정답 표시
                        if 'Answer' in q_detail and pd.notna(q_detail['Answer']):
                            st.write(f"**정답/Answer:** {q_detail['Answer']}")
                        
                        st.write(f"**오답 모델/Incorrect Models:** {row['incorrect_models']}")
        else:
            st.info("No problems that all models got wrong.")
        
        # 대부분 모델이 틀린 문제 (20% 이상)
        st.markdown("---")
        st.subheader(t['most_models_incorrect'])
        
        most_wrong = problem_analysis[problem_analysis['incorrect_rate'] >= 0.2]
        
        if len(most_wrong) > 0:
            display_most_wrong = pd.DataFrame({
                t['problem_id']: most_wrong['problem_id'],
                t['incorrect_count']: most_wrong['incorrect_count'].astype(int),
                t['correct_count']: most_wrong['correct_count'].astype(int),
                t['total_models']: most_wrong['total_count'].astype(int),
                t['wrong_rate']: (most_wrong['incorrect_rate'] * 100).round(2),
                '정답 모델' if lang == 'ko' else 'Correct Models': most_wrong['correct_models'],
                '오답 모델' if lang == 'ko' else 'Incorrect Models': most_wrong['incorrect_models']
            })
            
            st.dataframe(
                display_most_wrong.style.background_gradient(
                    subset=[t['wrong_rate']],
                    cmap='Reds',
                    vmin=0,
                    vmax=100
                ),
                use_container_width=True
            )
            
            # 문제 상세 보기 옵션
            if st.checkbox('문제 내용 보기 (대부분 틀린 문제)' if lang == 'ko' else 'Show Question Details (Most Incorrect)', key='most_wrong_details'):
                for idx, row in most_wrong.head(10).iterrows():  # 상위 10개만 표시
                    with st.expander(f"{row['problem_id']} - 오답률 {row['incorrect_rate']*100:.1f}%"):
                        q_detail = filtered_df[filtered_df['Question'] == row['Question']].iloc[0]
                        st.write(f"**{t['question']}:** {q_detail['Question']}")
                        if 'Subject' in q_detail and pd.notna(q_detail['Subject']):
                            st.write(f"**과목/Subject:** {q_detail['Subject']}")
                        
                        # 선택지 표시
                        if all(['Option 1' in q_detail, 'Option 2' in q_detail, 'Option 3' in q_detail, 'Option 4' in q_detail]):
                            st.write("**선택지/Options:**")
                            for i in range(1, 5):
                                option_key = f'Option {i}'
                                if option_key in q_detail and pd.notna(q_detail[option_key]):
                                    st.write(f"  {i}. {q_detail[option_key]}")
                        
                        # 정답 표시
                        if 'Answer' in q_detail and pd.notna(q_detail['Answer']):
                            st.write(f"**정답/Answer:** {q_detail['Answer']}")
                        
                        st.write(f"**✓ 정답 모델/Correct Models:** {row['correct_models']}")
                        st.write(f"**✗ 오답 모델/Incorrect Models:** {row['incorrect_models']}")
        else:
            st.info("No problems that most models got wrong.")
        
        # Top 10 오답률 높은 문제 차트
        st.markdown("---")
        top_10_chart = top_20.head(10)
        
        fig = px.bar(
            top_10_chart,
            x='problem_id',
            y='incorrect_rate',
            title='오답률 높은 문제 Top 10' if lang == 'ko' else 'Top 10 Problems by Incorrect Rate',
            text=[f"{x:.0%}" for x in top_10_chart['incorrect_rate']],
            color='incorrect_rate',
            color_continuous_scale='Reds',
            range_color=[0, 1]  # 컬러바 범위를 0~1로 고정
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            height=500,
            showlegend=False,
            yaxis_title=t['wrong_rate'],
            xaxis_title=t['problem_id'],
            yaxis=dict(range=[0, 1])  # y축 범위를 0~1로 고정
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # 탭 7: 난이도 분석
    with tabs[6]:
        st.header(f"📈 {t['difficulty_analysis']}")
        
        # 문제별 난이도 계산 (정답률 기반)
        difficulty = filtered_df.groupby('Question').agg({
            '정답여부': ['sum', 'count', 'mean']
        }).reset_index()
        difficulty.columns = ['Question', 'correct_count', 'total_count', 'difficulty_score']
        difficulty['difficulty_score'] = difficulty['difficulty_score'] * 100
        
        # 난이도 구간 분류
        def classify_difficulty(score):
            if score < 20:
                return '매우 어려움 (0-20%)'
            elif score < 40:
                return '어려움 (20-40%)'
            elif score < 60:
                return '보통 (40-60%)'
            elif score < 80:
                return '쉬움 (60-80%)'
            else:
                return '매우 쉬움 (80-100%)'
        
        difficulty['난이도_구간'] = difficulty['difficulty_score'].apply(classify_difficulty)
        
        # 난이도 구간 순서 정의 (어려운 것부터 쉬운 것 순)
        difficulty_order = [
            '매우 어려움 (0-20%)',
            '어려움 (20-40%)',
            '보통 (40-60%)',
            '쉬움 (60-80%)',
            '매우 쉬움 (80-100%)'
        ]
        difficulty['난이도_구간'] = pd.Categorical(difficulty['난이도_구간'], categories=difficulty_order, ordered=True)
        
        # 원본 데이터에 난이도 정보 병합
        analysis_df = filtered_df.merge(difficulty[['Question', 'difficulty_score', '난이도_구간']], on='Question')
        
        # analysis_df에도 동일한 순서 적용
        analysis_df['난이도_구간'] = pd.Categorical(analysis_df['난이도_구간'], categories=difficulty_order, ordered=True)
        
        # 1. 난이도 분포
        st.subheader("📈 문제 난이도 분포")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 난이도 분포 히스토그램
            fig = px.histogram(
                difficulty,
                x='difficulty_score',
                nbins=20,
                title=t['difficulty_score'] + ' Distribution',
                labels={'difficulty_score': t['difficulty_score'], 'count': t['problem_count']}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 난이도 구간별 문제 수
            difficulty_dist = difficulty['난이도_구간'].value_counts()
            # 난이도 순서대로 재정렬
            difficulty_dist = difficulty_dist.reindex(difficulty_order, fill_value=0)
            
            fig = px.bar(
                x=difficulty_dist.index,
                y=difficulty_dist.values,
                title=t['problem_count'] + ' by Difficulty',
                labels={'x': 'Difficulty', 'y': t['problem_count']},
                color=difficulty_dist.values,
                color_continuous_scale='RdYlGn_r'
            )
            fig.update_layout(
                height=400,
                showlegend=False
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # 통계 요약
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("평균 정답률", f"{difficulty['difficulty_score'].mean():.1f}%")
        with col2:
            st.metric("중앙값", f"{difficulty['difficulty_score'].median():.1f}%")
        with col3:
            very_hard = len(difficulty[difficulty['난이도_구간'] == '매우 어려움 (0-20%)'])
            st.metric("매우 어려운 문제", f"{very_hard}개")
        with col4:
            very_easy = len(difficulty[difficulty['난이도_구간'] == '매우 쉬움 (80-100%)'])
            st.metric("매우 쉬운 문제", f"{very_easy}개")
        
        st.markdown("---")
        
        # 2. 난이도별 모델 성능
        st.subheader("🎯 난이도별 모델 성능")
        
        # 모델별 난이도 구간별 정답률
        model_difficulty = analysis_df.groupby(['모델', '난이도_구간']).agg({
            '정답여부': ['mean', 'count']
        }).reset_index()
        model_difficulty.columns = ['모델', '난이도_구간', '정답률', '문제수']
        model_difficulty['정답률'] = model_difficulty['정답률'] * 100
        
        # 라인 차트
        fig = px.line(
            model_difficulty,
            x='난이도_구간',
            y='정답률',
            color='모델',
            markers=True,
            title='난이도별 모델 성능 비교',
            labels={'정답률': t['accuracy'] + ' (%)', '난이도_구간': 'Difficulty Level'},
            category_orders={'난이도_구간': difficulty_order}
        )
        fig.update_layout(height=500)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # 히트맵
        pivot_difficulty = model_difficulty.pivot(
            index='모델',
            columns='난이도_구간',
            values='정답률'
        )
        
        # 난이도 순서대로 컬럼 재정렬
        pivot_difficulty = pivot_difficulty.reindex(columns=difficulty_order)
        
        fig = px.imshow(
            pivot_difficulty,
            labels=dict(x="난이도 구간", y=t['model'], color=t['accuracy'] + " (%)"),
            x=pivot_difficulty.columns,
            y=pivot_difficulty.index,
            color_continuous_scale='RdYlGn',
            aspect="auto",
            title='모델 × 난이도 히트맵',
            text_auto='.1f'  # 숫자 표시
        )
        fig.update_layout(height=400)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # 3. 과목별 난이도 분석
        if 'Subject' in analysis_df.columns:
            st.subheader("📚 과목별 난이도 분석")
            
            subject_difficulty = analysis_df.groupby('Subject').agg({
                'difficulty_score': 'mean',
                'Question': 'count'
            }).reset_index()
            subject_difficulty.columns = ['과목', '평균_난이도', '문제수']
            subject_difficulty = subject_difficulty.sort_values('평균_난이도')
            
            fig = px.bar(
                subject_difficulty,
                x='과목',
                y='평균_난이도',
                title='과목별 평균 난이도 (정답률)',
                text='평균_난이도',
                color='평균_난이도',
                color_continuous_scale='RdYlGn'
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_xaxes(tickangle=45)
            fig.update_layout(
                height=500,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 과목 × 난이도 구간 히트맵
            subject_diff_dist = analysis_df.groupby(['Subject', '난이도_구간']).size().reset_index(name='문제수')
            pivot_subject_diff = subject_diff_dist.pivot(
                index='Subject',
                columns='난이도_구간',
                values='문제수'
            ).fillna(0)
            
            # 난이도 순서대로 컬럼 재정렬
            pivot_subject_diff = pivot_subject_diff.reindex(columns=difficulty_order, fill_value=0)
            
            fig = px.imshow(
                pivot_subject_diff,
                labels=dict(x="난이도 구간", y="과목", color="문제 수"),
                x=pivot_subject_diff.columns,
                y=pivot_subject_diff.index,
                color_continuous_scale='Blues',
                aspect="auto",
                title='과목 × 난이도 분포',
                text_auto=True  # 숫자 표시
            )
            fig.update_layout(height=500)
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # 4. 어려운 문제 vs 쉬운 문제 상세 분석
        st.subheader("🔍 어려운 문제 vs 쉬운 문제 비교")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 매우 어려운 문제 (정답률 < 20%)")
            very_hard_problems = difficulty[difficulty['difficulty_score'] < 20].sort_values('difficulty_score')
            
            if len(very_hard_problems) > 0:
                st.metric("문제 수", f"{len(very_hard_problems)}개")
                st.metric("평균 정답률", f"{very_hard_problems['difficulty_score'].mean():.1f}%")
                
                # 모델별 성능
                very_hard_questions = very_hard_problems['Question'].tolist()
                very_hard_model_perf = filtered_df[filtered_df['Question'].isin(very_hard_questions)].groupby('모델')['정답여부'].mean() * 100
                
                st.markdown("**모델별 성능**")
                for model, acc in very_hard_model_perf.sort_values(ascending=False).items():
                    st.write(f"- {model}: {acc:.1f}%")
            else:
                st.info("매우 어려운 문제가 없습니다.")
        
        with col2:
            st.markdown("#### 매우 쉬운 문제 (정답률 > 80%)")
            very_easy_problems = difficulty[difficulty['difficulty_score'] > 80].sort_values('difficulty_score', ascending=False)
            
            if len(very_easy_problems) > 0:
                st.metric("문제 수", f"{len(very_easy_problems)}개")
                st.metric("평균 정답률", f"{very_easy_problems['difficulty_score'].mean():.1f}%")
                
                # 모델별 성능
                very_easy_questions = very_easy_problems['Question'].tolist()
                very_easy_model_perf = filtered_df[filtered_df['Question'].isin(very_easy_questions)].groupby('모델')['정답여부'].mean() * 100
                
                st.markdown("**모델별 성능**")
                for model, acc in very_easy_model_perf.sort_values(ascending=False).items():
                    st.write(f"- {model}: {acc:.1f}%")
            else:
                st.info("매우 쉬운 문제가 없습니다.")
        
        st.markdown("---")
        
        # 5. 난이도 구간별 상세 테이블
        st.subheader("📋 난이도 구간별 상세 통계")
        
        detailed_difficulty = model_difficulty.pivot_table(
            index='모델',
            columns='난이도_구간',
            values='정답률',
            aggfunc='mean'
        ).round(2)
        
        # 난이도 순서대로 컬럼 재정렬
        detailed_difficulty = detailed_difficulty.reindex(columns=difficulty_order)
        
        st.dataframe(
            detailed_difficulty.style.background_gradient(cmap='RdYlGn', axis=None),
            use_container_width=True
        )
    
    # 탭 8: 테스트셋 통계
    with tabs[7]:
        st.header(f"📋 {t['testset_stats']}")
        
        if selected_tests:
            # 선택된 테스트들의 통계 표시
            for test_name in selected_tests:
                stats = get_testset_statistics(testsets, test_name, lang)
                if stats:
                    st.subheader(f"📖 {test_name}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(t['total_problems'], stats['total_problems'])
                    
                    with col2:
                        if 'law_problems' in stats:
                            st.metric(t['law_problems'], stats['law_problems'])
                    
                    with col3:
                        if 'non_law_problems' in stats:
                            st.metric(t['non_law_problems'], stats['non_law_problems'])
                    
                    # 과목별, 연도별, 세션별 통계
                    if 'by_subject' in stats or 'by_year' in stats or 'by_session' in stats:
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if 'by_subject' in stats:
                                st.markdown(f"**{t['by_subject']}**")
                                subject_df = pd.DataFrame(list(stats['by_subject'].items()), 
                                                         columns=['Subject', 'Count'])
                                fig = px.bar(subject_df, x='Subject', y='Count', 
                                           title=t['subject_distribution'])
                                fig.update_xaxes(tickangle=45)
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            if 'by_year' in stats:
                                st.markdown(f"**{t['by_year']}**")
                                year_df = pd.DataFrame(list(stats['by_year'].items()), 
                                                      columns=['Year', 'Count'])
                                fig = px.bar(year_df, x='Year', y='Count', 
                                           title=t['year_distribution'])
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with col3:
                            if 'by_session' in stats:
                                st.markdown(f"**{t['by_session']}**")
                                session_df = pd.DataFrame(list(stats['by_session'].items()), 
                                                         columns=['Session', 'Count'])
                                fig = px.bar(session_df, x='Session', y='Count', 
                                           title=t['session_distribution'])
                                st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
        else:
            st.info("테스트를 선택해주세요.")
    
    # 사이드바 하단 정보
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### 📌 {t['help']}")
    st.sidebar.markdown(f"""
    **{t['new_features']}:**
    - ✨ **{t['session']} {t['filters']}**: {t['session_filter']}
    - ✨ **{t['incorrect_analysis']}**: {t['incorrect_pattern']}
    - ✨ **{t['difficulty_analysis']}**: {t['difficulty_comparison']}
    - ✨ **{t['problem_type']} {t['filters']}**: {t['problem_type_filter']}
    
    **{t['existing_features']}:**
    - {t['basic_filters']}
    - {t['law_analysis_desc']}
    - {t['detail_analysis']}
    """)
    
    st.sidebar.info(f"📊 {t['current_data']}: {len(filtered_df):,}{t['problems']}")

if __name__ == "__main__":
    main()