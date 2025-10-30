import streamlit as st
from datetime import datetime, timedelta, timezone
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import pandas as pd
import io
import json
import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ================== إعداد الصفحة ==================
st.set_page_config(page_title="📘 نظام الغياب", page_icon="📘", layout="centered")

# ================== تحميل الخط ==================
FONT_PATH = "NotoNaskhArabic-Regular.ttf"
if not os.path.exists(FONT_PATH):
    url = "https://github.com/googlefonts/noto-fonts/blob/main/hinted/ttf/NotoNaskhArabic/NotoNaskhArabic-Regular.ttf?raw=true"
    r = requests.get(url)
    with open(FONT_PATH, "wb") as f:
        f.write(r.content)
pdfmetrics.registerFont(TTFont('Arabic', FONT_PATH))

# ================== Firebase ==================
if not firebase_admin._apps:
    try:
        firebase_config = dict(st.secrets["google_service_account"])
        cred = credentials.Certificate(firebase_config)
    except Exception:
        with open("class-absence-firebase-adminsdk-fbsvc-308afd9b8f.json") as f:
            firebase_config = json.load(f)
        cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ================== إعدادات Telegram ==================
TELEGRAM_BOT_TOKEN = "7517001841:AAFZZQM1hiprXxhPhK4GMfFwu-eP-DkOdMU"
TELEGRAM_CHAT_ID = "8108209758"

# ================== دوال المساعدة ==================
def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

def reshape_arabic_text(text):
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def record_absences(absent_students, teacher_name):
    egypt_time = datetime.now(timezone.utc) + timedelta(hours=2)
    date_str = egypt_time.strftime("%d/%m/%Y")
    batch = db.batch()
    for student in students:
        status = "غايب" if student in absent_students else "حاضر"
        doc_ref = db.collection("attendance").document()
        doc = {"name": student, "class": "6/C", "status": status, "teacher": teacher_name, "date": date_str}
        batch.set(doc_ref, doc)
    batch.commit()
    send_telegram_message(f"📢 تقرير غياب جديد\n👨‍🏫 المدرس: {teacher_name}\n📅 {date_str}\n🚫 الغائبين:\n" + "\n".join(absent_students))
    st.success("✅ تم تسجيل الغياب بنجاح!")

