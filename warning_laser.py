import pygame
import time

# Khởi tạo Pygame
pygame.init()

# Khởi tạo cửa sổ
WIDTH, HEIGHT = 200, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flashing Alert Icon")

# Khai báo màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load hình ảnh biểu tượng
alert_icon = pygame.image.load("asset/img/icons/warning.png")
# Scale hình ảnh biểu tượng để phù hợp với kích thước cửa sổ
alert_icon = pygame.transform.scale(alert_icon, (50, 50))
count = 0
# Cài đặt biến cho vòng lặp thời gian
last_toggle_time = 0
show_icon = True
display_duration = 2

# Vòng lặp chính
running = True
while running:
    # Kiểm tra và xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Xác định thời gian hiện tại
    current_time = time.time()

    # Tính toán thời gian kể từ lần cuối toggle
    time_since_last_toggle = current_time - last_toggle_time


    # Nếu đã qua 0.5 giây, thay đổi trạng thái của biểu tượng và cập nhật thời gian
    if time_since_last_toggle >= 0.5:
        show_icon = not show_icon
        last_toggle_time = current_time
        count += 1

    if time_since_last_toggle >= display_duration:
        show_icon = False

    # Xóa màn hình
    screen.fill(WHITE)

    # Vẽ biểu tượng nếu đang hiển thị
    if show_icon and count <= 6:
        screen.blit(alert_icon, (WIDTH // 2 - 25, HEIGHT // 2 - 25))

    elif count > 6:
        screen.fill((255,255,255))

    # Cập nhật màn hình
    pygame.display.flip()

    # Đặt tốc độ khung hình
    pygame.time.Clock().tick(30)

# Kết thúc Pygame
pygame.quit()