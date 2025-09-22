// Slide 管理系統
class SlideManager {
    constructor() {
        this.currentSlide = 0;
        this.totalSlides = document.querySelectorAll('.slide').length;
        this.slides = document.querySelectorAll('.slide');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.slideCounter = document.getElementById('slideCounter');
        this.menuBtn = document.getElementById('menuBtn');
        this.slideMenu = document.getElementById('slideMenu');
        this.menuItems = document.querySelectorAll('.menu-item');
        this.progressFill = document.querySelector('.progress-fill');
        
        this.init();
    }
    
    init() {
        this.updateSlideCounter();
        this.updateProgressBar();
        this.bindEvents();
        this.updateNavigationButtons();
        this.updateMenuActiveItem();
    }
    
    bindEvents() {
        // 導航按鈕事件
        this.prevBtn.addEventListener('click', () => this.previousSlide());
        this.nextBtn.addEventListener('click', () => this.nextSlide());
        
        // 鍵盤事件
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft':
                case 'ArrowUp':
                    e.preventDefault();
                    this.previousSlide();
                    break;
                case 'ArrowRight':
                case 'ArrowDown':
                case ' ':
                    e.preventDefault();
                    this.nextSlide();
                    break;
                case 'Home':
                    e.preventDefault();
                    this.goToSlide(0);
                    break;
                case 'End':
                    e.preventDefault();
                    this.goToSlide(this.totalSlides - 1);
                    break;
                case 'Escape':
                    this.closeMenu();
                    break;
            }
        });
        
        // 選單事件
        this.menuBtn.addEventListener('click', () => this.toggleMenu());
        
        // 選單項目點擊事件
        this.menuItems.forEach((item, index) => {
            item.addEventListener('click', () => {
                const slideIndex = parseInt(item.dataset.slide);
                this.goToSlide(slideIndex);
                this.closeMenu();
            });
        });
        
        // 點擊外部關閉選單
        document.addEventListener('click', (e) => {
            if (!this.slideMenu.contains(e.target) && !this.menuBtn.contains(e.target)) {
                this.closeMenu();
            }
        });
        
        // 觸控手勢支援
        this.bindTouchEvents();
    }
    
    bindTouchEvents() {
        let startX = 0;
        let startY = 0;
        let endX = 0;
        let endY = 0;
        
        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            const minSwipeDistance = 50;
            
            // 水平滑動優先
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    this.previousSlide();
                } else {
                    this.nextSlide();
                }
            }
        });
    }
    
    nextSlide() {
        if (this.currentSlide < this.totalSlides - 1) {
            this.goToSlide(this.currentSlide + 1);
        }
    }
    
    previousSlide() {
        if (this.currentSlide > 0) {
            this.goToSlide(this.currentSlide - 1);
        }
    }
    
    goToSlide(index) {
        if (index >= 0 && index < this.totalSlides) {
            // 移除當前活動狀態
            this.slides[this.currentSlide].classList.remove('active');
            
            // 添加過渡效果
            if (index > this.currentSlide) {
                this.slides[this.currentSlide].classList.add('prev');
            } else {
                this.slides[this.currentSlide].classList.remove('prev');
            }
            
            // 設定新的活動 slide
            this.currentSlide = index;
            this.slides[this.currentSlide].classList.add('active');
            this.slides[this.currentSlide].classList.remove('prev');
            
            // 更新 UI
            this.updateSlideCounter();
            this.updateProgressBar();
            this.updateNavigationButtons();
            this.updateMenuActiveItem();
            
            // 觸發 slide 切換事件
            this.onSlideChange();
        }
    }
    
    updateSlideCounter() {
        this.slideCounter.textContent = `${this.currentSlide + 1} / ${this.totalSlides}`;
    }
    
    updateProgressBar() {
        const progress = ((this.currentSlide + 1) / this.totalSlides) * 100;
        this.progressFill.style.width = `${progress}%`;
    }
    
    updateNavigationButtons() {
        this.prevBtn.disabled = this.currentSlide === 0;
        this.nextBtn.disabled = this.currentSlide === this.totalSlides - 1;
    }
    
    updateMenuActiveItem() {
        this.menuItems.forEach((item, index) => {
            const slideIndex = parseInt(item.dataset.slide);
            if (slideIndex === this.currentSlide) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }
    
    toggleMenu() {
        this.slideMenu.classList.toggle('active');
    }
    
    closeMenu() {
        this.slideMenu.classList.remove('active');
    }
    
    onSlideChange() {
        // 可以在這裡添加 slide 切換時的特殊效果或邏輯
        console.log(`Switched to slide ${this.currentSlide + 1}`);
        
        // 重新觸發動畫
        const currentSlideContent = this.slides[this.currentSlide].querySelector('.slide-content');
        if (currentSlideContent) {
            currentSlideContent.style.animation = 'none';
            currentSlideContent.offsetHeight; // 觸發重排
            currentSlideContent.style.animation = 'slideIn 0.8s ease-out';
        }
    }
}

// 工具函數
class PresentationUtils {
    static formatNumber(num) {
        return new Intl.NumberFormat('zh-TW').format(num);
    }
    
    static createChart(containerId, data, options = {}) {
        // 簡單的圖表創建函數，可以根據需要擴展
        const container = document.getElementById(containerId);
        if (!container) return;
        
        // 這裡可以整合 Chart.js 或其他圖表庫
        console.log('Creating chart for:', containerId, data);
    }
    
    static animateCounter(element, targetValue, duration = 2000) {
        const startValue = 0;
        const startTime = performance.now();
        
        function updateCounter(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = Math.floor(startValue + (targetValue - startValue) * progress);
            element.textContent = PresentationUtils.formatNumber(currentValue);
            
            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        }
        
        requestAnimationFrame(updateCounter);
    }
}

// 主題切換功能
class ThemeManager {
    constructor() {
        this.themes = {
            default: {
                primary: '#667eea',
                secondary: '#764ba2',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
            },
            dark: {
                primary: '#4f46e5',
                secondary: '#7c3aed',
                background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 100%)'
            },
            green: {
                primary: '#059669',
                secondary: '#0d9488',
                background: 'linear-gradient(135deg, #059669 0%, #0d9488 100%)'
            }
        };
        
        this.currentTheme = 'default';
    }
    
    switchTheme(themeName) {
        if (this.themes[themeName]) {
            this.currentTheme = themeName;
            this.applyTheme(this.themes[themeName]);
        }
    }
    
    applyTheme(theme) {
        document.documentElement.style.setProperty('--primary-color', theme.primary);
        document.documentElement.style.setProperty('--secondary-color', theme.secondary);
        document.body.style.background = theme.background;
    }
}

