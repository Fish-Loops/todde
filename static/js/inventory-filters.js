/**
 * Enhanced inventory filtering with dynamic model updates
 */
document.addEventListener('DOMContentLoaded', function() {
    const manufacturerInputs = document.querySelectorAll('input[name="manufacturer"]');
    const modelSection = document.querySelector('.model-filter-section');
    const form = document.querySelector('form[method="get"]');
    
    // Handle manufacturer selection to dynamically update models
    manufacturerInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.checked) {
                updateModelOptions(this.value);
            }
        });
    });
    
    async function updateModelOptions(manufacturerId) {
        if (!manufacturerId) {
            return;
        }
        
        try {
            // Make request to get models for selected manufacturer
            const response = await fetch(`/api/car-models/?manufacturer=${manufacturerId}`);
            const data = await response.json();
            
            // Update model options
            const modelContainer = document.querySelector('.model-options-container');
            if (modelContainer && data.models) {
                let modelHTML = '';
                data.models.forEach(model => {
                    modelHTML += `
                        <label class="flex items-center justify-between rounded-lg border border-todde-jet/10 bg-white px-3 py-2 text-sm text-todde-dark/80 transition hover:border-todde-blue/40">
                            <span class="flex items-center gap-3">
                                <input
                                    type="radio"
                                    name="model"
                                    value="${model.id}"
                                    class="h-4 w-4 border-todde-jet/20 text-todde-blue focus:ring-todde-blue"
                                />
                                ${model.name}
                            </span>
                            <span class="text-xs text-todde-dark/50">(${model.count || 0})</span>
                        </label>
                    `;
                });
                modelContainer.innerHTML = modelHTML;
            }
        } catch (error) {
            console.error('Error updating model options:', error);
        }
    }
    
    // Auto-submit form when filters change (optional enhancement)
    const autoSubmitInputs = document.querySelectorAll('select[name="sort"]');
    autoSubmitInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (form) {
                form.submit();
            }
        });
    });
    
    // Price range validation
    const priceMinInput = document.querySelector('input[name="price_min"]');
    const priceMaxInput = document.querySelector('input[name="price_max"]');
    
    if (priceMinInput && priceMaxInput) {
        function validatePriceRange() {
            const minValue = parseFloat(priceMinInput.value) || 0;
            const maxValue = parseFloat(priceMaxInput.value) || Infinity;
            
            if (minValue > maxValue) {
                priceMaxInput.setCustomValidity('Maximum price must be greater than minimum price');
            } else {
                priceMaxInput.setCustomValidity('');
            }
        }
        
        priceMinInput.addEventListener('input', validatePriceRange);
        priceMaxInput.addEventListener('input', validatePriceRange);
    }
    
    // Year range validation
    const yearMinInput = document.querySelector('input[name="year_min"]');
    const yearMaxInput = document.querySelector('input[name="year_max"]');
    
    if (yearMinInput && yearMaxInput) {
        function validateYearRange() {
            const minValue = parseInt(yearMinInput.value) || 0;
            const maxValue = parseInt(yearMaxInput.value) || new Date().getFullYear() + 1;
            
            if (minValue > maxValue) {
                yearMaxInput.setCustomValidity('Maximum year must be greater than minimum year');
            } else {
                yearMaxInput.setCustomValidity('');
            }
        }
        
        yearMinInput.addEventListener('input', validateYearRange);
        yearMaxInput.addEventListener('input', validateYearRange);
    }
});