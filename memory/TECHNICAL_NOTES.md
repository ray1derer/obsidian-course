# 기술 메모 - 옵시디언 마스터 클래스

## 🏗️ 프로젝트 구조

```
obsidian_course/
├── index.html              # 메인 페이지 (사이드바 네비게이션)
├── course_generator.py     # 자동 생성 시스템
├── README.md              # 프로젝트 설명
├── .gitignore             # Git 설정
├── PROJECT_STATUS.md      # 로컬 상태 추적
├── assets/                # 정적 자원
│   ├── lesson-style.css   # 완성됨 ✅
│   └── lesson-script.js   # 생성 필요 ❌
├── lessons/               # 강좌 HTML 파일
│   ├── lesson01.html      # ✅ 완성 (2,500줄)
│   ├── lesson02.html      # ✅ 완성 (2,800줄)
│   ├── lesson03.html      # ✅ 완성 (3,000줄)
│   ├── lesson04.html      # ✅ 완성 (2,700줄)
│   ├── lesson05.html      # ✅ 완성 (2,600줄)
│   └── lesson06-35.html   # ❌ 미완성
├── screenshots/           # 스크린샷 (현재 비어있음)
├── templates/             # HTML 템플릿
└── memory/               # 작업 메모리 ✨ NEW
    ├── README.md
    ├── PROJECT_STATUS.md
    ├── TODO_LIST.md
    └── TECHNICAL_NOTES.md
```

## 💻 코드 패턴

### HTML 구조 패턴
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <title>제X강: 제목 | 옵시디언 마스터 클래스</title>
    <link rel="stylesheet" href="../assets/lesson-style.css">
</head>
<body>
    <div class="lesson-container">
        <header class="lesson-header">...</header>
        <nav class="lesson-nav">...</nav>
        <main class="lesson-content">
            <section class="learning-objectives">...</section>
            <!-- 콘텐츠 섹션들 -->
            <section class="practice">...</section>
        </main>
        <footer class="lesson-footer">...</footer>
    </div>
    <script src="../assets/lesson-script.js"></script>
</body>
</html>
```

### 모의 UI 패턴
```html
<div class="obsidian-mock-ui">
    <div class="mock-titlebar">
        <div class="window-controls">
            <span class="window-control close"></span>
            <span class="window-control minimize"></span>
            <span class="window-control maximize"></span>
        </div>
        <span>제목</span>
    </div>
    <div class="mock-content">
        <!-- 내용 -->
    </div>
</div>
```

### 코드 블록 패턴
```html
<div class="code-header">
    <span class="code-language">언어</span>
    <button class="copy-button">복사</button>
</div>
<pre><code>코드 내용</code></pre>
```

## 🔧 필요한 JavaScript 기능

```javascript
// 1. 코드 복사 기능
document.querySelectorAll('.copy-button').forEach(button => {
    button.addEventListener('click', () => {
        // 복사 로직
    });
});

// 2. 체크리스트 상호작용
document.querySelectorAll('.checklist input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        // 체크 로직
    });
});

// 3. 진행률 표시
window.addEventListener('scroll', () => {
    // 스크롤 진행률 계산
});

// 4. 부드러운 스크롤
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        // 스크롤 애니메이션
    });
});
```

## 🎨 CSS 주요 클래스

- `.lesson-container` - 메인 컨테이너
- `.lesson-header` - 강의 헤더 (그라데이션)
- `.lesson-nav` - 네비게이션 바
- `.lesson-content` - 메인 콘텐츠 영역
- `.learning-objectives` - 학습 목표 섹션
- `.concept-card` - 개념 카드
- `.tip`, `.note`, `.warning`, `.important` - 알림 박스
- `.obsidian-mock-ui` - 모의 UI 컨테이너
- `.code-header` - 코드 블록 헤더
- `.practice` - 실습 섹션

## 🚀 Git 명령어

```bash
# 상태 확인
git status

# 모든 변경사항 추가
git add .

# 커밋
git commit -m "feat: lesson XX 추가"

# 푸시
git push origin main

# 다른 기기에서 작업 시작
git pull origin main
```

## 📌 주의사항

1. **파일 크기**: 각 레슨 HTML이 매우 크므로 (100KB+) 커밋 시 주의
2. **인코딩**: UTF-8 유지 필수
3. **경로**: 상대 경로 사용 (GitHub Pages 호환)
4. **이미지**: 현재 스크린샷 없이 placeholder 사용 중
5. **반응형**: 768px 기준으로 모바일/데스크톱 구분

## 🔍 디버깅 팁

- 브라우저 개발자 도구에서 콘솔 에러 확인
- CSS 클래스명 오타 주의
- JavaScript 파일 경로 확인
- 한글 깨짐 시 인코딩 확인

---
*기술적 이슈 발생 시 이 문서 참조*