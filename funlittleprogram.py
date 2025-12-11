import os
import tkinter as tk
import tkinter.font as tkfont
import ctypes
import random
import math

try:
    import pygame
except ImportError:
    pygame = None
    print("pygame is not installed. Music playback will be disabled.")

# --- UPDATED SCHEDULE WITH CHAOTIC TAGS ---
SCHEDULE = [
  {
    "text": "Frozen stairs,",
    "start": 12.4,
    "end": 16.1
  },
  {
    "text": "carpet in blood red",
    "start": 14.1,
    "end": 17.9
  },
  {
    "text": "Seating goodbyes left unsaid,",
    "start": 15.9,
    "end": 19.7
  },
   {
    "text": "Goodbyes left unsaid",
    "start": 17.9,
    "end": 21.7
  },
  {
    "text": "Despite our promises, here I am following your steps",
    "start": 19.7,
    "end": 26.5
  },
  {
    "text": "I’m following your steps",
    "start": 24.8,
    "end": 28.6
  },
  {
    "text": "Drop by drop",
    "start": 27.3,
    "end": 32.3
  },
  {
    "text": "As your unchanging reality dampen my sleeve",
    "start": 30.3,
    "end": 35.9
  },
  {
    "text": "You kissed them off",
    "start": 33.5,
    "end": 38.1
  },
  {
    "text": "Through the fibers of my handkerchief",
    "start": 36.1,
    "end": 42.4
  },
  # --- CHAOTIC STYLE ---
  {
    "text": "I AM FIRE",
    "start": 40.4,
    "end": 44.6,
    "style": "chaotic" 
  },
  {
    "text": "Burn those who dare to care for me",
    "start": 43.4,
    "end": 48.5
  },
  {
    "text": "And my fuel are memories,",
    "start": 47.5,
    "end": 51.8
  },
  {
    "text": "fuel are memories of you",
    "start": 49.6,
    "end": 53.3
  },
  {
    "text": "They perish with the heat, perish with the heat",
    "start": 51.0,
    "end": 56.3
  },
  {
    "text": "So I can move on",
    "start": 54.3,
    "end": 59.7
  },
  {
    "text": "Flower of iron",
    "start": 57.7,
    "end": 63.0
  },
  {
    "text": "Shrivelled up to hide the imposter in me",
    "start": 61.0,
    "end": 67.4
  },
  {
    "text": "“Hey, why did you leave?”",
    "start": 64.9,
    "end": 68.9
  },
   {
    "text": "“Why did you leave?”",
    "start": 66.9,
    "end": 70.4
  },
  {
    "text": "Don’t let those words out of me",
    "start": 68.2,
    "end": 72.5
  },
  {
    "text": "Imposter’s about to speak",
    "start": 70.2,
    "end": 74.0
  },
  {
    "text": "So I chewed on Huameitang",
    "start": 72.0,
    "end": 79.3
  },
  {
    "text": "For whom the shelves hold on to the pages,",
    "start": 77.3,
    "end": 82.3
  },
  {
    "text": "hold on to the pages",
    "start": 80.3,
    "end": 83.8
  },
  {
    "text": "Their pain, their joy were given value as they were rated",
    "start": 82.3,
    "end": 90.8
  },
  {
    "text": "Isn’t it ironic?",
    "start": 88.8,
    "end": 95.1
  },
  {
    "text": "Greed is unlimited;",
    "start": 93.1,
    "end": 97.2
  },
   {
    "text": "Freedom is a limited resource",
    "start": 94.7,
    "end": 99.6
  },
  {
    "text": "Extra large for you means less for me",
    "start": 97.7,
    "end": 102.9
  },
  {
    "text": "There’ll be less for me",
    "start": 100.9,
    "end": 104.6
  },
  {
    "text": "I banged the drums",
    "start": 103.9,
    "end": 108.8
  },
  {
    "text": "Court of hell",
    "start": 106.5,
    "end": 110.8
  },
  {
    "text": "Demanding a new trial",
    "start": 108.2,
    "end": 113.9
  },
  {
    "text": "You got the wrong head",
    "start": 111.9,
    "end": 115.9
  },
  {
    "text": "Would you take mine instead, take mine instead?",
    "start": 113.8,
    "end": 118.9
  },
  {
    "text": "Stop leading me on",
    "start": 116.9,
    "end": 122.1
  },
  {
    "text": "World of titan allows me to live",
    "start": 120.1,
    "end": 127.1
  },
  {
    "text": "Only in the mud down its feet",
    "start": 125.1,
    "end": 129.8
  },
  {
    "text": "Though you’re not with me,",
    "start": 127.8,
    "end": 131.5
  },
  {
    "text": "you’re not with me",
    "start": 129.4,
    "end": 133.0
  },
  {
    "text": "I’ll never admit defeat",
    "start": 131.0,
    "end": 135.0
  },
  {
    "text": "Cause when I thought that every nice thing about me has become Canxiang",
    "start": 132.5,
    "end": 141.6
  },
  {
    "text": "You showed me I still had an umbrella full of love inside me",
    "start": 139.6,
    "end": 146.7
  },
  {
    "text": "Without you I could never be",
    "start": 144.7,
    "end": 148.7
  },
  {
    "text": "So sincerely thank you for everything",
    "start": 146.7,
    "end": 151.6
  },
  {
    "text": "It pains me to think",
    "start": 148.6,
    "end": 153.7
  },
  {
    "text": "That my happiness turned out to be one of those fingers",
    "start": 152.1,
    "end": 157.4
  },
  {
    "text": "that strangled you until you couldn’t breathe",
    "start": 155.3,
    "end": 160.9
  },
  {
    "text": "Not ashamed to go this way",
    "start": 158.9,
    "end": 162.9
  },
  {
    "text": "I just want to choose my fate",
    "start": 159.7,
    "end": 164.7
  },
  {
    "text": "I’m on my last white rabbit Naitang",
    "start": 162.7,
    "end": 169.0
  },
  # --- CHAOTIC STYLE ---
  {
    "text": "I AM IRON",
    "start": 168.5,
    "end": 173.2,
    "style": "chaotic"
  },
  {
    "text": "In my blood it streams roots deep",
    "start": 170.2,
    "end": 176.8
  },
  {
    "text": "With bruises on my knees,",
    "start": 174.8,
    "end": 177.9
  },
  {
    "text": "bruises on my knees",
    "start": 176.3,
    "end": 179.9
  },
  {
    "text": "And ribs crushed down to pieces,",
    "start": 177.9,
    "end": 182.2
  },
   {
    "text": "crushed down to pieces",
    "start": 179.9,
    "end": 184.3
  },
  {
    "text": "Nothing left to hold on",
    "start": 181.3,
    "end": 186.3
  },
  {
    "text": "Actually wait",
    "start": 184.3,
    "end": 188.9
  },
  {
    "text": "I do have one regret",
    "start": 186.9,
    "end": 191.1
  },
  {
    "text": "That day before you left me",
    "start": 189.1,
    "end": 193.8
  },
  {
    "text": "“You’re my everything”",
    "start": 193.8,
    "end": 197.2
  },
  {
    "text": "Before my thoughts began to speak",
    "start": 195.2,
    "end": 199.9
  },
  {
    "text": "I bit my lip, said nothing",
    "start": 196.9,
    "end": 200.7
  },
  {
    "text": "And just sucked on Maiyatang",
    "start": 198.7,
    "end": 205.0
  }
]


