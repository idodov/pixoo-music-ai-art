"""
PIXOO 64 - AI MUSIC ART GENERATOR (ULTRA-VIVID EDITION)
------------------------------------------------------
Optimized for high-contrast LED visibility, conceptual song-title 
manifestation, and artist-identity persistence.

Example Configuration (apps.yaml):
pixoo_music_ai:
  module: pixoo_ai_art
  class: PixooMusicAI
  media_player: "media_player.spotify"
  pixoo_ip: "192.168.1.50"
  full_control: true
  boost: true
  ai_model: "turbo"
"""

import appdaemon.plugins.hass.hassapi as hass
import aiohttp
import asyncio
import base64
import logging
import io
import urllib.parse
import random
from PIL import Image, ImageOps, ImageEnhance

_LOGGER = logging.getLogger(__name__)

class PixooMusicAI(hass.Hass):

    async def initialize(self):
        # --- Config ---
        self.media_player = self.args.get("media_player")
        self.pixoo_ip = self.args.get("pixoo_ip")
        self.pixoo_url = f"http://{self.pixoo_ip}:80/post"
        self.pollinations_key = self.args.get("pollinations_api_key", None)
        self.ai_model = self.args.get("ai_model", "turbo") 
        self.boost = self.args.get("boost", True)
        self.full_control = self.args.get("full_control", True)

        # --- State & Cache ---
        self.previous_channel = 0 
        self.is_showing_art = False
        self.current_track_id = None
        self.gen_task = None 
        self.image_cache = {} # Basic session cache

        self.session = aiohttp.ClientSession(headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
        })
        
        self.listen_state(self.music_state_changed, self.media_player, attribute="all")
        _LOGGER.info(f"Pixoo Ultra-Vivid Engine: Monitoring {self.media_player}")

    def _generate_conceptual_prompt(self, artist, title):
        """Creates a high-contrast, color-optimized prompt."""
        
        # 1. Color Pairing (Optimized for LED luminosity)
        color_pairings = [
            "Amber and Deep Teal",
            "Neon Pink and Electric Blue",
            "Vivid Orange and Midnight Violet",
            "Emerald Green and Gold",
            "Crimson Red and Stark White",
            "Cybernetic Cyan and Magenta"
        ]
        
        # 2. Advanced Styles (Visual Weight)
        styles = [
            "Hyper-detailed digital fusion portrait",
            "High-contrast minimalist vector poster",
            "Graphic pop-art illustration",
            "Surrealist symbolic manifestation",
            "Retro-futurist cinematic keyart"
        ]

        # 3. Dynamic Fusions
        fusions = [
            f"The artist {artist} literally personifying the essence of the song '{title}'",
            f"A surreal manifestation of '{title}' featuring the iconic likeness of {artist}",
            f"A conceptual masterpiece where {artist} and the visual theme of '{title}' become one",
            f"The musical spirit of {artist} fused with the surreal imagery of '{title}'"
        ]

        # 4. Angle/Composition
        compositions = [
            "Centered close-up portrait",
            "Extreme dramatic angle",
            "Symmetrical artistic layout",
            "Iconic silhouette with internal detail"
        ]

        selected_colors = random.choice(color_pairings)
        selected_style = random.choice(styles)
        selected_fusion = random.choice(fusions)
        selected_comp = random.choice(compositions)

        # Building the multi-weighted prompt
        return (f"Professional square album cover. {selected_comp} of {selected_fusion}. "
                f"Likeness inspired by musical artist {artist}. "
                f"Theme: {title}. Style: {selected_style}. Colors: {selected_colors}. "
                f"Sharp outlines, high contrast, deep shadows, cinematic lighting, "
                f"vibrant and saturated, no text, 8k resolution.")

    async def music_state_changed(self, entity, attribute, old, new, kwargs):
        if not new: return
        state = new.get("state", "off")
        attributes = new.get("attributes", {})
        
        if state == "playing":
            raw_artist = attributes.get("media_artist", "Unknown Artist")
            title = attributes.get("media_title", "Unknown Track")
            
            clean_artist = raw_artist.split(' feat.')[0].split(' & ')[0].split(', ')[0]
            clean_title = title.split(' (')[0].split(' - ')[0]
            
            new_track_id = f"{clean_artist}_{clean_title}"
            if new_track_id == self.current_track_id: return
            self.current_track_id = new_track_id

            if self.gen_task and not self.gen_task.done():
                self.gen_task.cancel()

            # Check Cache first
            if new_track_id in self.image_cache:
                _LOGGER.info(f"Using cached art for: {new_track_id}")
                await self.display_cached_art(new_track_id)
            else:
                self.gen_task = asyncio.create_task(self.workflow_sequence(clean_artist, clean_title, new_track_id))
        
        elif state in ["paused", "idle", "off"] and self.is_showing_art:
            await self.stop_art_mode(state)

    async def workflow_sequence(self, artist, title, track_id):
        try:
            await asyncio.sleep(1.2)
            if not self.is_showing_art:
                self.previous_channel = await self.get_current_channel()
                self.is_showing_art = True

            await self.send_pixoo_command({"Command": "Channel/OnOffScreen", "OnOff": 1})
            await self.generate_ai_art(artist, title, track_id)
        except asyncio.CancelledError: pass 

    async def generate_ai_art(self, artist, title, track_id):
        prompt = self._generate_conceptual_prompt(artist, title)
        _LOGGER.info(f"AI Generate -> {artist} | {title}")

        params = {
            "model": self.ai_model,
            "width": 256,
            "height": 256,
            "seed": random.randint(0, 999999),
            "nologo": "true",
            "enhance": "false",
            "safe": "false"
        }
        if self.pollinations_key: params["key"] = self.pollinations_key

        url = f"https://gen.pollinations.ai/image/{urllib.parse.quote(prompt)}?{urllib.parse.urlencode(params)}"
        
        try:
            async with self.session.get(url, timeout=25) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    if len(data) > 5000:
                        b64_pixels = await self.run_in_executor(self._process_image_sync, data)
                        if b64_pixels:
                            self.image_cache[track_id] = b64_pixels
                            await self.display_b64(b64_pixels)
        except Exception as e:
            _LOGGER.error(f"Generation error: {e}")

    async def display_cached_art(self, track_id):
        """Displays art already in the session memory."""
        self.is_showing_art = True
        await self.send_pixoo_command({"Command": "Channel/OnOffScreen", "OnOff": 1})
        await self.display_b64(self.image_cache[track_id])

    async def display_b64(self, b64_data):
        """Sends raw pixel data to Pixoo."""
        await self.send_pixoo_command({
            "Command": "Draw/CommandList",
            "CommandList": [
                {"Command": "Draw/ResetHttpGifId"},
                {"Command": "Draw/SendHttpGif", "PicNum": 1, "PicWidth": 64, "PicOffset": 0,
                 "PicID": random.randint(1, 1000), "PicSpeed": 1000, "PicData": b64_data}
            ]
        })

    def _process_image_sync(self, image_data):
        """Optimized for LED luminous response."""
        try:
            img = Image.open(io.BytesIO(image_data)).convert("RGB")
            img = ImageOps.fit(img, (64, 64), method=Image.Resampling.LANCZOS)
            
            if self.boost:
                img = ImageEnhance.Color(img).enhance(2.0)
                img = ImageEnhance.Contrast(img).enhance(1.6)
                img = ImageEnhance.Sharpness(img).enhance(3.0)
            
            img = img.quantize(colors=64, method=Image.Quantize.MAXCOVERAGE).convert("RGB")
            return base64.b64encode(img.tobytes()).decode("utf-8")
        except: return None

    async def stop_art_mode(self, state):
        self.is_showing_art = False
        self.current_track_id = None
        if self.gen_task: self.gen_task.cancel()
        await self.send_pixoo_command({"Command": "Channel/SetIndex", "SelectIndex": self.previous_channel})
        if self.full_control and state == "off":
             await self.send_pixoo_command({"Command": "Channel/OnOffScreen", "OnOff": 0})

    async def get_current_channel(self):
        try:
            async with self.session.post(self.pixoo_url, json={"Command": "Channel/GetIndex"}, timeout=3) as r:
                return (await r.json()).get("SelectIndex", 0) if r.status == 200 else 0
        except: return 0 

    async def send_pixoo_command(self, payload):
        try:
            async with self.session.post(self.pixoo_url, json=payload, timeout=5): pass
        except: pass
