// static/header.js
document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.querySelector('.menuButton');
    const mobileMenu = document.querySelector('#mobileMenu');
    const mobileMenuBackdrop = document.querySelector('#mobileMenuBackdrop');
  
    if (menuButton && mobileMenu && mobileMenuBackdrop) {
      menuButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('open');
        mobileMenuBackdrop.classList.toggle('open');
        document.body.classList.toggle('menu-open');
      });
  
      mobileMenuBackdrop.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        mobileMenuBackdrop.classList.remove('open');
        document.body.classList.remove('menu-open');
      });
    }
  });