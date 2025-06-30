#!/usr/bin/env python3
"""
옵시디언 강좌 자동 생성 시스템
카테고리를 입력하면 자동으로 조사하고 강좌를 생성합니다.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import asyncio
from typing import Dict, List, Optional
import logging

class ObsidianCourseGenerator:
    def __init__(self):
        self.base_dir = Path("/data/data/com.termux/files/home/obsidian_course")
        self.lessons_dir = self.base_dir / "lessons"
        self.screenshots_dir = self.base_dir / "screenshots"
        self.templates_dir = self.base_dir / "templates"
        self.metadata_file = self.base_dir / "course_metadata.json"
        
        # 디렉토리 생성
        for dir_path in [self.lessons_dir, self.screenshots_dir, self.templates_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # 메타데이터 초기화
        self.metadata = self.load_metadata()
        
    def load_metadata(self) -> Dict:
        """메타데이터 로드"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "lessons": {},
            "categories": {},
            "last_updated": datetime.now().isoformat()
        }
    
    def save_metadata(self):
        """메타데이터 저장"""
        self.metadata["last_updated"] = datetime.now().isoformat()
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    async def research_topic(self, category: str, topic: str) -> Dict:
        """주제 조사 및 콘텐츠 수집"""
        self.logger.info(f"조사 시작: {category} - {topic}")
        
        # 여기서는 시뮬레이션으로 대체
        # 실제로는 웹 크롤링, API 호출 등을 통해 정보 수집
        research_data = {
            "category": category,
            "topic": topic,
            "key_concepts": [],
            "learning_objectives": [],
            "prerequisites": [],
            "content_sections": [],
            "practice_exercises": [],
            "resources": [],
            "screenshots_needed": []
        }
        
        # 카테고리별 특화된 조사
        if category == "basics":
            research_data.update(self._research_basics(topic))
        elif category == "intermediate":
            research_data.update(self._research_intermediate(topic))
        elif category == "advanced":
            research_data.update(self._research_advanced(topic))
        
        return research_data
    
    def _research_basics(self, topic: str) -> Dict:
        """초급 주제 조사"""
        return {
            "key_concepts": [
                "기본 개념 이해",
                "인터페이스 익히기",
                "첫 번째 노트 작성"
            ],
            "learning_objectives": [
                "옵시디언의 기본 기능 이해",
                "마크다운 문법 익히기",
                "노트 작성과 관리"
            ],
            "content_sections": [
                {"title": "소개", "content": ""},
                {"title": "기본 개념", "content": ""},
                {"title": "실습", "content": ""},
                {"title": "요약", "content": ""}
            ]
        }
    
    def _research_intermediate(self, topic: str) -> Dict:
        """중급 주제 조사"""
        return {
            "key_concepts": [
                "플러그인 활용",
                "고급 기능",
                "워크플로우 최적화"
            ],
            "learning_objectives": [
                "플러그인 설치와 설정",
                "고급 검색 기능 활용",
                "자동화 구현"
            ]
        }
    
    def _research_advanced(self, topic: str) -> Dict:
        """고급 주제 조사"""
        return {
            "key_concepts": [
                "API 활용",
                "커스텀 개발",
                "시스템 통합"
            ],
            "learning_objectives": [
                "플러그인 개발",
                "API 활용",
                "대규모 지식 관리"
            ]
        }
    
    def generate_lesson_html(self, lesson_data: Dict, lesson_number: int) -> str:
        """레슨 HTML 생성"""
        template = self.load_template()
        
        # HTML 콘텐츠 생성
        content_html = self._generate_content_html(lesson_data)
        navigation_html = self._generate_navigation(lesson_number)
        
        # 템플릿에 데이터 삽입
        html = template.format(
            title=lesson_data["topic"],
            lesson_number=lesson_number,
            category=lesson_data["category"],
            content=content_html,
            navigation=navigation_html,
            timestamp=datetime.now().strftime("%Y-%m-%d")
        )
        
        return html
    
    def load_template(self) -> str:
        """레슨 템플릿 로드"""
        template_path = self.templates_dir / "lesson_template.html"
        
        if not template_path.exists():
            # 기본 템플릿 생성
            template = self._create_default_template()
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template)
        else:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
        
        return template
    
    def _create_default_template(self) -> str:
        """기본 레슨 템플릿 생성"""
        return '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 옵시디언 마스터 클래스</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link rel="stylesheet" href="../assets/lesson-style.css">
