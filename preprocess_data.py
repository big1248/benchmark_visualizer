#!/usr/bin/env python3
"""
데이터 전처리 스크립트
CSV 파일들을 하나의 JSON 파일로 변환하여 로딩 속도 개선

사용법:
1. data 폴더에 CSV 파일들이 있는 상태에서 실행
2. python preprocess_data.py
3. 생성된 data.json을 프로젝트에 포함

또는 GitHub에서 다운로드 후 변환:
   python preprocess_data.py --download
"""

import json
import os
import sys
import glob
import re
from pathlib import Path

def parse_filename(filename):
    """파일명에서 모델, 상세도, 프롬프팅, 테스트명 추출"""
    name = Path(filename).stem
    parts = name.split('_')
    
    return {
        'model': parts[0] if len(parts) > 0 else 'Unknown',
        'detail': parts[1] if len(parts) > 1 else 'unknown',
        'prompting': parts[2] if len(parts) > 2 else 'unknown',
        'testname': '_'.join(parts[3:]) if len(parts) > 3 else 'Unknown'
    }

def process_csv_files(data_dir='./data', output_file='./data.json'):
    """CSV 파일들을 JSON으로 변환"""
    import csv
    
    all_data = []
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    
    print(f"📂 {len(csv_files)}개 CSV 파일 발견")
    
    for i, filepath in enumerate(csv_files):
        filename = os.path.basename(filepath)
        file_info = parse_filename(filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # 필요한 필드만 추출 (용량 최적화)
                    processed = {
                        'id': row.get('ID', ''),
                        'model': row.get('모델명', file_info['model']),
                        'test': row.get('Test Name', file_info['testname']),
                        'year': row.get('Year', ''),
                        'session': row.get('Session', ''),
                        'subject': row.get('Subject', ''),
                        'question': row.get('Question', ''),
                        'correct': row.get('정답여부', '') in ['True', 'true', '1', True],
                        'law': row.get('law', ''),
                        'image': row.get('image', ''),
                        'time': float(row.get('문제당평균시간(초)', 0) or 0),
                        'inputTokens': int(row.get('입력토큰', 0) or 0),
                        'outputTokens': int(row.get('출력토큰', 0) or 0),
                        'cost': float(row.get('비용($)', 0) or 0),
                        'detail': file_info['detail'],
                        'prompting': file_info['prompting']
                    }
                    
                    all_data.append(processed)
        
        except Exception as e:
            print(f"⚠️ 오류 ({filename}): {e}")
        
        # 진행률 표시
        if (i + 1) % 50 == 0:
            print(f"   처리 중... {i + 1}/{len(csv_files)}")
    
    print(f"✅ 총 {len(all_data):,}개 레코드 처리 완료")
    
    # JSON 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False)
    
    # 파일 크기 확인
    file_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"📁 {output_file} 저장 완료 ({file_size:.1f} MB)")
    
    # 압축 버전도 생성
    import gzip
    compressed_file = output_file + '.gz'
    with open(output_file, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            f_out.writelines(f_in)
    
    compressed_size = os.path.getsize(compressed_file) / (1024 * 1024)
    print(f"📦 {compressed_file} 저장 완료 ({compressed_size:.1f} MB)")
    
    return all_data

def download_and_process():
    """GitHub에서 데이터 다운로드 후 처리"""
    import requests
    import zipfile
    import shutil
    
    repo = "big1248/benchmark_visualizer"
    tag = "v2.2.0"
    url = f"https://github.com/{repo}/releases/download/{tag}/data.zip"
    
    print(f"📥 다운로드 중: {url}")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # ZIP 파일 저장
    with open('data.zip', 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    print("📂 압축 해제 중...")
    with zipfile.ZipFile('data.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    
    os.remove('data.zip')
    
    # 처리
    process_csv_files()
    
    # data 폴더 정리 (선택적)
    # shutil.rmtree('./data')

def create_summary_json(all_data, output_file='./summary.json'):
    """요약 통계 JSON 생성 (빠른 초기 로딩용)"""
    
    # 모델별 통계
    model_stats = {}
    test_stats = {}
    
    for row in all_data:
        model = row['model']
        test = row['test']
        
        # 모델별
        if model not in model_stats:
            model_stats[model] = {'total': 0, 'correct': 0}
        model_stats[model]['total'] += 1
        if row['correct']:
            model_stats[model]['correct'] += 1
        
        # 테스트별
        if test not in test_stats:
            test_stats[test] = {'total': 0, 'correct': 0}
        test_stats[test]['total'] += 1
        if row['correct']:
            test_stats[test]['correct'] += 1
    
    summary = {
        'totalRecords': len(all_data),
        'models': {k: {**v, 'accuracy': v['correct'] / v['total'] * 100} for k, v in model_stats.items()},
        'tests': {k: {**v, 'accuracy': v['correct'] / v['total'] * 100} for k, v in test_stats.items()}
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"📊 {output_file} 저장 완료")
    
    return summary

if __name__ == '__main__':
    if '--download' in sys.argv:
        download_and_process()
    else:
        if os.path.exists('./data'):
            data = process_csv_files()
            create_summary_json(data)
        else:
            print("❌ data 폴더가 없습니다.")
            print("   --download 옵션으로 GitHub에서 다운로드하거나")
            print("   data 폴더에 CSV 파일을 넣어주세요.")