// 全螢幕功能
class FullscreenManager {
    constructor() {
        this.isFullscreen = false;
        this.bindEvents();
    }
    
    bindEvents() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'F11') {
                e.preventDefault();
                this.toggleFullscreen();
            }
        });
        
        document.addEventListener('fullscreenchange', () => {
            this.isFullscreen = !!document.fullscreenElement;
        });
    }
    
    toggleFullscreen() {
        if (!this.isFullscreen) {
            document.documentElement.requestFullscreen().catch(err => {
                console.log('無法進入全螢幕模式:', err);
            });
        } else {
            document.exitFullscreen().catch(err => {
                console.log('無法退出全螢幕模式:', err);
            });
        }
    }
}

// 初始化應用程式
document.addEventListener('DOMContentLoaded', () => {
    // 初始化 slide 管理器
    const slideManager = new SlideManager();
    
    // 初始化主題管理器
    const themeManager = new ThemeManager();
    
    // 初始化全螢幕管理器
    const fullscreenManager = new FullscreenManager();
    
    // 將管理器實例掛載到全域，方便調試和擴展
    window.slideManager = slideManager;
    window.themeManager = themeManager;
    window.fullscreenManager = fullscreenManager;
    window.PresentationUtils = PresentationUtils;
    
    // 顯示載入完成訊息
    console.log('簡報系統初始化完成');
    console.log('快捷鍵說明:');
    console.log('- 方向鍵/空白鍵: 切換 slide');
    console.log('- Home/End: 跳到第一張/最後一張');
    console.log('- F11: 切換全螢幕');
    console.log('- Esc: 關閉選單');
});

// 錯誤處理
window.addEventListener('error', (e) => {
    console.error('簡報系統錯誤:', e.error);
});

// 性能監控
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log(`頁面載入時間: ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
        }, 0);
    });
}