</head>
<body>
    <div class="lesson-container">
        <header class="lesson-header">
            <h1>제{lesson_number}강: {title}</h1>
            <div class="lesson-meta">
                <span class="category">{category}</span>
                <span class="date">{timestamp}</span>
            </div>
        </header>
        
        <nav class="lesson-nav">
            {navigation}
        </nav>
        
        <main class="lesson-content">
            {content}
        </main>
        
        <footer class="lesson-footer">
            <p>&copy; 2025 옵시디언 마스터 클래스</p>
        </footer>
    </div>
    
    <script src="../assets/lesson-script.js"></script>
</body>
</html>'''
    
    def _generate_content_html(self, lesson_data: Dict) -> str:
        """레슨 콘텐츠 HTML 생성"""
        html_parts = []
        
        # 학습 목표
        if lesson_data.get("learning_objectives"):
            html_parts.append('<section class="learning-objectives">')
            html_parts.append('<h2>🎯 학습 목표</h2>')
            html_parts.append('<ul>')
            for obj in lesson_data["learning_objectives"]:
                html_parts.append(f'<li>{obj}</li>')
            html_parts.append('</ul>')
            html_parts.append('</section>')
        
        # 주요 개념
        if lesson_data.get("key_concepts"):
            html_parts.append('<section class="key-concepts">')
            html_parts.append('<h2>💡 주요 개념</h2>')
            html_parts.append('<div class="concepts-grid">')
            for concept in lesson_data["key_concepts"]:
                html_parts.append(f'<div class="concept-card">{concept}</div>')
            html_parts.append('</div>')
            html_parts.append('</section>')
        
        # 콘텐츠 섹션
        for section in lesson_data.get("content_sections", []):
            html_parts.append(f'<section class="content-section">')
            html_parts.append(f'<h2>{section["title"]}</h2>')
            html_parts.append(f'<div class="section-content">{section["content"]}</div>')
            
            # 스크린샷이 있다면 추가
            if section.get("screenshot"):
                html_parts.append(f'<div class="screenshot-container">')
                html_parts.append(f'<img src="../screenshots/{section["screenshot"]}" alt="{section["title"]}">')
                html_parts.append(f'</div>')
            
            html_parts.append('</section>')
        
        # 실습 예제
        if lesson_data.get("practice_exercises"):
            html_parts.append('<section class="practice">')
            html_parts.append('<h2>✍️ 실습하기</h2>')
            for exercise in lesson_data["practice_exercises"]:
                html_parts.append(f'<div class="exercise">')
                html_parts.append(f'<h3>{exercise["title"]}</h3>')
                html_parts.append(f'<p>{exercise["description"]}</p>')
                html_parts.append(f'</div>')
            html_parts.append('</section>')
        
        return '\n'.join(html_parts)
    
    def _generate_navigation(self, lesson_number: int) -> str:
        """네비게이션 HTML 생성"""
        nav_parts = []
        
        # 이전 강의 링크
        if lesson_number > 1:
            nav_parts.append(f'<a href="lesson{lesson_number-1:02d}.html" class="nav-prev">')
            nav_parts.append('<i class="fas fa-arrow-left"></i> 이전 강의</a>')
        
        # 목차로 돌아가기
        nav_parts.append('<a href="../index.html" class="nav-index">')
        nav_parts.append('<i class="fas fa-list"></i> 목차</a>')
        
        # 다음 강의 링크
        if lesson_number < 35:  # 총 35강 기준
            nav_parts.append(f'<a href="lesson{lesson_number+1:02d}.html" class="nav-next">')
            nav_parts.append('다음 강의 <i class="fas fa-arrow-right"></i></a>')
        
        return '\n'.join(nav_parts)
    
    async def generate_course(self, category: str, topics: List[str], start_number: int = 1):
        """전체 코스 생성"""
        self.logger.info(f"코스 생성 시작: {category} - {len(topics)}개 주제")
        
        for i, topic in enumerate(topics):
            lesson_number = start_number + i
            
            # 주제 조사
            lesson_data = await self.research_topic(category, topic)
            
            # HTML 생성
            html_content = self.generate_lesson_html(lesson_data, lesson_number)
            
            # 파일 저장
            file_path = self.lessons_dir / f"lesson{lesson_number:02d}.html"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 메타데이터 업데이트
            self.metadata["lessons"][f"lesson{lesson_number:02d}"] = {
                "title": topic,
                "category": category,
                "created": datetime.now().isoformat(),
                "file": str(file_path)
            }
            
            self.logger.info(f"생성 완료: 제{lesson_number}강 - {topic}")
        
        # 메타데이터 저장
        self.save_metadata()
        self.logger.info("전체 코스 생성 완료")
    
    def create_assets(self):
        """CSS 및 JavaScript 에셋 생성"""
        assets_dir = self.base_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        # CSS 파일 생성
        css_content = self._generate_lesson_css()
        with open(assets_dir / "lesson-style.css", 'w') as f:
            f.write(css_content)
        
        # JavaScript 파일 생성
        js_content = self._generate_lesson_js()
        with open(assets_dir / "lesson-script.js", 'w') as f:
            f.write(js_content)
    
    def _generate_lesson_css(self) -> str:
        """레슨 페이지 CSS 생성"""
        return '''/* 레슨 페이지 스타일 */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background-color: #1e1e1e;
    color: #e0e0e0;
    margin: 0;
    padding: 0;
}

