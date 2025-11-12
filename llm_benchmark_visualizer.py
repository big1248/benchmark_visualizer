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
        'response_time_analysis': '응답시간 분석',
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
        'most_models_incorrect': '대부분 모델이 틀린 문제 (≥50%)',
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
        'font_size': '화면 폰트 크기',
        'chart_text_size': '차트 텍스트 크기',
        'year_problem_distribution': '연도별 문제 수 분포',
        'problem_count_table': '연도별 문제 수 테이블',
        'year_problem_chart': '연도별 문제 수',
        'total_problem_count': '총 문제 수',
        'correct_models': '정답 모델',
        'incorrect_models': '오답 모델',
        'avg_accuracy_by_model': '모델별 평균 정확도',
        'difficulty_range': '난이도 구간',
        'avg_difficulty': '평균 난이도',
        'difficulty_stats_by_range': '난이도 구간별 상세 통계',
        'very_hard': '매우 어려움',
        'hard': '어려움',
        'medium': '보통',
        'easy': '쉬움',
        'very_easy': '매우 쉬운',
        'problem_distribution': '문제 분포',
        'response_time': '응답 시간',
        'avg_response_time': '평균 응답 시간',
        'response_time_distribution': '응답 시간 분포',
        'response_time_by_model': '모델별 응답 시간',
        'response_time_stats': '응답 시간 통계',
        'fastest_model': '가장 빠른 모델',
        'slowest_model': '가장 느린 모델',
        'response_time_vs_accuracy': '응답 시간 vs 정확도',
        'time_per_problem': '문제당 시간',
        'total_time': '총 소요 시간',
        'seconds': '초',
        'minutes': '분',
        # 토큰 및 비용 관련
        'token_cost_analysis': '토큰 및 비용 분석',
        'token_usage': '토큰 사용량',
        'input_tokens': '입력 토큰',
        'output_tokens': '출력 토큰',
        'total_tokens': '총 토큰',
        'avg_tokens_per_problem': '문제당 평균 토큰',
        'token_distribution': '토큰 분포',
        'token_efficiency': '토큰 효율성',
        'token_stats': '토큰 통계',
        'io_ratio': '입출력 토큰 비율',
        'token_per_correct': '정답당 토큰',
        'tokens': '토큰',
        'cost_level': '비용 수준',
        'cost_analysis': '비용 분석',
        'cost_per_problem': '문제당 비용',
        'total_cost_estimate': '총 예상 비용',
        'cost_vs_accuracy': '비용 vs 정확도',
        'cost_efficiency': '비용 효율성',
        'most_efficient': '가장 효율적인 모델',
        'least_efficient': '가장 비효율적인 모델',
        'cost_stats': '비용 통계',
        'high': '높음',
        'medium_cost': '중간',
        'low': '낮음',
        'very_low': '매우낮음',
        'free': '무료',
        'cost': '비용',
        'actual_cost': '실제 비용',
        'estimated_cost': '예상 비용',
        'cost_per_1k_tokens': '1K 토큰당 비용',
        'total_estimated_cost': '총 예상 비용',
        'usd': '달러',
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
        'response_time_analysis': 'Response Time Analysis',
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
        'most_models_incorrect': 'Problems Most Models Got Wrong (≥50%)',
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
        'font_size': 'Screen Font Size',
        'chart_text_size': 'Chart Text Size',
        'year_problem_distribution': 'Problem Distribution by Year',
        'problem_count_table': 'Problem Count by Year',
        'year_problem_chart': 'Problems by Year',
        'total_problem_count': 'Total Problems',
        'correct_models': 'Correct Models',
        'incorrect_models': 'Incorrect Models',
        'avg_accuracy_by_model': 'Average Accuracy by Model',
        'difficulty_range': 'Difficulty Range',
        'avg_difficulty': 'Average Difficulty',
        'difficulty_stats_by_range': 'Detailed Statistics by Difficulty Range',
        'very_hard': 'Very Hard',
        'hard': 'Hard',
        'medium': 'Medium',
        'easy': 'Easy',
        'very_easy': 'Very Easy',
        'problem_distribution': 'Problem Distribution',
        'response_time': 'Response Time',
        'avg_response_time': 'Average Response Time',
        'response_time_distribution': 'Response Time Distribution',
        'response_time_by_model': 'Response Time by Model',
        'response_time_stats': 'Response Time Statistics',
        'fastest_model': 'Fastest Model',
        'slowest_model': 'Slowest Model',
        'response_time_vs_accuracy': 'Response Time vs Accuracy',
        'time_per_problem': 'Time per Problem',
        'total_time': 'Total Time',
        'seconds': 'seconds',
        'minutes': 'minutes',
        # Token & Cost related
        'token_cost_analysis': 'Token & Cost Analysis',
        'token_usage': 'Token Usage',
        'input_tokens': 'Input Tokens',
        'output_tokens': 'Output Tokens',
        'total_tokens': 'Total Tokens',
        'avg_tokens_per_problem': 'Avg Tokens per Problem',
        'token_distribution': 'Token Distribution',
        'token_efficiency': 'Token Efficiency',
        'token_stats': 'Token Statistics',
        'io_ratio': 'Input/Output Token Ratio',
        'token_per_correct': 'Tokens per Correct Answer',
        'tokens': 'tokens',
        'cost_level': 'Cost Level',
        'cost_analysis': 'Cost Analysis',
        'cost_per_problem': 'Cost per Problem',
        'total_cost_estimate': 'Total Cost Estimate',
        'cost_vs_accuracy': 'Cost vs Accuracy',
        'cost_efficiency': 'Cost Efficiency',
        'most_efficient': 'Most Efficient Model',
        'least_efficient': 'Least Efficient Model',
        'cost_stats': 'Cost Statistics',
        'high': 'High',
        'medium_cost': 'Medium',
        'low': 'Low',
        'very_low': 'Very Low',
        'free': 'Free',
        'cost': 'cost',
        'actual_cost': 'Actual Cost',
        'estimated_cost': 'Estimated Cost',
        'cost_per_1k_tokens': 'Cost per 1K Tokens',
        'total_estimated_cost': 'Total Estimated Cost',
        'usd': 'USD',
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
            font-size: {int(16 * font_size_multiplier)}px !important;
        }}
        
        .dataframe th {{
            font-size: {int(16 * font_size_multiplier)}px !important;
            font-weight: 600 !important;
        }}
        
        .dataframe td {{
            font-size: {int(16 * font_size_multiplier)}px !important;
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

# Plotly 차트 글로벌 폰트 크기 설정
def set_plotly_font_size(chart_text_multiplier=1.0):
    """모든 Plotly 차트에 적용될 기본 폰트 크기 설정"""
    import plotly.io as pio
    
    # 기본 폰트 크기 계산
    title_size = int(20 * chart_text_multiplier)
    axis_size = int(14 * chart_text_multiplier)
    tick_size = int(12 * chart_text_multiplier)
    legend_size = int(12 * chart_text_multiplier)
    
    # plotly 기본 템플릿 복사
    pio.templates["custom"] = pio.templates["plotly"]
    
    # 전역 폰트 크기 설정
    pio.templates["custom"].layout.font.size = axis_size
    pio.templates["custom"].layout.title.font.size = title_size
    
    # 축 폰트 설정
    pio.templates["custom"].layout.xaxis.tickfont.size = tick_size
    pio.templates["custom"].layout.xaxis.title.font.size = axis_size
    pio.templates["custom"].layout.yaxis.tickfont.size = tick_size
    pio.templates["custom"].layout.yaxis.title.font.size = axis_size
    
    # 범례 폰트 설정
    pio.templates["custom"].layout.legend.font.size = legend_size
    
    # 기본 템플릿으로 설정
    pio.templates.default = "custom"
    
    return int(12 * chart_text_multiplier)  # 히트맵용 크기 반환

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
    
    # testset에서 테스트명 목록 추출 (자동 감지)
    available_test_names = list(testsets.keys())
    
    # 결과 파일들 로드
    result_files = glob.glob(os.path.join(data_dir, "*_detailed_*.csv")) + \
                   glob.glob(os.path.join(data_dir, "*_summary_*.csv"))
    
    results = []
    for file in result_files:
        filename = os.path.basename(file)
        
        try:
            # 파일명 형식: {모델명}_{상세도}_{프롬프팅}_{테스트명}.csv
            # 예: llama-3-3-70b_detailed_noprompting_산업안전기사.csv
            
            # 테스트명 찾기 및 제거 (testset에서 추출한 목록 사용)
            test_name = None
            filename_without_csv = filename.replace('.csv', '')
            
            # 가장 긴 테스트명부터 매칭 (부분 매칭 방지)
            sorted_test_names = sorted(available_test_names, key=len, reverse=True)
            
            for tn in sorted_test_names:
                if filename_without_csv.endswith('_' + tn):
                    test_name = tn
                    # 테스트명 제거
                    filename_without_test = filename_without_csv[:-len('_' + tn)]
                    break
            
            if test_name is None:
                continue
            
            # 남은 부분을 '_'로 분리
            parts = filename_without_test.split('_')
            
            if len(parts) < 3:
                continue
            
            # 상세도 찾기 (detailed 또는 summary)
            detail_type = None
            detail_idx = -1
            for i, part in enumerate(parts):
                if part in ['detailed', 'summary']:
                    detail_type = part
                    detail_idx = i
                    break
            
            if detail_type is None or detail_idx == -1:
                continue
            
            # 모델명 추출 (상세도 이전까지의 모든 부분을 결합)
            model_parts = parts[:detail_idx]
            model_raw = '_'.join(model_parts)
            
            # 프롬프팅 방식 추출 (상세도 다음부터 끝까지)
            prompt_parts = parts[detail_idx + 1:]
            prompt_raw = '_'.join(prompt_parts)
            
            # 프롬프팅 방식 정규화
            if "noprompting" in prompt_raw.lower() or "no-prompting" in prompt_raw.lower() or "no_prompting" in prompt_raw.lower():
                prompt_type = "no-prompting"
            elif "few-shot" in prompt_raw.lower() or "few_shot" in prompt_raw.lower() or "fewshot" in prompt_raw.lower():
                prompt_type = "few-shot"
            elif "cot" in prompt_raw.lower() or "chain-of-thought" in prompt_raw.lower():
                prompt_type = "cot"
            else:
                prompt_type = prompt_raw if prompt_raw else "unknown"
            
            # 🔥 모델명 자동 파싱 및 정규화 (하드코딩 제거)
            # 언더스코어를 하이픈으로 변환하고 소문자로 정규화
            model_normalized = model_raw.lower().replace('_', '-')
            
            # 스마트 모델명 표시 변환 함수
            def format_model_name(model_str):
                """
                모델명을 사람이 읽기 쉬운 형식으로 변환
                예: claude-sonnet-4-5-20250929 → Claude-Sonnet-4.5
                    gpt-4o-mini → GPT-4o-Mini
                    llama-3-3-70b → Llama-3.3-70b
                """
                # 날짜 패턴 제거 (8자리 숫자)
                import re
                model_str = re.sub(r'-\d{8}$', '', model_str)
                
                # 특수 케이스: GPT 모델
                if model_str.startswith('gpt-'):
                    # gpt-4o-mini → GPT-4o-Mini
                    parts = model_str.split('-')
                    formatted_parts = ['GPT']
                    
                    for i in range(1, len(parts)):
                        part = parts[i]
                        # 4o는 그대로 유지 (소문자 o)
                        if part == '4o' or part == '3.5':
                            formatted_parts.append(part)
                        # 숫자는 그대로
                        elif part.isdigit():
                            formatted_parts.append(part)
                        # mini, turbo 등은 첫 글자만 대문자
                        else:
                            formatted_parts.append(part.capitalize())
                    
                    return '-'.join(formatted_parts)
                
                # Claude 모델 처리
                if model_str.startswith('claude-'):
                    parts = model_str.split('-')
                    formatted_parts = ['Claude']
                    
                    i = 1
                    while i < len(parts):
                        part = parts[i]
                        
                        # 버전 번호 처리 (4-5 → 4.5, 3-5 → 3.5)
                        if i + 1 < len(parts) and part.isdigit() and parts[i+1].isdigit():
                            formatted_parts.append(f"{part}.{parts[i+1]}")
                            i += 2
                        # 모델 타입은 첫 글자 대문자
                        elif part in ['sonnet', 'haiku', 'opus']:
                            formatted_parts.append(part.capitalize())
                            i += 1
                        # 숫자는 그대로
                        elif part.isdigit():
                            formatted_parts.append(part)
                            i += 1
                        else:
                            formatted_parts.append(part.capitalize())
                            i += 1
                    
                    return '-'.join(formatted_parts)
                
                # 기타 모델: 스마트 버전 번호 처리
                # 예: llama-3-3-70b → Llama-3.3-70b
                #     qwen-2-5-72b → Qwen-2.5-72b
                #     qwen2-5-32b → Qwen2.5-32b
                parts = model_str.split('-')
                formatted_parts = []
                
                i = 0
                while i < len(parts):
                    part = parts[i]
                    
                    # 첫 번째 파트 (모델명)
                    if i == 0:
                        # 특수 케이스: qwen2, llama3 등 숫자가 붙은 모델명
                        if part[:-1].isalpha() and part[-1].isdigit():
                            # 다음 파트가 한 자리 숫자면 버전으로 변환
                            if i + 1 < len(parts) and parts[i+1].isdigit() and len(parts[i+1]) == 1:
                                formatted_parts.append(f"{part.capitalize()}.{parts[i+1]}")
                                i += 2
                                continue
                        formatted_parts.append(part.capitalize())
                        i += 1
                    # 연속된 두 개의 한 자리 숫자 → 버전 번호로 변환
                    elif (i + 1 < len(parts) and 
                          part.isdigit() and len(part) == 1 and 
                          parts[i+1].isdigit() and len(parts[i+1]) == 1):
                        formatted_parts.append(f"{part}.{parts[i+1]}")
                        i += 2
                    # 일반 단어는 첫 글자 대문자
                    elif not part.isdigit() and not any(c.isdigit() for c in part):
                        formatted_parts.append(part.capitalize())
                        i += 1
                    # 숫자나 숫자+문자 조합은 그대로
                    else:
                        formatted_parts.append(part)
                        i += 1
                
                return '-'.join(formatted_parts)
            
            model = format_model_name(model_normalized)
            
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
    
    # 화면 설정
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 " + ("화면 설정" if lang == 'ko' else "Display Settings"))
    
    # 폰트 크기 조정
    font_size = st.sidebar.slider(
        t['font_size'],
        min_value=0.8,
        max_value=1.5,
        value=1.0,
        step=0.1,
        help="화면 전체의 폰트 크기를 조절합니다"
    )
    
    # 차트 텍스트 크기 조정
    chart_text_size = st.sidebar.slider(
        t['chart_text_size'],
        min_value=0.7,
        max_value=1.8,
        value=1.0,
        step=0.1,
        help="차트 내부 텍스트, 숫자, 레이블 크기를 조절합니다"
    )
    
    apply_custom_css(font_size)
    annotation_size = set_plotly_font_size(chart_text_size)
    
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
        f"⏱️ {t['response_time_analysis']}",
        f"⚖️ {t['law_analysis']}",
        f"📚 {t['subject_analysis']}",
        f"📅 {t['year_analysis']}",
        f"❌ {t['incorrect_analysis']}",
        f"📈 {t['difficulty_analysis']}",
        f"💰 {t['token_cost_analysis']}",
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
        st.subheader("📋 " + ("테스트셋 정보" if lang == 'ko' else "Test Set Information"))
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 테스트셋 파일의 실제 문제 수 사용
            display_problems = total_problems if total_problems > 0 else unique_questions
            st.metric(
                "총 문제 수" if lang == 'ko' else "Total Problems",
                f"{display_problems:,}"
            )
        with col2:
            st.metric(
                "평가 모델 수" if lang == 'ko' else "Number of Models",
                f"{num_models}"
            )
        with col3:
            # 수정: 총 평가 횟수 = 총 문제 수 × 모델 수
            actual_eval_count = display_problems * num_models
            st.metric(
                "총 평가 횟수" if lang == 'ko' else "Total Evaluations",
                f"{actual_eval_count:,}"
            )
        
        st.markdown("---")
        
        # 모델 평균 성능
        st.subheader("🎯 " + ("모델 평균 성능" if lang == 'ko' else "Average Model Performance"))
        col1, col2, col3, col4 = st.columns(4)
        
        # 모델별 정확도 계산 후 평균
        model_accuracies = filtered_df.groupby('모델')['정답여부'].mean()
        avg_accuracy = model_accuracies.mean() * 100
        
        # 평균 정답/오답 수 (모델당)
        avg_problems_per_model = display_problems  # 모델당 평가한 문제 수 (테스트셋 기준)
        avg_correct = (avg_problems_per_model * avg_accuracy / 100) if avg_problems_per_model > 0 else 0
        avg_wrong = avg_problems_per_model - avg_correct
        
        with col1:
            st.metric(
                "평균 정확도" if lang == 'ko' else "Average Accuracy",
                f"{avg_accuracy:.2f}%"
            )
        with col2:
            st.metric(
                "모델당 평균 문제 수" if lang == 'ko' else "Avg Problems per Model",
                f"{avg_problems_per_model:.0f}"
            )
        with col3:
            st.metric(
                "평균 정답 수" if lang == 'ko' else "Avg Correct Answers",
                f"{avg_correct:.0f}"
            )
        with col4:
            st.metric(
                "평균 오답 수" if lang == 'ko' else "Avg Wrong Answers",
                f"{avg_wrong:.0f}"
            )
        
        # 법령/비법령 통계
        if 'law' in filtered_df.columns:
            st.markdown("---")
            st.subheader("⚖️ " + ("법령/비법령 분석" if lang == 'ko' else "Law/Non-Law Analysis"))
            
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
        st.subheader("📊 " + ("주요 지표 시각화" if lang == 'ko' else "Key Metrics Visualization"))
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 모델별 평균 정확도 바 차트
            model_acc_df = filtered_df.groupby('모델')['정답여부'].mean().reset_index()
            model_acc_df.columns = [t['model'], t['accuracy']]
            model_acc_df[t['accuracy']] = model_acc_df[t['accuracy']] * 100
            model_acc_df = model_acc_df.sort_values(t['accuracy'], ascending=False)
            
            fig = px.bar(
                model_acc_df,
                x=t['model'],
                y=t['accuracy'],
                title=t['avg_accuracy_by_model'],
                text=t['accuracy'],
                color=t['accuracy'],
                color_continuous_scale='RdYlGn'
            )
            fig.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                marker_line_color='black',
                marker_line_width=1.5
            )
            fig.update_layout(
                height=400,
                showlegend=False,
                yaxis_title=t['accuracy'] + ' (%)',
                xaxis_title=t['model'],
                yaxis=dict(range=[0, 100])
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 법령/비법령 정답률 비교 차트
            if 'law' in filtered_df.columns:
                law_comparison = pd.DataFrame({
                    '구분': [t['law'], t['non_law']],
                    '정답률': [law_accuracy, non_law_accuracy],
                    '문제수': [law_count, non_law_count]
                })
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name=t['correct_rate'] if lang == 'ko' else 'Accuracy',
                    x=law_comparison['구분'],
                    y=law_comparison['정답률'],
                    text=law_comparison['정답률'].round(1),
                    texttemplate='%{text}%',
                    textposition='outside',
                    marker_color=['#FF6B6B', '#4ECDC4'],
                    marker_line_color='black',
                    marker_line_width=1.5,
                    yaxis='y'
                ))
                
                fig.add_trace(go.Scatter(
                    name=t['problem_count'] if lang == 'ko' else 'Problem Count',
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
                    title='법령/비법령 정답률 및 문제 수 비교' if lang == 'ko' else 'Law/Non-Law Accuracy and Problem Count Comparison',
                    height=400,
                    yaxis=dict(
                        title=('정답률 (%)' if lang == 'ko' else 'Accuracy (%)'),
                        range=[0, 100]
                    ),
                    yaxis2=dict(
                        title=(t['problem_count'] if lang == 'ko' else 'Problem Count'),
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
                fig.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                marker_line_color='black',
                marker_line_width=1.5
            )
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
            fig.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                marker_line_color='black',
                marker_line_width=1.5
            )
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
                marker_color='lightgreen',
                marker_line_color='black',
                marker_line_width=1.5
            ))
            fig.add_trace(go.Bar(
                name=t['wrong'],
                x=model_stats['모델'],
                y=model_stats['오답'],
                marker_color='lightcoral',
                marker_line_color='black',
                marker_line_width=1.5
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
            
            # 히트맵 생성 (숫자 표시 및 셀 경계선 추가)
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_pivot.values,
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index,
                colorscale='RdYlGn',
                text=np.round(heatmap_pivot.values, 1),
                texttemplate='%{text:.1f}',
                textfont={"size": int(12 * chart_text_size)},
                colorbar=dict(title=t['accuracy'] + " (%)"),
                xgap=2,  # 셀 경계선
                ygap=2
            ))
            
            fig.update_layout(height=400)
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # 탭 3: 응답시간 분석
    with tabs[2]:
        st.header(f"⏱️ {t['response_time_analysis']}")
        
        # 문제당평균시간(초) 컬럼이 있는지 확인
        time_columns = ['문제당평균시간(초)', '총소요시간(초)', 'question_duration']
        available_time_col = None
        for col in time_columns:
            if col in filtered_df.columns:
                available_time_col = col
                break
        
        if available_time_col is None:
            st.info("Response time data not available in the dataset.")
        else:
            # 응답시간 데이터 준비
            if available_time_col == 'question_duration':
                # question_duration은 개별 문제 시간
                time_col = 'question_duration'
                is_per_problem = True
            elif available_time_col == '문제당평균시간(초)':
                time_col = '문제당평균시간(초)'
                is_per_problem = True
            else:
                time_col = '총소요시간(초)'
                is_per_problem = False
            
            # NaN 값 제거
            time_df = filtered_df[filtered_df[time_col].notna()].copy()
            
            if len(time_df) == 0:
                st.info("No valid response time data available.")
            else:
                # 1. 모델별 평균 응답시간 통계
                st.subheader(t['response_time_stats'])
                
                model_time_stats = time_df.groupby('모델').agg({
                    time_col: ['mean', 'median', 'std', 'min', 'max', 'count']
                }).reset_index()
                
                model_time_stats.columns = ['모델', '평균', '중앙값', '표준편차', '최소', '최대', '문제수']
                model_time_stats = model_time_stats.sort_values('평균')
                
                # 정확도도 함께 표시
                model_acc = filtered_df.groupby('모델')['정답여부'].mean().reset_index()
                model_acc.columns = ['모델', '정확도']
                model_acc['정확도'] = model_acc['정확도'] * 100
                
                model_time_stats = model_time_stats.merge(model_acc, on='모델')
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    fastest = model_time_stats.iloc[0]
                    st.metric(
                        t['fastest_model'],
                        fastest['모델'],
                        f"{fastest['평균']:.2f}{t['seconds']}"
                    )
                
                with col2:
                    slowest = model_time_stats.iloc[-1]
                    st.metric(
                        t['slowest_model'],
                        slowest['모델'],
                        f"{slowest['평균']:.2f}{t['seconds']}"
                    )
                
                with col3:
                    avg_time = model_time_stats['평균'].mean()
                    st.metric(
                        t['avg_response_time'],
                        f"{avg_time:.2f}{t['seconds']}"
                    )
                
                # 테이블
                st.dataframe(
                    model_time_stats.style.format({
                        '평균': '{:.2f}',
                        '중앙값': '{:.2f}',
                        '표준편차': '{:.2f}',
                        '최소': '{:.2f}',
                        '최대': '{:.2f}',
                        '문제수': '{:.0f}',
                        '정확도': '{:.2f}%'
                    }).background_gradient(subset=['평균'], cmap='RdYlGn_r'),
                    use_container_width=True
                )
                
                st.markdown("---")
                
                # 2. 시각화
                st.subheader(t['response_time_by_model'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # 평균 응답시간 바 차트
                    fig = px.bar(
                        model_time_stats,
                        x='모델',
                        y='평균',
                        title=t['avg_response_time'] + (' (' + t['time_per_problem'] + ')' if is_per_problem else ''),
                        text='평균',
                        color='평균',
                        color_continuous_scale='RdYlGn_r'
                    )
                    fig.update_traces(
                        texttemplate='%{text:.2f}s',
                        textposition='outside',
                        marker_line_color='black',
                        marker_line_width=1.5
                    )
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        yaxis_title=t['response_time'] + ' (' + t['seconds'] + ')',
                        xaxis_title=t['model']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # 박스플롯
                    fig = px.box(
                        time_df,
                        x='모델',
                        y=time_col,
                        title=t['response_time_distribution'],
                        color='모델'
                    )
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        yaxis_title=t['response_time'] + ' (' + t['seconds'] + ')',
                        xaxis_title=t['model']
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # 3. 응답시간 vs 정확도
                st.subheader(t['response_time_vs_accuracy'])
                
                fig = px.scatter(
                    model_time_stats,
                    x='평균',
                    y='정확도',
                    size='문제수',
                    text='모델',
                    title=t['response_time_vs_accuracy'],
                    labels={
                        '평균': t['avg_response_time'] + ' (' + t['seconds'] + ')',
                        '정확도': t['accuracy'] + ' (%)'
                    }
                )
                fig.update_traces(
                    textposition='top center',
                    marker=dict(
                        line=dict(width=2, color='black'),
                        opacity=0.7
                    )
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
                
                # 인사이트
                st.info(f"""
                💡 **인사이트**:
                - 가장 빠른 모델: **{fastest['모델']}** ({fastest['평균']:.2f}초, 정확도 {fastest['정확도']:.1f}%)
                - 가장 느린 모델: **{slowest['모델']}** ({slowest['평균']:.2f}초, 정확도 {slowest['정확도']:.1f}%)
                - 속도와 정확도의 상관관계를 차트에서 확인하세요.
                """)
                
                st.markdown("---")
                
                # 4. 테스트별 응답시간 (테스트가 여러 개인 경우)
                if '테스트명' in time_df.columns and time_df['테스트명'].nunique() > 1:
                    st.subheader(f"{t['response_time']} ({t['by_test']})" if 'by_test' in t else "테스트별 응답시간")
                    
                    test_time = time_df.groupby(['모델', '테스트명'])[time_col].mean().reset_index()
                    test_time.columns = ['모델', '테스트명', '평균시간']
                    
                    fig = px.bar(
                        test_time,
                        x='테스트명',
                        y='평균시간',
                        color='모델',
                        barmode='group',
                        title='테스트별 모델 응답시간' if lang == 'ko' else 'Response Time by Test',
                        labels={'평균시간': t['avg_response_time'] + ' (' + t['seconds'] + ')'}
                    )
                    fig.update_layout(
                        height=400,
                        xaxis_title=t['testname'],
                        yaxis_title=t['response_time'] + ' (' + t['seconds'] + ')'
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
    
    # 탭 4: 법령/비법령 분석
    with tabs[3]:
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
                    hole=0.3,
                    marker=dict(line=dict(color='black', width=2))
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
    
    # 탭 5: 과목별 분석
    with tabs[4]:
        if 'Subject' not in filtered_df.columns:
            st.info("Subject data not available.")
        else:
            st.header(f"📚 {t['subject_analysis']}")
            
            # 과목별 성능
            subject_stats = filtered_df.groupby('Subject').agg({
                '정답여부': ['sum', 'count', 'mean']
            }).reset_index()
            
            # 컬럼명 언어별 설정
            if lang == 'ko':
                subject_stats.columns = ['과목', '정답', '총문제', '정확도']
                subj_col = '과목'
                acc_col = '정확도'
                correct_col = '정답'
                total_col = '총문제'
            else:
                subject_stats.columns = ['Subject', 'Correct', 'Total', 'Accuracy']
                subj_col = 'Subject'
                acc_col = 'Accuracy'
                correct_col = 'Correct'
                total_col = 'Total'
            
            subject_stats[acc_col] = subject_stats[acc_col] * 100
            subject_stats = subject_stats.sort_values(acc_col, ascending=False)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # 테이블
                st.dataframe(
                    subject_stats.style.format({acc_col: '{:.2f}%'})
                    .background_gradient(subset=[acc_col], cmap='RdYlGn'),
                    use_container_width=True
                )
            
            with col2:
                # 바 차트
                fig = px.bar(
                    subject_stats,
                    x=subj_col,
                    y=acc_col,
                    title=t['subject_performance'],
                    text=acc_col,
                    color=acc_col,
                    color_continuous_scale='RdYlGn',
                    labels={subj_col: t['by_subject'].replace('별', ''), acc_col: t['accuracy'] + ' (%)'}
                )
                fig.update_traces(
                    texttemplate='%{text:.1f}%',
                    textposition='outside',
                    marker_line_color='black',
                    marker_line_width=1.5
                )
                fig.update_layout(
                    height=400,
                    showlegend=False,
                    yaxis_title=t['accuracy'] + ' (%)',
                    xaxis_title=t['by_subject'].replace('별', '')
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
            
            # 모델별 과목 성능 히트맵 (셀 경계선 추가)
            st.markdown("---")
            subject_model = filtered_df.groupby(['모델', 'Subject'])['정답여부'].mean() * 100
            subject_model_pivot = subject_model.unstack(fill_value=0)
            
            fig = go.Figure(data=go.Heatmap(
                z=subject_model_pivot.values,
                x=subject_model_pivot.columns,
                y=subject_model_pivot.index,
                colorscale='RdYlGn',
                text=np.round(subject_model_pivot.values, 1),
                texttemplate='%{text:.1f}',
                textfont={"size": int(12 * chart_text_size)},
                colorbar=dict(title=t['accuracy'] + " (%)"),
                xgap=2,  # 셀 경계선
                ygap=2
            ))
            fig.update_layout(height=400)
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # 탭 6: 연도별 분석
    with tabs[5]:
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
                    fig.update_traces(
                        texttemplate='%{text:.1f}%',
                        textposition='top center',
                        marker_size=10,
                        marker_line_color='black',
                        marker_line_width=2,
                        line_width=3
                    )
                    fig.update_layout(
                        height=400,
                        yaxis_title=t['accuracy'] + ' (%)',
                        xaxis_title=t['year']
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # 연도별 문제 수 차트 추가
                st.markdown("---")
                st.subheader(f"📊 {t['year_problem_distribution']}")
                
                # 다국어 컬럼명 설정
                year_col = t['year']
                count_col = t['problem_count']
                
                # 테스트셋에서 실제 문제 수 계산 (중복 제거)
                if selected_tests:
                    year_problem_count = []
                    for test_name in selected_tests:
                        if test_name in testsets and 'Year' in testsets[test_name].columns:
                            test_year_counts = testsets[test_name].groupby('Year').size()
                            for year, count in test_year_counts.items():
                                year_int = safe_convert_to_int(year)
                                if year_int:
                                    year_problem_count.append({year_col: year_int, count_col: count})
                    
                    if year_problem_count:
                        year_problem_df = pd.DataFrame(year_problem_count)
                        year_problem_df = year_problem_df.groupby(year_col)[count_col].sum().reset_index()
                        year_problem_df = year_problem_df.sort_values(year_col)
                    else:
                        # 백업: filtered_df에서 고유 문제 수 계산
                        year_problem_df = year_df.groupby('Year_Int')['Question'].nunique().reset_index()
                        year_problem_df.columns = [year_col, count_col]
                        year_problem_df[year_col] = year_problem_df[year_col].astype(int)
                        year_problem_df = year_problem_df.sort_values(year_col)
                else:
                    # 테스트 선택 안 됨: filtered_df에서 계산
                    year_problem_df = year_df.groupby('Year_Int')['Question'].nunique().reset_index()
                    year_problem_df.columns = [year_col, count_col]
                    year_problem_df[year_col] = year_problem_df[year_col].astype(int)
                    year_problem_df = year_problem_df.sort_values(year_col)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # 연도별 문제 수 테이블
                    st.dataframe(
                        year_problem_df.style.format({
                            year_col: '{:.0f}',
                            count_col: '{:.0f}'
                        })
                        .background_gradient(subset=[count_col], cmap='Blues'),
                        use_container_width=True
                    )
                    
                    # 총 문제 수 표시
                    st.metric(t['total_problem_count'], f"{year_problem_df[count_col].sum():,.0f}" + (t['problems'] if lang == 'ko' else ''))
                
                with col2:
                    # 바 차트
                    fig = px.bar(
                        year_problem_df,
                        x=year_col,
                        y=count_col,
                        title=t['year_problem_chart'],
                        text=count_col,
                        color=count_col,
                        color_continuous_scale='Blues'
                    )
                    fig.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                marker_line_color='black',
                marker_line_width=1.5
            )
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        yaxis_title=t['problem_count'],
                        xaxis_title=t['year'],
                        xaxis=dict(tickmode='linear')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # 모델별 연도 성능 히트맵
                st.markdown("---")
                year_model = year_df.groupby(['모델', 'Year_Int'])['정답여부'].mean() * 100
                year_model_pivot = year_model.unstack(fill_value=0)
                
                # 컬럼명을 정수로 변환
                year_model_pivot.columns = year_model_pivot.columns.astype(int)
                
                fig = go.Figure(data=go.Heatmap(
                    z=year_model_pivot.values,
                    x=year_model_pivot.columns,
                    y=year_model_pivot.index,
                    colorscale='RdYlGn',
                    text=np.round(year_model_pivot.values, 1),
                    texttemplate='%{text:.1f}',
                    textfont={"size": int(12 * chart_text_size)},
                    colorbar=dict(title=t['accuracy'] + " (%)"),
                    xgap=2,  # 셀 경계선
                    ygap=2
                ))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("연도 정보가 있는 데이터가 없습니다.")
    
    # 탭 7: 오답 분석
    with tabs[6]:
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
            
            # 문제 상세 보기 옵션 - 모든 문제 표시
            if st.checkbox('문제 내용 보기' if lang == 'ko' else 'Show Question Details'):
                st.info(f"총 {len(all_wrong)}개 문제의 상세 내용을 표시합니다." if lang == 'ko' else f"Showing details for all {len(all_wrong)} problems.")
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
        
        # 대부분 모델이 틀린 문제 (50% 이상)
        st.markdown("---")
        st.subheader(t['most_models_incorrect'])
        
        most_wrong = problem_analysis[problem_analysis['incorrect_rate'] >= 0.5]
        
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
            
            # 문제 상세 보기 옵션 - 모든 문제 표시
            if st.checkbox('문제 내용 보기 (대부분 틀린 문제)' if lang == 'ko' else 'Show Question Details (Most Incorrect)', key='most_wrong_details'):
                st.info(f"총 {len(most_wrong)}개 문제의 상세 내용을 표시합니다." if lang == 'ko' else f"Showing details for all {len(most_wrong)} problems.")
                for idx, row in most_wrong.iterrows():  # 모든 문제 표시
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
    
    # 탭 8: 난이도 분석
    with tabs[7]:
        st.header(f"📈 {t['difficulty_analysis']}")
        
        # 문제별 난이도 계산 (정답률 기반)
        difficulty = filtered_df.groupby('Question').agg({
            '정답여부': ['sum', 'count', 'mean']
        }).reset_index()
        difficulty.columns = ['Question', 'correct_count', 'total_count', 'difficulty_score']
        difficulty['difficulty_score'] = difficulty['difficulty_score'] * 100
        
        # 난이도 구간 분류
        def classify_difficulty(score, lang='ko'):
            if lang == 'ko':
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
            else:  # English
                if score < 20:
                    return 'Very Hard (0-20%)'
                elif score < 40:
                    return 'Hard (20-40%)'
                elif score < 60:
                    return 'Medium (40-60%)'
                elif score < 80:
                    return 'Easy (60-80%)'
                else:
                    return 'Very Easy (80-100%)'
        
        difficulty['난이도_구간'] = difficulty['difficulty_score'].apply(lambda x: classify_difficulty(x, lang))
        
        # 난이도 구간 순서 정의 (어려운 것부터 쉬운 것 순)
        if lang == 'ko':
            difficulty_order = [
                '매우 어려움 (0-20%)',
                '어려움 (20-40%)',
                '보통 (40-60%)',
                '쉬움 (60-80%)',
                '매우 쉬움 (80-100%)'
            ]
        else:
            difficulty_order = [
                'Very Hard (0-20%)',
                'Hard (20-40%)',
                'Medium (40-60%)',
                'Easy (60-80%)',
                'Very Easy (80-100%)'
            ]
        difficulty['난이도_구간'] = pd.Categorical(difficulty['난이도_구간'], categories=difficulty_order, ordered=True)
        
        # 원본 데이터에 난이도 정보 병합
        analysis_df = filtered_df.merge(difficulty[['Question', 'difficulty_score', '난이도_구간']], on='Question')
        
        # analysis_df에도 동일한 순서 적용
        analysis_df['난이도_구간'] = pd.Categorical(analysis_df['난이도_구간'], categories=difficulty_order, ordered=True)
        
        # 1. 난이도 분포
        st.subheader("📈 " + (t['problem_distribution'] if 'problem_distribution' in t else ('문제 난이도 분포' if lang == 'ko' else 'Problem Difficulty Distribution')))
        
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
            fig.update_traces(
                marker_line_color='black',
                marker_line_width=1.5
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
                title=t['problem_count'] + (' by ' + t['difficulty_range'] if lang == 'en' else ' (' + t['difficulty_range'] + '별)'),
                labels={'x': t['difficulty_range'], 'y': t['problem_count']},
                text=difficulty_dist.values,
                color=difficulty_dist.values,
                color_continuous_scale='RdYlGn_r'
            )
            fig.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                marker_line_color='black',
                marker_line_width=1.5
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
            st.metric(
                t['correct_rate'] if lang == 'ko' else 'Average Correct Rate',
                f"{difficulty['difficulty_score'].mean():.1f}%"
            )
        with col2:
            st.metric(
                '중앙값' if lang == 'ko' else 'Median',
                f"{difficulty['difficulty_score'].median():.1f}%"
            )
        with col3:
            very_hard_label = difficulty_order[0]
            very_hard = len(difficulty[difficulty['난이도_구간'] == very_hard_label])
            st.metric(
                t['very_hard'] + (' 문제' if lang == 'ko' else ' Problems'),
                f"{very_hard}" + (t['problems'] if lang == 'ko' else '')
            )
        with col4:
            very_easy_label = difficulty_order[-1]
            very_easy = len(difficulty[difficulty['난이도_구간'] == very_easy_label])
            st.metric(
                t['very_easy'] + (' 문제' if lang == 'ko' else ' Problems'),
                f"{very_easy}" + (t['problems'] if lang == 'ko' else '')
            )
        
        st.markdown("---")
        
        # 2. 난이도별 모델 성능
        st.subheader("🎯 " + ('난이도별 모델 성능' if lang == 'ko' else 'Model Performance by Difficulty Level'))
        
        # 모델별 난이도 구간별 정답률
        model_difficulty = analysis_df.groupby(['모델', '난이도_구간']).agg({
            '정답여부': ['mean', 'count']
        }).reset_index()
        
        # 컬럼명 언어별 설정
        if lang == 'ko':
            model_difficulty.columns = ['모델', '난이도_구간', '정답률', '문제수']
        else:
            model_difficulty.columns = ['Model', 'Difficulty', 'Correct Rate', 'Problem Count']
        
        # 정답률 컬럼명 (언어별)
        acc_col = '정답률' if lang == 'ko' else 'Correct Rate'
        model_col = '모델' if lang == 'ko' else 'Model'
        diff_col = '난이도_구간' if lang == 'ko' else 'Difficulty'
        
        model_difficulty[acc_col] = model_difficulty[acc_col] * 100
        
        # 라인 차트
        fig = px.line(
            model_difficulty,
            x=diff_col,
            y=acc_col,
            color=model_col,
            markers=True,
            title='난이도별 모델 성능 비교' if lang == 'ko' else 'Model Performance by Difficulty Level',
            labels={
                acc_col: t['accuracy'] + ' (%)',
                diff_col: t['difficulty_range'],
                model_col: t['model']
            },
            category_orders={diff_col: difficulty_order}
        )
        fig.update_traces(
            marker_size=10,
            marker_line_color='black',
            marker_line_width=2,
            line_width=3
        )
        fig.update_layout(height=500)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # 히트맵
        pivot_difficulty = model_difficulty.pivot(
            index=model_col,
            columns=diff_col,
            values=acc_col
        )
        
        # 난이도 순서대로 컬럼 재정렬
        pivot_difficulty = pivot_difficulty.reindex(columns=difficulty_order)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_difficulty.values,
            x=pivot_difficulty.columns,
            y=pivot_difficulty.index,
            colorscale='RdYlGn',
            text=np.round(pivot_difficulty.values, 1),
            texttemplate='%{text:.1f}',
            textfont={"size": int(12 * chart_text_size)},
            colorbar=dict(title=t['accuracy'] + " (%)"),
            xgap=2,  # 셀 경계선
            ygap=2
        ))
        fig.update_layout(
            height=400,
            title='모델 × 난이도 히트맵' if lang == 'ko' else 'Model × Difficulty Heatmap',
            xaxis_title=t['difficulty_range'],
            yaxis_title=t['model']
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # 3. 과목별 난이도 분석
        if 'Subject' in analysis_df.columns:
            st.subheader("📚 " + ('과목별 난이도 분석' if lang == 'ko' else 'Difficulty Analysis by Subject'))
            
            subject_difficulty = analysis_df.groupby('Subject').agg({
                'difficulty_score': 'mean',
                'Question': 'count'
            }).reset_index()
            
            # 컬럼명 언어별 설정
            if lang == 'ko':
                subject_difficulty.columns = ['과목', '평균_난이도', '문제수']
                subj_col = '과목'
                avg_diff_col = '평균_난이도'
            else:
                subject_difficulty.columns = ['Subject', 'Avg Difficulty', 'Problem Count']
                subj_col = 'Subject'
                avg_diff_col = 'Avg Difficulty'
            
            subject_difficulty = subject_difficulty.sort_values(avg_diff_col)
            
            fig = px.bar(
                subject_difficulty,
                x=subj_col,
                y=avg_diff_col,
                title='과목별 평균 난이도 (정답률)' if lang == 'ko' else 'Average Difficulty by Subject (Correct Rate)',
                text=avg_diff_col,
                color=avg_diff_col,
                color_continuous_scale='RdYlGn',
                labels={subj_col: t['by_subject'].replace('별', ''), avg_diff_col: t['avg_difficulty']}
            )
            fig.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                marker_line_color='black',
                marker_line_width=1.5
            )
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
            
            fig = go.Figure(data=go.Heatmap(
                z=pivot_subject_diff.values,
                x=pivot_subject_diff.columns,
                y=pivot_subject_diff.index,
                colorscale='Blues',
                text=pivot_subject_diff.values.astype(int),
                texttemplate='%{text}',
                textfont={"size": int(12 * chart_text_size)},
                colorbar=dict(title=t['problem_count']),
                xgap=2,  # 셀 경계선
                ygap=2
            ))
            fig.update_layout(
                height=500,
                title='과목 × 난이도 분포' if lang == 'ko' else 'Subject × Difficulty Distribution',
                xaxis_title=t['difficulty_range'],
                yaxis_title=t['by_subject'].replace('별', '')  # '과목' or 'Subject'
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # 4. 어려운 문제 vs 쉬운 문제 상세 분석
        st.subheader("🔍 " + (
            "어려운 문제 vs 쉬운 문제 비교" if lang == 'ko' else "Hard vs Easy Problems Comparison"
        ))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### " + (
                "매우 어려운 문제 (정답률 < 20%)" if lang == 'ko' else "Very Hard Problems (Correct Rate < 20%)"
            ))
            very_hard_problems = difficulty[difficulty['difficulty_score'] < 20].sort_values('difficulty_score')
            
            if len(very_hard_problems) > 0:
                st.metric(
                    t['problem_count'],
                    f"{len(very_hard_problems)}" + (t['problems'] if lang == 'ko' else '')
                )
                st.metric(
                    '평균 정답률' if lang == 'ko' else 'Average Correct Rate',
                    f"{very_hard_problems['difficulty_score'].mean():.1f}%"
                )
                
                # 모델별 성능
                very_hard_questions = very_hard_problems['Question'].tolist()
                very_hard_model_perf = filtered_df[filtered_df['Question'].isin(very_hard_questions)].groupby('모델')['정답여부'].mean() * 100
                
                st.markdown("**" + (
                    "모델별 성능" if lang == 'ko' else "Performance by Model"
                ) + "**")
                for model, acc in very_hard_model_perf.sort_values(ascending=False).items():
                    st.write(f"- {model}: {acc:.1f}%")
            else:
                st.info(
                    "매우 어려운 문제가 없습니다." if lang == 'ko' else "No very hard problems found."
                )
        
        with col2:
            st.markdown("#### " + (
                "매우 쉬운 문제 (정답률 > 80%)" if lang == 'ko' else "Very Easy Problems (Correct Rate > 80%)"
            ))
            very_easy_problems = difficulty[difficulty['difficulty_score'] > 80].sort_values('difficulty_score', ascending=False)
            
            if len(very_easy_problems) > 0:
                st.metric(
                    t['problem_count'],
                    f"{len(very_easy_problems)}" + (t['problems'] if lang == 'ko' else '')
                )
                st.metric(
                    '평균 정답률' if lang == 'ko' else 'Average Correct Rate',
                    f"{very_easy_problems['difficulty_score'].mean():.1f}%"
                )
                
                # 모델별 성능
                very_easy_questions = very_easy_problems['Question'].tolist()
                very_easy_model_perf = filtered_df[filtered_df['Question'].isin(very_easy_questions)].groupby('모델')['정답여부'].mean() * 100
                
                st.markdown("**" + (
                    "모델별 성능" if lang == 'ko' else "Performance by Model"
                ) + "**")
                for model, acc in very_easy_model_perf.sort_values(ascending=False).items():
                    st.write(f"- {model}: {acc:.1f}%")
            else:
                st.info(
                    "매우 쉬운 문제가 없습니다." if lang == 'ko' else "No very easy problems found."
                )
        
        st.markdown("---")
        
        # 5. 난이도 구간별 상세 테이블
        st.subheader("📋 " + t['difficulty_stats_by_range'])
        
        detailed_difficulty = model_difficulty.pivot_table(
            index=model_col,
            columns=diff_col,
            values=acc_col,
            aggfunc='mean'
        ).round(2)
        
        # 난이도 순서대로 컬럼 재정렬
        detailed_difficulty = detailed_difficulty.reindex(columns=difficulty_order)
        
        st.dataframe(
            detailed_difficulty.style.background_gradient(cmap='RdYlGn', axis=None),
            use_container_width=True
        )
    
    # 탭 9: 토큰 및 비용 분석
    with tabs[8]:
        st.header(f"💰 {t['token_cost_analysis']}")
        
        # 토큰 관련 컬럼 확인
        token_columns = {
            'input': ['입력토큰', 'input_tokens', 'Input Tokens'],
            'output': ['출력토큰', 'output_tokens', 'Output Tokens'],
            'total': ['총토큰', 'total_tokens', 'Total Tokens'],
            'cost': ['비용수준', 'cost_level', 'Cost Level']
        }
        
        # 사용 가능한 컬럼 찾기
        available_cols = {}
        for key, possible_names in token_columns.items():
            for col_name in possible_names:
                if col_name in filtered_df.columns:
                    available_cols[key] = col_name
                    break
        
        if not available_cols:
            st.info("Token usage data not available in the dataset." if lang == 'en' else "토큰 사용량 데이터가 데이터셋에 없습니다.")
        else:
            # 데이터 준비
            token_df = filtered_df.copy()
            
            # NaN 제거
            for key, col in available_cols.items():
                if col in token_df.columns:
                    token_df = token_df[token_df[col].notna()]
            
            if len(token_df) == 0:
                st.info("No valid token data available after filtering." if lang == 'en' else "필터링 후 유효한 토큰 데이터가 없습니다.")
            else:
                # 1. 토큰 통계 요약
                st.subheader(f"📊 {t['token_stats']}")
                
                # 모델별 토큰 사용량 계산
                agg_dict = {}
                if 'input' in available_cols:
                    agg_dict[available_cols['input']] = ['sum', 'mean']
                if 'output' in available_cols:
                    agg_dict[available_cols['output']] = ['sum', 'mean']
                if 'total' in available_cols:
                    agg_dict[available_cols['total']] = ['sum', 'mean']
                
                model_token_stats = token_df.groupby('모델').agg(agg_dict).reset_index()
                
                # 컬럼명 정리
                new_cols = ['모델']
                for col in model_token_stats.columns[1:]:
                    if col[0] == available_cols.get('input', ''):
                        if col[1] == 'sum':
                            new_cols.append('총_입력토큰')
                        else:
                            new_cols.append('평균_입력토큰')
                    elif col[0] == available_cols.get('output', ''):
                        if col[1] == 'sum':
                            new_cols.append('총_출력토큰')
                        else:
                            new_cols.append('평균_출력토큰')
                    elif col[0] == available_cols.get('total', ''):
                        if col[1] == 'sum':
                            new_cols.append('총_토큰')
                        else:
                            new_cols.append('평균_토큰')
                
                model_token_stats.columns = new_cols
                
                # 정확도 추가
                model_acc = token_df.groupby('모델')['정답여부'].mean().reset_index()
                model_acc.columns = ['모델', '정확도']
                model_acc['정확도'] = model_acc['정확도'] * 100
                
                model_token_stats = model_token_stats.merge(model_acc, on='모델')
                
                # 문제 수 추가
                model_problem_count = token_df.groupby('모델')['Question'].count().reset_index()
                model_problem_count.columns = ['모델', '문제수']
                model_token_stats = model_token_stats.merge(model_problem_count, on='모델')
                
                # 비용 수준 추가 (있는 경우)
                if 'cost' in available_cols:
                    cost_col = available_cols['cost']
                    # 가장 빈번한 비용 수준 찾기
                    model_cost = token_df.groupby('모델')[cost_col].agg(lambda x: x.mode()[0] if len(x.mode()) > 0 else 'unknown').reset_index()
                    model_cost.columns = ['모델', '비용수준']
                    model_token_stats = model_token_stats.merge(model_cost, on='모델')
                
                # 토큰 효율성 계산 (정답당 토큰)
                if '총_토큰' in model_token_stats.columns:
                    model_token_stats['정답당_토큰'] = model_token_stats.apply(
                        lambda row: row['총_토큰'] / (row['문제수'] * row['정확도'] / 100) if row['정확도'] > 0 else 0,
                        axis=1
                    )
                
                # 주요 메트릭 표시
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if '총_토큰' in model_token_stats.columns:
                        total_tokens = model_token_stats['총_토큰'].sum()
                        st.metric(
                            t['total_tokens'],
                            f"{total_tokens:,.0f}"
                        )
                
                with col2:
                    if '평균_토큰' in model_token_stats.columns:
                        avg_tokens = model_token_stats['평균_토큰'].mean()
                        st.metric(
                            t['avg_tokens_per_problem'],
                            f"{avg_tokens:,.0f}"
                        )
                
                with col3:
                    if '총_입력토큰' in model_token_stats.columns and '총_출력토큰' in model_token_stats.columns:
                        total_input = model_token_stats['총_입력토큰'].sum()
                        total_output = model_token_stats['총_출력토큰'].sum()
                        io_ratio = total_input / total_output if total_output > 0 else 0
                        st.metric(
                            t['io_ratio'],
                            f"{io_ratio:.2f}:1"
                        )
                
                with col4:
                    if '정답당_토큰' in model_token_stats.columns and len(model_token_stats[model_token_stats['정답당_토큰'] > 0]) > 0:
                        # 가장 효율적인 모델 (정답당 토큰이 적은 모델)
                        valid_stats = model_token_stats[model_token_stats['정답당_토큰'] > 0]
                        most_efficient = valid_stats.loc[valid_stats['정답당_토큰'].idxmin()]
                        st.metric(
                            t['most_efficient'],
                            most_efficient['모델'],
                            f"{most_efficient['정답당_토큰']:,.0f} " + t['tokens']
                        )
                
                # 상세 테이블
                st.markdown("---")
                st.subheader("📋 " + ("모델별 토큰 사용량 상세" if lang == 'ko' else "Detailed Token Usage by Model"))
                
                # 컬럼 순서 정리
                display_cols = ['모델']
                if '총_입력토큰' in model_token_stats.columns:
                    display_cols.append('총_입력토큰')
                if '총_출력토큰' in model_token_stats.columns:
                    display_cols.append('총_출력토큰')
                if '총_토큰' in model_token_stats.columns:
                    display_cols.append('총_토큰')
                if '평균_토큰' in model_token_stats.columns:
                    display_cols.append('평균_토큰')
                display_cols.extend(['정확도', '문제수'])
                if '비용수준' in model_token_stats.columns:
                    display_cols.append('비용수준')
                if '정답당_토큰' in model_token_stats.columns:
                    display_cols.append('정답당_토큰')
                
                display_df = model_token_stats[display_cols].sort_values('총_토큰' if '총_토큰' in display_cols else '모델', ascending=False)
                
                # 포맷팅
                format_dict = {
                    '총_입력토큰': '{:,.0f}',
                    '총_출력토큰': '{:,.0f}',
                    '총_토큰': '{:,.0f}',
                    '평균_토큰': '{:,.0f}',
                    '정확도': '{:.2f}%',
                    '정답당_토큰': '{:,.0f}'
                }
                
                st.dataframe(
                    display_df.style.format(format_dict).background_gradient(
                        subset=['정답당_토큰'] if '정답당_토큰' in display_cols else [],
                        cmap='RdYlGn_r'
                    ),
                    use_container_width=True
                )
                
                st.markdown("---")
                
                # 2. 시각화
                st.subheader("📊 " + ("토큰 사용량 시각화" if lang == 'ko' else "Token Usage Visualization"))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # 모델별 총 토큰 사용량
                    if '총_토큰' in model_token_stats.columns:
                        fig = px.bar(
                            display_df,
                            x='모델',
                            y='총_토큰',
                            title=t['total_tokens'] + ' (' + ('모델별' if lang == 'ko' else 'by Model') + ')',
                            text='총_토큰',
                            color='총_토큰',
                            color_continuous_scale='Blues'
                        )
                        fig.update_traces(
                            texttemplate='%{text:,.0f}',
                            textposition='outside',
                            marker_line_color='black',
                            marker_line_width=1.5
                        )
                        fig.update_layout(
                            height=400,
                            showlegend=False,
                            yaxis_title=t['total_tokens'],
                            xaxis_title=t['model']
                        )
                        fig.update_xaxes(tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # 입출력 토큰 비교
                    if '총_입력토큰' in model_token_stats.columns and '총_출력토큰' in model_token_stats.columns:
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            name=t['input_tokens'],
                            x=display_df['모델'],
                            y=display_df['총_입력토큰'],
                            marker_color='lightblue',
                            marker_line_color='black',
                            marker_line_width=1.5
                        ))
                        fig.add_trace(go.Bar(
                            name=t['output_tokens'],
                            x=display_df['모델'],
                            y=display_df['총_출력토큰'],
                            marker_color='lightcoral',
                            marker_line_color='black',
                            marker_line_width=1.5
                        ))
                        
                        fig.update_layout(
                            barmode='stack',
                            title=f"{t['input_tokens']} vs {t['output_tokens']}",
                            height=400,
                            yaxis_title=t['tokens'],
                            xaxis_title=t['model']
                        )
                        fig.update_xaxes(tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # 3. 토큰 효율성 분석
                if '정답당_토큰' in model_token_stats.columns:
                    st.subheader("🎯 " + (t['token_efficiency']))
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 정답당 토큰 사용량
                        fig = px.bar(
                            display_df.sort_values('정답당_토큰'),
                            x='모델',
                            y='정답당_토큰',
                            title=t['token_per_correct'],
                            text='정답당_토큰',
                            color='정답당_토큰',
                            color_continuous_scale='RdYlGn_r'
                        )
                        fig.update_traces(
                            texttemplate='%{text:,.0f}',
                            textposition='outside',
                            marker_line_color='black',
                            marker_line_width=1.5
                        )
                        fig.update_layout(
                            height=400,
                            showlegend=False,
                            yaxis_title=t['tokens'] + ' / ' + t['correct'],
                            xaxis_title=t['model']
                        )
                        fig.update_xaxes(tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # 토큰 vs 정확도 산점도
                        if '평균_토큰' in model_token_stats.columns:
                            fig = px.scatter(
                                display_df,
                                x='평균_토큰',
                                y='정확도',
                                size='문제수',
                                text='모델',
                                title=t['token_efficiency'] + ' vs ' + t['accuracy'],
                                labels={
                                    '평균_토큰': t['avg_tokens_per_problem'],
                                    '정확도': t['accuracy'] + ' (%)'
                                }
                            )
                            fig.update_traces(
                                textposition='top center',
                                marker=dict(
                                    line=dict(width=2, color='black'),
                                    opacity=0.7
                                )
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # 4. 비용 분석 (비용 수준 데이터가 있는 경우)
                if 'cost' in available_cols:
                    st.subheader("💵 " + t['cost_analysis'])
                    
                    cost_col = available_cols['cost']
                    
                    # 비용 수준을 정규화 및 순서 정의
                    def normalize_cost_level(level):
                        if pd.isna(level):
                            return 'unknown'
                        level_str = str(level).lower().strip()
                        # 무료/로컬 모델
                        if level_str in ['무료', 'free', 'f', '0', 'local', 'localhost', '로컬']:
                            return t['free']
                        # 매우 낮음
                        elif level_str in ['매우낮음', 'very low', 'very_low', 'vl', 'verylow']:
                            return t['very_low']
                        # 낮음
                        elif level_str in ['낮음', 'low', 'l']:
                            return t['low']
                        # 중간
                        elif level_str in ['중간', 'medium', 'mid', 'm']:
                            return t['medium_cost']
                        # 높음
                        elif level_str in ['높음', 'high', 'h']:
                            return t['high']
                        return level
                    
                    # 비용 순서 정의 (무료 → 매우낮음 → 낮음 → 중간 → 높음)
                    cost_order = [t['free'], t['very_low'], t['low'], t['medium_cost'], t['high']]
                    
                    token_df['비용수준_정규화'] = token_df[cost_col].apply(normalize_cost_level)
                    model_token_stats['비용수준_정규화'] = model_token_stats['비용수준'].apply(normalize_cost_level) if '비용수준' in model_token_stats.columns else t['medium_cost']
                    
                    # 🆕 실제 비용 계산 기능 추가
                    st.markdown("---")
                    st.subheader("💰 " + t['actual_cost'] + " " + ('계산기' if lang == 'ko' else 'Calculator'))
                    
                    # 모델별 API 가격 정의 (2024-2025 기준, USD per 1M tokens)
                    MODEL_PRICING = {
                        # OpenAI
                        'GPT-4o': {'input': 2.50, 'output': 10.00},
                        'GPT-4o-Mini': {'input': 0.150, 'output': 0.600},
                        'GPT-4-Turbo': {'input': 10.00, 'output': 30.00},
                        'GPT-3.5-Turbo': {'input': 0.50, 'output': 1.50},
                        # Anthropic
                        'Claude-3.5-Sonnet': {'input': 3.00, 'output': 15.00},
                        'Claude-Sonnet-4': {'input': 3.00, 'output': 15.00},
                        'Claude-3.5-Haiku': {'input': 0.80, 'output': 4.00},
                        'Claude-3-Opus': {'input': 15.00, 'output': 75.00},
                        'Claude-3-Sonnet': {'input': 3.00, 'output': 15.00},
                        'Claude-3-Haiku': {'input': 0.25, 'output': 1.25},
                        # Google
                        'Gemini-1.5-Pro': {'input': 1.25, 'output': 5.00},
                        'Gemini-1.5-Flash': {'input': 0.075, 'output': 0.30},
                        # LG AI Research
                        'EXAONE-3.5': {'input': 0.00, 'output': 0.00},  # 로컬/무료
                    }
                    
                    # 가격 정보 표시
                    with st.expander("📋 " + ("모델별 API 가격 정보 (2024-2025)" if lang == 'ko' else "API Pricing by Model (2024-2025)")):
                        pricing_data = []
                        for model, prices in MODEL_PRICING.items():
                            pricing_data.append({
                                '모델' if lang == 'ko' else 'Model': model,
                                '입력 ($/1M)' if lang == 'ko' else 'Input ($/1M)': f"${prices['input']:.3f}",
                                '출력 ($/1M)' if lang == 'ko' else 'Output ($/1M)': f"${prices['output']:.3f}"
                            })
                        st.dataframe(pd.DataFrame(pricing_data), use_container_width=True)
                        st.caption("💡 " + ("가격은 변동될 수 있습니다. 최신 가격은 각 제공업체 웹사이트를 확인하세요." if lang == 'ko' else "Prices may vary. Check provider websites for latest pricing."))
                    
                    # 실제 비용 계산
                    if '총_입력토큰' in model_token_stats.columns and '총_출력토큰' in model_token_stats.columns:
                        st.markdown("---")
                        
                        cost_calculations = []
                        for _, row in model_token_stats.iterrows():
                            model = row['모델']
                            input_tokens = row['총_입력토큰']
                            output_tokens = row['총_출력토큰']
                            
                            # 모델명 매칭 (부분 매칭)
                            matched_pricing = None
                            for price_model, pricing in MODEL_PRICING.items():
                                if price_model.replace('-', '').replace('.', '').lower() in model.replace('-', '').replace('.', '').lower():
                                    matched_pricing = pricing
                                    break
                            
                            if matched_pricing:
                                # 비용 계산 (USD)
                                input_cost = (input_tokens / 1_000_000) * matched_pricing['input']
                                output_cost = (output_tokens / 1_000_000) * matched_pricing['output']
                                total_cost = input_cost + output_cost
                                
                                # 문제당 비용
                                cost_per_problem = total_cost / row['문제수'] if row['문제수'] > 0 else 0
                                
                                # 정답당 비용 (효율성 지표)
                                correct_answers = row['문제수'] * row['정확도'] / 100
                                cost_per_correct = total_cost / correct_answers if correct_answers > 0 else 0
                                
                                cost_calculations.append({
                                    '모델' if lang == 'ko' else 'Model': model,
                                    '총비용 ($)' if lang == 'ko' else 'Total Cost ($)': total_cost,
                                    '문제당 ($)' if lang == 'ko' else 'Per Problem ($)': cost_per_problem,
                                    '정답당 ($)' if lang == 'ko' else 'Per Correct ($)': cost_per_correct,
                                    '정확도 (%)' if lang == 'ko' else 'Accuracy (%)': row['정확도'],
                                    '입력비용 ($)' if lang == 'ko' else 'Input Cost ($)': input_cost,
                                    '출력비용 ($)' if lang == 'ko' else 'Output Cost ($)': output_cost
                                })
                        
                        if cost_calculations:
                            cost_df = pd.DataFrame(cost_calculations)
                            
                            # 비용 효율성으로 정렬 (정답당 비용 기준)
                            cost_df = cost_df.sort_values('정답당 ($)' if lang == 'ko' else 'Per Correct ($)')
                            
                            st.subheader("💵 " + t['actual_cost'] + " " + ('분석' if lang == 'ko' else 'Analysis'))
                            
                            # 주요 메트릭
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                total_cost_all = cost_df['총비용 ($)' if lang == 'ko' else 'Total Cost ($)'].sum()
                                st.metric(
                                    t['total_estimated_cost'],
                                    f"${total_cost_all:.4f}"
                                )
                            
                            with col2:
                                avg_cost_per_problem = cost_df['문제당 ($)' if lang == 'ko' else 'Per Problem ($)'].mean()
                                st.metric(
                                    t['cost_per_problem'],
                                    f"${avg_cost_per_problem:.6f}"
                                )
                            
                            with col3:
                                # 가장 비용 효율적인 모델
                                most_efficient = cost_df.iloc[0]
                                st.metric(
                                    '최고 효율' if lang == 'ko' else 'Most Efficient',
                                    most_efficient['모델' if lang == 'ko' else 'Model'],
                                    f"${most_efficient['정답당 ($)' if lang == 'ko' else 'Per Correct ($)']:.6f}"
                                )
                            
                            with col4:
                                # 가장 비용 비효율적인 모델
                                least_efficient = cost_df.iloc[-1]
                                st.metric(
                                    '최저 효율' if lang == 'ko' else 'Least Efficient',
                                    least_efficient['모델' if lang == 'ko' else 'Model'],
                                    f"${least_efficient['정답당 ($)' if lang == 'ko' else 'Per Correct ($)']:.6f}"
                                )
                            
                            # 상세 테이블
                            st.markdown("---")
                            st.dataframe(
                                cost_df.style.format({
                                    '총비용 ($)' if lang == 'ko' else 'Total Cost ($)': '${:.6f}',
                                    '문제당 ($)' if lang == 'ko' else 'Per Problem ($)': '${:.8f}',
                                    '정답당 ($)' if lang == 'ko' else 'Per Correct ($)': '${:.8f}',
                                    '정확도 (%)' if lang == 'ko' else 'Accuracy (%)': '{:.2f}%',
                                    '입력비용 ($)' if lang == 'ko' else 'Input Cost ($)': '${:.6f}',
                                    '출력비용 ($)' if lang == 'ko' else 'Output Cost ($)': '${:.6f}'
                                }).background_gradient(
                                    subset=['정답당 ($)' if lang == 'ko' else 'Per Correct ($)'],
                                    cmap='RdYlGn_r'
                                ),
                                use_container_width=True
                            )
                            
                            st.markdown("---")
                            
                            # 비용 시각화
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # 총 비용 비교
                                fig = px.bar(
                                    cost_df,
                                    x='모델' if lang == 'ko' else 'Model',
                                    y='총비용 ($)' if lang == 'ko' else 'Total Cost ($)',
                                    title=t['total_estimated_cost'],
                                    text='총비용 ($)' if lang == 'ko' else 'Total Cost ($)',
                                    color='총비용 ($)' if lang == 'ko' else 'Total Cost ($)',
                                    color_continuous_scale='Reds'
                                )
                                fig.update_traces(
                                    texttemplate='$%{text:.6f}',
                                    textposition='outside',
                                    marker_line_color='black',
                                    marker_line_width=1.5
                                )
                                fig.update_layout(
                                    height=400,
                                    showlegend=False,
                                    yaxis_title=t['cost'] + ' (USD)',
                                    xaxis_title=t['model']
                                )
                                fig.update_xaxes(tickangle=45)
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                # 정답당 비용 (효율성)
                                fig = px.bar(
                                    cost_df.sort_values('정답당 ($)' if lang == 'ko' else 'Per Correct ($)'),
                                    x='모델' if lang == 'ko' else 'Model',
                                    y='정답당 ($)' if lang == 'ko' else 'Per Correct ($)',
                                    title=t['cost_efficiency'] + ' (' + ('정답당 비용' if lang == 'ko' else 'Cost per Correct') + ')',
                                    text='정답당 ($)' if lang == 'ko' else 'Per Correct ($)',
                                    color='정답당 ($)' if lang == 'ko' else 'Per Correct ($)',
                                    color_continuous_scale='RdYlGn_r'
                                )
                                fig.update_traces(
                                    texttemplate='$%{text:.8f}',
                                    textposition='outside',
                                    marker_line_color='black',
                                    marker_line_width=1.5
                                )
                                fig.update_layout(
                                    height=400,
                                    showlegend=False,
                                    yaxis_title=t['cost'] + ' (USD)',
                                    xaxis_title=t['model']
                                )
                                fig.update_xaxes(tickangle=45)
                                st.plotly_chart(fig, use_container_width=True)
                            
                            st.markdown("---")
                            
                            # 비용 vs 정확도 산점도
                            fig = px.scatter(
                                cost_df,
                                x='총비용 ($)' if lang == 'ko' else 'Total Cost ($)',
                                y='정확도 (%)' if lang == 'ko' else 'Accuracy (%)',
                                text='모델' if lang == 'ko' else 'Model',
                                title=t['cost'] + ' vs ' + t['accuracy'],
                                color='정확도 (%)' if lang == 'ko' else 'Accuracy (%)',
                                color_continuous_scale='RdYlGn',
                                size='문제당 ($)' if lang == 'ko' else 'Per Problem ($)'
                            )
                            fig.update_traces(
                                textposition='top center',
                                marker=dict(
                                    line=dict(width=2, color='black'),
                                    opacity=0.7
                                )
                            )
                            fig.update_layout(
                                height=500,
                                yaxis=dict(range=[0, 100])
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # 인사이트
                            st.success(f"""
                            💡 **{t['cost_efficiency']} {'인사이트' if lang == 'ko' else 'Insights'}**:
                            - **{'최고 효율' if lang == 'ko' else 'Most Efficient'}**: {most_efficient['모델' if lang == 'ko' else 'Model']} (${most_efficient['정답당 ($)' if lang == 'ko' else 'Per Correct ($)']:.8f} / {'정답' if lang == 'ko' else 'correct'})
                            - **{'최저 효율' if lang == 'ko' else 'Least Efficient'}**: {least_efficient['모델' if lang == 'ko' else 'Model']} (${least_efficient['정답당 ($)' if lang == 'ko' else 'Per Correct ($)']:.8f} / {'정답' if lang == 'ko' else 'correct'})
                            - **{'효율 차이' if lang == 'ko' else 'Efficiency Gap'}**: {(least_efficient['정답당 ($)' if lang == 'ko' else 'Per Correct ($)'] / most_efficient['정답당 ($)' if lang == 'ko' else 'Per Correct ($)']):.1f}x
                            """)
                        else:
                            st.info("💡 " + ("현재 데이터의 모델들에 대한 가격 정보가 없습니다. 모델명을 확인하거나 가격 정보를 추가하세요." if lang == 'ko' else "No pricing information available for current models. Please check model names or add pricing info."))
                    
                    st.markdown("---")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 비용 수준별 모델 분포
                        cost_dist = token_df.groupby('비용수준_정규화')['모델'].nunique().reset_index()
                        cost_dist.columns = ['비용수준', '모델수']
                        
                        fig = px.pie(
                            cost_dist,
                            values='모델수',
                            names='비용수준',
                            title=t['cost_level'] + ' ' + ('분포' if lang == 'ko' else 'Distribution'),
                            hole=0.3,
                            category_orders={'비용수준': cost_order}
                        )
                        fig.update_traces(
                            textposition='inside',
                            textinfo='percent+label',
                            marker=dict(line=dict(color='black', width=2))
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # 비용 수준별 평균 정확도
                        cost_acc = token_df.groupby('비용수준_정규화')['정답여부'].mean().reset_index()
                        cost_acc.columns = ['비용수준', '정확도']
                        cost_acc['정확도'] = cost_acc['정확도'] * 100
                        
                        fig = px.bar(
                            cost_acc,
                            x='비용수준',
                            y='정확도',
                            title=t['cost_level'] + ' vs ' + t['accuracy'],
                            text='정확도',
                            color='정확도',
                            color_continuous_scale='RdYlGn',
                            category_orders={'비용수준': cost_order}
                        )
                        fig.update_traces(
                            texttemplate='%{text:.1f}%',
                            textposition='outside',
                            marker_line_color='black',
                            marker_line_width=1.5
                        )
                        fig.update_layout(
                            height=400,
                            showlegend=False,
                            yaxis_title=t['accuracy'] + ' (%)',
                            yaxis=dict(range=[0, 100]),
                            xaxis=dict(
                                categoryorder='array',
                                categoryarray=cost_order
                            )
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                    
                    # 비용 효율성 매트릭스
                    st.subheader("📊 " + t['cost_efficiency'] + (' 매트릭스' if lang == 'ko' else ' Matrix'))
                    
                    # 비용 수준과 정확도로 모델 분류
                    if '비용수준_정규화' in model_token_stats.columns:
                        # 데이터 준비 (Categorical 변환 제거)
                        plot_data = model_token_stats.copy()
                        
                        fig = px.scatter(
                            plot_data,
                            x='비용수준_정규화',
                            y='정확도',
                            size='총_토큰' if '총_토큰' in plot_data.columns else '문제수',
                            text='모델',
                            title=t['cost_level'] + ' vs ' + t['accuracy'],
                            color='정확도',
                            color_continuous_scale='RdYlGn',
                            category_orders={'비용수준_정규화': cost_order}
                        )
                        fig.update_traces(
                            textposition='top center',
                            marker=dict(
                                line=dict(width=2, color='black'),
                                opacity=0.7
                            )
                        )
                        fig.update_layout(
                            height=500,
                            yaxis=dict(range=[0, 100]),
                            xaxis=dict(
                                title=t['cost_level'],
                                categoryorder='array',
                                categoryarray=cost_order
                            ),
                            yaxis_title=t['accuracy'] + ' (%)'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # 인사이트
                        st.info(f"""
                        💡 **{t['cost_efficiency']} {'인사이트' if lang == 'ko' else 'Insights'}**:
                        - **{'고효율 영역' if lang == 'ko' else 'High Efficiency Zone'}** ({'낮은 비용 + 높은 정확도' if lang == 'ko' else 'Low cost + High accuracy'}): {'좌측 상단' if lang == 'ko' else 'Top left'}
                        - **{'고비용 영역' if lang == 'ko' else 'High Cost Zone'}** ({'높은 비용' if lang == 'ko' else 'High cost'}): {'우측' if lang == 'ko' else 'Right side'}
                        - {'모델 선택 시 비용 대비 성능을 고려하세요' if lang == 'ko' else 'Consider cost-performance ratio when selecting models'}
                        """)
                
                st.markdown("---")
                
                # 5. 테스트별 토큰 분석 (테스트가 여러 개인 경우)
                if '테스트명' in token_df.columns and token_df['테스트명'].nunique() > 1:
                    st.subheader("📚 " + ("테스트별 토큰 사용량" if lang == 'ko' else "Token Usage by Test"))
                    
                    token_col = available_cols.get('total', available_cols.get('input', list(available_cols.values())[0]))
                    test_token = token_df.groupby(['모델', '테스트명'])[token_col].sum().reset_index()
                    test_token.columns = ['모델', '테스트명', '총토큰']
                    
                    fig = px.bar(
                        test_token,
                        x='테스트명',
                        y='총토큰',
                        color='모델',
                        barmode='group',
                        title='테스트별 모델 토큰 사용량' if lang == 'ko' else 'Token Usage by Test and Model',
                        labels={'총토큰': t['total_tokens']}
                    )
                    fig.update_layout(
                        height=400,
                        xaxis_title=t['testname'],
                        yaxis_title=t['total_tokens']
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                # 6. 문제 유형별 토큰 분석 (이미지 문제가 있는 경우)
                if 'image' in token_df.columns:
                    st.subheader("🖼️ " + ("문제 유형별 토큰 사용량" if lang == 'ko' else "Token Usage by Problem Type"))
                    
                    # 이미지 문제 여부 구분
                    token_df['문제유형'] = token_df['image'].apply(
                        lambda x: t['text_only'] if str(x).lower() == 'text_only' or str(x) == 'X' else t['image_problem']
                    )
                    
                    token_col = available_cols.get('total', available_cols.get('input', list(available_cols.values())[0]))
                    problem_type_token = token_df.groupby(['모델', '문제유형']).agg({
                        token_col: 'mean',
                        '정답여부': 'mean'
                    }).reset_index()
                    problem_type_token.columns = ['모델', '문제유형', '평균토큰', '정확도']
                    problem_type_token['정확도'] = problem_type_token['정확도'] * 100
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 문제 유형별 평균 토큰
                        fig = px.bar(
                            problem_type_token,
                            x='모델',
                            y='평균토큰',
                            color='문제유형',
                            barmode='group',
                            title=t['avg_tokens_per_problem'] + ' (' + t['problem_type'] + '별)',
                            labels={'평균토큰': t['avg_tokens_per_problem']}
                        )
                        fig.update_layout(
                            height=400,
                            xaxis_title=t['model']
                        )
                        fig.update_xaxes(tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # 문제 유형별 정확도 비교
                        fig = px.bar(
                            problem_type_token,
                            x='모델',
                            y='정확도',
                            color='문제유형',
                            barmode='group',
                            title=t['accuracy'] + ' (' + t['problem_type'] + '별)',
                            labels={'정확도': t['accuracy'] + ' (%)'}
                        )
                        fig.update_layout(
                            height=400,
                            xaxis_title=t['model'],
                            yaxis=dict(range=[0, 100])
                        )
                        fig.update_xaxes(tickangle=45)
                        st.plotly_chart(fig, use_container_width=True)
    
    # 탭 10: 테스트셋 통계
    with tabs[9]:
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
    - ✨ **{t['token_cost_analysis']}**: 토큰 사용량 및 비용 효율성 분석
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