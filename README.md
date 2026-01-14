# LLM Benchmark Visualizer (HTML/JS Version)

기존 Streamlit 기반 앱을 순수 HTML/JavaScript로 변환한 버전입니다.

## 🚀 특징

- **빠른 로딩**: 서버 사이드 렌더링 없이 클라이언트에서 직접 렌더링
- **Vercel 배포**: 정적 호스팅으로 빠른 글로벌 배포
- **반응형 디자인**: 모바일/데스크톱 모두 지원
- **다국어 지원**: 한국어/영어

## 📁 프로젝트 구조

```
benchmark-html/
├── index.html          # 메인 HTML
├── js/
│   └── app.js          # 핵심 로직 (데이터 로딩, 필터링, 차트)
├── vercel.json         # Vercel 배포 설정
└── README.md
```

## 🔧 사용된 라이브러리

- **Tailwind CSS**: 스타일링
- **Plotly.js**: 차트 시각화
- **Papa Parse**: CSV 파싱
- **JSZip**: ZIP 파일 처리

## 🌐 Vercel 배포 방법

### 방법 1: Vercel CLI 사용

```bash
# Vercel CLI 설치
npm install -g vercel

# 배포
cd benchmark-html
vercel

# 프로덕션 배포
vercel --prod
```

### 방법 2: GitHub 연동

1. 이 폴더를 새 GitHub 저장소에 푸시
2. [Vercel](https://vercel.com)에서 "Import Project"
3. GitHub 저장소 선택
4. 설정 없이 바로 배포!

### 방법 3: Vercel Dashboard에서 직접 업로드

1. [Vercel Dashboard](https://vercel.com/dashboard) 접속
2. "Add New" → "Project"
3. "Upload" 선택
4. 이 폴더를 드래그 앤 드롭

## ⚙️ 데이터 소스

데이터는 GitHub Releases에서 자동으로 다운로드됩니다:
- 저장소: `big1248/benchmark_visualizer`
- 태그: `v2.2.0`
- 파일: `data.zip`

## 📊 주요 기능

1. **전체 요약**: 메트릭 카드, 모델/테스트별 정확도, 히트맵
2. **모델별 비교**: 성능 비교 차트 및 상세 통계
3. **응답시간 분석**: 모델별 응답시간, 분포, 정확도 상관관계
4. **법령/비법령 분석**: 문제 유형별 성능 비교
5. **과목별 분석**: 과목별 정답률
6. **연도별 분석**: 연도별 추이
7. **오답 분석**: 오답률 높은 문제, 모델 간 오답 일치도
8. **난이도 분석**: 난이도 구간별 분포 및 모델 성능
9. **토큰/비용 분석**: 비용 효율성

## 🔄 기존 Streamlit 버전과의 차이

| 항목 | Streamlit | HTML/JS |
|------|-----------|---------|
| 로딩 시간 | 느림 (서버 처리) | 빠름 (클라이언트 렌더링) |
| 호스팅 비용 | 높음 | 무료 (Vercel) |
| 확장성 | 제한적 | 높음 |
| 개발 복잡도 | 낮음 | 중간 |

## 🐛 문제 해결

### CORS 오류 발생 시

GitHub에서 직접 다운로드 시 CORS 오류가 발생할 수 있습니다.
앱이 자동으로 CORS 프록시를 시도합니다.

### 데이터 로딩 실패 시

1. GitHub Releases URL 확인
2. 브라우저 콘솔에서 오류 메시지 확인
3. 네트워크 연결 상태 확인

## 📝 라이선스

MIT License
