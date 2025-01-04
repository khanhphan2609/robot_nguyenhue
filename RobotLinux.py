import time
import cv2
import random
import pygame
import threading
import numpy as np
import os

# Đặt thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Đặt thư mục của các tài nguyên (Resources)
RESOURCES_DIR = os.path.join(BASE_DIR, '..', 'Resources')

# Hàm khởi tạo pygame mixer trước khi sử dụng
def init_pygame_mixer():
    try:
        pygame.mixer.init()  # Khởi động pygame mixer
        print("Pygame mixer initialized successfully.")
    except Exception as e:
        print("Lỗi khi khởi tạo pygame mixer:", e)

# Hàm hiển thị mắt với âm thanh đồng bộ
def display_eye(video_path):
    # Khởi tạo Pygame để lấy thông tin màn hình
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    print(f"Màn hình hiện tại: {screen_width} x {screen_height}")

    video_path = os.path.join(RESOURCES_DIR, video_path)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Không thể mở video:", video_path)
        return

    # Lấy kích thước video
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Kích thước khung hình nền (màu đen)
    background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)  # Khung màu đen

    # Tạo cửa sổ hiển thị video
    window_name = "ROBOT"

    loop_count = 0
    loop_max = 10

    while loop_count < loop_max:
        ret, frame = cap.read()  # Đọc từng frame của video
        if not ret:  # Nếu video kết thúc
            loop_count = loop_count + 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Quay lại frame đầu tiên
            continue

        # Thay đổi kích thước frame để vừa với kích thước màn hình
        frame_resized = cv2.resize(frame, (screen_width, screen_height))

        # Xóa nền cũ và chèn video vào giữa
        background[:, :] = frame_resized

        # Hiển thị video với nền đen
        cv2.imshow(window_name, background)

        # Thoát nếu người dùng nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Người dùng đã nhấn 'q', thoát chương trình.")
            break

    # Giải phóng tài nguyên
    cap.release()
    pygame.quit()

# Hàm phát âm thanh chúc mừng năm mới 
def play_greeting_audio(): 
    greeting_sounds = ['VN', 'EN', 'CHINA', 'FR', 'JP', 'KR', 'RUS']
    for i in greeting_sounds:
        audio_path = os.path.join(RESOURCES_DIR, 'Sound_Greeting', f'HPNewYear_{i}.mp3')
        try:
            sound = pygame.mixer.Sound(audio_path)
            sound.play()
            time.sleep(1)  # Thêm thời gian nghỉ giữa các âm thanh
        except Exception as e:
            print("Lỗi khi phát âm thanh:", e)

# Hàm phát âm thanh
def play_audio(audio_path): 
    audio_path = os.path.join(RESOURCES_DIR, audio_path)
    try:
        sound = pygame.mixer.Sound(audio_path)
        sound.play()
    except Exception as e:
        print("Lỗi khi phát âm thanh:", e)

def display_eye_with_audio(video_path):
    # Phát âm thanh trong một thread riêng biệt
    audio_thread = threading.Thread(target=play_greeting_audio)
    audio_thread.start()
    
    # Phát video
    display_eye(video_path)

    # Đợi âm thanh kết thúc
    audio_thread.join()

# Định nghĩa các hàm gesture
def gesture_happy():
    return "Hành động: Vẫy tay vui vẻ!"

def gesture_roll():
    return "Hành động: Xoay tròn mắt!"

def gesture_heart():
    return "Hành động: Tạo hình trái tim bằng tay!"

def gesture_blink():
    return "Hành động: Chớp mắt liên tục!"

# Tạo danh sách trạng thái cảm xúc
def create_emotion_dict(eye, gesture):
    return {
        "eye": eye,
        "gesture": gesture
    }

happy = create_emotion_dict("Happy/happy.mp4", gesture_happy)
roll = create_emotion_dict("Roll/roll.mp4", gesture_roll)
heart = create_emotion_dict("Heart/heart.mp4", gesture_heart)
blink = create_emotion_dict("Blink/blink.mp4", gesture_blink)

def main():
    # Khởi tạo pygame mixer
    init_pygame_mixer()

    emotions = [happy, roll, heart, blink]

    while True:
        selected_emotion = random.choice(emotions)
        print(selected_emotion)
        display_eye_with_audio(selected_emotion["eye"])

if __name__ == "__main__":
    main()
