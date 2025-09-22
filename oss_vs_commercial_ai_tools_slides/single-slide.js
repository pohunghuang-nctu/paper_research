// 單頁 slide 的簡化 JavaScript
document.addEventListener('DOMContentLoaded', () => {
    const menuBtn = document.getElementById('menuBtn');
    const slideMenu = document.getElementById('slideMenu');
    
    // 選單切換
    if (menuBtn && slideMenu) {
        menuBtn.addEventListener('click', () => {
            slideMenu.classList.toggle('active');
        });
        
        // 點擊外部關閉選單
        document.addEventListener('click', (e) => {
            if (!slideMenu.contains(e.target) && !menuBtn.contains(e.target)) {
                slideMenu.classList.remove('active');
            }
        });
    }
    
    // 鍵盤導航
    document.addEventListener('keydown', (e) => {
        const prevLink = document.querySelector('a[href*="slide-"]:first-of-type');
        const nextLink = document.querySelector('a[href*="slide-"]:last-of-type');
        
        switch(e.key) {
            case 'ArrowLeft':
            case 'ArrowUp':
                e.preventDefault();
                if (prevLink && !prevLink.classList.contains('disabled')) {
                    window.location.href = prevLink.href;
                }
                break;
            case 'ArrowRight':
            case 'ArrowDown':
            case ' ':
                e.preventDefault();
                if (nextLink && !nextLink.classList.contains('disabled')) {
                    window.location.href = nextLink.href;
                }
                break;
            case 'Home':
                e.preventDefault();
                window.location.href = 'slide-00.html';
                break;
            case 'End':
                e.preventDefault();
                window.location.href = 'slide-19.html';
                break;
            case 'Escape':
                slideMenu.classList.remove('active');
                break;
        }
    });
    
    // 添加載入動畫
    const slideContent = document.querySelector('.slide-content');
    if (slideContent) {
        slideContent.style.animation = 'slideIn 0.8s ease-out';
    }
    
    console.log('單頁 slide 系統初始化完成');
});
