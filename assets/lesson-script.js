// 레슨 페이지 스크립트
document.addEventListener('DOMContentLoaded', function() {
    // 진행률 추적
    trackProgress();
    
    // 이미지 클릭 시 확대
    setupImageZoom();
    
    // 코드 블록 복사 기능
    setupCodeCopy();
});

function trackProgress() {
    const lessonNumber = document.querySelector('.lesson-header h1').textContent.match(/\d+/)[0];
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
}