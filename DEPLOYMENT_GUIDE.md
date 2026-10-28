# 🚀 AgroBiometrix: 1-Click Public Cloud Deployment Guide

This guide explains how to deploy **AgroBiometrix** to a public URL in 2 minutes so you can share it with investors, research partners, and grant committees worldwide.

---

## 🌟 Option A: Streamlit Community Cloud (Recommended — 100% Free)
*Best for instant public URL with zero server management.*

1. **Push your code to GitHub**:
   - Create a repository on [GitHub](https://github.com/) (e.g. `agrobiometrix`).
   - Push this workspace to your GitHub repository:
     ```bash
     git init
     git add .
     git commit -m "AgroBiometrix initial release"
     git branch -M main
     git remote add origin https://github.com/YOUR_USERNAME/agrobiometrix.git
     git push -u origin main
     ```
2. **Deploy on Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
   - Click **"New app"**.
   - Select your repository (`YOUR_USERNAME/agrobiometrix`), Branch (`main`), and Main file path (`app.py`).
   - Click **"Deploy!"**.
3. **Live Public URL**:
   - Your application will be live at `https://agrobiometrix.streamlit.app` in under 90 seconds!
   - You can copy this link and open it on your smartphone or send it to anyone globally.

---

## 🐳 Option B: Docker Container Deployment (Enterprise / Private Cloud)
*Best for self-hosting on AWS EC2, Google Cloud Run, DigitalOcean, or university servers.*

1. **Build the Docker container**:
   ```bash
   docker build -t agrobiometrix:latest .
   ```
2. **Run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```
3. **Access the application**:
   - Open `http://YOUR_SERVER_IP:8501`.

---

## 🤗 Option C: Hugging Face Spaces (Free Machine Learning Showcase)
*Best for sharing with the global AI / research community.*

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces).
2. Click **"Create new Space"**.
3. Set SDK to **Streamlit**.
4. Clone the repository and push your project files.
5. Hugging Face builds and hosts your app with a permanent `hf.space` URL!

---

## 🔐 Managing API Keys in Production
AgroBiometrix functions **100% offline out-of-the-box** using deterministic biometrics engines and pre-loaded African evidence bases. 
To enable Live Gemini or OpenAI orchestration in production:
1. In Streamlit Cloud: Go to **App Settings $\to$ Secrets**.
2. Paste the contents of `.streamlit/secrets.toml.example` with your real keys.
