import streamlit as st
import requests
import os
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="یه قرار کوچولو 🌙",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# TELEGRAM
# =====================================================

try:
    BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
except Exception:
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram credentials are missing.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": message},
            timeout=10
        )
    except Exception as e:
        print("Telegram error:", e)


# =====================================================
# MUSIC
# =====================================================

MUSIC_FOLDER = "assets/music"

MUSIC_OPTIONS = {
    "pop1": {"label": "آهنگ شماره ۲ 🎵", "file": "Mammrez - Yare Chish Ghashang.mp3"},
    "pop2": {"label": "آهنگ شماره ۱ 🎵", "file": "Arman-Garshasbi-Royaye-Man-128.mp3"},
    "pop3": {"label": "آهنگ شماره ۳ 🎵", "file": "Baroon.mp3"},
    "pop4": {"label": "آهنگ شماره ۴ 🎵", "file": "Roozbeh-Bemani-Payane-Khob-128.mp3"},
    "pop5": {"label": "آهنگ شماره ۵ 🎵", "file": "Siavash-Ghomayshi-Panjereh-128.mp3"},
    "Rap": {"label": "آهنگ شماره ۶ 🎵", "file": "84034d11-42fb-4e6c-84ef-3a54ce7315eb.mp3"},  # آهنگ جدیدی که اضافه کردید
}

# =====================================================
# DAYS
# =====================================================

DAY_OPTIONS = ["پنج‌شنبه", "جمعه", "شنبه"]

DAY_MAPPING = {
    "پنج‌شنبه": "پنج‌شنبه",
    "جمعه": "پنج‌شنبه",
    "شنبه": "پنج‌شنبه",
}


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "step": 0,
    "mood": "",
    "selected_day": "",
    "actual_day": "",
    "selected_time": "",
    "selected_music": "",
    "sent": False,
    "rejection_sent": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# CSS
