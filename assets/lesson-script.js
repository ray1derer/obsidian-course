/**
 * 옵시디언 마스터 클래스 - 레슨 인터랙티브 스크립트
 * 모든 레슨 페이지에서 공통으로 사용되는 JavaScript 기능
 */

// DOM이 로드되면 실행
document.addEventListener('DOMContentLoaded', function() {
    initializeCopyButtons();
    initializeChecklists();
    initializeProgressBar();
    initializeSmoothScrolling();
    initializeCodeHighlight();
    initializeTooltips();
    initializeInteractiveExamples();
    initializeThemeToggle();
    trackUserProgress();
});

/**
 * 코드 복사 기능
 */
function initializeCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-button');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const codeBlock = this.parentElement.nextElementSibling;
            const code = codeBlock.querySelector('code');
            
            try {
                await navigator.clipboard.writeText(code.textContent);
                
                // 성공 피드백
                const originalText = this.textContent;
                this.textContent = '✓ 복사됨';
                this.classList.add('copied');
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.classList.remove('copied');
                }, 2000);
            } catch (err) {
                console.error('복사 실패:', err);
                this.textContent = '❌ 실패';
                setTimeout(() => {
                    this.textContent = '복사';
                }, 2000);
            }
        });
    });
}

/**
 * 체크리스트 상호작용
 */
function initializeChecklists() {
    const checkboxes = document.querySelectorAll('.checklist input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        // 로컬 스토리지에서 상태 복원
        const checkboxId = checkbox.id || generateCheckboxId(checkbox);
        const savedState = localStorage.getItem(`obsidian-course-${checkboxId}`);
        
        if (savedState === 'true') {
            checkbox.checked = true;
            checkbox.parentElement.classList.add('completed');
        }
        
        checkbox.addEventListener('change', function() {
            const listItem = this.parentElement;
            
            if (this.checked) {
                listItem.classList.add('completed');
                localStorage.setItem(`obsidian-course-${checkboxId}`, 'true');
                
                // 완료 애니메이션
                animateCompletion(listItem);
            } else {
                listItem.classList.remove('completed');
                localStorage.removeItem(`obsidian-course-${checkboxId}`);
            }
            
            updateProgressCount();
        });
    });
}

/**
 * 진행률 표시바
 */
function initializeProgressBar() {
    // 진행률 바 생성
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.innerHTML = '<div class="progress-fill"></div>';
    document.body.appendChild(progressBar);
    
    // 스크롤 이벤트 처리
    let ticking = false;
    function updateProgress() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / scrollHeight) * 100;
        
        const progressFill = document.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.style.width = scrollPercent + '%';
        }
        
        ticking = false;
    }
    
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(updateProgress);
            ticking = true;
        }
    });
}

/**
 * 부드러운 스크롤
 */
function initializeSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const offset = 80; // 헤더 높이 고려
                const targetPosition = targetElement.offsetTop - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // URL 해시 업데이트
                history.pushState(null, null, '#' + targetId);
            }
        });
    });
}

/**
 * 코드 하이라이트 향상
 */
function initializeCodeHighlight() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        // 라인 번호 추가
        const lines = block.textContent.split('\n');
        if (lines.length > 1) {
            const numberedLines = lines.map((line, index) => {
                return `<span class="line-number">${index + 1}</span>${escapeHtml(line)}`;
            }).join('\n');
            
            block.innerHTML = numberedLines;
            block.classList.add('line-numbers');
        }
    });
}

/**
 * 툴팁 초기화
 */
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        let tooltip = null;
        
        element.addEventListener('mouseenter', function() {
            const text = this.getAttribute('data-tooltip');
            tooltip = createTooltip(text, this);
        });
        
        element.addEventListener('mouseleave', function() {
            if (tooltip) {
                tooltip.remove();
                tooltip = null;
            }
        });
    });
}

/**
 * 인터랙티브 예제
 */
function initializeInteractiveExamples() {
    const interactiveExamples = document.querySelectorAll('.interactive-example');
    
    interactiveExamples.forEach(example => {
        const runButton = example.querySelector('.run-example');
        const resetButton = example.querySelector('.reset-example');
        const output = example.querySelector('.example-output');
        
        if (runButton) {
            runButton.addEventListener('click', function() {
                // 예제 실행 로직 (예제별로 다름)
                const exampleType = example.getAttribute('data-example-type');
                runExample(exampleType, example, output);
            });
        }
        
        if (resetButton) {
            resetButton.addEventListener('click', function() {
                resetExample(example, output);
            });
        }
    });
}

/**
 * 테마 토글 (다크/라이트)
 */
function initializeThemeToggle() {
    // 테마 버튼이 있는 경우에만 실행
    const themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) return;
    
    // 저장된 테마 불러오기
    const savedTheme = localStorage.getItem('obsidian-course-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('obsidian-course-theme', newTheme);
        
        // 아이콘 변경
        this.innerHTML = newTheme === 'dark' ? 
            '<i class="fas fa-sun"></i>' : 
            '<i class="fas fa-moon"></i>';
    });
}

/**
 * 사용자 진행 상황 추적
 */
