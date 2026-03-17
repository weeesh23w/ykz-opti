const translations = {
    es: {
        page_title: "YKZ Premium Optimizer | Elite Performance Suite",
        why_title: "¿Por qué YKZ Optimizer?",
        why_desc: "Diseñado con una interfaz intuitiva y potente, YKZ Optimizer combina años de experiencia en tuning de Windows en una sola suite. No solo limpia, sino que recalibra tu sistema para obtener la máxima estabilidad y fluidez posible.",
        why_item1: "Actualizaciones constantes",
        why_item2: "Comunidad activa",
        why_item3: "Compatible con Windows 10 & 11",
        hero_title: "YKZ Premium Optimizer",
        hero_desc: "YKZ Optimizer es la herramienta definitiva para maximizar el rendimiento de tu sistema, reducir la latencia y desbloquear todo el potencial de tu hardware.",
        features_title: "Características Principales",
        feat1_title: "Optimización Gamers",
        feat1_desc: "Configuraciones extremas para Valorant, CS2 y FiveM. Prioridad de CPU y limpieza de caché automática.",
        feat2_title: "Control de GPU",
        feat2_desc: "NVIDIA & AMD Center. MSI Mode, limpieza de drivers y optimización de latencia DPC.",
        feat3_title: "Limpieza Profunda",
        feat3_desc: "Elimina archivos basura, temporales y optimiza el registro de Windows sin riesgos.",
        feat4_title: "Input Lag Extremo",
        feat4_desc: "FilterKeys Fix, USB Polling Rate y System Timer Resolution para la respuesta más rápida.",
        feat5_title: "Performance para Laptops",
        feat5_desc: "Perfiles específicos para portátiles, control de energía y mitigación de thermal throttling.",
        feat6_title: "Seguridad y Debloat",
        feat6_desc: "Elimina bloatware innecesario de Windows y crea puntos de restauración antes de cada cambio.",
        gallery_title: "Nuestra Interfaz",
        gallery_desc: "Capturas reales del optimizador en acción.",
        dl_title: "¿Listo para optimizar tu PC?",
        dl_desc: "Descarga la última versión de YKZ Premium Optimizer y siente la diferencia.",
        dl_btn: "Descargar",
        gal1_title: "Resumen del Sistema",
        gal1_desc: "Hardware & Componentes",
        gal2_title: "Game Boosters",
        gal2_desc: "Optimización Extrema",
        gal3_title: "Driver Center",
        gal3_desc: "Actualización Inteligente",
        footer_source: "Código Fuente"
    },
    en: {
        page_title: "YKZ Premium Optimizer | Elite Performance Suite",
        why_title: "Why YKZ Optimizer?",
        why_desc: "Designed with an intuitive and powerful interface, YKZ Optimizer combines years of Windows tuning experience into a single suite. It doesn't just clean; it recalibrates your system for maximum stability and fluidity.",
        why_item1: "Constant updates",
        why_item2: "Active community",
        why_item3: "Windows 10 & 11 compatible",
        hero_title: "YKZ Premium Optimizer",
        hero_desc: "YKZ Optimizer is the ultimate tool to maximize system performance, reduce latency, and unlock your hardware's full potential.",
        features_title: "Main Features",
        feat1_title: "Gaming Optimization",
        feat1_desc: "Extreme settings for Valorant, CS2, and FiveM. CPU priority and automatic cache cleaning.",
        feat2_title: "GPU Control",
        feat2_desc: "NVIDIA & AMD Center. MSI Mode, driver cleaning, and DPC latency optimization.",
        feat3_title: "Deep Cleaning",
        feat3_desc: "Removes junk files, temporary files, and optimizes Windows registry safely.",
        feat4_title: "Extreme Input Lag",
        feat4_desc: "FilterKeys Fix, USB Polling Rate, and System Timer Resolution for the fastest response.",
        feat5_title: "Laptop Performance",
        feat5_desc: "Specific laptop profiles, power control, and thermal throttling mitigation.",
        feat6_title: "Security & Debloat",
        feat6_desc: "Removes unnecessary Windows bloatware and creates restore points before every change.",
        gallery_title: "Our Interface",
        gallery_desc: "Real captures of the optimizer in action.",
        dl_title: "Ready to optimize your PC?",
        dl_desc: "Download the latest version of YKZ Premium Optimizer and feel the difference.",
        dl_btn: "Download",
        gal1_title: "System Overview",
        gal1_desc: "Hardware & Components",
        gal2_title: "Game Boosters",
        gal2_desc: "Extreme Optimization",
        gal3_title: "Driver Center",
        gal3_desc: "Smart Updates",
        footer_source: "Source Code"
    }
};

function setLanguage(lang) {
    localStorage.setItem('ykz_lang', lang);
    document.documentElement.lang = lang;
    document.getElementById('current-lang').textContent = lang.toUpperCase();

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
}

// Initialize i18n
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('ykz_lang') || 'es';
    setLanguage(savedLang);

    // Toggle dropdown
    const langBtn = document.getElementById('lang-btn');
    const dropdown = document.querySelector('.lang-dropdown');

    langBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('active');
    });

    document.addEventListener('click', () => {
        dropdown.classList.remove('active');
    });
});
