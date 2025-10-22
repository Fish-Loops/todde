document.addEventListener('DOMContentLoaded', function() {
    const dropdownContainers = document.querySelectorAll('.dropdown-container');
    
    dropdownContainers.forEach(container => {
        const menu = container.querySelector('.dropdown-menu');
        const icon = container.querySelector('.dropdown-icon');
        let timeout;
        
        container.addEventListener('mouseenter', function() {
            clearTimeout(timeout);
            menu.classList.remove('opacity-0', 'invisible', 'scale-95');
            menu.classList.add('opacity-100', 'visible', 'scale-100');
            if (icon) {
                icon.style.transform = 'rotate(180deg)';
            }
        });
        
        container.addEventListener('mouseleave', function() {
            timeout = setTimeout(() => {
                menu.classList.add('opacity-0', 'invisible', 'scale-95');
                menu.classList.remove('opacity-100', 'visible', 'scale-100');
                if (icon) {
                    icon.style.transform = 'rotate(0deg)';
                }
            }, 150);
        });
    });
});