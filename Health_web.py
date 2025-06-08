# --- 页面配置 ---
import streamlit as st
import os
import re
import requests
import subprocess
from dotenv import load_dotenv

st.set_page_config(page_title="每日健康小宝", page_icon="💖", layout="wide")

# --- 加载密钥 ---
load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# --- 文本清理函数 ---
def clean_text(text):
    text = re.sub(r"[-=]{3,}", "", text)
    text = re.sub(r"~{2,}(.*?)~{2,}", "", text)
    text = re.sub(r"<s>.*?</s>", "", text)
    text = re.sub(r"<del>.*?</del>", "", text)
    text = re.sub(r"[（(][^）)]+[）)]", "", text)
    text = text.replace("✅ 小宝回答：", "")
    return text.strip()

# --- Mac 朗读 ---
def speak_mac(text, rate=160):
    try:
        subprocess.Popen(["say", "-r", str(rate), text])
    except Exception as e:
        st.warning(f"播放失败：{e}")

# --- 提取健康关键词（更精准）---
def extract_health_keywords(text):
    keywords = set()
    for line in text.splitlines():
        if any(kw in line for kw in ["建议", "提醒", "风险", "健康", "习惯", "注意"]):
            words = re.findall(r"[健康饮食作息锻炼睡眠压力心率血压肥胖抽烟熬夜糖尿病心脏疾病肥胖癌症焦虑]+", line)
            keywords.update(words)
    return list(keywords)[:3] or ["健康建议"]

# --- YouTube 推荐 ---
def recommend_youtube_videos(query, max_results=3):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults={max_results}&q={query}&key={YOUTUBE_API_KEY}"
    res = requests.get(url)
    videos = []
    if res.status_code == 200:
        for item in res.json().get("items", []):
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            link = f"https://www.youtube.com/watch?v={video_id}"
            videos.append((title, link))
    return videos

# --- 多语言 UI ---
language = st.selectbox("🌐 选择语言 / Language", ["中文", "English"])
is_zh = language == "中文"

T = {
    "title": "💖 每日健康小宝" if is_zh else "💖 Daily Health Buddy",
    "city": "📍 你在哪座城市呀？" if is_zh else "📍 Which city are you in?",
    "weather_fail": "天气获取失败" if is_zh else "Weather fetch failed",
    "weather_none": "👕 小宝暂时没拿到天气数据" if is_zh else "👕 XiaoBao didn't get weather data yet~",
    "disease": "请写写你现在有没有慢性病或基础病" if is_zh else "Any chronic diseases (optional)",
    "habit": "有没有什么生活习惯（如抽烟、熬夜、喝酒等）？告诉我吧~" if is_zh else "Any habits?",
    "heart": "💓 心率大概是多少呢？比如80～100" if is_zh else "💓 Heart rate (e.g. 80~100)",
    "exercise": "🏃 这次心率是运动完测的吗？" if is_zh else "🏃 Heart rate after exercise?",
    "oxygen": "🩸 你的小血氧是多少呢？比如96～98%" if is_zh else "🩸 Oxygen level (e.g. 96–98%)",
    "steps": "🚶 今天大概走了多少步呢？" if is_zh else "🚶 Steps today?",
    "temp": "🌡 小宝来测体温啦，现在大概多少度呀？" if is_zh else "🌡 Temperature now?",
    "btn": "🧠 生成健康建议" if is_zh else "🧠 Generate Advice",
    "ask_subtitle": "🙋 有什么想问问小宝的吗？" if is_zh else "🙋 Anything to ask XiaoBao?",
    "question": "🐣 和小宝聊聊吧！" if is_zh else "🐣 Chat with XiaoBao!",
    "send": "发送 / Send",
    "answer": "✅ 小宝回答：" if is_zh else "✅ XiaoBao's reply:",
    "history": "📜 小宝回答记录" if is_zh else "📜 XiaoBao's Chat History",
}

st.title(T["title"])

