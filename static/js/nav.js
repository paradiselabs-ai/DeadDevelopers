document.addEventListener('DOMContentLoaded', function() {
    console.log('Navigation JS loaded - Simplified for Mobile');
    
    // Handle scroll effect
    window.addEventListener('scroll', () => {
        const header = document.querySelector('.site-header');
        if (window.scrollY > 10) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    // Mobile menu toggle functionality
    const menuButton = document.querySelector('.menu-button');
    const navCenter = document.querySelector('.nav-center');
    const navRight = document.querySelector('.nav-right');
    const body = document.body;
    
    if (!menuButton || !navCenter || !navRight) {
        console.error('Navigation elements not found');
        return;
    }
    
    // Force hamburger button to right side
    menuButton.style.position = 'absolute';
    menuButton.style.right = '1rem';
    menuButton.style.top = '50%';
    menuButton.style.transform = 'translateY(-50%)';
    
    // Function to update all navigation states based on screen size
    function updateNavigationState() {
        const isMobile = window.innerWidth <= 980;
        
        // Show/hide menu button based on screen size
        menuButton.style.display = isMobile ? 'block' : 'none';
        
        // Desktop view - always show nav links
        if (!isMobile) {
            navCenter.style.display = 'flex';
            navRight.style.display = 'flex';
            
            // Remove mobile classes
            navCenter.classList.remove('active');
            navRight.classList.remove('active');
            body.classList.remove('menu-open');
            backdrop.style.display = 'none';
        } 
        // Mobile view - hide nav links unless menu is active
        else {
            const isMenuActive = navCenter.classList.contains('active');
            
            // Only show links if menu is active
            navCenter.style.display = isMenuActive ? 'flex' : 'none';
            navRight.style.display = isMenuActive ? 'flex' : 'none';
            
            // Control backdrop visibility
            backdrop.style.display = isMenuActive ? 'block' : 'none';
        }
    }
    
    // Create backdrop element - no transitions
    const backdrop = document.createElement('div');
    backdrop.classList.add('mobile-menu-backdrop');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(4px);
        z-index: 1003;
        display: none;
    `;
    document.body.appendChild(backdrop);
    
    // Menu button click handler - no animations
    menuButton.addEventListener('click', function(e) {
        e.stopPropagation();
        
        // Toggle active class
        const isActive = navCenter.classList.contains('active');
        
        if (isActive) {
            // Close menu
            navCenter.classList.remove('active');
            navRight.classList.remove('active');
            body.classList.remove('menu-open');
            
            // Hide elements immediately
            navCenter.style.display = 'none';
            navRight.style.display = 'none';
            backdrop.style.display = 'none';
        } else {
            // Open menu
            navCenter.classList.add('active');
            navRight.classList.add('active');
            body.classList.add('menu-open');
            
            // Show elements immediately
            navCenter.style.display = 'flex';
            navRight.style.display = 'flex';
            backdrop.style.display = 'block';
        }
        
        // Update accessibility
        menuButton.setAttribute('aria-expanded', !isActive);
    });
    
    // Close menu when clicking backdrop - no animations
    backdrop.addEventListener('click', closeMenu);
    
    // Close menu when clicking links (in mobile view)
    const navLinks = document.querySelectorAll('.nav-center a, .nav-right a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 980) {
                closeMenu();
            }
        });
    });
    
    // Close menu function - no animations
    function closeMenu() {
        navCenter.classList.remove('active');
        navRight.classList.remove('active');
        body.classList.remove('menu-open');
        
        // Hide elements immediately in mobile view
        if (window.innerWidth <= 980) {
            navCenter.style.display = 'none';
            navRight.style.display = 'none';
            backdrop.style.display = 'none';
        }
    }
    
    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.main-nav') && 
            !e.target.closest('.menu-button') && 
            navCenter.classList.contains('active')) {
            closeMenu();
        }
    });
    
    // Run initially
    updateNavigationState();
    
    // Run on resize
    window.addEventListener('resize', updateNavigationState);
    
    // Prevent scrolling when mobile menu is open
    function preventDefault(e) {
        e.preventDefault();
    }

    // Disable scroll
    function disableScroll() {
        document.body.addEventListener('touchmove', preventDefault, { passive: false });
    }

    // Enable scroll
    function enableScroll() {
        document.body.removeEventListener('touchmove', preventDefault, { passive: false });
    }

    // Toggle scroll when menu opens/closes
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                if (body.classList.contains('menu-open')) {
                    disableScroll();
                } else {
                    enableScroll();
                }
            }
        });
    });

    observer.observe(body, { attributes: true });
});