# Default fade durations (seconds)
DEFAULT_FADE_IN = 1.0
DEFAULT_FADE_OUT = 1.0

# Fade update interval (ms)
FADE_INTERVAL_MS = 40

# Font
FONT_NAME = "Segoe UI"
FONT_SIZE = 40
FONT_WEIGHT = "normal"

# Glow config
DEFAULT_GLOW_COLOR = "#fff3a0"  # subtle bluish glow
CHAOTIC_GLOW_COLOR = "#ff4500"  # Orange/Fire color

# --- CINDER CONFIG ---
CINDER_COLOR = "#ff6f00"  # Deep orange/ember
CINDER_SPAWN_RATE_LOW = 0.1  # Chance to spawn per frame (Fire phase)
CINDER_SPAWN_RATE_HIGH = 0.4 # Chance to spawn per frame (Iron phase)
CINDER_LIFETIME = 600        # Frames (approx 20 seconds at 30ms interval)

# --- FIRE PARTICLE CONFIG ---
FIRE_COLORS = ["#ff3300", "#ff6600", "#ffcc00", "#ffff00"] # Red to Yellow gradient
FIRE_GRAVITY = -3.0  # Upward acceleration
FIRE_WIND_NORMAL = 0
FIRE_WIND_INTENSE = 4.0 # Strong breeze to the right

