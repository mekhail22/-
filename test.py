import streamlit as st
import pandas as pd
from datetime import datetime
import random

# إعدادات الصفحة
st.set_page_config(
    page_title="مدرسة السلام - كريسماس 2024",
    page_icon="🎄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحميل CSS مخصص
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1a5c48 0%, #0a3d2f 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .school-name {
        font-size: 3rem;
        color: #ffd700;
        margin-bottom: 0.5rem;
    }
    
    .department {
        font-size: 2rem;
        color: #fff;
    }
    
    .christmas-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-right: 5px solid #dc3545;
    }
    
    .student-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-right: 4px solid #28a745;
    }
    
    .countdown-box {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .gallery-item {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    
    .gallery-item:hover {
        transform: translateY(-5px);
    }
</style>
""", unsafe_allow_html=True)

# بيانات المدرسة
school_data = {
    "name": "مدرسة السلام الإعدادية الثانوية",
    "department": "قسم ابتدائي",
    "principal": "أ/ محمد أحمد",
    "address": "شارع النصر، منطقة السلام",
    "phone": "01234567890",
    "email": "info@alsalam-school.edu.eg",
    "students_count": 450,
    "teachers_count": 25
}

# بيانات الطلاب والأعمال
students_artworks = [
    {"name": "يوسف أحمد", "grade": "الصف الأول", "artwork": "رسم شجرة كريسماس", "color": "🎨"},
    {"name": "مريم خالد", "grade": "الصف الثاني", "artwork": "بطاقة معايدة", "color": "✉️"},
    {"name": "عمر سعيد", "grade": "الصف الثالث", "artwork": "مجسم نجمة", "color": "⭐"},
    {"name": "سارة محمود", "grade": "الصف الرابع", "artwork": "زينة ورقية", "color": "🎀"},
    {"name": "خالد وائل", "grade": "الصف الخامس", "artwork": "رسم العائلة", "color": "👨‍👩‍👧‍👦"},
    {"name": "فاطمة حسن", "grade": "الصف السادس", "artwork": "كروت معايدة", "color": "🎁"}
]

# بيانات الفعاليات
events = [
    {"date": "2024-12-20", "title": "معرض الفنون", "time": "10:00 ص"},
    {"date": "2024-12-22", "title": "حفل توزيع الهدايا", "time": "11:00 ص"},
    {"date": "2024-12-23", "title": "ورشة عمل الزينة", "time": "9:00 ص"},
    {"date": "2024-12-24", "title": "الحفل الختامي", "time": "12:00 م"}
]

# الواجهة الرئيسية
def main():
    # شريط جانبي
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/197/197558.png", width=100)
        st.title("القائمة الرئيسية")
        
        menu = st.radio(
            "اختر قسم:",
            ["🏠 الصفحة الرئيسية", "🎨 معرض الأعمال", "📅 الفعاليات", "👥 عن المدرسة", "✉️ معايدة خاصة"]
        )
        
        st.markdown("---")
        st.markdown("### عدّاد الكريسماس")
        christmas_date = datetime(2024, 12, 25)
        current_date = datetime.now()
        days_left = (christmas_date - current_date).days
        st.markdown(f"""
        <div class='countdown-box'>
            <h3>🎄 {days_left} يوم</h3>
            <p>متبقي على عيد الميلاد</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("🎅 كل عام وأنتم بخير بمناسبة الكريسماس!")
    
    # المحتوى الرئيسي
    if menu == "🏠 الصفحة الرئيسية":
        show_homepage()
    elif menu == "🎨 معرض الأعمال":
        show_gallery()
    elif menu == "📅 الفعاليات":
        show_events()
    elif menu == "👥 عن المدرسة":
        show_about()
    elif menu == "✉️ معايدة خاصة":
        show_greeting_card()

def show_homepage():
    # الهيدر الرئيسي
    st.markdown(f"""
    <div class='main-header'>
        <h1 class='school-name'>{school_data['name']}</h1>
        <h2 class='department'>{school_data['department']}</h2>
        <h3>🎄 كل عام وأنتم بخير بمناسبة الكريسماس 🎄</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # أقسام رئيسية
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='christmas-card'>
            <h3>🎁 رسالة المدير</h3>
            <p>يسعدني أن أتقدم بأحر التهاني بمناسبة عيد الميلاد المجيد، 
            متمنياً لجميع الطلاب وأولياء الأمور عاماً مليئاً بالفرح والسلام.</p>
            <p><strong>مدير المدرسة</strong><br>{}</p>
        </div>
        """.format(school_data['principal']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='christmas-card'>
            <h3>✨ فعالياتنا</h3>
            <p>ننظم هذا الأسبوع العديد من الفعاليات والأنشطة الخاصة بالكريسماس، 
            بما في ذلك ورش عمل فنية ومعارض وحفل توزيع الهدايا.</p>
            <p>🎨 معرض الفنون<br>🎭 الحفل الختامي<br>🎁 توزيع الهدايا</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='christmas-card'>
            <h3>🏆 إنجازات الطلاب</h3>
            <p>طلابنا المبدعون قدموا أعمالاً رائعة تعبر عن روح الكريسماس 
            وقيم المحبة والسلام التي نحرص على غرسها فيهم.</p>
            <p>👦 450 طالب وطالبة<br>🎨 120 عمل فني<br>⭐ 25 جائزة تقديرية</p>
        </div>
        """, unsafe_allow_html=True)
    
    # قسم أعمال الطلاب
    st.markdown("## 🎨 إبداعات طلابنا")
    
    for student in students_artworks[:3]:
        with st.container():
            st.markdown(f"""
            <div class='student-card'>
                <h4>{student['color']} {student['name']} - {student['grade']}</h4>
                <p><strong>العمل الفني:</strong> {student['artwork']}</p>
            </div>
            """, unsafe_allow_html=True)

def show_gallery():
    st.title("🎨 معرض الأعمال الفنية")
    
    # فلترة حسب الصف
    grades = ["جميع الصفوف"] + list(set([s["grade"] for s in students_artworks]))
    selected_grade = st.selectbox("اختر الصف:", grades)
    
    # عرض الأعمال
    cols = st.columns(2)
    
    filtered_artworks = students_artworks
    if selected_grade != "جميع الصفوف":
        filtered_artworks = [s for s in students_artworks if s["grade"] == selected_grade]
    
    for idx, student in enumerate(filtered_artworks):
        with cols[idx % 2]:
            st.markdown(f"""
            <div class='gallery-item'>
                <div style='background: linear-gradient(135deg, #ff6b6b 0%, #4CAF50 100%); 
                padding: 2rem; text-align: center; color: white;'>
                    <h1 style='font-size: 4rem;'>{student['color']}</h1>
                </div>
                <div style='padding: 1rem; background: white;'>
                    <h4>{student['name']}</h4>
                    <p><strong>الصف:</strong> {student['grade']}</p>
                    <p><strong>العمل:</strong> {student['artwork']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_events():
    st.title("📅 فعاليات الكريسماس")
    
    # تقويم الفعاليات
    for event in events:
        with st.container():
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.markdown(f"### 📅")
                st.write(event["date"].split("-")[2])
            with col2:
                st.markdown(f"#### {event['title']}")
                st.write(f"⏰ {event['time']}")
            with col3:
                if st.button("تسجيل", key=event["title"]):
                    st.success(f"تم تسجيلك في {event['title']}")
    
    # نموذج تسجيل لفعالية جديدة
    st.markdown("---")
    st.subheader("🎯 سجل في فعالية جديدة")
    
    with st.form("event_registration"):
        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input("اسم الطالب")
            grade = st.selectbox("الصف", ["الصف الأول", "الصف الثاني", "الصف الثالث", 
                                         "الصف الرابع", "الصف الخامس", "الصف السادس"])
        with col2:
            parent_name = st.text_input("اسم ولي الأمر")
            phone = st.text_input("رقم الهاتف")
        
        selected_event = st.selectbox("الفعالية", [e["title"] for e in events])
        
        if st.form_submit_button("تسجيل"):
            st.success(f"تم تسجيل {student_name} في {selected_event} بنجاح!")

def show_about():
    st.title("🏫 عن مدرسة السلام")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style='background: white; padding: 2rem; border-radius: 15px; color: #333;'>
            <h3>معلومات المدرسة</h3>
            <p><strong>👨‍🏫 المدير:</strong> {school_data['principal']}</p>
            <p><strong>🏠 العنوان:</strong> {school_data['address']}</p>
            <p><strong>📞 الهاتف:</strong> {school_data['phone']}</p>
            <p><strong>✉️ الإيميل:</strong> {school_data['email']}</p>
            <p><strong>👥 عدد الطلاب:</strong> {school_data['students_count']}</p>
            <p><strong>👩‍🏫 عدد المعلمين:</strong> {school_data['teachers_count']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1a5c48 0%, #0a3d2f 100%); 
        padding: 2rem; border-radius: 15px; color: white;'>
            <h3>🎯 رؤيتنا</h3>
            <p>نطمح إلى تربية جيل مبدع يحمل قيم السلام والمحبة والتسامح، 
            ويساهم في بناء مجتمع أفضل.</p>
            <h3>🎄 رسالة الكريسماس</h3>
            <p>نؤمن بأن الأعياد فرصة لنشر المحبة والفرح بين جميع أفراد المجتمع، 
            بغض النظر عن الديانة أو الخلفية.</p>
        </div>
        """, unsafe_allow_html=True)

def show_greeting_card():
    st.title("✉️ صمم بطاقة معايدتك")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("اسم المرسل")
        to_name = st.text_input("اسم المستقبل")
        message = st.text_area("رسالتك", "كل عام وأنتم بخير بمناسبة الكريسماس!")
        
        card_style = st.selectbox("تصميم البطاقة", 
                                 ["كلاسيكي 🎄", "حديث ⭐", "ملون 🌈"])
        
        colors = {
            "كلاسيكي 🎄": ["#1a5c48", "#dc3545"],
            "حديث ⭐": ["#0a3d2f", "#ffd700"],
            "ملون 🌈": ["#ff6b6b", "#4CAF50"]
        }
    
    with col2:
        if name and to_name:
            selected_colors = colors[card_style]
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {selected_colors[0]} 0%, {selected_colors[1]} 100%);
            padding: 3rem; border-radius: 20px; color: white; text-align: center;'>
                <h2>🎄 بطاقة معايدة 🎄</h2>
                <h3>إلى: {to_name}</h3>
                <p style='font-size: 1.2rem; margin: 2rem 0;'>{message}</p>
                <h4>من: {name}</h4>
                <p style='margin-top: 2rem;'>مدرسة السلام الإعدادية الثانوية<br>قسم ابتدائي</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📥 حفظ البطاقة"):
                st.success("تم حفظ البطاقة بنجاح!")
                st.download_button(
                    label="📄 تحميل البطاقة",
                    data=f"""
                    بطاقة معايدة كريسماس
                    ===================
                    إلى: {to_name}
                    
                    {message}
                    
                    من: {name}
                    
                    مدرسة السلام الإعدادية الثانوية
                    قسم ابتدائي
                    """,
                    file_name="christmas_card.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()