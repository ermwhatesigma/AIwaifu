import pygame
import win32api
import win32con
import win32gui
import sys
import random
import os
import time
import tkinter as tk
from tkinter import scrolledtext
import ollama
import threading
import queue

ollama_model = "ermwhatesigma420/hanna" #2.7b 1.6gb model. Use ermwhatesigam420\hanna:7B for the 7b model based of dolphin-mistral or you can use model of own choice
msg_queue = queue.Queue()
conversation_history = [{'role': 'system', 'content': 'Name= hanna, You are kind. ANSWER 10 WORDS MAX'}]

root = tk.Tk()
root.title("Waifu Controller")
root.geometry("640x640")
root.configure(bg='#FFC0CB')

label = tk.Label(root, text="Chat with Waifu:", bg='#FFC0CB')
label.pack(pady=5)

text_area = scrolledtext.ScrolledText(root, width=70, height=20, wrap=tk.WORD, bg="#FFF0F5")
text_area.config(state='disabled')
text_area.pack(padx=10, pady=10)

current_bubble_text = ""
bubble_start_time = 0
bubble_visible_time = 8
bubble_fade_time = 4

def handle_send(event=None):
    user_text = entry_field.get().strip()
    if user_text:
        text_area.config(state='normal')
        text_area.insert(tk.END, f"You: {user_text}\n")
        text_area.config(state='disabled')
        text_area.see(tk.END)
        entry_field.delete(0, tk.END)
        thread = threading.Thread(target=get_ai_response, args=(user_text,))
        thread.daemon = True
        thread.start()

def get_ai_response(prompt):
    try:
        conversation_history.append({'role': 'user', 'content': prompt})
        response = ollama.chat(model=ollama_model, messages=conversation_history)
        reply = response['message']['content']
        conversation_history.append({'role': 'assistant', 'content': reply})
        msg_queue.put(reply)
    except Exception as e:
        msg_queue.put(f"Error: {str(e)}")

SECONDS_PER_WORD = 1.2
FADE_TIME = 1.5

def display_ai_reply(reply):
    global current_bubble_text, bubble_start_time, bubble_visible_time, bubble_fade_time
    text_area.config(state='normal')
    text_area.insert(tk.END, f"Hanna: {reply}\n\n")
    text_area.config(state='disabled')
    text_area.see(tk.END)
    current_bubble_text = reply
    word_count = max(1, len(reply.split()))
    bubble_visible_time = word_count * SECONDS_PER_WORD
    bubble_fade_time = FADE_TIME
    bubble_start_time = time.time()

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        w, h = font.size(test_line)
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            w_word, _ = font.size(word)
            if w_word > max_width:
                part = ""
                for ch in word:
                    if font.size(part + ch)[0] <= max_width:
                        part += ch
                    else:
                        if part:
                            lines.append(part)
                        part = ch
                if part:
                    current_line = [part]
                else:
                    current_line = []
            else:
                current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

entry_field = tk.Entry(root, width=50)
entry_field.pack(padx=10, pady=10)
entry_field.bind("<Return>", handle_send)

def on_closing():
    global running
    running = False
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

pygame.init()
CHROMA_KEY = (255, 0, 128)

script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, r"waifu\waifu_idle.png") #you can use your won image of choice but you'll have to probably tune it on own choice

if not os.path.exists(image_path):
    pygame.quit()
    sys.exit()

temp_img = pygame.image.load(image_path)
WAIFU_W, WAIFU_H = temp_img.get_size()

extra_top_space = 70
CANVAS_W = WAIFU_W + 100
CANVAS_H = WAIFU_H + extra_top_space

screen = pygame.display.set_mode((CANVAS_W, CANVAS_H), pygame.NOFRAME)
waifu_img = temp_img.convert_alpha()

time.sleep(0.1)
hwnd = pygame.display.get_wm_info()["window"]

win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) |
                       win32con.WS_EX_LAYERED |
                       win32con.WS_EX_TOPMOST |
                       win32con.WS_EX_TOOLWINDOW)

win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*CHROMA_KEY), 0, win32con.LWA_COLORKEY)

SCREEN_W = win32api.GetSystemMetrics(0)
SCREEN_H = win32api.GetSystemMetrics(1)

min_x = SCREEN_W // 2
max_x = max(min_x, SCREEN_W - CANVAS_W - 50)
initial_x = max_x
min_window_y = 0
max_window_y = max(0, SCREEN_H - CANVAS_H - 50)
initial_y = max(0, SCREEN_H - CANVAS_H - 50)

x, y = initial_x, initial_y
clock = pygame.time.Clock()
velocity_x, velocity_y = 0.4, 0.0
running = True