.lesson-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.lesson-header {
    background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
    padding: 40px;
    border-radius: 12px;
    margin-bottom: 30px;
    color: white;
}

.lesson-header h1 {
    margin: 0 0 20px 0;
    font-size: 2.5rem;
}

.lesson-meta {
    display: flex;
    gap: 20px;
    font-size: 0.9rem;
    opacity: 0.9;
}

.lesson-nav {
    display: flex;
    justify-content: space-between;
    margin-bottom: 40px;
    padding: 20px;
    background-color: #2d2d2d;
    border-radius: 8px;
}

.lesson-nav a {
    color: #a78bfa;
    text-decoration: none;
    padding: 10px 20px;
    border-radius: 6px;
    transition: all 0.3s ease;
}

.lesson-nav a:hover {
    background-color: #7c3aed;
    color: white;
}

.lesson-content {
    background-color: #2d2d2d;
    padding: 40px;
    border-radius: 12px;
    margin-bottom: 30px;
}

.lesson-content h2 {
    color: #a78bfa;
    margin-top: 40px;
    margin-bottom: 20px;
    font-size: 1.8rem;
}

.lesson-content h2:first-child {
    margin-top: 0;
}

.learning-objectives ul {
    list-style: none;
    padding-left: 0;
}

.learning-objectives li {
    padding: 10px 0 10px 30px;
    position: relative;
}

.learning-objectives li:before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #7c3aed;
    font-weight: bold;
}

.concepts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.concept-card {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #3d3d3d;
    transition: all 0.3s ease;
}

.concept-card:hover {
    border-color: #7c3aed;
    transform: translateY(-2px);
}

.screenshot-container {
    margin: 30px 0;
    text-align: center;
}

