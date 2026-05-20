document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'dark';

    // Set initial theme
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateToggleIcon(currentTheme);

    themeToggle.addEventListener('click', () => {
        let theme = document.documentElement.getAttribute('data-theme');
        let newTheme = 'dark';
        
        if (theme === 'dark') newTheme = 'sunset';
        else if (theme === 'sunset') newTheme = 'light';
        else newTheme = 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateToggleIcon(newTheme);
    });

    function updateToggleIcon(theme) {
        const icon = themeToggle.querySelector('i');
        // Reset classes
        icon.className = 'fas';
        
        if (theme === 'dark') {
            icon.classList.add('fa-moon');
            icon.style.color = '#00D4FF'; // electric blue
        } else if (theme === 'sunset') {
            icon.classList.add('fa-cloud-sun');
            icon.style.color = '#FF8C00'; // sunset orange
        } else {
            icon.classList.add('fa-sun');
            icon.style.color = '#FFD700'; // light sun gold
        }
    }
});
