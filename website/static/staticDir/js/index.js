'use strict';

/* ══════════════════════════════════════════
   1. NAVBAR — scroll & active link tracking
══════════════════════════════════════════ */
const Navbar = (() => {
  const navbar  = document.getElementById('navbar');
  const SCROLL_THRESHOLD = 60;

  function onScroll() {
    if (window.scrollY > SCROLL_THRESHOLD) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    updateActiveLink();
  }

  function updateActiveLink() {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + 120;

    sections.forEach(section => {
      const id     = section.getAttribute('id');
      const top    = section.offsetTop;
      const bottom = top + section.offsetHeight;
      const links  = document.querySelectorAll(`[data-section="${id}"]`);

      links.forEach(link => {
        if (scrollPos >= top && scrollPos < bottom) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    });
  }

  function init() {
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // run once on load
  }

  return { init };
})();


/* ══════════════════════════════════════════
   2. MOBILE MENU
══════════════════════════════════════════ */
const MobileMenu = (() => {
  const toggleBtn  = document.getElementById('menu-toggle');
  const menu       = document.getElementById('mobile-menu');
  const icon       = document.getElementById('menu-icon');
  let   isOpen     = false;

  function open() {
    isOpen = true;
    menu.classList.remove('hidden');
    icon.textContent = 'close';
    toggleBtn.setAttribute('aria-expanded', 'true');
    toggleBtn.setAttribute('aria-label', 'إغلاق القائمة');
    // Animate in
    menu.style.animation = 'none';
    menu.offsetHeight; // reflow
    menu.style.animation = '';
  }

  function close() {
    isOpen = false;
    menu.classList.add('hidden');
    icon.textContent = 'menu';
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.setAttribute('aria-label', 'فتح القائمة');
  }

  function toggle() {
    isOpen ? close() : open();
  }

  function init() {
    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', toggle);

    // Close when a mobile nav link is clicked
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', () => {
        setTimeout(close, 100);
      });
    });

    // Close on outside click
    document.addEventListener('click', e => {
      if (isOpen && !menu.contains(e.target) && !toggleBtn.contains(e.target)) {
        close();
      }
    });
  }

  return { init, close };
})();


/* ══════════════════════════════════════════
   3. DROPDOWNS
══════════════════════════════════════════ */
const Dropdowns = (() => {
  const dropdowns = [
    { btn: 'notif-btn',   panel: 'notif-dropdown'   },
    { btn: 'profile-btn', panel: 'profile-dropdown'  },
  ];

  let activeDropdown = null;

  function open(panel, btn) {
    panel.classList.remove('hidden');
    btn.setAttribute('aria-expanded', 'true');
    activeDropdown = { panel, btn };
  }

  function close(panel, btn) {
    panel.classList.add('hidden');
    btn.setAttribute('aria-expanded', 'false');
    if (activeDropdown && activeDropdown.panel === panel) {
      activeDropdown = null;
    }
  }

  function closeAll() {
    dropdowns.forEach(({ btn: btnId, panel: panelId }) => {
      const btn   = document.getElementById(btnId);
      const panel = document.getElementById(panelId);
      if (btn && panel) close(panel, btn);
    });
  }

  function init() {
    dropdowns.forEach(({ btn: btnId, panel: panelId }) => {
      const btn   = document.getElementById(btnId);
      const panel = document.getElementById(panelId);
      if (!btn || !panel) return;

      btn.addEventListener('click', e => {
        e.stopPropagation();
        const isOpen = !panel.classList.contains('hidden');
        closeAll();
        if (!isOpen) open(panel, btn);
      });
    });

    // Close on outside click
    document.addEventListener('click', () => closeAll());

    // Close on Escape key
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeAll();
    });
  }

  return { init, closeAll };
})();


/* ══════════════════════════════════════════
   4. SMOOTH SCROLL — anchor nav
══════════════════════════════════════════ */
const SmoothScroll = (() => {
  const NAVBAR_HEIGHT = 80;

  function scrollTo(targetId) {
    const el = document.getElementById(targetId);
    if (!el) return;
    const top = el.getBoundingClientRect().top + window.scrollY - NAVBAR_HEIGHT;
    window.scrollTo({ top, behavior: 'smooth' });
  }

  function init() {
    document.querySelectorAll('a[href^="#"]').forEach(link => {
      link.addEventListener('click', e => {
        const href = link.getAttribute('href');
        if (href.length <= 1) return;
        const targetId = href.slice(1);
        const target   = document.getElementById(targetId);
        if (!target) return;
        e.preventDefault();
        scrollTo(targetId);
      });
    });
  }

  return { init, scrollTo };
})();


