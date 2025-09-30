import pygame, sys
import random
from button import Button
from LOGIC import Stage, Rut_gon, Hai_khoang, Anh_xa, Float, Score, Hint, Money
from DATA import STAGE, HINT_GROUPS

# -------------------------
# CẤU HÌNH GAME
# -------------------------
pygame.init()
SCREEN_W, SCREEN_H = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Guess a Number - GUI")

BG = pygame.image.load("Background.png")
FONT_PATH = "DejaVuSans.ttf"

# -------------------------
# TIỆN ÍCH GUI
# -------------------------
def get_font(size):
    return pygame.font.Font(FONT_PATH, size)

def draw_text_center(surface, text, font, color, pos):
    render = font.render(text, True, color)
    rect = render.get_rect(center=pos)
    surface.blit(render, rect)

def draw_text_multiline(surface, text, font, color, pos, line_height=32):
    """Vẽ nhiều dòng text, pos là (center_x, start_y)."""
    lines = text.split("\n")
    x, y = pos
    for i, line in enumerate(lines):
        render = font.render(line, True, color)
        rect = render.get_rect(center=(x, y + i * line_height))
        surface.blit(render, rect)

class TextBox:
    def __init__(self, rect, font):
        self.rect = pygame.Rect(rect)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font = font
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                val = self.text
                self.text = ""
                return val
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return None

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.color)
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self):
        return self.text

    def clear(self):
        self.text = ""

# -------------------------
# BIẾN TOÀN CỤC
# -------------------------
money_global = Money(0)   # Bắt đầu có $0
hint_global = Hint()       # Túi hint chung

