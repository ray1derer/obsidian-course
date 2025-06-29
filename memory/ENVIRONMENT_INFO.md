# 환경 정보 및 설정

## 🖥️ 작업 환경

### 현재 환경
- **OS**: Linux (Android/Termux)
- **Platform**: linux
- **OS Version**: Linux 6.1.99-android14-11-30958380-abS928NKSS4BYE9
- **Working Directory**: /data/data/com.termux/files/home/obsidian_course
- **Home Directory**: /data/data/com.termux/files/home
- **Date**: 2025-06-29

### Git 설정
```bash
# 현재 Git 사용자 설정
git config user.name "Obsidian Course"
git config user.email "obsidian-course@example.com"

# GitHub CLI 설치됨
gh --version

# 원격 저장소
git remote -v
# origin  https://github.com/ray1derer/obsidian-course.git
```

## 📁 중요 디렉토리 구조

### 프로젝트 관련
```
/data/data/com.termux/files/home/
├── obsidian_course/          # 현재 프로젝트
├── browser_automation_mcp/   # 노션 강좌 프로젝트
├── api-keys-collection.md    # 전체 API 키 모음
├── CLAUDE.md                 # 전체 프로젝트 메모리
├── .claude/CLAUDE.md         # 개인 글로벌 설정
├── MCP_서버_한국어_전체_카탈로그.md
├── MCP_서버_사용_가이드.md
├── MCP_컨텍스트_관리_가이드.md
└── MCP_통합_워크플로우_가이드.md
```

## 🔧 설치된 도구 및 패키지

### 시스템 도구
- **git**: 버전 관리
- **gh**: GitHub CLI (설치됨)
- **python3**: Python 3.x
- **pip**: Python 패키지 관리자

### MCP 서버 목록 (18개)
1. filesystem - 파일 시스템 관리
2. memory - 영구 메모리 저장소
3. git - Git 저장소 관리
4. github - GitHub API 통합
5. fetch - 웹 콘텐츠 가져오기
6. time - 시간 관련 작업
7. filesystem-android - Android 특화 파일시스템
8. everything - 메타 서버
9. sequential-thinking - 순차적 사고 ✅
10. whisper - 음성 인식
11. obsidian - Obsidian 노트 관리
12. kakao - 카카오톡 스크린샷 분석
13. brave-search - 웹 검색
14. youtube-transcript - YouTube 자막 추출
15. aws-ec2 - AWS EC2 인스턴스 관리
16. context7 - 문서 지식 관리
17. magicui - UI 컴포넌트 라이브러리
18. 21st-dev - AI UI 생성기

## 🌐 관련 프로젝트 정보

### 1. AWS 블로그 프로젝트
- **URL**: http://43.203.57.64 (artisan-code-lab)
- **상태**: 하드코딩된 정적 페이지
- **문제**: SSH 접속 불가

### 2. 노션 마스터 클래스
- **위치**: /home/browser_automation_mcp/
- **진행**: 30개 중 1개 완성
- **특징**: 스크린샷 자동화 시스템

### 3. MCP 한국어 카탈로그
- **규모**: 6,850개 서버 번역 완료
- **상태**: 완성

### 4. 옵시디언 마스터 클래스 (현재)
- **진행**: 35개 중 5개 완성
- **특징**: 최고 퀄리티, 실습 중심

## 🔐 보안 설정

### .gitignore 설정
```
# Sensitive files
memory/API_KEYS.md
.env
config.json
```

### 민감한 파일 위치
- API_KEYS.md는 gitignore에 포함
- 실수로 커밋되지 않도록 주의

## 💡 유용한 명령어

### Git 작업
```bash
# 상태 확인
git status

# 변경사항 추가 및 커밋
git add .
git commit -m "feat: 기능 추가"

# GitHub 푸시
git push origin main

# 다른 기기에서 가져오기
git pull origin main
```

### 프로젝트 관리
```bash
# 현재 위치 확인
pwd

# 프로젝트로 이동
cd /data/data/com.termux/files/home/obsidian_course

# 파일 목록 보기
ls -la

# 메모리 상태 확인
cat memory/PROJECT_STATUS.md
```

## 📊 리소스 사용량

### 디스크 사용량
```bash
# 프로젝트 크기 확인
du -sh .

# 각 레슨 파일 크기
ls -lh lessons/
```

### 파일 수
- HTML 파일: 6개 (index + 5 lessons)
- 메모리 파일: 5개
- 기타: CSS, Python, README 등

## 🔄 동기화 전략

1. **작업 시작**: `git pull`로 최신 상태 확인
2. **작업 중**: 주요 변경사항마다 커밋
3. **작업 종료**: memory 폴더 업데이트 후 푸시
4. **정기 백업**: 로컬 백업도 유지

---
*이 문서는 작업 환경 재구성 시 참조용입니다*