/* ══════════════════════════════════════════
   5. SCROLL ANIMATIONS — IntersectionObserver
══════════════════════════════════════════ */
const ScrollAnimations = (() => {
  function init() {
    if (!('IntersectionObserver' in window)) {
      // Fallback: make all visible immediately
      document.querySelectorAll('.animate-on-scroll').forEach(el => {
        el.classList.add('is-visible');
      });
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px',
    });

    document.querySelectorAll('.animate-on-scroll').forEach((el, i) => {
      // Stagger delay from animation-delay if set inline
      observer.observe(el);
    });
  }

  return { init };
})();


/* ══════════════════════════════════════════
   6. MODAL SYSTEM
══════════════════════════════════════════ */
const Modal = (() => {
  let previousFocus = null;

  function getFocusableElements(modal) {
    return Array.from(
      modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
    ).filter(el => !el.disabled && !el.hidden);
  }

  function trapFocus(modal, e) {
    if (e.key !== 'Tab') return;
    const focusable = getFocusableElements(modal);
    if (focusable.length === 0) return;
    const first = focusable[0];
    const last  = focusable[focusable.length - 1];

    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault();
        last.focus();
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  }

  function open(modalId, presetLevel) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    previousFocus = document.activeElement;

    modal.classList.remove('hidden');
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    // Preset level if provided
    if (presetLevel && modalId === 'register-modal') {
      const levelMap = {
        'ربع القرآن':  'quarter',
        'نصف القرآن': 'half',
        'القرآن كاملاً': 'full',
      };
      const select = document.getElementById('reg-level');
      if (select && levelMap[presetLevel]) {
        select.value = levelMap[presetLevel];
      }
    }

    // Focus first focusable element
    const focusable = getFocusableElements(modal);
    if (focusable.length > 0) {
      setTimeout(() => focusable[0].focus(), 50);
    }

    // Keyboard handler
    modal._trapFn = e => trapFocus(modal, e);
    document.addEventListener('keydown', modal._trapFn);

    // Escape to close
    modal._escapeFn = e => {
      if (e.key === 'Escape') close(modalId);
    };
    document.addEventListener('keydown', modal._escapeFn);
  }

  function close(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    modal.classList.add('hidden');
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';

    // Remove listeners
    if (modal._trapFn)   document.removeEventListener('keydown', modal._trapFn);
    if (modal._escapeFn) document.removeEventListener('keydown', modal._escapeFn);

    // Return focus
    if (previousFocus) {
      previousFocus.focus();
      previousFocus = null;
    }
  }

  function init() {
    // Close buttons
    document.getElementById('modal-close')?.addEventListener('click', () => close('register-modal'));
    document.getElementById('about-modal-close')?.addEventListener('click', () => close('about-modal'));

    // Close on backdrop click
    ['register-modal', 'about-modal'].forEach(id => {
      const modal = document.getElementById(id);
      if (!modal) return;
      modal.addEventListener('click', e => {
        if (e.target === modal) close(id);
      });
    });
  }

  return { init, open, close };
})();


