import streamlit as st

st.set_page_config(page_title="عایا پیشنهاد دعوت پابرجاست؟", layout="centered")

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

def save_response(q, ans):
    with open("responses.txt", "a", encoding="utf-8") as f:
        f.write(f"{q}: {ans}\n")

# سوال اول
if st.session_state.step == 1:
    st.markdown("## عایا همچنان دعوت پا برجاست؟")
    if st.button("بله"):
        save_response("دعوت", "بله")
        st.session_state.step = 2
        st.rerun()
    if st.button("خیر"):
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
    
    if st.button("بله، حتماً!"):
        save_response("فیلم", "بله")
        st.session_state.step = 3
        st.rerun()

# سوال سوم (فر)
elif st.session_state.step == 3:
    st.markdown("## فر دارید تو آشپزخونه؟")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("بله "):
            save_response("فر", "بله")
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("خیر "):
            save_response("فر", "خیر")
            st.session_state.step = 4
            st.rerun()

# سوال چهارم (ساعت)
elif st.session_state.step == 4:
    st.markdown("## چه ساعتی؟")
    time = st.time_input("ساعت:")
    if st.button("ثبت نهایی"):
        save_response("ساعت", str(time))
        st.session_state.step = 5
        st.rerun()

# صفحه آخر
elif st.session_state.step == 5:
    st.markdown("<h1 style='margin-top: 50px;'>مرسی از اینکه جواب دادی ❤️</h1>", unsafe_allow_html=True)