GLOW_OFFSETS = [
    (-2, 0), (2, 0), (0, -2), (0, 2),
    (-2, -2), (2, -2), (-2, 2), (2, 2),
]

# Windows click-through flags
GWL_EXSTYLE = -20
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020


class Overlay:
    def __init__(self, schedule, music_path=None):
        # Prepare schedule (compute durations)
        self.sentences = self._prepare_schedule(schedule)

        # Looping flag
        self.loop_enabled = False

        # Root is a tiny invisible "manager" window
        self.root = tk.Tk()
        self.bg_color = "black"

        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.configure(bg=self.bg_color)
        self.root.geometry("1x1+0+0")
        try:
            self.root.wm_attributes("-transparentcolor", self.bg_color)
        except tk.TclError:
            pass
        self.root.attributes("-alpha", 0.0)

        # Font for measuring
        self.font = tkfont.Font(family=FONT_NAME, size=FONT_SIZE, weight=FONT_WEIGHT)

        # Padding around text
        self.padding_x = 40
        self.padding_y = 40

        # --- Cinder State ---
        self.cinders = [] # List of particles
        self.cinder_intensity = 0 # 0=Off, 1=Low, 2=High

        self.fire_particles = []
        self.fire_state = 0 # 0=Off, 1=Standard Fire, 2=Intense/Right Spread
        
        # --- Background Layer for Cinders ---
        # A full-screen persistent window acting as the particle canvas
        self.bg_top = tk.Toplevel(self.root)
        self.bg_top.overrideredirect(True)
        self.bg_top.wm_attributes("-topmost", True) # Keep behind text, but top of desktop
        self.bg_top.configure(bg="black")
        
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.bg_top.geometry(f"{sw}x{sh}+0+0")

        # Make transparent
        try:
            self.bg_top.wm_attributes("-transparentcolor", "black")
        except tk.TclError:
            pass
            
        # Canvas for particles
        self.bg_canvas = tk.Canvas(self.bg_top, width=sw, height=sh, 
                                   bg="black", highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        
        # Apply click-through to background
        self._make_click_through(self.bg_top)

        # Start the physics loop immediately
        self._update_cinders_loop()
        self._update_fire_loop()

        # Last used angle for less redundant rotations
        self.last_angle = None

        # Pre-compute a base window size from the longest sentence
        if self.sentences:
            longest_text = max(self.sentences, key=lambda s: len(s["text"]))["text"]
        else:
            longest_text = "X"

        text_width = self.font.measure(longest_text)
        text_height = self.font.metrics("linespace")

        self.base_window_width = text_width + self.padding_x
        self.base_window_height = text_height + self.padding_y

        # ESC exits the whole overlay
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Ctrl+L toggles looping
        self.root.bind("<Control-l>", self._toggle_loop_key)

        # Track total run duration (for looping)
        self.total_run_ms = 0
        if self.sentences:
            last_end = max(s["end"] for s in self.sentences)
            self.total_run_ms = int(last_end * 1000)

        # ---- music setup ----
        self.music_path = music_path or os.path.join("music", "IronLotus_2.mp3")
        self.music_enabled = pygame is not None and os.path.exists(self.music_path)
        self.music_loaded = False

        if not self.music_enabled:
            if pygame is None:
                print("Music disabled: pygame is not installed. Install with 'pip install pygame'.")
            else:
                print(f"Music disabled: file not found at {self.music_path!r}.")

    # ---------- Music helpers ----------

    def _ensure_music_loaded(self):
        if not self.music_enabled:
            return False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            if not self.music_loaded:
                pygame.mixer.music.load(self.music_path)
                self.music_loaded = True
            return True
        except Exception as e:
            print(f"Error initializing/loading music: {e}")
            self.music_enabled = False
            return False

    def _start_music(self):
        if not self._ensure_music_loaded():
            return
        try:
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error playing music: {e}")
            self.music_enabled = False

    def _restart_music(self):
        if not self._ensure_music_loaded():
            return
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error restarting music: {e}")
            self.music_enabled = False

    # ---------- Public API: loop control ----------

    def set_loop(self, enabled: bool):
        self.loop_enabled = bool(enabled)
        print(f"[Overlay] Looping is now {'ON' if self.loop_enabled else 'OFF'}")

    def _toggle_loop_key(self, event=None):
        self.set_loop(not self.loop_enabled)

    # ---------- Schedule prep ----------

    def _prepare_schedule(self, schedule):
        sorted_sched = sorted(schedule, key=lambda s: s["start"])
        for s in sorted_sched:
            s["duration"] = max(0.1, s["end"] - s["start"])
        return sorted_sched

    # ---------- Click-through helper ----------

    def _make_click_through(self, window):
        try:
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            styles = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            styles |= WS_EX_LAYERED | WS_EX_TRANSPARENT
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, styles)
        except Exception:
            # Non-Windows or error: just ignore
            pass

    # ---------- Rotation helper (less redundant) ----------

    def _get_next_angle(self, min_angle=-20, max_angle=20, min_diff=10):
        if self.last_angle is None:
            angle = random.uniform(min_angle, max_angle)
        else:
            attempts = 0
            angle = self.last_angle
            while attempts < 20:
                candidate = random.uniform(min_angle, max_angle)
                if abs(candidate - self.last_angle) >= min_diff:
                    angle = candidate
                    break
                attempts += 1
            if abs(angle - self.last_angle) < min_diff:
                angle = min_angle if self.last_angle > 0 else max_angle

        self.last_angle = angle
        return angle

    # ---------- Entry point ----------
    def _set_cinder_intensity(self, level):
        """Helper to change spawn rate via scheduler."""
        self.cinder_intensity = level

    def _update_cinders_loop(self):
        """Main physics loop for particles with Fading and Shrinking."""
        sw = self.bg_top.winfo_screenwidth()
        sh = self.bg_top.winfo_screenheight()

        # 1. SPAWN LOGIC
        spawn_chance = 0
        if self.cinder_intensity == 1:
            spawn_chance = CINDER_SPAWN_RATE_LOW
        elif self.cinder_intensity == 2:
            spawn_chance = CINDER_SPAWN_RATE_HIGH

        if random.random() < spawn_chance:
            # Random starting X
            x = random.randint(0, sw)
            y = sh + 10 
            
            # Initial size (Store original radius to shrink later)
            radius = random.randint(2, 5)
            
            # Create oval (start solid)
            item = self.bg_canvas.create_oval(x, y, x, y, 
                                              fill=CINDER_COLOR, outline="", stipple="")
            
            self.cinders.append({
                "id": item,
                "x": float(x),
                "y": float(y),
                "radius": float(radius), 
                "speed": random.uniform(1.0, 2.5),
                "sway_freq": random.uniform(0.05, 0.1),
                "sway_amp": random.uniform(0.5, 2.0),
                "sway_phase": random.uniform(0, 6.28),
                "life": CINDER_LIFETIME,
                "max_life": CINDER_LIFETIME,
                "current_stipple": "" # Track current state to avoid over-updating
            })

        # 2. UPDATE LOGIC
        to_remove = []
        for p in self.cinders:
            p["life"] -= 1
            if p["life"] <= 0:
                to_remove.append(p)
                continue

            # --- MOVEMENT ---
            p["y"] -= p["speed"]
            current_sway = math.sin(p["life"] * p["sway_freq"] + p["sway_phase"]) * p["sway_amp"]
            draw_x = p["x"] + current_sway

            # --- FADING & SHRINKING ---
            life_percent = p["life"] / p["max_life"]
            
            # Determine Transparency (Stipple) based on life percentage
            # 'gray75' is 75% opaque, 'gray50' is 50%, etc.
            new_stipple = ""
            if life_percent < 0.2:    # Last 20% of life
                new_stipple = "gray12"
            elif life_percent < 0.4:  # Last 40% of life
                new_stipple = "gray25"
            elif life_percent < 0.6:  # Last 60% of life
                new_stipple = "gray50"
            elif life_percent < 0.8:  # Last 80% of life
                new_stipple = "gray75"
            
            # Determine Size (Shrink slightly near death)
            current_r = p["radius"]
            if life_percent < 0.3:
                current_r = max(0, p["radius"] * (life_percent / 0.3))

            # Update Canvas
            self.bg_canvas.coords(p["id"], 
                                  draw_x, p["y"], 
                                  draw_x + current_r, p["y"] + current_r)
            
            # Only update stipple if it changed (optimization)
            if new_stipple != p["current_stipple"]:
                try:
                    self.bg_canvas.itemconfig(p["id"], stipple=new_stipple)
                    p["current_stipple"] = new_stipple
                except tk.TclError:
                    pass

        # 3. CLEANUP
        for p in to_remove:
            self.bg_canvas.delete(p["id"])
            self.cinders.remove(p)

        # Loop
        self.root.after(30, self._update_cinders_loop)
    
    def _set_fire_state(self, state):
        self.fire_state = state

    def _update_fire_loop(self):
        """Separate physics loop for bottom-screen and side fire particles."""
        sw = self.bg_top.winfo_screenwidth()
        sh = self.bg_top.winfo_screenheight()

        # --- 1. SPAWN LOGIC ---
        
        # A. BOTTOM FIRE (Standard)
        spawn_count = 0
        if self.fire_state == 1:
            spawn_count = 2
        elif self.fire_state == 2:
            spawn_count = 6
            
        for _ in range(spawn_count):
            # Normal bottom spawn logic
            x = random.randint(0, sw)
            if self.fire_state == 2 and random.random() < 0.3:
                x = random.randint(0, sw // 2)
            y = sh + 5
            radius = random.randint(4, 10)
            color = random.choice(FIRE_COLORS)
            
            # Bottom Fire Physics
            x_vel = random.uniform(-0.5, 0.5) 
            if self.fire_state == 2:
                # The "Wind" effect for bottom fire
                x_vel = random.uniform(2.0, 6.0) 

            item = self.bg_canvas.create_oval(x, y, x, y, fill=color, outline="", stipple="")
            self.fire_particles.append({
                "id": item, "x": float(x), "y": float(y),
                "vx": x_vel, 
                "vy": random.uniform(-2.0, -5.0),
                "life": random.randint(20, 40), "max_life": 40, "radius": radius
            })

        # B. SIDE FIRE (New: Only during Iron Phase)
        if self.fire_state == 2:
            # Spawn 3 particles per side per frame
            for _ in range(3):
                radius = random.randint(3, 8)
                color = random.choice(FIRE_COLORS)
                
                # --- LEFT SIDE ---
                item_l = self.bg_canvas.create_oval(-10, -10, -5, -5, fill=color, outline="", stipple="")
                self.fire_particles.append({
                    "id": item_l,
                    "x": float(random.randint(0, 20)),       # Close to left edge
                    # CHANGED: From (sh // 2) to 0 to cover full height
                    "y": float(random.randint(0, sh)),       
                    "vx": random.uniform(0.0, 1.5),          # Slight drift inward
                    "vy": random.uniform(-4.0, -8.0),        # Fast upward burn
                    "life": random.randint(15, 30), "max_life": 30, "radius": radius
                })

                # --- RIGHT SIDE ---
                item_r = self.bg_canvas.create_oval(-10, -10, -5, -5, fill=color, outline="", stipple="")
                self.fire_particles.append({
                    "id": item_r,
                    "x": float(random.randint(sw - 20, sw)), # Close to right edge
                    # CHANGED: From (sh // 2) to 0 to cover full height
                    "y": float(random.randint(0, sh)),       
                    "vx": random.uniform(-1.5, 0.0),         # Slight drift inward
                    "vy": random.uniform(-4.0, -8.0),        # Fast upward burn
                    "life": random.randint(15, 30), "max_life": 30, "radius": radius
                })

        # --- 2. UPDATE LOGIC ---
        to_remove = []
        for p in self.fire_particles:
            p["life"] -= 1
            if p["life"] <= 0:
                to_remove.append(p)
                continue
                
            # Physics (vx/vy handles the difference between bottom and side fire)
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            
            # Shrink
            life_pct = p["life"] / p["max_life"]
            r = p["radius"] * life_pct
            
            # Fade
            stipple = ""
            if life_pct < 0.3: stipple = "gray50"
            if life_pct < 0.1: stipple = "gray25"
            
            try:
                self.bg_canvas.coords(p["id"], p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r)
                if stipple:
                    self.bg_canvas.itemconfig(p["id"], stipple=stipple)
            except tk.TclError:
                pass

        # --- 3. CLEANUP ---
        for p in to_remove:
            self.bg_canvas.delete(p["id"])
            self.fire_particles.remove(p)

        # Loop
        self.root.after(30, self._update_fire_loop)

    def start(self):
        if not self.sentences:
            return

        # Start music and schedule one "run" of all sentences
        if self.music_enabled:
            self._start_music()

        self._schedule_run()
        self.root.mainloop()

    def _schedule_run(self):
        self._set_cinder_intensity(0) 
        self._set_fire_state(0) # <--- Reset fire
        
        # 2. Schedule "I AM FIRE" (approx 40.4s) -> Low Cinders + Normal Fire
        self.root.after(40400, lambda: self._set_cinder_intensity(1))
        self.root.after(40400, lambda: self._set_fire_state(1)) # <--- Fire Phase 1
        
        # 3. Schedule "I AM IRON" (approx 168.0s) -> High Cinders + Intense Rightward Fire
        self.root.after(168000, lambda: self._set_cinder_intensity(2))
        self.root.after(168000, lambda: self._set_fire_state(2)) # <--- Fire Phase 2 (Spread Right)

        for sentence in self.sentences:
            delay_ms = int(sentence["start"] * 1000)
            self.root.after(delay_ms, lambda s=sentence: self._play_sentence(s))

        if self.total_run_ms > 0:
            self.root.after(self.total_run_ms + 200, self._on_run_finished)

    def _on_run_finished(self):
      # --- Cinder Reset ---
        self.cinder_intensity = 0
        for p in self.cinders:
            self.bg_canvas.delete(p["id"])
        self.cinders.clear()

        self.fire_state = 0
        for p in self.fire_particles:
            self.bg_canvas.delete(p["id"])
        self.fire_particles.clear()

        # --------------------
        if not self.loop_enabled:
            # Give a moment for last fade-out to finish, then quit
            self.root.after(1000, self.root.destroy)
            return

        # If no music, just loop immediately like before
        if not self.music_enabled:
            self._schedule_run()
            return

        # Wait until the music is finished, then restart both music and text
        def wait_for_music():
            try:
                busy = pygame.mixer.music.get_busy()
            except Exception as e:
                print(f"Error checking music state: {e}")
                self.music_enabled = False
                self._schedule_run()
                return

            if busy:
                # Song still playing; check again shortly
                self.root.after(200, wait_for_music)
            else:
                # Song finished -> restart song and text together
                self._restart_music()
                self._schedule_run()

        wait_for_music()

    # ---------- Single sentence window + animation ----------

    def _play_sentence(self, sentence):
        # Each sentence spawns its own transparent, click-through window
        SentenceWindow(self, sentence)


class SentenceWindow:
    def __init__(self, overlay: Overlay, sentence: dict):
        self.overlay = overlay
        self.sentence = sentence
        self.running = True  # Flag to stop animation threads on destroy

        # Check for Chaos style
        self.is_chaotic = self.sentence.get("style") == "chaotic"
        
        # Set Glow Color based on style
        self.glow_color = CHAOTIC_GLOW_COLOR if self.is_chaotic else DEFAULT_GLOW_COLOR

        # Track font size for expansion effects
        self.current_font_size = float(FONT_SIZE)

        # Store current raw text (unformatted)
        self.current_raw_text = ""

        # Separate window for this sentence
        self.top = tk.Toplevel(self.overlay.root)
        self.top.overrideredirect(True)
        self.top.wm_attributes("-topmost", True)
        self.top.configure(bg=self.overlay.bg_color)

        # Initial size based on precomputed base window
        self.window_width = self.overlay.base_window_width
        self.window_height = self.overlay.base_window_height

        # Start centered; will move randomly later
        self.top.update_idletasks()
        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()
        x = (sw - self.window_width) // 2
        y = (sh - self.window_height) // 2
        self.top.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        # Canvas for drawing text
        self.canvas = tk.Canvas(
            self.top,
            width=self.window_width,
            height=self.window_height,
            bg=self.overlay.bg_color,
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        # Main (bright) text item
        self.text_item = self.canvas.create_text(
            self.window_width // 2,
            self.window_height // 2,
            text="",
            font=(FONT_NAME, FONT_SIZE, FONT_WEIGHT),
            fill="white",
        )

        # Glow text items (created later)
        self.glow_items = []

        try:
            self.top.wm_attributes("-transparentcolor", self.overlay.bg_color)
        except tk.TclError:
            pass

        self.top.attributes("-alpha", 0.0)

        # Make this window click-through
        self.overlay._make_click_through(self.top)
        
        # Handle cleanup
        self.top.bind("<Destroy>", self._on_destroy)

        # Kick off animation
        self._start_animation()

    def _on_destroy(self, event):
        self.running = False

    def _set_text_display(self, display_text: str):
        """Update main text and all glow copies on the canvas."""
        try:
            self.canvas.itemconfig(self.text_item, text=display_text)
            for item in self.glow_items:
                self.canvas.itemconfig(item, text=display_text)
        except tk.TclError:
            # Window might be closed
            pass

    def _start_expansion_loop(self):
        """Gradually increases font size for visual expansion."""
        if not self.running: return

        # Increment size
        self.current_font_size += 0.25
        new_font = (FONT_NAME, int(self.current_font_size), FONT_WEIGHT)

        try:
            self.canvas.itemconfig(self.text_item, font=new_font)
            for item in self.glow_items:
                self.canvas.itemconfig(item, font=new_font)
        except tk.TclError:
            pass
        
        # Run every 30ms for smooth expansion
        self.top.after(30, self._start_expansion_loop)

    def _position_randomly(self):
        self.top.update_idletasks()
        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()

        if self.is_chaotic:
            # Force Center Screen
            x = (sw - self.window_width) // 2
            y = (sh - self.window_height) // 2
        else:
            # Random Position
            margin = 50
            center_x = random.randint(margin, max(margin, sw - margin))
            center_y = random.randint(margin, max(margin, sh - margin))
            x = center_x - self.window_width // 2
            y = center_y - self.window_height // 2

        self.top.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")


    def _start_animation(self):
        text = self.sentence["text"]
        total = self.sentence["duration"]

        # Allocate time for fade in, typewriter, fade out
        fade_in = min(DEFAULT_FADE_IN, total / 3)
        fade_out = min(DEFAULT_FADE_OUT, total / 3)
        typing_duration = max(0.0, total - fade_in - fade_out)

        fade_in_steps = max(1, int(fade_in * 1000 / FADE_INTERVAL_MS)) if fade_in > 0 else 0
        fade_out_steps = max(1, int(fade_out * 1000 / FADE_INTERVAL_MS)) if fade_out > 0 else 0

        # Rotation Logic
        if self.is_chaotic:
            angle = 0  # No rotation for chaotic
        else:
            angle = self.overlay._get_next_angle()
            
        try:
            self.canvas.itemconfig(self.text_item, angle=angle)
        except tk.TclError:
            angle = 0.0
            self.overlay.last_angle = angle

        # Measure text to adjust window size
        self.current_raw_text = text 
        self._set_text_display(text)
        self.top.update_idletasks()
        bbox = self.canvas.bbox(self.text_item)

        if bbox:
            x1, y1, x2, y2 = bbox
            width = x2 - x1
            height = y2 - y1
        else:
            width = self.overlay.font.measure(text)
            height = self.overlay.font.metrics("linespace")

        # Add some padding for glow
        glow_pad = 2 * max((abs(dx) for dx, dy in GLOW_OFFSETS), default=0)

        # Size the window based on THIS sentence only
        # Get screen dimensions
        sw = self.top.winfo_screenwidth()
        sh = self.top.winfo_screenheight()

        if self.is_chaotic:
            # 1. CHAOTIC: Make window FULL SCREEN so ripples can go everywhere
            self.window_width = sw
            self.window_height = sh
        else:
            # 2. NORMAL: Size tightly around text
            self.window_width = int(width + self.overlay.padding_x + glow_pad)
            self.window_height = int(height + self.overlay.padding_y + glow_pad)
            
            # Clamp normal windows so they don't look weird
            self.window_width = min(self.window_width, max(200, sw - 100))
            self.window_height = min(self.window_height, max(100, sh - 100))


        # Resize canvas and window
        self.canvas.config(width=self.window_width, height=self.window_height)
        cx = self.window_width // 2
        cy = self.window_height // 2
        self.canvas.coords(self.text_item, cx, cy)
        self.top.geometry(f"{self.window_width}x{self.window_height}+0+0")

        # Create glow copies around the main text
        self.glow_items = []
        for dx, dy in GLOW_OFFSETS:
            item = self.canvas.create_text(
                cx + dx,
                cy + dy,
                text="",  # will be filled via _set_text
                font=(FONT_NAME, FONT_SIZE, FONT_WEIGHT),
                fill=self.glow_color, 
            )
            try:
                self.canvas.itemconfig(item, angle=angle)
            except tk.TclError:
                pass
            self.glow_items.append(item)

        # Make sure main text is on top
        self.canvas.tag_raise(self.text_item)

        # Hide text again for typewriter effect
        self.current_raw_text = ""
        self._set_text_display("")

        # Start fully invisible
        self.top.attributes("-alpha", 0.0)

        # Position (Center if chaotic, Random if not)
        self._position_randomly()

        # START EXPANSION LOOP IF CHAOTIC
        if self.is_chaotic:
            self._start_expansion_loop()
            self._start_ripple_sequence()

        # ---- nested helpers ----

        def start_typing():
            if not text:
                start_fade_out()
                return

            if typing_duration <= 0:
                # No time for typing effect, just show full text
                self.current_raw_text = text
                self._set_text_display(text)
                start_fade_out()
                return

            char_delay_ms = max(1, int(typing_duration * 1000 / max(1, len(text))))

            def type_char(i=0):
                if not self.running: return
                if i <= len(text):
                    # Update the raw text
                    self.current_raw_text = text[:i]
                    self._set_text_display(self.current_raw_text)

                    if i < len(text):
                        self.top.after(char_delay_ms, lambda: type_char(i + 1))
                    else:
                        # Done typing, small delay then fade out
                        self.top.after(FADE_INTERVAL_MS, start_fade_out)

            type_char(0)

        def start_fade_out():
            if not self.running: return
            if fade_out_steps <= 0:
                self.top.attributes("-alpha", 0.0)
                self.current_raw_text = ""
                self._set_text_display("")
                self.top.destroy()
                return

            def do_fade_out(step=0):
                if not self.running: return
                alpha = 1.0 - step / fade_out_steps
                self.top.attributes("-alpha", max(0.0, alpha))
                if step < fade_out_steps:
                    self.top.after(FADE_INTERVAL_MS, lambda: do_fade_out(step + 1))
                else:
                    self.top.attributes("-alpha", 0.0)
                    self.current_raw_text = ""
                    self._set_text_display("")
                    self.top.destroy()

            do_fade_out(0)

        def start_fade_in():
            if fade_in_steps <= 0:
                self.top.attributes("-alpha", 1.0)
                start_typing()
                return

            def do_fade_in(step=0):
                if not self.running: return
                alpha = step / fade_in_steps
                self.top.attributes("-alpha", max(0.0, min(1.0, alpha)))
                if step < fade_in_steps:
                    self.top.after(FADE_INTERVAL_MS, lambda: do_fade_in(step + 1))
                else:
                    self.top.attributes("-alpha", 1.0)
                    start_typing()

            do_fade_in(0)

        # Kick off the fade-in -> typing -> fade-out chain
        start_fade_in()
        # --- RIPPLE / SHOCKWAVE METHODS ---

    def _start_ripple_sequence(self):
        """Spawns multiple expanding rings to simulate a shockwave."""
        if not self.running: return

        cx = self.window_width // 2
        cy = self.window_height // 2
        
        # Spawn 3 rings with slight delays (0ms, 200ms, 400ms)
        for i in range(3):
            delay = i * 200 
            self.top.after(delay, lambda: self._spawn_single_ring(cx, cy))

    def _spawn_single_ring(self, cx, cy):
        if not self.running: return
        
        # INCREASED: Start thickness 25 (was 12) so it lasts longer
        start_thickness = 25
        
        item = self.canvas.create_oval(cx, cy, cx, cy, outline=self.glow_color, width=start_thickness)
        
        self.canvas.tag_lower(item) 
        
        self._animate_ring(item, cx, cy, radius=0, thickness=start_thickness)

    def _animate_ring(self, item, cx, cy, radius, thickness):
        if not self.running: return

        # INCREASED: Expand by 25 pixels per frame (was 15) - faster shockwave
        radius += 25
        
        # DECREASED: Fade by 0.3 per frame (was 0.5) - stays visible longer
        thickness -= 0.3

        # Math check: 25 start / 0.3 fade = ~83 frames
        # 83 frames * 25 speed = ~2000 pixels distance (Covers 1080p/1440p/4k screens easily)

        if thickness <= 0 or radius > max(self.window_width, self.window_height):
            self.canvas.delete(item)
            return

        x1 = cx - radius
        y1 = cy - radius
        x2 = cx + radius
        y2 = cy + radius

        try:
            self.canvas.coords(item, x1, y1, x2, y2)
            self.canvas.itemconfig(item, width=thickness)
            self.top.after(30, lambda: self._animate_ring(item, cx, cy, radius, thickness))
        except tk.TclError:
            pass

if __name__ == "__main__":
    overlay = Overlay(SCHEDULE)  # uses music/IronLotus_2.mp3 by default
    # Turn looping on or off here:
    overlay.set_loop(True)   # set to False if you don't want looping
    overlay.start()