/* ══════════════════════════════════════════
   7. REGISTRATION FORM — validation & submit
══════════════════════════════════════════ */
const RegisterForm = (() => {
  const RULES = {
    'reg-name': {
      required: true,
      minLength: 3,
      label: 'الاسم الكامل',
      messages: {
        required:  'الاسم الكامل مطلوب',
        minLength: 'الاسم يجب أن يكون على الأقل ٣ أحرف',
      }
    },
    'reg-email': {
      required: true,
      email: true,
      label: 'البريد الإلكتروني',
      messages: {
        required: 'البريد الإلكتروني مطلوب',
        email:    'صيغة البريد الإلكتروني غير صحيحة',
      }
    },
    'reg-phone': {
      required: true,
      phone: true,
      label: 'رقم الجوال',
      messages: {
        required: 'رقم الجوال مطلوب',
        phone:    'رقم الجوال غير صحيح',
      }
    },
    'reg-age': {
      required: true,
      min: 5,
      max: 80,
      label: 'العمر',
      messages: {
        required: 'العمر مطلوب',
        min:      'الحد الأدنى للعمر هو ٥ سنوات',
        max:      'الحد الأقصى للعمر هو ٨٠ سنة',
      }
    },
    'reg-level': {
      required: true,
      label: 'مستوى المشاركة',
      messages: {
        required: 'يرجى اختيار مستوى المشاركة',
      }
    },
    'reg-country': {
      required: true,
      minLength: 2,
      label: 'الدولة',
      messages: {
        required:  'اسم الدولة مطلوب',
        minLength: 'أدخل اسم الدولة كاملاً',
      }
    },
  };

  function validateField(fieldId) {
    const field   = document.getElementById(fieldId);
    const errorEl = document.getElementById(`${fieldId}-error`);
    if (!field || !errorEl) return true;

    const rule  = RULES[fieldId];
    const value = field.value.trim();
    let   error = '';

    if (rule.required && !value) {
      error = rule.messages.required;
    } else if (value && rule.minLength && value.length < rule.minLength) {
      error = rule.messages.minLength;
    } else if (value && rule.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
      error = rule.messages.email;
    } else if (value && rule.phone && !/^[+]?[\d\s\-()]{7,15}$/.test(value)) {
      error = rule.messages.phone;
    } else if (value && rule.min !== undefined && Number(value) < rule.min) {
      error = rule.messages.min;
    } else if (value && rule.max !== undefined && Number(value) > rule.max) {
      error = rule.messages.max;
    }

    if (error) {
      field.classList.add('is-invalid');
      errorEl.textContent = error;
      errorEl.classList.remove('hidden');
      field.setAttribute('aria-invalid', 'true');
      return false;
    } else {
      field.classList.remove('is-invalid');
      errorEl.textContent = '';
      errorEl.classList.add('hidden');
      field.setAttribute('aria-invalid', 'false');
      return true;
    }
  }

  function validateTerms() {
    const checkbox = document.getElementById('reg-terms');
    const errorEl  = document.getElementById('reg-terms-error');
    if (!checkbox.checked) {
      errorEl.textContent = 'يجب الموافقة على الشروط والأحكام';
      errorEl.classList.remove('hidden');
      return false;
    }
    errorEl.classList.add('hidden');
    return true;
  }

  function validateAll() {
    const fieldResults = Object.keys(RULES).map(id => validateField(id));
    const termsResult  = validateTerms();
    return fieldResults.every(Boolean) && termsResult;
  }

  function setLoading(isLoading) {
    const btn     = document.getElementById('form-submit-btn');
    const label   = btn.querySelector('.btn-label');
    const spinner = btn.querySelector('.btn-spinner');

    if (isLoading) {
      btn.disabled = true;
      label.classList.add('hidden');
      spinner.classList.remove('hidden');
    } else {
      btn.disabled = false;
      label.classList.remove('hidden');
      spinner.classList.add('hidden');
    }
  }

  function resetForm() {
    const form = document.getElementById('register-form');
    if (!form) return;
    form.reset();

    // Clear all errors
    Object.keys(RULES).forEach(id => {
      const field   = document.getElementById(id);
      const errorEl = document.getElementById(`${id}-error`);
      if (field) {
        field.classList.remove('is-invalid');
        field.removeAttribute('aria-invalid');
      }
      if (errorEl) { errorEl.textContent = ''; errorEl.classList.add('hidden'); }
    });

    const termsError = document.getElementById('reg-terms-error');
    if (termsError) { termsError.textContent = ''; termsError.classList.add('hidden'); }
  }

  async function handleSubmit(e) {
    e.preventDefault();

    if (!validateAll()) {
      // Focus first invalid field
      const firstInvalid = document.querySelector('.form-input.is-invalid');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    setLoading(true);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1800));

    setLoading(false);
    Modal.close('register-modal');
    resetForm();

    Toast.show({
      type:    'success',
      title:   'تم التسجيل بنجاح! 🎉',
      message: 'سيتم التواصل معك عبر البريد الإلكتروني خلال ٢٤ ساعة.',
    });
  }

  function init() {
    const form = document.getElementById('register-form');
    if (!form) return;

    form.addEventListener('submit', handleSubmit);

    // Live validation on blur
    Object.keys(RULES).forEach(id => {
      const field = document.getElementById(id);
      if (field) {
        field.addEventListener('blur', () => validateField(id));
        // Clear error on input
        field.addEventListener('input', () => {
          if (field.classList.contains('is-invalid')) validateField(id);
        });
      }
    });

    // Terms live check
    const termsChk = document.getElementById('reg-terms');
    if (termsChk) {
      termsChk.addEventListener('change', () => {
        if (termsChk.checked) {
          const err = document.getElementById('reg-terms-error');
          if (err) err.classList.add('hidden');
        }
      });
    }
  }

  return { init, resetForm };
})();