# -------------------------
# MENU MUA HINT
# -------------------------
def buy_hint_menu():
    clock = pygame.time.Clock()
    font_title = get_font(48)
    font_small = get_font(28)

    back_btn = Button(None, (SCREEN_W//2, SCREEN_H-60),
                      "Quay lại Menu", font_small, "White", "Yellow")

    # ---- Gom toàn bộ hint vào list phẳng ----
    all_hints = []
    for group in HINT_GROUPS.values():
        for key, item in group["items"].items():
            all_hints.append((key, item))

    # ---- Lấy ngẫu nhiên 3 hint theo xác suất ----
    chosen = random.sample(all_hints, k=3)
    # ---- Tạo nút cho 3 hint ----
    hint_btns = []
    y_offset = 220
    for key, item in chosen:
        btn = Button(None, (SCREEN_W//2, y_offset),
                     f"{item['desc']}  (${item['cost']})",
                     font_small, "White", "Yellow")
        hint_btns.append((btn, key, item["cost"]))
        y_offset += 60

    shop_message = ""

    while True:
        clock.tick(30)
        SCREEN.blit(BG, (0,0))
        draw_text_center(SCREEN, "SHOP GỢI Ý", font_title, "Yellow", (SCREEN_W//2, 100))
        draw_text_center(SCREEN, f"Tiền hiện tại: {money_global.thong_bao()}",
                         font_small, "Green", (SCREEN_W//2, 160))

        mouse_pos = pygame.mouse.get_pos()
        for btn, key, cost in hint_btns:
            btn.changeColor(mouse_pos)
            btn.update(SCREEN)

        back_btn.changeColor(mouse_pos)
        back_btn.update(SCREEN)

        # ✅ Hiện thông báo ở dưới
        if shop_message:
            draw_text_center(SCREEN, shop_message, font_small, "Red",
                             (SCREEN_W // 2, SCREEN_H - 120))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.checkForInput(mouse_pos):
                    return
                for btn, key, cost in hint_btns:
                    if btn.checkForInput(mouse_pos):
                        ok, msg = hint_global.buy_hint(key, money_global)
                        shop_message = msg  # ✅ lưu thông báo
                        break

        pygame.display.update()


    # Tạo danh sách nút cho từng hint
    hint_btns = []
    i = 0
    for group_name, group in HINT_GROUPS.items():
        for key, item in group["items"].items():
            btn = Button(None, (SCREEN_W//2, 180 + i*40),
                         f"{item['desc']}  (${item['cost']})",
                         font_small, "White", "Yellow")
            hint_btns.append((btn, key, item["cost"]))
            i += 1

    back_btn = Button(None, (SCREEN_W//2, SCREEN_H-80),
                      "Quay lại Menu", font_small, "White", "Yellow")

    while True:
        clock.tick(30)
        SCREEN.blit(BG, (0,0))
        draw_text_center(SCREEN, "MUA GỢI Ý", font_title, "Yellow", (SCREEN_W//2, 100))
        draw_text_center(SCREEN, f"Tiền hiện tại: {money_global.thong_bao()}",
                         font_small, "Green", (SCREEN_W//2, 140))

        mouse_pos = pygame.mouse.get_pos()
        for btn, key, cost in hint_btns:
            btn.changeColor(mouse_pos)
            btn.update(SCREEN)

        back_btn.changeColor(mouse_pos)
        back_btn.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.checkForInput(mouse_pos):
                    return
                for btn, key, cost in hint_btns:
                    if btn.checkForInput(mouse_pos):
                        ok = hint_global.buy_hint(key, money_global)
                        if ok:
                            print(f"Đã mua hint: {key}")
                        else:
                            print("Không đủ tiền!")

        pygame.display.update()

# -------------------------
# LOOP CHƠI MỖI STAGE
# -------------------------
def play_stage(stage):
    clock = pygame.time.Clock()
    font_big = get_font(48)
    font_small = get_font(28)

    # Ô nhập số đoán
    input_box = TextBox((SCREEN_W//2 - 180, 250, 360, 56), font_small)
    # Ô nhập hint riêng
    hint_input = TextBox((SCREEN_W // 2 - 100, 460, 200, 40), font_small)
    # Ô nhập giá trị phụ cho hint
    hint_value_box = TextBox((SCREEN_W // 2 - 25, 510, 50, 40), font_small)

    # Các nút
    submit_btn = Button(None, (SCREEN_W//2, 340), "SUBMIT",
                        font_small, "White", "Yellow")
    hint_btn   = Button(None, (SCREEN_W//2, 425), "Dùng Hint",
                        font_small, "White", "Yellow")
    back_btn   = Button(None, (100, 40), "Menu",   # góc trên trái
                        font_small, "White", "Red")

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            val = input_box.handle_event(event)
            if val is not None:
                handle_guess(stage, val)
                if stage.turn <= 0 or stage.status.startswith("Bingo") or "thắng" in stage.status:
                    return "Bingo" in stage.status or "thắng" in stage.status
                input_box.clear()

            hint_input.handle_event(event)
            hint_value_box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_btn.checkForInput(pygame.mouse.get_pos()):
                    val = input_box.get_value()
                    if val:
                        handle_guess(stage, val)
                        if stage.turn <= 0 or stage.status.startswith("Bingo") or "thắng" in stage.status:
                            return "Bingo" in stage.status or "thắng" in stage.status
                        input_box.clear()

                if hint_btn.checkForInput(pygame.mouse.get_pos()):
                    hint_key = hint_input.get_value().strip()
                    hint_val = hint_value_box.get_value().strip()  # giá trị phụ (1/2, số tiền…)

                    if not hint_key:
                        stage.status = "Nhập từ khóa hint trước!"
                    elif hint_key not in hint_global.inventory:
                        stage.status = f"Bạn chưa mua hint '{hint_key}'!"
                    else:
                        msg = hint_global.use_1_hint(
                            stage,
                            hint_key,  # key của hint
                            hint_val,  # giá trị phụ
                            input_box.get_value()  # số đoán hiện tại
                        )
                        stage.status = msg
                        hint_input.clear()
                        hint_value_box.clear()

                if back_btn.checkForInput(pygame.mouse.get_pos()):
                    return "menu"   # quay lại menu ngay

        # --- Vẽ ---
        SCREEN.blit(BG, (0,0))
        draw_text_center(SCREEN, f"Stage {stage.round}", font_big, (200,200,0), (SCREEN_W//2, 80))
        draw_text_multiline(SCREEN, stage.status, font_small, (255, 255, 255), (SCREEN_W // 2, 150))
        draw_text_center(SCREEN, f"Lượt còn lại: {stage.turn}", font_small, (255,255,0), (SCREEN_W//2, 200))
        draw_text_center(SCREEN, f"Tiền: {money_global.thong_bao()}", font_small, "Green", (SCREEN_W//2, 230))

        if hint_global.inventory:
            draw_text_center(SCREEN, "Hint đã mua:", font_small, "Cyan", (SCREEN_W // 2, 580))

            y_offset = 620
            for key in hint_global.inventory:
                desc = None
                # tìm desc trong HINT_GROUPS
                for group in HINT_GROUPS.values():
                    if key in group["items"]:
                        desc = group["items"][key]["desc"]
                        break

                if desc is None:
                    desc = "(Không rõ)"

                # Hiển thị: key → desc
                text_line = f"{key}  →  {desc}"
                render = font_small.render(text_line, True, pygame.Color("cyan"))
                rect = render.get_rect(center=(SCREEN_W // 2, y_offset))
                SCREEN.blit(render, rect)

                y_offset += 30  # mỗi hint xuống 1 dòng

        input_box.draw(SCREEN)
        submit_btn.changeColor(pygame.mouse.get_pos()); submit_btn.update(SCREEN)

        font_info = get_font(28)
        if isinstance(stage, Hai_khoang):
            text_range = f"Khoảng 1: [{stage.left}, {stage.right}]   Khoảng 2: [{stage.left2}, {stage.right2}]"
        else:
            text_range = f"Khoảng: [{stage.left}, {stage.right}]"
        draw_text_center(SCREEN, text_range, font_info, "White", (SCREEN_W // 2, 380))

        hint_input.draw(SCREEN)
        hint_btn.changeColor(pygame.mouse.get_pos()); hint_btn.update(SCREEN)

        hint_value_box.draw(SCREEN)
        hint_btn.changeColor(pygame.mouse.get_pos()); hint_btn.update(SCREEN)

        # Nút quay lại menu
        back_btn.changeColor(pygame.mouse.get_pos()); back_btn.update(SCREEN)

        if isinstance(stage, Score) and stage.S >= 50:
            stage.status = "Chúc mừng!! Bạn đã thắng được boss"
            return True

        pygame.display.update()



def handle_guess(stage, val):
    if isinstance(stage, Hai_khoang):
        try:
            y1, y2 = map(int, val.split())
            stage.so_sanh(y1, y2)
        except Exception:
            stage.status = "Sai định dạng, nhập: <A> <B>"
    else:
        y = stage.kt_so(val)
        if y is not None:   # ✅ chỉ xử lý khi nhập số hợp lệ
            stage.so_sanh(y)
        else:
            stage.status = "Bạn phải nhập số nguyên!"

# -------------------------
# MENU CHÍNH
# -------------------------
def main_menu():
    clock = pygame.time.Clock()
    font_big = get_font(48)
    font_small = get_font(30)

    while True:
        clock.tick(30)
        SCREEN.blit(BG, (0,0))
        draw_text_center(SCREEN, "GUESS A NUMBER", font_big, "Yellow", (SCREEN_W//2, 100))

        mouse_pos = pygame.mouse.get_pos()
        stage_btns = []
        for i in range(1,9):
            btn = Button(None, (SCREEN_W//2, 180 + i*40),
                         f"Stage {i}", font_small, "White", "Yellow")
            btn.changeColor(mouse_pos)
            btn.update(SCREEN)
            stage_btns.append((btn,i))

        # ✅ Thêm nút Mua Hint
        shop_btn = Button(None, (SCREEN_W//2, 600),
                          "Mua Hint", font_small, "White", "Yellow")
        shop_btn.changeColor(mouse_pos)
        shop_btn.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn,i in stage_btns:
                    if btn.checkForInput(mouse_pos):
                        return i   # trả về stage_id
                if shop_btn.checkForInput(mouse_pos):
                    buy_hint_menu()   # mở shop hint

        pygame.display.update()


# -------------------------
# END SCREEN
# -------------------------
def end_screen(result, stage_id, stage_obj):
    clock = pygame.time.Clock()
    font_big   = get_font(60)
    font_small = get_font(32)

    msg   = (f"Bạn đã thắng Stage {stage_id}!" if result
             else f"Bạn đã thua Stage {stage_id}!")
    color = "green" if result else "red"

    if stage_id == 7 and hasattr(stage_obj, "X"):
        answer_text = f"Đáp án: {stage_obj.X / 10:.1f}"
    else:
        answer_text = f"Đáp án: {getattr(stage_obj, 'X', '?')}"

    back_btn = Button(None, (SCREEN_W // 2, SCREEN_H // 2 + 120),
                      "Quay lại Menu", font_small, "White", "Yellow")

    # ✅ Thêm nút Buy Hint nếu thắng
    if result:
        buy_btn = Button(None, (SCREEN_W // 2, SCREEN_H // 2 + 60),
                         "Buy Hint", font_small, "White", "Yellow")
    else:
        buy_btn = None

    if result:  # nếu thắng
        reward = stage_obj.turn  # số lượt dư
        reward_text = ""
        if reward > 0:
            money_global.earn(reward)
            reward_text = f"Thưởng {reward}$ cho {reward} lượt dư!"
            print(reward_text)
        else:
            reward_text = "Không có lượt dư để thưởng."
    else:
        reward_text = ""

    while True:
        clock.tick(30)
        SCREEN.blit(BG, (0, 0))
        draw_text_center(SCREEN, msg, font_big, color,
                         (SCREEN_W // 2, SCREEN_H // 2 - 80))
        draw_text_center(SCREEN, answer_text, font_small, "white",
                         (SCREEN_W // 2, SCREEN_H // 2 - 20))
        if reward_text:
            draw_text_center(SCREEN, reward_text, font_small, "yellow",
                             (SCREEN_W // 2, SCREEN_H // 2 + 20))

        # Vẽ nút Buy Hint nếu thắng
        if buy_btn:
            buy_btn.changeColor(pygame.mouse.get_pos())
            buy_btn.update(SCREEN)

        back_btn.changeColor(pygame.mouse.get_pos())
        back_btn.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buy_btn and buy_btn.checkForInput(pygame.mouse.get_pos()):
                    buy_hint_menu()   # mở shop hint ngay tại end_screen
                if back_btn.checkForInput(pygame.mouse.get_pos()):
                    return
        pygame.display.update()

# -------------------------
# MAIN LOOP
# -------------------------
def main():
    while True:
        stage_id = main_menu()
        conf = STAGE[stage_id]

        if stage_id in [1, 3]:
            stage = Rut_gon(conf[0], conf[1], conf[2], "Nhập số", conf[3])
        elif stage_id in [2, 5, 6]:
            stage = Anh_xa(conf[0], conf[1], conf[2], "Nhập số", conf[3])
        elif stage_id == 4:
            stage = Hai_khoang(conf[0], conf[1], conf[2], "Nhập số", conf[3], conf[4], conf[5])
        elif stage_id == 7:
            stage = Float(conf[0], conf[1], conf[2], "Nhập số", conf[3])
        elif stage_id == 8:
            stage = Score(conf[0], conf[1], conf[2], "Nhập số", conf[3])
        else:
            stage = Stage(conf[0], conf[1], conf[2], "Nhập số", conf[3])

        result = play_stage(stage)
        if result == "menu":
            continue  # quay lại menu chính, không end_screen
        end_screen(result, stage_id, stage)

if __name__ == "__main__":
    main()