.screenshot-container img {
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.exercise {
    background-color: #1e1e1e;
    padding: 25px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 4px solid #7c3aed;
}

.exercise h3 {
    color: #a78bfa;
    margin-top: 0;
}

@media (max-width: 768px) {
    .lesson-header h1 {
        font-size: 1.8rem;
    }
    
    .lesson-nav {
        flex-direction: column;
        gap: 10px;
    }
    
    .lesson-nav a {
        text-align: center;
    }
}'''
    
    def _generate_lesson_js(self) -> str:
        """레슨 페이지 JavaScript 생성"""
        return '''// 레슨 페이지 스크립트
document.addEventListener('DOMContentLoaded', function() {
    // 진행률 추적
    trackProgress();
    
    // 이미지 클릭 시 확대
    setupImageZoom();
    
    // 코드 블록 복사 기능
    setupCodeCopy();
});

function trackProgress() {
    const lessonNumber = document.querySelector('.lesson-header h1').textContent.match(/\\d+/)[0];
    const progress = localStorage.getItem('courseProgress') || '{}';
    const progressData = JSON.parse(progress);
    
    progressData[`lesson${lessonNumber}`] = {
        completed: true,
        timestamp: new Date().toISOString()
    };
    
    localStorage.setItem('courseProgress', JSON.stringify(progressData));
}

function setupImageZoom() {
    const images = document.querySelectorAll('.screenshot-container img');
    
    images.forEach(img => {
        img.addEventListener('click', function() {
            const modal = document.createElement('div');
            modal.className = 'image-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <img src="${this.src}" alt="${this.alt}">
                </div>
            `;
            
            document.body.appendChild(modal);
            
            modal.querySelector('.close').addEventListener('click', () => {
                modal.remove();
            });
            
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.remove();
                }
            });
        });
    });
}

function setupCodeCopy() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = '복사';
        
        button.addEventListener('click', () => {
            navigator.clipboard.writeText(block.textContent);
            button.textContent = '복사됨!';
            setTimeout(() => {
                button.textContent = '복사';
            }, 2000);
        });
        
        block.parentElement.style.position = 'relative';
        block.parentElement.appendChild(button);
    });
}'''


# 개별 레슨 생성 함수
async def generate_single_lesson(lesson_number: int, topic: str, category: str = "advanced"):
    generator = ObsidianCourseGenerator()
    
    # 주제 조사
    lesson_data = await generator.research_topic(category, topic)
    
    # HTML 생성
    html_content = generator.generate_lesson_html(lesson_data, lesson_number)
    
    # 파일 저장
    file_path = generator.lessons_dir / f"lesson{lesson_number:02d}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 메타데이터 업데이트
    generator.metadata["lessons"][f"lesson{lesson_number:02d}"] = {
        "title": topic,
        "category": category,
        "created": datetime.now().isoformat(),
        "file": str(file_path)
    }
    
    generator.save_metadata()
    generator.logger.info(f"생성 완료: 제{lesson_number}강 - {topic}")

# 메인 실행 함수
async def main():
    generator = ObsidianCourseGenerator()
    
    # 에셋 생성
    generator.create_assets()
    
    # 초급 과정 주제들
    basic_topics = [
        "옵시디언 첫걸음",
        "볼트(Vault)의 이해",
        "기본 노트 작성",
        "내부 링크의 마법",
        "태그와 속성",
        "일일 노트와 템플릿",
        "파일 임베드와 트랜스클루전",
        "검색과 필터링",
        "그래프 뷰 기초",
        "필수 커뮤니티 플러그인"
    ]
    
    # 코스 생성
    await generator.generate_course("basics", basic_topics, start_number=1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 레슨 번호가 제공된 경우 개별 레슨 생성
        lesson_num = int(sys.argv[1])
        
        # 레슨별 주제 정의
        lesson_topics = {
            32: "AI 콘텐츠 생성 능력",
            33: "Cursor의 혁신적 기능들",
            34: "Cursor Pro와 무료 버전 비교",
            35: "Cursor 마스터되기"
        }
        
        if lesson_num in lesson_topics:
            asyncio.run(generate_single_lesson(lesson_num, lesson_topics[lesson_num]))
        else:
            print(f"레슨 {lesson_num}에 대한 주제가 정의되지 않았습니다.")
    else:
        asyncio.run(main())