function trackUserProgress() {
    const lessonNumber = getLessonNumber();
    if (!lessonNumber) return;
    
    // 방문 기록
    const visitedLessons = JSON.parse(localStorage.getItem('obsidian-course-visited') || '[]');
    if (!visitedLessons.includes(lessonNumber)) {
        visitedLessons.push(lessonNumber);
        localStorage.setItem('obsidian-course-visited', JSON.stringify(visitedLessons));
    }
    
    // 읽은 시간 추적
    let readingTime = 0;
    const startTime = Date.now();
    
    setInterval(() => {
        readingTime = Math.floor((Date.now() - startTime) / 1000);
        updateReadingTime(readingTime);
    }, 1000);
    
    // 페이지 이탈 시 시간 저장
    window.addEventListener('beforeunload', () => {
        const totalTime = parseInt(localStorage.getItem(`obsidian-course-time-${lessonNumber}`) || 0);
        localStorage.setItem(`obsidian-course-time-${lessonNumber}`, totalTime + readingTime);
    });
}

// 유틸리티 함수들

function generateCheckboxId(checkbox) {
    const parent = checkbox.closest('.checklist');
    const index = Array.from(parent.querySelectorAll('input[type="checkbox"]')).indexOf(checkbox);
    const lessonNumber = getLessonNumber();
    return `lesson${lessonNumber}-checkbox-${index}`;
}

function animateCompletion(element) {
    element.style.transition = 'all 0.3s ease';
    element.style.transform = 'scale(1.05)';
    setTimeout(() => {
        element.style.transform = 'scale(1)';
    }, 300);
}

function updateProgressCount() {
    const total = document.querySelectorAll('.checklist input[type="checkbox"]').length;
    const completed = document.querySelectorAll('.checklist input[type="checkbox"]:checked').length;
    
    const progressText = document.querySelector('.checklist-progress');
    if (progressText) {
        progressText.textContent = `완료: ${completed}/${total}`;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function createTooltip(text, element) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
    
    return tooltip;
}

function getLessonNumber() {
    const match = window.location.pathname.match(/lesson(\d+)\.html/);
    return match ? parseInt(match[1]) : null;
}

function updateReadingTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const readingTimeElement = document.querySelector('.reading-time');
    if (readingTimeElement) {
        readingTimeElement.textContent = `읽은 시간: ${minutes}분 ${seconds % 60}초`;
    }
}

function runExample(type, container, output) {
    // 예제 타입별 실행 로직
    switch(type) {
        case 'markdown':
            runMarkdownExample(container, output);
            break;
        case 'links':
            runLinksExample(container, output);
            break;
        case 'tags':
            runTagsExample(container, output);
            break;
        default:
            output.textContent = '예제가 실행되었습니다.';
    }
}

function runMarkdownExample(container, output) {
    const input = container.querySelector('.example-input').value;
    // 간단한 마크다운 파싱 시뮬레이션
    let html = input
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*)\*/g, '<em>$1</em>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
        .replace(/\n/g, '<br>');
    
    output.innerHTML = html;
}

function runLinksExample(container, output) {
    const input = container.querySelector('.example-input').value;
    const linkPattern = /\[\[([^\]]+)\]\]/g;
    const matches = input.match(linkPattern);
    
    if (matches) {
        output.innerHTML = '<h4>발견된 내부 링크:</h4><ul>' + 
            matches.map(link => `<li>${link}</li>`).join('') + 
            '</ul>';
    } else {
        output.textContent = '내부 링크가 없습니다.';
    }
}

function runTagsExample(container, output) {
    const input = container.querySelector('.example-input').value;
    const tagPattern = /#[\w가-힣]+/g;
    const matches = input.match(tagPattern);
    
    if (matches) {
        output.innerHTML = '<h4>발견된 태그:</h4>' + 
            matches.map(tag => `<span class="tag">${tag}</span>`).join(' ');
    } else {
        output.textContent = '태그가 없습니다.';
    }
}

function resetExample(container, output) {
    const input = container.querySelector('.example-input');
    if (input) {
        input.value = input.getAttribute('data-default') || '';
    }
    output.innerHTML = '<em>결과가 여기에 표시됩니다.</em>';
}

// CSS 추가 (읽기 진행률 바)
const style = document.createElement('style');
style.textContent = `
    .reading-progress {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: rgba(124, 58, 237, 0.1);
        z-index: 9999;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #7c3aed 0%, #a855f7 100%);
        width: 0%;
        transition: width 0.1s ease;
    }
    
    .line-numbers .line-number {
        display: inline-block;
        width: 3em;
        padding-right: 1em;
        text-align: right;
        color: #666;
        user-select: none;
    }
    
    .tooltip {
        position: absolute;
        background: #333;
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 14px;
        z-index: 10000;
        pointer-events: none;
    }
    
    .copy-button.copied {
        background: #10b981;
        color: white;
    }
    
    .checklist li.completed {
        text-decoration: line-through;
        opacity: 0.7;
    }
    
    .tag {
        display: inline-block;
        background: rgba(124, 58, 237, 0.1);
        color: #7c3aed;
        padding: 2px 8px;
        border-radius: 4px;
        margin: 2px;
        font-size: 0.9em;
    }
`;
document.head.appendChild(style);

console.log('옵시디언 마스터 클래스 스크립트 로드됨 ✅');