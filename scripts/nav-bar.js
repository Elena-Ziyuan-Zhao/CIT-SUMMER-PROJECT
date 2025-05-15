document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('menu-toggle');
    const menu = document.getElementById('menu');
  
    toggleBtn.addEventListener('click', () => {
        menu.classList.toggle('open');
    });
});