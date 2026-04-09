// login.js
let currentMethod = '';

function selectMethod(method) {
    currentMethod = method;
    
    // Toggle classes on cards
    document.querySelectorAll('.method-card').forEach(card => card.classList.remove('selected'));
    document.getElementById(`btn-${method}`).classList.add('selected');

    // Show input section
    const dynamicSection = document.getElementById('dynamicInputs');
    dynamicSection.classList.add('active');

    // Update Input visuals
    const label = document.getElementById('identityLabel');
    const input = document.getElementById('identity');
    const icon = document.getElementById('identityIcon');

    switch(method) {
        case 'email':
            label.innerText = 'البريد الإلكتروني';
            input.placeholder = 'example@domain.com';
            input.type = 'email';
            icon.innerText = 'mail';
            break;
        case 'phone':
            label.innerText = 'رقم الهاتف';
            input.placeholder = '01xxxxxxxxx';
            input.type = 'tel';
            icon.innerText = 'phone_iphone';
            break;
        case 'username':
            label.innerText = 'اسم المستخدم';
            input.placeholder = 'أدخل اسم المستخدم';
            input.type = 'text';
            icon.innerText = 'person_outline';
            break;
    }
    
    validateForm();

    // انتظر قليلاً حتى يكتمل تأثير الفتح ثم قم بالتمرير إلى بداية الحقل
    setTimeout(() => {
        const identityField = document.getElementById('identity');
        if (identityField) {
            identityField.scrollIntoView({
                behavior: 'smooth',
                block: 'center',  // جعل الحقل في المنتصف لضمان ظهور ما تحته
            });
        }
    }, 100);
}

function validateForm() {
    const identity = document.getElementById('identity').value;
    const password = document.getElementById('password').value;
    const submitBtn = document.getElementById('submitBtn');

    if (currentMethod && identity.length > 3 && password.length >= 6) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

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

// إخفاء التنبيهات التلقائي بعد 5 ثوانٍ
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.message-alert');
    alerts.forEach(alert => {
        // لا نريد إخفاء رسائل الخطأ تلقائياً لكي يقرأها المستخدم براحة
        if (!alert.classList.contains('bg-error-container')) {
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.classList.add('fade-out');
                    setTimeout(() => alert.remove(), 300);
                }
            }, 5000);
        }
    });
});