def get_student_absences(name):
    docs = db.collection("attendance").where("name", "==", name).stream()
    rows = []
    for d in docs:
        data = d.to_dict()
        rows.append({
            "المرة": None,
            "الطالب": data["name"],
            "المدرس": data["teacher"],
            "التاريخ": data["date"],
            "الحالة": data["status"],
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("التاريخ").reset_index(drop=True)
        df["المرة"] = df.index + 1
        df = df[["المرة", "الطالب", "المدرس", "التاريخ", "الحالة"]]
    return df

# ================== دالة تصحيح التاريخ النهائي ==================
def format_date_for_pdf(date_str):
    try:
        if isinstance(date_str, datetime):
            return date_str.strftime("%d / %m / %Y")
        cleaned = str(date_str).replace(" ", "").replace("-", "").replace(".", "")
        if len(cleaned) == 8 and cleaned.isdigit():
            dt = datetime.strptime(cleaned, "%d%m%Y")
            return dt.strftime("%d / %m / %Y")
        elif "/" in cleaned:
            parts = cleaned.split("/")
            if len(parts) == 3:
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                dt = datetime(year, month, day)
                return dt.strftime("%d / %m / %Y")
        return str(date_str)
    except:
        return str(date_str)

# ================== دالة إنشاء PDF ==================
def generate_pdf(student_name, df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    style = ParagraphStyle(name='Arabic', fontName='Arabic', fontSize=12, alignment=2)
    title = ParagraphStyle(name='Title', fontName='Arabic', fontSize=16, alignment=1)

    elements.append(Paragraph(reshape_arabic_text("تقرير غياب الطالب"), title))
    elements.append(Spacer(1, 12))

    absences = df[df["الحالة"] == "غايب"].shape[0]
    presents = df[df["الحالة"] == "حاضر"].shape[0]

    elements.append(Paragraph(reshape_arabic_text(f"الاسم: {student_name}"), style))
    elements.append(Paragraph(reshape_arabic_text(f"عدد مرات الغياب: {absences}"), style))
    elements.append(Paragraph(reshape_arabic_text(f"عدد مرات الحضور: {presents}"), style))
    elements.append(Spacer(1, 12))

    pdf_data = df.copy()
    pdf_data["التاريخ"] = pdf_data["التاريخ"].apply(format_date_for_pdf)

    data = [["المرة", "الطالب", "المدرس", "التاريخ", "الحالة"]] + pdf_data.values.tolist()
    data = [[reshape_arabic_text(str(cell)) for cell in row] for row in data]

    table = Table(data, hAlign='CENTER')
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Arabic'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ================== بيانات الطلاب والمعلمين ==================
students = [
    "ميخائيل صابر فوزي", "مينا ريمون خيري", "توني هاني نصرالله",
    "يوسف شادي كمال", "ادم مايكل فوزي", "مارك نادر فؤاد",
    "بيشوي عاطف فايز", "جورج مينا نجيب", "كيرلس فادي صادق",
    "يوستينا مجدي فادي"
]
teachers = ["مينا سمير", "فادي حبيب"]

# ================== واجهة المستخدم ==================
if "page" not in st.session_state:
    st.session_state.page = "اختيار"

st.markdown("""
<style>
body { background: linear-gradient(135deg, #e0f2fe, #f8fafc); animation: fadeIn 1s ease-in-out; }
@keyframes fadeIn { from {opacity:0;} to {opacity:1;} }
h1,h2,h3,h4 { font-family: 'Cairo', sans-serif; color: #1e293b; text-align: center; }
.stButton>button { width: 250px; height: 60px; border-radius: 15px; background-color: #2563eb; color: white;
font-size: 22px; font-weight: bold; transition: 0.3s; }
.stButton>button:hover { background-color: #1d4ed8; transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# ======= صفحة الاختيار =======
if st.session_state.page == "اختيار":
    st.title("📘 نظام الغياب")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍🏫 مدرس"):
            st.session_state.page = "تسجيل دخول المدرس"
            st.rerun()
    with col2:
        if st.button("👨‍🎓 طالب"):
            st.session_state.page = "واجهة الطالب"
            st.rerun()

elif st.session_state.page == "تسجيل دخول المدرس":
    st.header("🔐 تسجيل دخول المدرس")
    teacher_name = st.selectbox("👨‍🏫 اختر اسمك:", teachers)
    password = st.text_input("🔑 كلمة السر:", type="password")
    if st.button("تسجيل الدخول"):
        if password == "1234":
            st.session_state.teacher_name = teacher_name
            st.session_state.page = "واجهة الغياب"
            st.rerun()
        else:
            st.error("❌ كلمة السر غير صحيحة")
    if st.button("رجوع"):
        st.session_state.page = "اختيار"
        st.rerun()

elif st.session_state.page == "واجهة الغياب":
    st.header("📋 تسجيل الغياب")
    teacher_name = st.session_state.teacher_name
    absent_students = []
    cols = st.columns(2)
    for i, s in enumerate(students):
        with cols[i % 2]:
            if st.checkbox(s, key=f"chk_{i}"):
                absent_students.append(s)
    if st.button("✅ تسجيل"):
        record_absences(absent_students, teacher_name)
    if st.button("رجوع", key="back_from_teacher"):
        st.session_state.page = "اختيار"
        st.rerun()

elif st.session_state.page == "واجهة الطالب":
    st.header("🔍 البحث عن الغياب")
    name = st.text_input("✏️ اكتب اسمك الثلاثي:")
    if name:
        df = get_student_absences(name)
        if df.empty:
            st.info("✅ لا يوجد غياب مسجل.")
        else:
            st.dataframe(df.set_index("المرة"), use_container_width=True)
            pdf = generate_pdf(name, df)
            st.download_button("📄 تحميل PDF", pdf, f"{name}_غياب.pdf", mime="application/pdf")
    if st.button("🔙 رجوع", key="back_from_student"):
        st.session_state.page = "اختيار"
        st.rerun()
