// Hero Slider Functionality
class HeroSlider {
    constructor() {
        this.slider = document.querySelector('.hero-slider');
        this.slides = document.querySelectorAll('.hero-slide');
        this.dots = document.querySelectorAll('.hero-dot');
        this.prevButton = document.querySelector('.hero-prev');
        this.nextButton = document.querySelector('.hero-next');
        
        this.currentSlide = 0;
        this.autoPlayInterval = null;
        this.autoPlayDelay = 5000; // 5 seconds
        
        if (this.slider && this.slides.length > 1) {
            this.init();
        }
    }
    
    init() {
        // Set initial state
        this.updateSlideDisplay();
        
        // Add event listeners
        this.addEventListeners();
        
        // Start autoplay
        this.startAutoplay();
    }
    
    addEventListeners() {
        // Dot navigation
        this.dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                this.goToSlide(index);
            });
        });
        
        // Arrow navigation
        if (this.prevButton) {
            this.prevButton.addEventListener('click', () => {
                this.previousSlide();
            });
        }
        
        if (this.nextButton) {
            this.nextButton.addEventListener('click', () => {
                this.nextSlide();
            });
        }
        
        // Pause autoplay on hover
        this.slider.addEventListener('mouseenter', () => {
            this.pauseAutoplay();
        });
        
        this.slider.addEventListener('mouseleave', () => {
            this.startAutoplay();
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            // Only respond if slider is visible
            const sliderRect = this.slider.getBoundingClientRect();
            const isVisible = sliderRect.top < window.innerHeight && sliderRect.bottom > 0;
            
            if (isVisible) {
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    this.previousSlide();
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    this.nextSlide();
                }
            }
        });
        
        // Touch/swipe support
        this.addTouchSupport();
    }
    
    addTouchSupport() {
        let startX = 0;
        let startY = 0;
        let endX = 0;
        let endY = 0;
        
        this.slider.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        this.slider.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            
            const deltaX = endX - startX;
            const deltaY = endY - startY;
            
            // Only trigger if horizontal swipe is more prominent than vertical
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
                if (deltaX > 0) {
                    this.previousSlide();
                } else {
                    this.nextSlide();
                }
            }
        });
    }
    
    updateSlideDisplay() {
        // Update slides
        this.slides.forEach((slide, index) => {
            if (index === this.currentSlide) {
                slide.classList.add('opacity-100');
                slide.classList.remove('opacity-0');
                slide.classList.add('active');
            } else {
                slide.classList.remove('opacity-100');
                slide.classList.add('opacity-0');
                slide.classList.remove('active');
            }
        });
        
        // Update dots
        this.dots.forEach((dot, index) => {
            if (index === this.currentSlide) {
                dot.classList.add('bg-white');
                dot.classList.remove('bg-white/40');
            } else {
                dot.classList.remove('bg-white');
                dot.classList.add('bg-white/40');
            }
        });
    }
    
    goToSlide(index) {
        if (index < 0 || index >= this.slides.length || index === this.currentSlide) {
            return;
        }
        
        this.currentSlide = index;
        this.updateSlideDisplay();
        
        // Restart autoplay
        this.restartAutoplay();
    }
    
    nextSlide() {
        const nextIndex = (this.currentSlide + 1) % this.slides.length;
        this.goToSlide(nextIndex);
    }
    
    previousSlide() {
        const prevIndex = (this.currentSlide - 1 + this.slides.length) % this.slides.length;
        this.goToSlide(prevIndex);
    }
    
    startAutoplay() {
        if (this.slides.length <= 1) return;
        
        this.pauseAutoplay(); // Clear any existing interval
        this.autoPlayInterval = setInterval(() => {
            this.nextSlide();
        }, this.autoPlayDelay);
    }
    
    pauseAutoplay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
    
    restartAutoplay() {
        this.pauseAutoplay();
        this.startAutoplay();
    }
}

// Initialize slider when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    new HeroSlider();
});