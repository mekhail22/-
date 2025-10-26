import streamlit as st
from datetime import datetime, timedelta, timezone
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import pandas as pd

# 🔧 إعدادات Firebase و Telegram
PATH_TO_SERVICE_ACCOUNT = "attendance-streamlit-app-c3aa8-firebase-adminsdk-fbsvc-5ebf06ba1f.json"
TELEGRAM_BOT_TOKEN = "7517001841:AAFZZQM1hiprXxhPhK4GMfFwu-eP-DkOdMU"
TELEGRAM_CHAT_ID = "8108209758"

# 🔥 تهيئة Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(PATH_TO_SERVICE_ACCOUNT)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ✉️ إرسال إشعار لتليجرام
def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram error:", e)

# 💾 تسجيل الغياب في Firebase
def record_absence(student_name, teacher_name):
    egypt_time = datetime.now(timezone.utc) + timedelta(hours=2)
    date_str = egypt_time.strftime("%d/%m/%Y")  # يوم/شهر/سنة فقط
    
    doc = {
        "name": student_name.strip(),
        "class": "6/C",
        "status": "غايب",
        "teacher": teacher_name.strip(),
        "date": date_str,
    }
    db.collection("attendance").add(doc)

# 📊 إحضار جدول الغياب لطالب
def get_student_absences_table(student_name):
    query = db.collection("attendance").where("name", "==", student_name.strip()).stream()
    rows = []
    for d in query:
        data = d.to_dict()
        rows.append({
            "التاريخ": data.get("date", ""),
            "المدرس": data.get("teacher", "غير معروف"),
            "الحالة": data.get("status", "غايب"),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(by="التاريخ", ascending=False).reset_index(drop=True)
        df.index = df.index + 1  # يبدأ الترتيب من 1 بدل 0
        df.index.name = "م#"
    return df

# 🧾 إشعار المدرس
def notify_teacher_action(teacher_name, absent_students):
    egypt_time = datetime.now(timezone.utc) + timedelta(hours=2)
    date_str = egypt_time.strftime("%d/%m/%Y")

    msg = (
        f"📢 تقرير غياب جديد\n"
        f"👨‍🏫 المدرس: {teacher_name}\n"
        f"🏫 الفصل: 6/C\n"
        f"📅 التاريخ: {date_str}\n\n"
        f"🚫 الطلاب الغائبين:\n" + "\n".join([f"- {s}" for s in absent_students])
    )
    send_telegram_message(msg)

# 🌟 إعداد الصفحة
st.set_page_config(page_title="نظام غياب الفصل", layout="centered")

# 📌 الصفحة الرئيسية
st.title("📘 نظام غياب الفصل")
page = st.radio("اختار نوع الدخول:", ["-- اختر --", "👨‍🎓 طالب", "👨‍🏫 مدرس"])

# 👨‍🎓 واجهة الطالب
if page == "👨‍🎓 طالب":
    st.header("🔍 البحث عن الغياب")
    student_name = st.text_input("اكتب اسمك الثلاثي:")
    if student_name:
        df = get_student_absences_table(student_name)
        if df.empty:
            st.info("✅ لا يوجد غياب مسجل لهذا الطالب.")
        else:
            st.success(f"📋 الطالب {student_name} غاب {len(df)} مرات.")
            st.dataframe(df, use_container_width=True)

# 👨‍🏫 واجهة المدرس
elif page == "👨‍🏫 مدرس":
    st.header("🧑‍🏫 تسجيل غياب الطلاب")

    teachers = ["مينا سمير", "فادي حبيب"]
    students = [
        "ميخائيل صابر فوزي",
        "مينا ريمون خيري",
        "توني هاني نصرالله",
        "يوسف شادي كمال",
        "ادم مايكل فوزي",
        "مارك نادر فؤاد",
        "بيشوي عاطف فايز",
        "جورج مينا نجيب",
        "كيرلس فادي صادق",
        "يوستينا مجدي فادي",
    ]

    teacher_name = st.selectbox("اختار اسمك:", teachers)
    st.markdown("### ✅ علم على الطلاب الغايبين:")

    absent_students = []
    cols = st.columns(2)
    for i, student in enumerate(students):
        with cols[i % 2]:
            if st.checkbox(student):
                absent_students.append(student)

    if st.button("📋 تسجيل الغياب"):
        if not absent_students:
            st.warning("من فضلك علم على الطلاب الغايبين قبل التسجيل.")
        else:
            for s in absent_students:
                record_absence(s, teacher_name)
            notify_teacher_action(teacher_name, absent_students)
            st.success(f"✅ تم تسجيل غياب {len(absent_students)} طالب وإرسال إشعار لتليجرام.")
