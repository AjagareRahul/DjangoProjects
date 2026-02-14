// Feature List Interactivity
document.addEventListener('DOMContentLoaded', function() {
    const featureList = document.querySelector('.feature-list');
    
    if (featureList) {
        const listItems = featureList.querySelectorAll('li');
        
        listItems.forEach(function(item) {
            item.addEventListener('click', function() {
                // Remove active class from all items
                listItems.forEach(function(li) {
                    li.style.background = 'rgba(255, 255, 255, 0.15)';
                });
                // Add active state to clicked item
                this.style.background = 'rgba(255, 255, 255, 0.3)';
                
                // Add a subtle scale effect
                this.style.transform = 'scale(1.02)';
                setTimeout(() => {
                    this.style.transform = 'translateX(10px)';
                }, 150);
            });
            
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(10px) scale(1.02)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0) scale(1)';
            });
        });
    }
    
    // Login Form Animation
    const loginBtn = document.querySelector('.login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            if (this.type === 'submit') {
                this.textContent = 'Signing In...';
                this.style.opacity = '0.8';
            }
        });
    }
});