/* ══════════════════════════════════════════
   8. TOAST NOTIFICATIONS
══════════════════════════════════════════ */
const Toast = (() => {
  const container = document.getElementById('toast-container');

  const ICONS = {
    success: 'check_circle',
    error:   'error',
    info:    'info',
  };

  function show({ type = 'info', title = '', message = '', duration = 5000 }) {
    if (!container) return;

    const toast = document.createElement('div');
    toast.className    = `toast toast--${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');

    toast.innerHTML = `
      <div class="toast-icon">
        <span class="material-symbols-outlined text-base">${ICONS[type] || ICONS.info}</span>
      </div>
      <div class="flex-1 min-w-0">
        ${title   ? `<p class="toast-title">${title}</p>`   : ''}
        ${message ? `<p class="toast-message">${message}</p>` : ''}
      </div>
      <button class="toast-dismiss" aria-label="إغلاق الإشعار">
        <span class="material-symbols-outlined text-sm">close</span>
      </button>
    `;

    const dismissBtn = toast.querySelector('.toast-dismiss');
    dismissBtn.addEventListener('click', () => dismiss(toast));

    container.appendChild(toast);

    // Auto-dismiss
    if (duration > 0) {
      setTimeout(() => dismiss(toast), duration);
    }

    return toast;
  }

  function dismiss(toast) {
    if (!toast || toast.classList.contains('leaving')) return;
    toast.classList.add('leaving');
    toast.addEventListener('animationend', () => toast.remove(), { once: true });
    // Fallback remove
    setTimeout(() => toast.remove(), 400);
  }

  return { show, dismiss };
})();


/* ══════════════════════════════════════════
   9. BUTTON WIRING — connect all CTAs
══════════════════════════════════════════ */
const Buttons = (() => {
  function openRegisterModal(presetLevel) {
    Dropdowns.closeAll();
    MobileMenu.close();
    Modal.open('register-modal', presetLevel);
  }

  function openAboutModal() {
    Dropdowns.closeAll();
    Modal.open('about-modal');
  }

  function init() {
    // ── Hero ──
    document.getElementById('hero-register-btn')?.addEventListener('click', () => openRegisterModal());
    document.getElementById('hero-about-btn')?.addEventListener('click', () => {
      SmoothScroll.scrollTo('about');
    });

    // ── Navbar ──
    document.getElementById('nav-register-btn')?.addEventListener('click', () => openRegisterModal());
    document.getElementById('mobile-register-btn')?.addEventListener('click', () => openRegisterModal());

    // ── Level cards ──
    document.querySelectorAll('.level-register-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const level = btn.dataset.level;
        openRegisterModal(level);
      });
    });

    // ── CTA section ──
    document.getElementById('cta-register-btn')?.addEventListener('click', () => openRegisterModal());
    document.getElementById('cta-guide-btn')?.addEventListener('click', () => DownloadGuide.trigger());
  }

  return { init };
})();


/* ══════════════════════════════════════════
   10. DOWNLOAD GUIDE — mock handler
══════════════════════════════════════════ */
const DownloadGuide = (() => {
  function trigger() {
    const btn = document.getElementById('cta-guide-btn');
    if (!btn) return;

    // Show loading state
    const originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `
      <span class="material-symbols-outlined animate-spin text-base">autorenew</span>
      جارٍ التحضير…
    `;

    setTimeout(() => {
      btn.disabled = false;
      btn.innerHTML = originalHTML;

      Toast.show({
        type:    'info',
        title:   'الدليل التعريفي',
        message: 'سيكون الدليل متاحاً للتحميل قريباً. يمكنك التسجيل للحصول على إشعار.',
        duration: 6000,
      });
    }, 1600);
  }

  return { trigger };
})();


/* ══════════════════════════════════════════
   INIT — Bootstrap all modules
══════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  Navbar.init();
  MobileMenu.init();
  Dropdowns.init();
  SmoothScroll.init();
  ScrollAnimations.init();
  Modal.init();
  RegisterForm.init();
  Buttons.init();

  // Welcome toast (delayed slightly for UX)
  setTimeout(() => {
    Toast.show({
      type:    'info',
      title:   'مرحباً بك في أهل القرآن',
      message: 'التسجيل مفتوح الآن للموسم الرابع ١٤٤٥ هـ',
      duration: 6000,
    });
  }, 2500);
});
