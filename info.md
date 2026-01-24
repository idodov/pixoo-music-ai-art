# 🎨 Pixoo Music AI Art (Ultra-Vivid Edition)

Turn your **Divoom Pixoo 64** into a conceptual art gallery that reacts to your music in real-time.

This is not just a simple album-art viewer. This script uses advanced AI to **interpret** your music, fusing the identity of the artist with the atmosphere of the song title to create a unique visual manifestation on your LED display.

## 🚀 Why this is different:
Most Pixoo scripts show low-resolution album covers that look blurry. This script uses the **Ultra-Vivid Engine**:
- **Conceptual Fusion**: If you play *'Ocean Eyes'* by *Billie Eilish*, the AI doesn't just show Billie; it manifests her likeness fused with oceanic imagery.
- **Hardware Optimized**: Every image is processed with boosted Saturation (2.0x), Contrast (1.6x), and Sharpness (3.0x) to ensure it looks "punchy" on physical LEDs.
- **Smart Color Theory**: Uses specific high-contrast color pairings (like Amber/Teal or Neon Pink/Cyan) for maximum visibility.
- **Dithered Quantization**: Reduces images to a specific 64-color palette to remove shimmer and create a professional "pixel-art" finish.

## ✨ Main Features
- **Instant Caching**: Remembers art for previously played songs for zero-lag display.
- **Smart Cleaning**: Automatically strips "Remastered," "Live," and "feat." tags to keep AI focused on the core subject.
- **Full Device Control**: Automatically turns your screen ON when music starts and restores your previous clock/weather channel when it stops.
- **Task Management**: Cancel pending AI generations instantly when you skip tracks.

## 🛠 Prerequisites
- **AppDaemon 4** installed via Home Assistant Add-ons.
- **Pillow (PIL)** and **aiohttp** added to your AppDaemon `python_packages`.
- A **Divoom Pixoo 64** (connected to your local network).

## 📖 Quick Setup
Once installed, simply add the configuration to your `apps.yaml` and watch your music come to life!

---
*Powered by Pollinations.ai*
