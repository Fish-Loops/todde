// Real-time search functionality
class RealTimeSearch {
    constructor(inputElement, resultsContainer) {
        this.input = inputElement;
        this.resultsContainer = resultsContainer;
        this.searchTimeout = null;
        this.isVisible = false;
        this.currentFocus = -1;
        
        this.init();
    }
    
    init() {
        // Add event listeners
        this.input.addEventListener('input', (e) => this.handleInput(e));
        this.input.addEventListener('focus', (e) => this.handleFocus(e));
        this.input.addEventListener('blur', (e) => this.handleBlur(e));
        this.input.addEventListener('keydown', (e) => this.handleKeydown(e));
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.input.contains(e.target) && !this.resultsContainer.contains(e.target)) {
                this.hideResults();
            }
        });
        
        // Create results container structure
        this.createResultsContainer();
    }
    
    createResultsContainer() {
        this.resultsContainer.className = `
            absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-b-lg shadow-lg 
            max-h-96 overflow-y-auto z-50 hidden
        `.trim();
        
        // Position relative to search input
        this.input.parentElement.classList.add('relative');
    }
    
    handleInput(e) {
        const query = e.target.value.trim();
        
        // Clear previous timeout
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }
        
        if (query.length < 2) {
            this.hideResults();
            return;
        }
        
        // Debounce search requests
        this.searchTimeout = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    }
    
    handleFocus(e) {
        const query = e.target.value.trim();
        if (query.length >= 2) {
            this.performSearch(query);
        }
    }
    
    handleBlur(e) {
        // Delay hiding to allow clicks on results
        setTimeout(() => {
            if (!this.resultsContainer.matches(':hover')) {
                this.hideResults();
            }
        }, 150);
    }
    
    handleKeydown(e) {
        if (!this.isVisible) return;
        
        const items = this.resultsContainer.querySelectorAll('.search-result-item');
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.currentFocus = Math.min(this.currentFocus + 1, items.length - 1);
                this.updateFocus(items);
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.currentFocus = Math.max(this.currentFocus - 1, -1);
                this.updateFocus(items);
                break;
                
            case 'Enter':
                e.preventDefault();
                if (this.currentFocus >= 0 && items[this.currentFocus]) {
                    const link = items[this.currentFocus].querySelector('a');
                    if (link) {
                        window.location.href = link.href;
                    }
                }
                break;
                
            case 'Escape':
                this.hideResults();
                this.input.blur();
                break;
        }
    }
    
    updateFocus(items) {
        items.forEach((item, index) => {
            if (index === this.currentFocus) {
                item.classList.add('bg-gray-50');
            } else {
                item.classList.remove('bg-gray-50');
            }
        });
    }
    
    async performSearch(query) {
        try {
            const response = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.results && data.results.length > 0) {
                this.displayResults(data.results);
                this.showResults();
            } else {
                this.displayNoResults(query);
                this.showResults();
            }
        } catch (error) {
            console.error('Search error:', error);
            this.hideResults();
        }
    }
    
    displayResults(results) {
        const html = results.map(result => this.createResultItem(result)).join('');
        this.resultsContainer.innerHTML = html;
        this.currentFocus = -1;
    }
    
    createResultItem(result) {
        const typeIcon = this.getTypeIcon(result.type);
        const imageHtml = result.image 
            ? `<img src="${result.image}" alt="${result.title}" class="w-12 h-8 object-cover rounded flex-shrink-0">`
            : `<div class="w-12 h-8 bg-gray-100 rounded flex items-center justify-center flex-shrink-0">
                <svg class="w-4 h-4 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd"></path>
                </svg>
               </div>`;
        
        return `
            <div class="search-result-item border-b border-gray-100 last:border-b-0 hover:bg-gray-50 cursor-pointer">
                <a href="${result.url}" class="block p-3">
                    <div class="flex items-center space-x-3">
                        <div class="flex-shrink-0">
                            ${typeIcon}
                        </div>
                        ${imageHtml}
                        <div class="flex-1 min-w-0">
                            <div class="text-sm font-medium text-gray-900 truncate">
                                ${result.title}
                            </div>
                            <div class="text-xs text-gray-500 truncate">
                                ${result.subtitle}
                            </div>
                        </div>
                    </div>
                </a>
            </div>
        `;
    }
    
    getTypeIcon(type) {
        const iconClass = "w-4 h-4 text-gray-400";
        
        switch (type) {
            case 'manufacturer':
                return `<svg class="${iconClass}" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 2a2 2 0 00-2 2v11a3 3 0 106 0V4a2 2 0 00-2-2H4zM3 15a1 1 0 011-1h1a1 1 0 011 1v1a1 1 0 01-1 1H4a1 1 0 01-1-1v-1zm7-1a1 1 0 000 2h1a1 1 0 100-2h-1zm2-1a1 1 0 011-1h1a1 1 0 110 2h-1a1 1 0 01-1-1zm1-5a1 1 0 100 2h1a1 1 0 100-2h-1z" clip-rule="evenodd"></path>
                </svg>`;
                
            case 'model':
                return `<svg class="${iconClass}" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M8 5a1 1 0 100 2h5.586l-1.293 1.293a1 1 0 001.414 1.414L16.414 7a1 1 0 000-1.414L13.707 3.293a1 1 0 00-1.414 1.414L13.586 6H8a3 3 0 100 6h5.586l-1.293 1.293a1 1 0 101.414 1.414L16.414 13a1 1 0 000-1.414L13.707 9.293a1 1 0 00-1.414 1.414L13.586 12H8a1 1 0 010-2z"></path>
                </svg>`;
                
            case 'variant':
                return `<svg class="${iconClass}" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M8 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM15 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"></path>
                    <path d="M3 4a1 1 0 00-1 1v10a1 1 0 001 1h1.05a2.5 2.5 0 014.9 0H10a1 1 0 001-1V5a1 1 0 00-1-1H3zM14 7a1 1 0 00-1 1v6.05A2.5 2.5 0 0115.95 16H17a1 1 0 001-1V8a1 1 0 00-1-1h-3z"></path>
                </svg>`;
                
            default:
                return `<svg class="${iconClass}" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
                </svg>`;
        }
    }
    
    displayNoResults(query) {
        this.resultsContainer.innerHTML = `
            <div class="p-4 text-center">
                <div class="text-gray-500 text-sm">
                    <svg class="w-8 h-8 text-gray-300 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"></path>
                    </svg>
                    <div>No results found for "${query}"</div>
                    <div class="text-xs text-gray-400 mt-1">Try searching for car brands, models, or years</div>
                </div>
            </div>
        `;
        this.currentFocus = -1;
    }
    
    showResults() {
        this.resultsContainer.classList.remove('hidden');
        this.isVisible = true;
    }
    
    hideResults() {
        this.resultsContainer.classList.add('hidden');
        this.isVisible = false;
        this.currentFocus = -1;
    }
}

// Initialize search when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput && searchResults) {
        new RealTimeSearch(searchInput, searchResults);
    }
});