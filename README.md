# 🎨 Pixoo64 Music AI Art: The Ultra-Vivid Conceptual Engine

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![AppDaemon](https://img.shields.io/badge/AppDaemon-4.0+-blue.svg?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

**Stop showing blurry album covers. Start manifesting the soul of your music.**

**Pixoo Music AI Art** is a high-performance AppDaemon script for **Home Assistant** that transforms your **Divoom Pixoo64** into a conceptual art gallery. It generates unique visual interpretations of your music in real-time, optimized specifically for LED hardware.

---

## 🖼️ Gallery
*Experience the fusion of music and AI on your wall.*

|  |  |  |
| :---: | :---: | :---: |
|![pixoo_demo3](https://github.com/user-attachments/assets/f689500a-509d-491c-8a8f-1cacf897d61e)|![pixoo_demo4](https://github.com/user-attachments/assets/c073ea7a-0b81-4dd3-9845-dfd0cd679844)|![pixoo_demo5](https://github.com/user-attachments/assets/ed34c076-76ed-459d-bb78-51b6e39f6045)|
|![pixoo_demo](https://github.com/user-attachments/assets/ea74891f-493e-4f10-ae0d-8108d6b371a8)|![pixoo_demo1](https://github.com/user-attachments/assets/d37e2f34-4023-4e46-9358-8ff618f3da99)|![pixoo_demo2](https://github.com/user-attachments/assets/07308c9d-a44b-4978-a7ac-ced42f9e6046)|

---

## 🚀 Key Features

### 💎 Ultra-Vivid Hardware Engine
Standard images often look "muddy" on 64x64 LED grids. Our engine applies professional-grade post-processing:
- **Saturation Boost (2.0x):** Deep, glowing colors that pop from across the room.
- **Contrast Enhancement (1.6x):** Dramatic shadows to separate the subject from the background.
- **Extreme Sharpness (3.0x):** Edge-clarity logic to reduce the "blur" of small LEDs.
- **64-Color Quantization:** Professional dithering that removes shimmer and creates a "hand-crafted" pixel-art finish.

### 🧠 Smart "Fusion" Prompting
The script builds a complex prompt for every song:
- **Color Theory Matrix:** Randomizes high-contrast color pairings (Amber/Teal, Neon Pink/Cyan).
- **Style Rotation:** Cycles through Surrealism, Pop-Art, Cyberpunk, and more.
- **Context Cleaning:** Automatically strips `(Remastered)`, `(Live)`, or `feat.` tags to keep the AI focused on the song's meaning.

---

## 🔑 How to get a Pollinations API Key
Using an API key ensures higher priority, faster generation, and avoids rate limits during long listening sessions.

1.  Visit [**Pollinations.ai**](https://pollinations.ai/).
2.  Click **Login** and select **Login with GitHub**.
3.  Authorize the application with your GitHub account.
4.  Once logged in, navigate to your **Profile/Account** page (or [enter.pollinations.ai](https://enter.pollinations.ai/)).
5.  Copy your **API Key** (it usually starts with `pk_`).
6.  Paste the key into your `apps.yaml` under `pollinations_api_key`.

---

## 🛠 Installation

### 1. Requirements
Ensure your AppDaemon environment has these Python packages installed:
- `Pillow` (for image processing)

*In Home Assistant OS, add these to the `python_packages` section of the AppDaemon add-on configuration.*

### 2. HACS Installation
1. Go to **HACS** > **Integrations**.
2. Click the three dots (top-right) and select **Custom repositories**.
3. Paste your GitHub repository URL and select **AppDaemon** as the category.
4. Click **Install**.

---

## ⚙️ Configuration

Add the following to your `apps.yaml` file:

```yaml
pixoo_music_ai:
  module: pixoo_ai_art
  class: PixooMusicAI
  
  # Device Settings
  media_player: "media_player.spotify_your_name" # Your HA media player entity
  pixoo_ip: "192.168.1.50"                       # Static IP of your Pixoo 64
  
  # Behavior Settings
  full_control: true                             # ON when music starts, Restore when stopped
  boost: true                                    # Enable the Ultra-Vivid hardware engine
  
  # AI Settings
  ai_model: "turbo"                              # "turbo" (Fast/Stable) or "flux" (High Detail)
  pollinations_api_key: "pk_your_key_here"       # Your GitHub-linked key from Pollinations.ai
```

---

## ❓ FAQ

**Q: Why does it take a few seconds for art to appear?**  
A: The AI is "painting" a unique image from scratch for you. This takes ~5-10 seconds. Once a song is cached in your current session, it becomes instant!

**Q: Does it remember my previous Pixoo screen?**  
A: Yes. The script saves your current channel (like your clock) before starting the art and restores it the moment the music stops or pauses.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙌 Credits
- AI Generation by [Pollinations.ai](https://pollinations.ai)
- Built with [AppDaemon](https://appdaemon.readthedocs.io/)
- Optimized for the [Divoom Pixoo 64](https://www.divoom.com/)
