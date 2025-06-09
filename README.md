# 💖 每日健康小宝（Health Buddy）

一个基于 Streamlit 的智能健康助手，为你每日生成个性化健康建议，并配套语音朗读和 YouTube 健康视频推荐功能。  


---

## 🌟 功能特色

- 🧠 **健康建议生成**：基于你的体温、心率、血氧、步数、生活习惯等生成轻松俏皮但专业的健康建议  
- 🌦️ **天气感知**：自动获取城市天气，结合气候调整建议  
- 🎤 **语音朗读**：使用 `say` 命令朗读报告，可调节语速  
- 🎥 **健康视频推荐**：根据建议提取关键词，自动推荐 YouTube 健康相关视频  
- 🗣️ **多轮对话问答**：与健康顾问“小宝”持续对话，保存聊天记录  
- 🌐 **中英文界面切换**：支持简体中文和英文用户界面

---

## 🚀 启动方法

### 1. 克隆项目

```bash
git clone https://github.com/your-username/health-buddy.git
cd health-buddy
```

### 2. 安装依赖

建议使用虚拟环境：

```bash
pip install -r requirements.txt
```

### 3. 设置环境变量 `.env`

创建 `.env` 文件，填入你的 API Key：

```env
DEEPSEEK_API_KEY=your_deepseek_key
WEATHER_API_KEY=your_weatherapi_key
YOUTUBE_API_KEY=your_youtube_key
```

> 🔐 建议不要将 `.env` 上传至 GitHub。

### 4. 启动应用

```bash
streamlit run app.py
```

> 🎧 注意：朗读功能仅适用于 macOS（依赖系统自带的 `say` 命令）

---

## 📦 依赖包

```text
streamlit
requests
python-dotenv
```

---

## 📌 项目结构

```
health-buddy/
├── app.py              # 主程序入口
├── requirements.txt    # 依赖包
├── .env.example        # 环境变量示例
├── README.md           # 项目说明
└── examples/           # 截图与演示
```

---

## 🙌 致谢

- [DeepSeek API](https://deepseek.com/) - 生成健康建议
- [WeatherAPI](https://www.weatherapi.com/) - 实时天气数据
- [YouTube Data API](https://developers.google.com/youtube) - 视频推荐
- [Streamlit](https://streamlit.io/) - 快速构建可视化 Web 界面

---

## 🧠 作者

由 Jenson（sg子子） 和团队（Ray & 啧肉）开发 ✨  
欢迎贡献和提出建议！
