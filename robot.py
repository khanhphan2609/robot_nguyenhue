import time
import cv2
import random
import pygame
import threading
import numpy as np

# Hàm khởi tạo pygame mixer trước khi sử dụng
def init_pygame_mixer():
    try:
        pygame.mixer.init()  # Khởi động pygame mixer
        print("Pygame mixer initialized successfully.")
    except Exception as e:
        print("Lỗi khi khởi tạo pygame mixer:", e)

# Hàm hiển thị mắt với âm thanh đồng bộ
def display_eye(video_path):
    # Lấy kích thước màn hình động
    pygame.init()  # Khởi tạo Pygame để truy vấn thông tin màn hình
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    print(f"Màn hình hiện tại: {screen_width} x {screen_height}")

    # Khởi tạo VideoCapture
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Không thể mở video:", video_path)
        return

    # Lấy kích thước video gốc
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Tạo nền đen có kích thước khung hình phù hợp với màn hình
    background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

    # Tạo cửa sổ hiển thị video
    window_name = "ROBOT"

    loop_count = 0
    loop_max = 10

    while loop_count < loop_max:
        ret, frame = cap.read()  # Đọc từng frame của video
        if not ret:  # Nếu video kết thúc
            loop_count += 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Quay lại frame đầu tiên
            continue

        # Tính toán kích thước khung hình sau khi resize
        aspect_ratio = video_width / video_height
        new_width = min(screen_width, int(aspect_ratio * screen_height))
        new_height = min(screen_height, int(screen_width / aspect_ratio))

        # Resize frame để vừa với không gian màn hình
        resized_frame = cv2.resize(frame, (new_width, new_height))

        # Đặt video vào giữa nền đen
        start_x = (screen_width - new_width) // 2
        start_y = (screen_height - new_height) // 2
        end_x = start_x + new_width
        end_y = start_y + new_height

        # Xóa nền cũ và chèn video vào giữa
        background[:, :] = 0  # Đặt lại nền đen
        background[start_y:end_y, start_x:end_x] = resized_frame

        # Hiển thị video với nền đen
        cv2.imshow(window_name, background)

        # Thoát nếu người dùng nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Người dùng đã nhấn 'q', thoát chương trình.")
            break

    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()

# Hàm phát âm thanh chúc mừng năm mới
def play_greeting_audio(): 
    greeting_sounds = ['VN', 'EN', 'CHINA', 'FR', 'JP', 'KR', 'RUS']
    for i in greeting_sounds:
        audio_path = 'resouces/sound_greeting/HPNewYear_' + i + '.mp3'
        try:
            sound = pygame.mixer.Sound(audio_path)
            sound.play()
            time.sleep(1)  # Thêm thời gian nghỉ giữa các âm thanh
        except Exception as e:
            print("Lỗi khi phát âm thanh:", e)

# Hàm phát âm thanh
def play_audio(audio_path): 
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

happy = create_emotion_dict("resouces/happy/happy.mp4", gesture_happy)
roll = create_emotion_dict("resouces/roll/roll.mp4", gesture_roll)
heart = create_emotion_dict("resouces/heart/heart.mp4", gesture_heart)
blink = create_emotion_dict("resouces/blink/blink.mp4", gesture_blink)

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