# --- 天气 ---
def get_weather(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang={'zh' if is_zh else 'en'}"
        res = requests.get(url)
        data = res.json()
        desc = data["current"]["condition"]["text"]
        temp = data["current"]["temp_c"]
        tip = ("🧥 今天天气凉快，小宝建议你穿暖一点哦~" if temp < 15 else
               "👕 今天天气适中，穿件小外套就好啦~" if temp < 25 else
               "🩳 天气热乎乎的，注意防晒和补水喔~") if is_zh else (
               "🧥 It's chilly, dress warm~" if temp < 15 else
               "👕 Mild today, light jacket's good~" if temp < 25 else
               "🩳 It's hot! Stay hydrated & use sunscreen~")
        return f"{desc}, {temp}°C", tip
    except:
        return T["weather_fail"], T["weather_none"]

# --- 输入部分 ---
city = st.text_input(T["city"], value="秦皇岛" if is_zh else "Qinhuangdao")
weather_str, weather_tip = get_weather(city)
st.info(f"📍 {city} 当前天气：{weather_str} | 💡 {weather_tip}")

col1, col2 = st.columns(2)
disease = col1.text_area(T["disease"], height=100)
habit = col2.text_area(T["habit"], height=100)
col3, col4 = st.columns(2)
heart = col3.text_input(T["heart"])
exercise = col4.checkbox(T["exercise"])
col5, col6 = st.columns(2)
oxygen = col5.text_input(T["oxygen"])
steps = col6.text_input(T["steps"])
temp = st.text_input(T["temp"])

# --- 健康建议生成 ---
if st.button(T["btn"]):
    prompt = f"""
📍 城市：{city}
🌤 天气：{weather_str} | {weather_tip}
💓 心率：{heart}（{"运动后" if exercise else "静息"}）
🩸 血氧：{oxygen}
🚶 步数：{steps}
🌡 体温：{temp}
🩺 慢性病/基础病：{disease}
🧠 生活习惯：{habit}

请你作为健康顾问“小宝”，语气要轻松温暖、俏皮有趣但专业，帮我生成：
1️⃣ 健康状况简评
2️⃣ 风险提示或提醒
3️⃣ 饮食与生活建议（结合城市天气）
4️⃣ 鼓励关心的话（结合用户数据）
"""
    r = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
    )
    if r.status_code == 200:
        result = clean_text(r.json()["choices"][0]["message"]["content"])
        st.session_state["health_result"] = result
    else:
        st.error("❌ 小宝没能生成建议，请检查网络或API")

# --- 显示建议 + 控制朗读 + 视频推荐 ---
if "health_result" in st.session_state:
    st.markdown("### ✅ 小宝生成的健康报告：")
    st.write(st.session_state["health_result"])

    with st.expander("🗣️ 小宝朗读控制", expanded=True):
        rate = st.slider("语速调节", 120, 240, 160, step=10)
        colr1, colr2 = st.columns([1, 1])
        if colr1.button("🦜 点我朗读健康报告"):
            speak_mac(st.session_state["health_result"], rate)
        if colr2.button("🛑 停止朗读"):
            subprocess.run(["killall", "say"])

    st.markdown("### 🎥 小宝为你推荐的视频：")
    keywords = extract_health_keywords(st.session_state["health_result"])
    search_query = " ".join(keywords)
    videos = recommend_youtube_videos(search_query)
    if videos:
        for title, link in videos:
            st.markdown(f"- [{title}]({link})")
    else:
        st.info("🧐 没找到相关视频，可以换个关键词试试~")

# --- 问答模块 ---
st.markdown("---")
st.subheader(T["ask_subtitle"])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

question = st.text_input(T["question"])
if st.button(T["send"]) and question.strip():
    history = "\n".join([f"你：{q}\n小宝：{a}" for q, a in st.session_state.chat_history[-3:]])
    full_prompt = f"{history}\n你：{question}\n小宝："

    r = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": full_prompt}]}
    )
    if r.status_code == 200:
        reply = clean_text(r.json()["choices"][0]["message"]["content"])
        st.session_state.chat_history.append((question, reply))
        st.success(T["answer"])
        st.write(reply)

# --- 聊天记录展示 ---
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader(T["history"])
    for q, a in reversed(st.session_state.chat_history[-5:]):
        st.markdown(f"**🧍 你：** {q}")
        st.markdown(f"**🤖 小宝：** {a}")
