import streamlit as st
import requests

# تنظیمات تلگرام (توکن و چت آیدی خود را اینجا وارد کنید)
TELEGRAM_TOKEN = "8684668902:AAEB89rzQBfi133AkEGM_87jBMtbHfIcfI4"
CHAT_ID = "98904984"

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=data)
    except:
        pass

st.set_page_config(page_title="قرار ما", layout="centered")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0b132b; }
    .stApp { background-color: #0b132b; }
    
    div, h1, h2, p { 
        text-align: center !important; 
        font-family: Tahoma, sans-serif !important;
    }
    
    .stButton>button { 
        margin: 10px auto; 
        display: block; 
        width: fit-content;
        padding: 10px 30px;
        border-radius: 12px;
        background-color: #2563eb;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state: 
    st.session_state.step = 1

# ذخیره موقت پاسخ‌ها در طول مراحل
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# سوال اول
if st.session_state.step == 1:
    st.markdown("## عایا همچنان دعوت پا برجاست؟")
    if st.button("بله"):
        st.session_state.answers["دعوت"] = "بله"
        st.session_state.step = 2
        st.rerun()
    if st.button("خیر"):
        st.session_state.answers["دعوت"] = "خیر"
        send_to_telegram("کاربر به سوال اول پاسخ داد: خیر (تعارف!)")
        st.error("دیدی گفتم داری تعارف می‌کنی!")

# سوال دوم (دکمه فراری فیلم)
elif st.session_state.step == 2:
    st.markdown("## امشب با هم فیلم ببینیم؟")
    
    import streamlit.components.v1 as components
    html_code = """
    <div style="display: flex; justify-content: center; align-items: center; gap: 40px; height: 120px; position: relative;" dir="rtl">
        <button id="no" style="padding: 12px 30px; background: #ef4444; color: white; border: none; border-radius: 12px; cursor: pointer; font-family: Tahoma; font-size: 16px; font-weight: bold; position: absolute;">خیر 🙈</button>
    </div>
    <p id="msg" style="color: white; font-family: Tahoma; font-size: 16px; font-weight: bold; margin-top: 10px;"></p>
    <script>
        let clicks = 0;
        function moveNo() {
            clicks++;
            if(clicks > 3) {
                document.getElementById('msg').innerText = "راهی جز بله گفتن نداری!";
            }
            const randomX = (Math.random() - 0.5) * 200;
            const randomY = (Math.random() - 0.5) * 100;
            const noBtn = document.getElementById('no');
            noBtn.style.transform = `translate(${randomX}px, ${randomY}px)`;
        }
        document.getElementById('no').onmouseover = moveNo;
        document.getElementById('no').onclick = moveNo;
    </script>
    """
    components.html(html_code, height=180)
    
    if st.button("بله، حتماً! ❤️"):
        st.session_state.answers["فیلم"] = "بله"
        st.session_state.step = 3
        st.rerun()

# سوال سوم (فر)
elif st.session_state.step == 3:
    st.markdown("## فر دارید تو آشپزخونه؟")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("بله "):
            st.session_state.answers["فر"] = "بله"
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("خیر "):
            st.session_state.answers["فر"] = "خیر"
            st.session_state.step = 4
            st.rerun()

# سوال چهارم (ساعت)
elif st.session_state.step == 4:
    st.markdown("## چه ساعتی؟")
    time_val = st.time_input("ساعت:")
    if st.button("ثبت نهایی"):
        st.session_state.answers["ساعت"] = str(time_val)
        
        # ارسال تمام پاسخ‌ها به تلگرام شما
        final_text = "🎉 پاسخ‌های جدید دریافت شد:\n\n"
        for q, a in st.session_state.answers.items():
            final_text += f"- {q}: {a}\n"
        send_to_telegram(final_text)
        
        st.session_state.step = 5
        st.rerun()

# صفحه آخر
elif st.session_state.step == 5:
    st.markdown("<h1 style='margin-top: 50px;'>مرسی از اینکه جواب دادی ❤️</h1>", unsafe_allow_html=True)