# =====================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"],
    [data-testid="stAppViewContainer"] {
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* راست چین کردن متن‌های فارسی */
    .stApp {
        direction: rtl;
        text-align: right;
        background:
            radial-gradient(
                ellipse at 50% 0%,
                rgba(190, 143, 55, 0.18),
                transparent 55%
            ),
            linear-gradient(
                180deg,
                #17130e 0%,
                #100d09 55%,
                #080706 100%
            );
        color: #f4e6cc;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    .block-container {
        max-width: 600px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    p, label, h1, h2, h3 {
        text-align: right;
    }

    .hero {
        text-align: right;
        padding: 1.5rem 0 1rem;
    }

    .eyebrow {
        color: #b99a63;
        letter-spacing: 3px;
        font-size: 0.7rem;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        color: #f7e7c6;
        font-size: clamp(2rem, 8vw, 3rem);
        font-weight: 700;
        line-height: 1.7;
    }

    .hero-subtitle {
        color: #b9aa91;
        font-size: 0.95rem;
        line-height: 2;
    }

    .divider {
        width: 75px;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            #b99a63,
            transparent
        );
        margin: 1.5rem 0;
    }

    .question {
        text-align: right;
        color: #f0dfbf;
        font-size: 1.1rem;
        line-height: 2.2;
        margin: 1.5rem 0;
    }

    .note {
        text-align: right;
        color: #91816a;
        font-size: 0.85rem;
        line-height: 2;
    }

    .stButton > button {
        width: 100%;
        min-height: 3.2rem;
        border-radius: 15px;
        font-family: 'Vazirmatn', sans-serif;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        direction: rtl;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(
            135deg,
            #c8a76b,
            #a78346
        );
        color: #17110a;
        border: none;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(
            135deg,
            #e0c28a,
            #b99453
        );
        transform: translateY(-2px);
    }

    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.025);
        color: #d6c4a5;
        border: 1px solid rgba(198, 164, 102, 0.25);
    }

    .stButton > button[kind="secondary"]:hover {
        border-color: #c8a76b;
        color: #f4dfb6;
    }

    /* Radio buttons */
    div[data-testid="stRadio"] {
        direction: rtl;
    }

    div[data-testid="stRadio"] label {
        color: #e8d8bc;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.025);
        border: 1px solid rgba(190, 153, 91, 0.2);
        border-radius: 14px;
        padding: 0.8rem;
    }

    /* Text area */
    textarea {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Vazirmatn', sans-serif !important;
    }

    /* Selectbox */
    div[data-testid="stSelectbox"] {
        direction: rtl;
        text-align: right;
    }

    /* Day shake */
    .shake {
        animation: shake 0.65s ease-in-out;
    }

    @keyframes shake {
        0%   { transform: translateX(0); }
        15%  { transform: translateX(-9px); }
        30%  { transform: translateX(9px); }
        45%  { transform: translateX(-7px); }
        60%  { transform: translateX(7px); }
        75%  { transform: translateX(-4px); }
        100% { transform: translateX(0); }
    }

    /* Rejection page */
    .dark-page {
        text-align: center;
        padding: 2rem 0;
        animation: fadeIn 1.2s ease;
    }

    .broken-heart {
        font-size: 100px;
        display: inline-block;
        animation: brokenHeart 2s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(180, 40, 55, 0.3));
    }

    @keyframes brokenHeart {
        0% {
            transform: scale(0.9) rotate(-5deg);
            opacity: 0.75;
        }
        50% {
            transform: scale(1.12) rotate(5deg);
            opacity: 1;
        }
        100% {
            transform: scale(0.9) rotate(-5deg);
            opacity: 0.75;
        }
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .sad-title {
        color: #d9b8b8;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 1.5rem;
    }

    .sad-text {
        color: #a99494;
        font-size: 1rem;
        line-height: 2.3;
        margin-top: 1rem;
    }

    .footer {
        text-align: right;
        color: #6d604e;
        font-size: 0.7rem;
        margin-top: 3rem;
    }

    @media (max-width: 600px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero-title {
            font-size: 2rem;
        }

        .broken-heart {
            font-size: 85px;
        }
    }
    
    /* مخفی کردن پلیر صدا در صفحه رد درخواست */
    .hidden-audio audio {
        opacity: 0.01;
        height: 1px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# HTML HELPER
# =====================================================

def render_html(content):
    st.html(content)


# =====================================================
# HEADER
# =====================================================

if st.session_state.step not in [5, 7]:
    
    headers = {
        0: ("سلام بچه! 🌙", "یه چیزی می‌خواستم ازت بپرسم..."),
        1: ("بچه، نظرت چیه؟ 🌙", "وقتشه یه تصمیم قشنگ بگیریم..."),
        2: ("چه روزی بچه؟ 🌙", "تقویمت رو ببین و انتخاب کن..."),
        3: ("چه ساعتی بچه؟ 🌙", "عقربه‌ها رو تنظیم کن..."),
        4: ("بچه، موزیک چی؟ 🌙", "بریم تو فاز آهنگ...")
    }
    
    title, subtitle = headers.get(st.session_state.step, ("سلام بچه! 🌙", "یه چیزی می‌خواستم ازت بپرسم..."))
    
    render_html(
        f"""
        <div class="hero">
            <div class="eyebrow">A LITTLE MOMENT</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">
                {subtitle}
            </div>
            <div class="divider"></div>
        </div>
        """
    )


# =====================================================
# STEP 0 — HOW ARE YOU?
# =====================================================

if st.session_state.step == 0:

    render_html(
        """
        <div class="question">
            اول از همه،<br>
            حالت چطوره؟ 💛
        </div>
        """
    )

    mood = st.text_area(
        "حالت رو برام بنویس:",
        placeholder="مثلاً خوبم، خسته‌ام، دلم گرفته...",
        height=100,
        label_visibility="collapsed"
    )

    if st.button("بذار بهت بگم چی تو ذهنمه ✨", type="primary"):

        if not mood.strip():
            st.warning("اول بهم بگو حالت چطوره 🥺")
        else:
            st.session_state.mood = mood.strip()
            st.session_state.step = 1
            st.rerun()


# =====================================================
# STEP 1 — INVITATION
# =====================================================

elif st.session_state.step == 1:

    render_html(
        """
        <div class="question">
            مرسی که از حالت برام گفتی... 💛<br><br>
            با هم بریم بیرون و یه خاطره‌ی قشنگ بسازیم.
        </div>

        <div class="note">
            یه قرار کوچولو، بدون هیچ برنامه‌ی پیچیده‌ای 🌙
        </div>
        """
    )

    st.write("")

    if st.button("باشه، ببینیم چه روزی! 💛", type="primary"):
        st.session_state.step = 2
        st.rerun()

    if st.button(
        "من آدم بی‌ادبی هستم و نمی‌خوام باهات بیام بیرون، این‌قدر بهم نگو 😡",
        type="secondary"
    ):
        st.session_state.step = 7
        st.rerun()


# =====================================================
# STEP 2 — DAY SELECTION
# =====================================================

elif st.session_state.step == 2:

    render_html(
        """
        <div class="question">
            خب، حالا تو انتخاب کن...<br>
            کدوم روز بیشتر به دلت می‌شینه؟ 🌷
        </div>
        """
    )

    col1, col2, col3 = st.columns(3)

    day_labels = {}

    for day in DAY_OPTIONS:
        if st.session_state.selected_day == day:
            day_labels[day] = "پنج‌شنبه ✓"
        else:
            day_labels[day] = day

    with col1:
        if st.button(
            day_labels["پنج‌شنبه"],
            key="day_thursday",
            type=(
                "primary"
                if st.session_state.selected_day == "پنج‌شنبه"
                else "secondary"
            )
        ):
            st.session_state.selected_day = "پنج‌شنبه"
            st.session_state.actual_day = "پنج‌شنبه"
            st.rerun()

    with col2:
        if st.button(
            day_labels["جمعه"],
            key="day_friday",
            type=(
                "primary"
                if st.session_state.selected_day == "جمعه"
                else "secondary"
            )
        ):
            st.session_state.selected_day = "جمعه"
            st.session_state.actual_day = "پنج‌شنبه"
            st.rerun()

    with col3:
        if st.button(
            day_labels["شنبه"],
            key="day_saturday",
            type=(
                "primary"
                if st.session_state.selected_day == "شنبه"
                else "secondary"
            )
        ):
            st.session_state.selected_day = "شنبه"
            st.session_state.actual_day = "پنج‌شنبه"
            st.rerun()

    if st.session_state.selected_day:

        if st.session_state.selected_day != "پنج‌شنبه":
            render_html(
                """
                <div class="shake">
                    <div class="question">
                        اِ... یه اتفاقی افتاد! 😳
                    </div>
                </div>
                """
            )
        else:
            render_html(
                """
                <div class="question">
                    پنج‌شنبه انتخاب خیلی خوبیه! 🌙
                </div>
                """
            )

        if st.button("خب، ادامه بدیم 💫", type="primary"):
            st.session_state.step = 3
            st.rerun()

    if st.button("برگردیم عقب", type="secondary"):
        st.session_state.step = 1
        st.rerun()


# =====================================================
# STEP 3 — TIME SELECTION
# =====================================================

elif st.session_state.step == 3:

    render_html(
        """
        <div class="question">
            حالا بگو چه زمانی رو بیشتر دوست داری؟ 🌙
        </div>
        """
    )

    time_options = [
        "عصر، مثلاً ساعت ۱۷ که هوا خنک‌تر شده 🌆",
        "غروب، طرفای ساعت ۱۹ قبل از تاریک شدن 🌅",
        "شب، حدود ساعت ۲۱ که شهر آروم‌تره 🌙"
    ]

    selected_time = st.radio(
        "زمان:",
        time_options,
        index=None,
        label_visibility="collapsed"
    )

    if st.button(
        "این زمان خوبه ✨",
        type="primary",
        disabled=selected_time is None
    ):
        st.session_state.selected_time = selected_time
        st.session_state.step = 4
        st.rerun()

    if st.button("برگردیم به انتخاب روز", type="secondary"):
        st.session_state.step = 2
        st.rerun()


# =====================================================
# STEP 4 — MUSIC SELECTION
# =====================================================

elif st.session_state.step == 4:

    render_html(
        """
        <div class="question">
            خب، حالا یه آهنگ انتخاب کن... 🎵<br>
            نیت کن و آهنگ رو انتخاب کن!
        </div>

        <div class="note">
            فقط یکی رو می‌تونی انتخاب کنی :)<br>
            برای گوش دادن آهنگ تا آخر، همینجا بمون 🎧
        </div>
        """
    )

    music_columns = st.columns(2)

    music_keys = list(MUSIC_OPTIONS.keys())

    for index, music_key in enumerate(music_keys):

        column = music_columns[index % 2]

        with column:

            label = MUSIC_OPTIONS[music_key]["label"]

            is_locked = bool(st.session_state.selected_music) and (st.session_state.selected_music != music_key)

            if st.button(
                label,
                key=f"music_{music_key}",
                type=(
                    "primary"
                    if st.session_state.selected_music == music_key
                    else "secondary"
                ),
                disabled=is_locked
            ):
                st.session_state.selected_music = music_key
                st.rerun()

    if st.session_state.selected_music:

        selected_file = MUSIC_OPTIONS[
            st.session_state.selected_music
        ]["file"]

        music_path = os.path.join(MUSIC_FOLDER, selected_file)

        if os.path.exists(music_path):
            st.audio(music_path, autoplay=True)
        else:
            st.warning(f"فایل آهنگ پیدا نشد: {music_path}")

    if st.button(
        "این آهنگ رو انتخاب می‌کنم",
        type="primary",
        disabled=not st.session_state.selected_music
    ):

        if not st.session_state.sent:

            message = (
                "🌙 دعوت جدید ثبت شد!\n\n"
                f"حال فاطمه: {st.session_state.mood}\n\n"
                f"روز انتخاب اولیه: {st.session_state.selected_day}\n"
                f"روز واقعی: {st.session_state.actual_day}\n"
                f"زمان انتخابی: {st.session_state.selected_time}\n"
                f"آهنگ: {MUSIC_OPTIONS[st.session_state.selected_music]['label']}\n"
                f"شناسه آهنگ: {st.session_state.selected_music}\n\n"
                f"زمان ثبت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            send_telegram(message)
            st.session_state.sent = True

        st.session_state.step = 5
        st.rerun()

    if st.button("برگردیم به انتخاب زمان", type="secondary"):
        st.session_state.step = 3
        st.rerun()


# =====================================================
# STEP 5 — FINAL
# =====================================================

elif st.session_state.step == 5:

    render_html(
        f"""
        <div class="hero">
            <div class="eyebrow">A LITTLE MOMENT</div>
            <div class="hero-title">پس قرارمون شد بچه! 🌙</div>
            <div class="hero-subtitle">
                بی‌صبرانه منتظر روز قرارمونم...
            </div>
            <div class="divider"></div>
        </div>

        <div class="question">
            خیلی خوشحالم که قراره ببینمت و کلی ذوق دارم! 😍<br><br>
            <strong>روز قرار:</strong> {st.session_state.actual_day}<br>
            <strong>زمان قرار:</strong> {st.session_state.selected_time}
        </div>

        <div class="note">
            این دعوت با کمی ستاره و کلی ذوق ساخته شده.
        </div>
        """
    )

    if st.button("از اول شروع کنیم 🌙", type="secondary"):

        for key, value in defaults.items():
            st.session_state[key] = value

        st.rerun()


# =====================================================
# STEP 7 — REJECTION
# =====================================================

elif st.session_state.step == 7:

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(
                    ellipse at 50% 35%,
                    rgba(90, 20, 30, 0.20),
                    transparent 55%
                ),
                linear-gradient(
                    180deg,
                    #10090c 0%,
                    #090608 60%,
                    #050405 100%
                ) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    render_html(
        """
        <div class="dark-page">
            <div class="eyebrow">OH NO...</div>

            <div class="broken-heart">
                💔
            </div>

            <div class="sad-title">
                قلبم شکست...
            </div>

            <div class="sad-text">
                باشه بابااا...<br><br>
                فقط خواستم یه وقت کوچولو<br>
                باهات داشته باشم.
            </div>

            <div class="divider"></div>

            <div class="note">
                البته هنوز یه ذره امیدوارم...
            </div>
        </div>
        """
    )

    # نمایش متن اطلاع‌رسانی پخش آهنگ در صفحه رد درخواست
    st.info("🎵 آهنگ نارفیق خوب در حال پخش است...")

    # پخش خودکار موزیک «نارفیق خوب» در صفحه رد درخواست با استایل مخفی
    sad_music_path = os.path.join(MUSIC_FOLDER, "Mehdi-Yaghmaei-Narefighe-Khob-128.mp3")
    if os.path.exists(sad_music_path):
        st.markdown('<div class="hidden-audio">', unsafe_allow_html=True)
        st.audio(sad_music_path, autoplay=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if not st.session_state.rejection_sent:

        send_telegram(
            "💔 فاطمه گزینه‌ی رد دعوت را انتخاب کرد.\n"
            f"حال ثبت‌شده: {st.session_state.mood}\n"
            f"زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        st.session_state.rejection_sent = True

    if st.button("باشه، یه فرصت دیگه بهم بده 🌷", type="primary"):
        st.session_state.step = 1
        st.session_state.rejection_sent = False
        st.rerun()


# =====================================================
# FOOTER
# =====================================================

render_html(
    """
    <div class="footer">
        made with a little bit of starlight ✨
    </div>
    """
)