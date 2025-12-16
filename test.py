import streamlit as st

st.set_page_config(
    page_title="🎄 أنيميشن كريسماس",
    page_icon="⭐",
    layout="centered"
)

# أنيميشن JavaScript خالص داخل صندوق
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    body {
        background: linear-gradient(135deg, #0a3d2f 0%, #1a5c48 100%);
        margin: 0;
        padding: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }
    
    .animation-container {
        width: 100%;
        max-width: 700px;
        height: 500px;
        background: white;
        border-radius: 20px;
        overflow: hidden;
        position: relative;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        border: 8px solid #dc3545;
        font-family: 'Cairo', sans-serif;
    }
    
    #christmasMessage {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 2.8rem;
        color: #0a3d2f;
        text-align: center;
        width: 90%;
        line-height: 1.5;
        direction: rtl;
        opacity: 0;
    }
    
    .cursor {
        display: inline-block;
        width: 4px;
        height: 3.2rem;
        background: #dc3545;
        margin-right: 5px;
        vertical-align: middle;
        animation: blink 0.8s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    .decoration {
        position: absolute;
        font-size: 3rem;
        opacity: 0;
        animation: float 3s infinite ease-in-out;
    }
    
    @keyframes float {
        0%, 100% { 
            transform: translateY(0) rotate(0deg); 
            opacity: 0.7;
        }
        50% { 
            transform: translateY(-20px) rotate(10deg); 
            opacity: 1;
        }
    }
    
    .firework {
        position: absolute;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        animation: explode 1s forwards;
    }
    
    @keyframes explode {
        0% {
            transform: scale(1);
            opacity: 1;
        }
        100% {
            transform: scale(30);
            opacity: 0;
        }
    }
</style>

<div class="animation-container" id="container">
    <!-- العناصر المتحركة تضاف بالجافاسكريبت -->
</div>

<script>
// الرسالة الأساسية
const message = "كل عام وأنتم بخير 🎄";
const message2 = "عيد ميلاد مجيد ⭐";
const message3 = "من مدرسة السلام 🏫";

let currentMessage = "";
let charIndex = 0;
let messageType = 0;
const messages = [message, message2, message3];

const container = document.getElementById('container');
const messageElement = document.createElement('div');
messageElement.id = 'christmasMessage';
container.appendChild(messageElement);

// دالة الكتابة النصية
function typeWriter() {
    if (charIndex < currentMessage.length) {
        const char = currentMessage.charAt(charIndex);
        const span = document.createElement('span');
        span.textContent = char;
        span.style.display = 'inline-block';
        span.style.opacity = '0';
        span.style.transform = 'translateY(20px)';
        
        messageElement.appendChild(span);
        
        // تأثير ظهور الحرف
        setTimeout(() => {
            span.style.transition = 'all 0.3s ease';
            span.style.opacity = '1';
            span.style.transform = 'translateY(0)';
            
            // تأثير خاص للأيقونات
            if (char === '🎄' || char === '⭐' || char === '🏫') {
                createFirework(50, 50);
            }
        }, 50);
        
        charIndex++;
        setTimeout(typeWriter, 120);
    } else {
        // إضافة المؤشر الوامض
        const cursor = document.createElement('span');
        cursor.className = 'cursor';
        messageElement.appendChild(cursor);
        
        // الانتقال للرسالة التالية بعد فترة
        setTimeout(nextMessage, 2000);
    }
}

// الانتقال للرسالة التالية
function nextMessage() {
    // مسح الرسالة السابقة
    messageElement.innerHTML = '';
    messageElement.style.opacity = '0';
    
    // الانتقال للرسالة التالية
    messageType = (messageType + 1) % messages.length;
    currentMessage = messages[messageType];
    charIndex = 0;
    
    // ظهور الرسالة الجديدة
    setTimeout(() => {
        messageElement.style.transition = 'opacity 0.5s';
        messageElement.style.opacity = '1';
        typeWriter();
    }, 500);
}

// إنشاء الألعاب النارية
function createFirework(x, y) {
    const colors = ['#dc3545', '#ffd700', '#28a745', '#17a2b8'];
    
    for (let i = 0; i < 30; i++) {
        const firework = document.createElement('div');
        firework.className = 'firework';
        firework.style.left = x + '%';
        firework.style.top = y + '%';
        firework.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        // اتجاهات عشوائية
        const angle = Math.random() * Math.PI * 2;
        const distance = 20 + Math.random() * 30;
        const targetX = x + Math.cos(angle) * distance;
        const targetY = y + Math.sin(angle) * distance;
        
        firework.style.setProperty('--tx', targetX + '%');
        firework.style.setProperty('--ty', targetY + '%');
        
        firework.style.animation = `explode 0.8s forwards`;
        firework.style.animationDelay = (i * 0.02) + 's';
        
        container.appendChild(firework);
        
        // إزالة الألعاب النارية بعد الانتهاء
        setTimeout(() => {
            if (firework.parentNode) {
                firework.parentNode.removeChild(firework);
            }
        }, 1000);
    }
}

// إنشاء زينة عائمة
function createFloatingDecorations() {
    const decorations = ['🎄', '⭐', '🎁', '🔔', '🎅', '🤶'];
    const positions = [
        {top: 20, left: 15},
        {top: 30, left: 80},
        {top: 70, left: 20},
        {top: 80, left: 70},
        {top: 40, left: 40},
        {top: 60, left: 60}
    ];
    
    positions.forEach((pos, index) => {
        const deco = document.createElement('div');
        deco.className = 'decoration';
        deco.textContent = decorations[index];
        deco.style.top = pos.top + '%';
        deco.style.left = pos.left + '%';
        deco.style.animationDelay = (index * 0.5) + 's';
        deco.style.color = index % 2 === 0 ? '#dc3545' : '#28a745';
        container.appendChild(deco);
        
        // جعلها تظهر
        setTimeout(() => {
            deco.style.opacity = '0.7';
            deco.style.transition = 'opacity 1s';
        }, index * 200);
    });
}

// تأثير خلفية متحركة
function createBackgroundEffect() {
    const canvas = document.createElement('canvas');
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.zIndex = '-1';
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    const particles = [];
    const particleCount = 50;
    
    // إنشاء جسيمات
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 4 + 1,
            speed: Math.random() * 0.5 + 0.2,
            color: `rgba(${Math.random() * 100 + 155}, ${Math.random() * 100 + 155}, 255, 0.5)`,
            angle: Math.random() * Math.PI * 2
        });
    }
    
    // رسم الجسيمات
    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(p => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.fill();
            
            // حركة الجسيمات
            p.x += Math.cos(p.angle) * p.speed;
            p.y += Math.sin(p.angle) * p.speed;
            
            // ارتداد من الحواف
            if (p.x < 0 || p.x > canvas.width) p.angle = Math.PI - p.angle;
            if (p.y < 0 || p.y > canvas.height) p.angle = -p.angle;
            
            // إبقاء الجسيمات داخل الإطار
            p.x = Math.max(0, Math.min(canvas.width, p.x));
            p.y = Math.max(0, Math.min(canvas.height, p.y));
        });
        
        requestAnimationFrame(drawParticles);
    }
    
    drawParticles();
}

