// auth/register.js

// إغلاق التنبيهات (Messages)
function closeAlert(button) {
    const alertBox = button.closest('.message-alert');
    if (alertBox) {
        alertBox.classList.add('fade-out');
        setTimeout(() => {
            alertBox.remove();
        }, 300);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // إخفاء التنبيهات التلقائي بعد 5 ثوانٍ
    const alerts = document.querySelectorAll('.message-alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('bg-error-container')) {
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.classList.add('fade-out');
                    setTimeout(() => alert.remove(), 300);
                }
            }, 5000);
        }
    });

    // تأثير كشاف الإضاءة المنفصل لكل حقل باسورد
    const eyeToggles = document.querySelectorAll('.eye-toggle');
    const overlay = document.getElementById('dark-overlay');
    const beam = document.getElementById('spotlight-beam');
    
    let activeEye = null;

    function updateBeam() {
        if (!activeEye) return;
        
        const btn = activeEye;
        const pwUnit = btn.closest('.password-unit');
        const iconSpan = btn.querySelector('span'); // ايقونة العين
        
        const pwRect = pwUnit.getBoundingClientRect();
        const iconRect = iconSpan.getBoundingClientRect();
        
        const startX = iconRect.left + iconRect.width / 2;
        const startY = iconRect.top + iconRect.height / 2;
        
        const padding = 25; 
        const leftX = pwRect.left - padding;
        const rightX = pwRect.right + padding;
        const topY = pwRect.top - padding;
        const bottomY = pwRect.bottom + padding;
        
        const top = topY;
        const width = rightX - leftX;
        const height = bottomY - topY;
        
        const docTop = window.scrollY + top;
        const docLeft = window.scrollX + leftX;
        
        beam.style.top = `${docTop}px`;
        beam.style.left = `${docLeft}px`;
        beam.style.width = `${width}px`;
        beam.style.height = `${height}px`;
        
        const vertexPercentX = ((startX - leftX) / width) * 100;
        const vertexPercentY = ((startY - topY) / height) * 100;
        
        // شعاع نور أبيض ينطلق من موقع العين (اليسار) في اتجاه حقل الإدخال المستهدف (نحو اليمين)
        beam.style.clipPath = `polygon(${vertexPercentX}% ${vertexPercentY}%, 100% 0%, 100% 100%)`;
        beam.style.background = 'linear-gradient(90deg, rgba(255, 255, 255, 0.7) 0%, rgba(255, 255, 255, 0.0) 100%)';
    }

    eyeToggles.forEach(btn => {
        btn.addEventListener('click', () => {
            const pwUnit = btn.closest('.password-unit');
            const inp = pwUnit.querySelector('.pw-input');
            const iconSpan = btn.querySelector('span');
            
            const isCurrentlyActive = (inp.type === 'text');
            
            if (isCurrentlyActive) {
                // إطفاء كشاف هذا الحقل
                inp.type = 'password';
                iconSpan.innerText = 'visibility';
                btn.classList.remove('text-primary');
                
                // إرجاع الصندوق للون العادي وتنزيل الـ Z-Index
                pwUnit.classList.remove('z-50', 'bg-white', 'p-3', '-m-3', 'rounded-xl', 'shadow-[0_0_80px_-15px_rgba(255,255,255,0.6)]');
                pwUnit.classList.add('z-10');
                
                // فحص إذا كان هناك حقل آخر مفتوح
                const anyActive = Array.from(document.querySelectorAll('.pw-input')).some(i => i.type === 'text');
                if (!anyActive) {
                overlay.classList.remove('opacity-80');
                    overlay.classList.add('opacity-0');
                    beam.classList.remove('opacity-100');
                    beam.classList.add('opacity-0');
                    activeEye = null;
                } else {
                    // إذا كان الحقل الثاني مفتوح، اجعل الكشاف يتوجه إليه
                    activeEye = document.querySelector('.pw-input[type="text"]').closest('.password-unit').querySelector('.eye-toggle');
                    requestAnimationFrame(updateBeam);
                }
            } else {
                // تشغيل الكشاف لهذا الحقل
                inp.type = 'text';
                iconSpan.innerText = 'visibility_off';
                btn.classList.add('text-primary');
                
                // إضاءة هذا الصندوق ورفعه ليطفو
                pwUnit.classList.add('z-50', 'bg-white', 'p-3', '-m-3', 'rounded-xl', 'shadow-[0_0_80px_-15px_rgba(255,255,255,0.6)]');
                pwUnit.classList.remove('z-10');
                
                overlay.classList.remove('opacity-0');
                overlay.classList.add('opacity-80');
                beam.classList.remove('opacity-0');
                beam.classList.add('opacity-100');
                
                activeEye = btn;
                requestAnimationFrame(updateBeam);
            }
        });
    });

    window.addEventListener('resize', updateBeam);
});

// Modal Logic
window.openModal = function(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.remove('opacity-0', 'pointer-events-none');
    modal.classList.add('opacity-100');
    
    const content = modal.querySelector('.modal-content');
    content.classList.remove('scale-95');
    content.classList.add('scale-100');
};

window.closeModal = function(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.add('opacity-0', 'pointer-events-none');
    modal.classList.remove('opacity-100');
    
    const content = modal.querySelector('.modal-content');
    content.classList.add('scale-95');
    content.classList.remove('scale-100');
};