while running:
    try:
        root.update()
    except:
        break

    while not msg_queue.empty():
        reply = msg_queue.get()
        display_ai_reply(reply)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            running = False

    if random.random() < 0.01:
        velocity_x = random.uniform(-0.45, 0.45)
        velocity_y = random.uniform(-0.15, 0.15)

    x += velocity_x
    y += velocity_y

    if x < min_x:
        x = min_x
        velocity_x = abs(velocity_x)
    if x > max_x:
        x = max_x
        velocity_x = -abs(velocity_x)

    if y < min_window_y:
        y = min_window_y
        velocity_y = abs(velocity_y)
    if y > max_window_y:
        y = max_window_y
        velocity_y = -abs(velocity_y)

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, int(x), int(y), CANVAS_W, CANVAS_H, win32con.SWP_NOACTIVATE)

    screen.fill(CHROMA_KEY)

    waifu_x = (CANVAS_W - WAIFU_W) // 2
    waifu_y = CANVAS_H - WAIFU_H - 20

    screen.blit(waifu_img, (waifu_x, waifu_y))

    if current_bubble_text:
        elapsed = time.time() - bubble_start_time
        total_time = bubble_visible_time + bubble_fade_time
        if elapsed >= total_time:
            current_bubble_text = ""
        else:
            if elapsed <= bubble_visible_time:
                alpha = 255
            else:
                fade_elapsed = elapsed - bubble_visible_time
                alpha = max(0, int(255 * (1 - (fade_elapsed / bubble_fade_time))))

            base_font_size = 36 #biggest font size
            min_font_size = 14 #smallest font size
            max_bubble_width = CANVAS_W - 120
            padding_x = 40
            padding_y = 22
            tail_h = 18
            margin_top = 8

            available_above = waifu_y - margin_top

            font_size = base_font_size
            font = pygame.font.SysFont("Arial", font_size, bold=True)
            lines = wrap_text(current_bubble_text, font, max_bubble_width - padding_x)
            line_height = font.get_linesize()
            bubble_h = (len(lines) * line_height) + padding_y * 2

            max_line_width = 0
            for ln in lines:
                w, _ = font.size(ln)
                if w > max_line_width:
                    max_line_width = w

            while (bubble_h + tail_h > available_above or max_line_width > (max_bubble_width - padding_x)) and font_size > min_font_size:
                font_size -= 2
                font = pygame.font.SysFont("Arial", font_size, bold=True)
                lines = wrap_text(current_bubble_text, font, max_bubble_width - padding_x)
                line_height = font.get_linesize()
                bubble_h = (len(lines) * line_height) + padding_y * 2
                max_line_width = 0
                for ln in lines:
                    w, _ = font.size(ln)
                    if w > max_line_width:
                        max_line_width = w

            bubble_w = min(max_bubble_width, max_line_width + padding_x)
            if bubble_w < 160:
                bubble_w = min(160, max_bubble_width)

            bubble_x = waifu_x + WAIFU_W // 2 - bubble_w // 2
            if bubble_x < 10:
                bubble_x = 10
            if bubble_x + bubble_w > CANVAS_W - 10:
                bubble_x = CANVAS_W - bubble_w - 10

            place_above = True 

            if place_above:
                bubble_y = waifu_y - bubble_h - tail_h
                if bubble_y < margin_top:
                    bubble_y = margin_top
                
                surf_h = bubble_h + tail_h
                bubble_surf = pygame.Surface((bubble_w, surf_h), pygame.SRCALPHA)
                rect_y = 0
                pygame.draw.rect(bubble_surf, (255, 255, 255, alpha), pygame.Rect(0, rect_y, bubble_w, bubble_h), border_radius=18)
                pygame.draw.rect(bubble_surf, (0, 0, 0, alpha), pygame.Rect(0, rect_y, bubble_w, bubble_h), 3, border_radius=18)
                tail_w = min(40, bubble_w // 8)
                point_list = [
                    (bubble_w // 2 - tail_w, bubble_h - 2),
                    (bubble_w // 2 + tail_w, bubble_h - 2),
                    (bubble_w // 2, bubble_h + tail_h) 
                ]
                pygame.draw.polygon(bubble_surf, (255, 255, 255, alpha), point_list)
                pygame.draw.lines(bubble_surf, (0, 0, 0, alpha), False, [point_list[0], point_list[2], point_list[1]], 3)
                text_y = rect_y + padding_y
                text_x = padding_x // 2
                render_font = pygame.font.SysFont("Arial", font_size, bold=True)
                for line in lines:
                    text_surf = render_font.render(line, True, (0, 0, 0))
                    if alpha < 255:
                        text_surf.set_alpha(alpha)
                    bubble_surf.blit(text_surf, (text_x, text_y))
                    text_y += line_height
                screen.blit(bubble_surf, (bubble_x, bubble_y))
            else:
                bubble_y = waifu_y + 30
                if bubble_y + bubble_h + tail_h > CANVAS_H - margin_top:
                    bubble_y = CANVAS_H - bubble_h - tail_h - margin_top
                surf_h = bubble_h + tail_h
                bubble_surf = pygame.Surface((bubble_w, surf_h), pygame.SRCALPHA)
                rect_y = tail_h
                pygame.draw.rect(bubble_surf, (255, 255, 255, alpha), pygame.Rect(0, rect_y, bubble_w, bubble_h), border_radius=18)
                pygame.draw.rect(bubble_surf, (0, 0, 0, alpha), pygame.Rect(0, rect_y, bubble_w, bubble_h), 3, border_radius=18)
                tail_w = min(40, bubble_w // 8)
                point_list = [
                    (bubble_w // 2 - tail_w, rect_y),
                    (bubble_w // 2 + tail_w, rect_y),
                    (bubble_w // 2, 0)
                ]
                pygame.draw.polygon(bubble_surf, (255, 255, 255, alpha), point_list)
                pygame.draw.lines(bubble_surf, (0, 0, 0, alpha), False, [point_list[0], point_list[2], point_list[1]], 3)
                text_y = rect_y + padding_y
                text_x = padding_x // 2
                render_font = pygame.font.SysFont("Arial", font_size, bold=True)
                for line in lines:
                    text_surf = render_font.render(line, True, (0, 0, 0))
                    if alpha < 255:
                        text_surf.set_alpha(alpha)
                    bubble_surf.blit(text_surf, (text_x, text_y))
                    text_y += line_height
                screen.blit(bubble_surf, (bubble_x, bubble_y))
    else:
        current_bubble_text = ""

    pygame.display.update()
    clock.tick(60)

pygame.quit()