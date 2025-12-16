import streamlit as st
import time
from datetime import datetime

# إعدادات الصفحة
st.set_page_config(
    page_title="🎄 معايدة كريسماس متحركة",
    page_icon="🎅",
    layout="centered"
)

# CSS مخصص + JavaScript للأنيميشن
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    .main-container {
        font-family: 'Cairo', sans-serif;
    }
    
    .christmas-box {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 25px;
        padding: 40px;
        margin: 30px auto;
        max-width: 800px;
        box-shadow: 
            0 20px 60px rgba(220, 53, 69, 0.3),
            0 0 0 10px #dc3545,
            0 0 0 15px #ffd700;
        position: relative;
        overflow: hidden;
        border: 5px solid #1a5c48;
        text-align: center;
        min-height: 400px;
    }
    
    /* زينة الزوايا */
    .corner {
        position: absolute;
        width: 60px;
        height: 60px;
        font-size: 40px;
        opacity: 0.7;
    }
    
    .top-left { top: 10px; left: 10px; }
    .top-right { top: 10px; right: 10px; }
    .bottom-left { bottom: 10px; left: 10px; }
    .bottom-right { bottom: 10px; right: 10px; }
    
    /* نص الأنيميشن */
    .animated-text {
        font-size: 2.2rem;
        line-height: 1.8;
        color: #0a3d2f;
        margin: 30px 0;
        min-height: 200px;
        text-align: center;
        direction: rtl;
        padding: 20px;
    }
    
    .cursor {
        display: inline-block;
        width: 3px;
        background-color: #dc3545;
        animation: blink 1s infinite;
        margin-right: 5px;
        height: 2.5rem;
        vertical-align: middle;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    /* ندفة ثلج */
    .snowflake {
        position: absolute;
        color: #4dabf7;
        font-size: 24px;
        opacity: 0;
        animation: fall linear infinite;
    }
    
    @keyframes fall {
        to {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    /* الأزرار */
    .stButton > button {
        background: linear-gradient(45deg, #dc3545, #c82333);
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 1.2rem;
        border-radius: 50px;
        font-family: 'Cairo', sans-serif;
        transition: all 0.3s;
        box-shadow: 0 5px 15px rgba(220, 53, 69, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(220, 53, 69, 0.6);
    }
    
    /* العنوان */
    .header-title {
        text-align: center;
        color: #dc3545;
        font-size: 2.8rem;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .school-name {
        text-align: center;
        color: #1a5c48;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 30px;
    }
    
    /* تأثيرات إضافية */
    .sparkle {
        position: absolute;
        width: 20px;
        height: 20px;
        background: gold;
        border-radius: 50%;
        animation: sparkle 2s infinite;
    }
    
    @keyframes sparkle {
        0%, 100% { transform: scale(1); opacity: 0.7; }
        50% { transform: scale(1.5); opacity: 1; }
    }
</style>

<script>
// دالة لإنشاء ندف الثلج
function createSnowflakes() {
    const container = document.querySelector('.christmas-box');
    for (let i = 0; i < 15; i++) {
        const snowflake = document.createElement('div');
        snowflake.classList.add('snowflake');
        snowflake.innerHTML = '❄';
        snowflake.style.left = Math.random() * 100 + '%';
        snowflake.style.animationDuration = (Math.random() * 3 + 2) + 's';
        snowflake.style.animationDelay = Math.random() * 5 + 's';
        container.appendChild(snowflake);
    }
}

// دالة لإنشاء الومضات الذهبية
function createSparkles() {
    const container = document.querySelector('.christmas-box');
    for (let i = 0; i < 10; i++) {
        const sparkle = document.createElement('div');
        sparkle.classList.add('sparkle');
        sparkle.style.left = Math.random() * 100 + '%';
        sparkle.style.top = Math.random() * 100 + '%';
        sparkle.style.animationDelay = Math.random() * 2 + 's';
        container.appendChild(sparkle);
    }
}

// دالة الأنيميشن النصية
function typeWriter(text, elementId, speed = 50) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.innerHTML = '';
    let i = 0;
    
    function type() {
        if (i < text.length) {
            // إضافة حرف مع تأثير
            const char = text.charAt(i);
            const span = document.createElement('span');
            span.textContent = char;
            
            // تأثير للأحرف الجديدة
            span.style.opacity = '0';
            span.style.transform = 'translateY(10px)';
            span.style.display = 'inline-block';
            span.style.transition = 'all 0.1s';
            
            element.appendChild(span);
            
            // تأثير ظهور الحرف
            setTimeout(() => {
                span.style.opacity = '1';
                span.style.transform = 'translateY(0)';
            }, 10);
            
            i++;
            setTimeout(type, speed);
        } else {
            // إضافة المؤشر الوامض بعد الانتهاء
            const cursor = document.createElement('span');
            cursor.classList.add('cursor');
            element.appendChild(cursor);
        }
    }
    
    // بدء الأنيميشن بعد فترة قصيرة
    setTimeout(type, 500);
}

// بدء التأثيرات عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    createSnowflakes();
    createSparkles();
    
    // البدء في كتابة الرسالة الأولى تلقائياً
    setTimeout(() => {
        typeWriter(
            "كل عام وأنتم بخير بمناسبة عيد الميلاد المجيد 🎄",
            "animatedMessage",
            60
        );
    }, 1000);
});

// دالة لإعادة التشغيل
function restartAnimation() {
    const element = document.getElementById('animatedMessage');
    if (element) {
        // إخفاء النص القديم
        element.style.opacity = '0';
        
        // البدء من جديد بعد فترة قصيرة
        setTimeout(() => {
            element.style.opacity = '1';
            const texts = [
                "كل عام وأنتم بخير بمناسبة عيد الميلاد المجيد 🎄",
                "نتمنى لكم سنة جديدة مليئة بالفرح والسلام ❤️",
                "من طلاب ومعلمي مدرسة السلام الإعدادية 🏫",
                "عيد ميلاد سعيد ومبارك للجميع ✨",
                "🎅🎄🎁 بركة العيد تعم على الجميع 🎁🎄🎅"
            ];
            const randomText = texts[Math.floor(Math.random() * texts.length)];
            typeWriter(randomText, "animatedMessage", 60);
        }, 300);
    }
}
</script>
""", unsafe_allow_html=True)

# HTML للصندوق والأنيميشن
st.markdown("""
<div class="main-container">
    <h1 class="header-title">🎄 معايدة كريسماس 🎄</h1>
    <div class="school-name">مدرسة السلام الإعدادية الثانوية - قسم ابتدائي</div>
    
    <div class="christmas-box">
        <!-- زينة الزوايا -->
        <div class="corner top-left">🎄</div>
        <div class="corner top-right">⭐</div>
        <div class="corner bottom-left">🎁</div>
        <div class="corner bottom-right">🔔</div>
        
        <!-- الرسالة المتحركة -->
        <div id="animatedMessage" class="animated-text"></div>
        
        <!-- نص تهنئة ثابت -->
        <div style="margin-top: 20px; padding: 20px; background: rgba(26, 92, 72, 0.1); border-radius: 15px;">
            <p style="font-size: 1.3rem; color: #0a3d2f; margin-bottom: 10px;">
                <strong>🎅 رسالة خاصة:</strong>
            </p>
            <p style="font-size: 1.1rem; color: #555; line-height: 1.6;">
                يسرنا أن نتقدم بأحر التهاني والتبريكات بمناسبة عيد الميلاد المجيد، 
                متمنين لجميع الطلاب وأولياء الأمور والمعلمين سنة جديدة مليئة بالفرح 
                والبركة والسلام. كل عام وأنتم بخير.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# أزرار التحكم
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 إعادة تشغيل الأنيميشن"):
        st.markdown("""
        <script>
            restartAnimation();
        </script>
        """, unsafe_allow_html=True)
        st.success("تم إعادة تشغيل الأنيميشن!")

with col2:
    if st.button("🎵 تشغيل الموسيقى"):
        # إضافة موسيقى خلفية
        st.markdown("""
        <audio autoplay loop>
            <source src="https://assets.mixkit.co/music/preview/mixkit-jingle-bells-311.mp3" type="audio/mpeg">
        </audio>
        <script>
            document.querySelector('audio').volume = 0.3;
        </script>
        """, unsafe_allow_html=True)
        st.info("🎶 تشغيل موسيقى الكريسماس...")

with col3:
    if st.button("📤 مشاركة المعايدة"):
        st.markdown("""
        <script>
            // محاكاة نسخ الرسالة
            const message = "🎄 معايدة كريسماس من مدرسة السلام 🎄\\nكل عام وأنتم بخير!\\nwww.alsalam-school.edu.eg";
            navigator.clipboard.writeText(message);
            alert('تم نسخ المعايدة! يمكنك مشاركتها الآن.');
        </script>
        """, unsafe_allow_html=True)
        st.success("تم نسخ المعايدة للحافظة!")

# قسم إضافي للتهاني المخصصة
st.markdown("---")
st.subheader("✍️ اكتب معايدتك المخصصة")

user_message = st.text_area(
    "اكتب رسالة التهنئة:",
    "كل عام وأنتم بخير بمناسبة الكريسماس! 🎄",
    height=100
)

if st.button("✨ عرض معايدتي"):
    st.markdown(f"""
    <div style="background: linear-gradient(45deg, #ffd700, #ffed4e); 
                padding: 25px; border-radius: 15px; margin: 20px 0; 
                border: 3px solid #dc3545;">
        <h3 style="color: #0a3d2f; text-align: center;">معايدتك الشخصية ✨</h3>
        <p style="font-size: 1.4rem; text-align: center; color: #333; 
                   padding: 15px; direction: rtl;">
            {user_message}
        </p>
        <p style="text-align: left; color: #666; font-size: 0.9rem;">
            من: مدرسة السلام الإعدادية الثانوية
        </p>
    </div>
    """, unsafe_allow_html=True)

# معلومات المدرسة
with st.expander("🏫 معلومات المدرسة"):
    st.markdown("""
    ### مدرسة السلام الإعدادية الثانوية
    **القسم:** الابتدائي  
    **العنوان:** شارع النصر، منطقة السلام  
    **الهاتف:** 01234567890  
    **البريد الإلكتروني:** info@alsalam-school.edu.eg  
    
    ---
    
    ### 🎄 فعاليات الكريسماس
    1. معرض الأعمال الفنية: 20 ديسمبر
    2. حفل توزيع الهدايا: 22 ديسمبر
    3. ورشة صناعة الزينة: 23 ديسمبر
    4. الحفل الختامي: 24 ديسمبر
    """)

# JavaScript إضافي لتأثيرات تفاعلية
st.markdown("""
<script>
// إضافة تأثير عند النقر على الصندوق
document.querySelector('.christmas-box').addEventListener('click', function() {
    this.style.transform = 'scale(0.98)';
    setTimeout(() => {
        this.style.transform = 'scale(1)';
    }, 150);
    
    // إضافة قلب عند النقر
    const heart = document.createElement('div');
    heart.innerHTML = '❤️';
    heart.style.position = 'absolute';
    heart.style.fontSize = '30px';
    heart.style.left = (Math.random() * 80 + 10) + '%';
    heart.style.top = (Math.random() * 80 + 10) + '%';
    heart.style.animation = 'floatUp 2s ease-out forwards';
    this.appendChild(heart);
    
    setTimeout(() => heart.remove(), 2000);
});

// تأثير الطفو للقلوب
const style = document.createElement('style');
style.textContent = `
@keyframes floatUp {
    0% { transform: translateY(0) scale(1); opacity: 1; }
    100% { transform: translateY(-100px) scale(0.5); opacity: 0; }
}
`;
document.head.appendChild(style);
</script>
""", unsafe_allow_html=True)