// بدء كل التأثيرات
window.onload = function() {
    // بدء بالرسالة الأولى
    currentMessage = messages[0];
    messageElement.style.opacity = '1';
    typeWriter();
    
    // إنشاء التأثيرات
    createFloatingDecorations();
    createBackgroundEffect();
    
    // إضافة بعض الألعاب النارية العشوائية
    setInterval(() => {
        if (Math.random() > 0.7) {
            createFirework(
                Math.random() * 80 + 10,
                Math.random() * 80 + 10
            );
        }
    }, 3000);
};

// جعل الحاوية متجاوبة مع التغيير في الحجم
window.addEventListener('resize', function() {
    const canvas = container.querySelector('canvas');
    if (canvas) {
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
    }
});
</script>
""", unsafe_allow_html=True)

# زر التحكم الوحيد
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 إعادة التشغيل"):
        st.markdown("""
        <script>
            // إعادة تعيين الرسالة
            messageType = -1;
            nextMessage();
            
            // إضافة ألعاب نارية احتفالية
            createFirework(50, 50);
            setTimeout(() => createFirework(30, 70), 300);
            setTimeout(() => createFirework(70, 30), 600);
        </script>
        """, unsafe_allow_html=True)

with col2:
    if st.button("🎆 عرض الألعاب النارية"):
        st.markdown("""
        <script>
            // عرض مجموعة من الألعاب النارية
            for(let i = 0; i < 5; i++) {
                setTimeout(() => {
                    createFirework(
                        Math.random() * 80 + 10,
                        Math.random() * 80 + 10
                    );
                }, i * 300);
            }
        </script>
        """, unsafe_allow_html=True)
