import random
import numpy as np
import os
import time
import keyboard

def int_input(prompt, left, right):
    while True:
        try:
            a = int(input(prompt))
            if not left <= a <= right:
                continue
            return a
        except ValueError:
            continue

hints = {1: ["Tổng các chữ số", 4],
         2: ["Số chữ số chẵn", 2],
         3: ["Số chữ số lẻ", 2],
         4: ["Chữ số lớn nhất", 5],
         5: ["Chữ số nhỏ nhất", 5],
         6: ["Số chữ số lớn hơn bằng 5", 3],
         7: ["Số chữ số là số nguyên tố", 2],
         8: ["Tiết lộ chữ số cuối", 5],
         9: ["Tiết lộ chữ số đầu", 10],
         10: ["Miễn phí 1 lượt đoán", 1],
         11: ["Miễn phí 2 lượt đoán", 3],
         12: ["Miễn phí 3 lượt đoán", 6],
         13: ["- 50%", 4],
         14: ["Loại bỏ 1 khoảng sai", -1],
         15: ["Kiểm tra số trong khoảng +-10", 7],
         16: ["Kiểm tra số trong khoảng +-25", 4],
         17: ["A fun fact", 1],
         18: ["Roulette (10% nhận $10)", 1],
         19: ["Vé cược (dùng trong lượt)", -1],
         20: ["Đổi tiền thành lượt chơi ($2 = 1 lượt)", -1]
         }

probility = [0.05, 0.1, 0.1, 0.06, 0.06, 0.075, 0.075, 0.05, 0.01, 0.1, 0.05, 0.025, 0, 0.01, 0.025, 0.05, 0, 0.125, 0.025, 0.01]
# rep_hint = [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 14, 15, 16]
# rep_turn = [10, 11, 12]
# rep_money = [18, 19]

def use_hint(hint, CPU, left, right):
    global money
    match hint:
        case 1:
            hint = f"Tổng các chữ số là {sum(int(i) for i in str(CPU))}"
            return hint
        case 2:
            hint = f"Số chữ số chẵn là {sum(1 for i in str(CPU) if int(i) % 2 == 0)}"
            return hint
        case 3:
            hint = f"Số chữ số lẻ là {sum(1 for i in str(CPU) if int(i) % 2 != 0)}"
            return hint
        case 4:
            hint = f"Chữ số lớn nhất là {max(int(i) for i in str(abs(CPU)))}"
            return hint
        case 5:
            hint = f"Chữ số nhỏ nhất là {min(int(i) for i in str(abs(CPU)))}"
            return hint
        case 6:
            hint = f"Số chữ số lớn hơn bằng 5 là {sum(1 for i in str(CPU) if int(i) > 4)}"
            return hint
        case 7:
            def is_prime(n):
                if n in (0, 1, 4, 6, 8, 9):
                    return False
                return True
            hint = f"Số chữ số là số nguyên tố là {sum(1 for i in str(CPU) if is_prime(int(i)))}"
            return hint
        case 8:
            hint = f"Chữ số cuối là {str(CPU)[-1]}"
            return hint
        case 9:
            hint = f"Chữ số đầu là {str(CPU)[0]}"
            return hint
        case 10 | 11 | 12:
            return hint - 9
        case 13:
            res = []
            while len(res) == (right - left) // 2:
                a = random.randint(left, right)
                if a != CPU and a not in res:
                    res.append(a)
            return sorted(res)
        case 14:
            print(f"Số tiền bạn đang có: {money}")
            n = int_input("Nhập số tiền bạn muốn dùng (10% = $1, tối đa $9): ", 1, 9)
            hints[hint][1] = n
            cl = (10 - n) * (right - left + 1) // 10
            toLeft = min(random.randint(0, cl), CPU - left)
            hint = f"Số thuộc khoảng {CPU - toLeft} đến {CPU + (cl - toLeft)}"
            return hint
        case 15:
            player = int_input("Nhập số bạn muốn kiểm tra: ", left, right)
            if player - 10 <= CPU <= player + 10:
                hint = f"Số thuộc khoảng {player - 10} đến {player + 10}"
                return hint
            else:
                print("Kiểm tra thất bại, trừ 1 lượt")
                time.sleep(1)
                return -1
        case 16:
            player = int_input("Nhập số bạn muốn kiểm tra: ", left, right)
            if player - 25 <= CPU <= player + 25:
                hint = f"Số thuộc khoảng {player - 25} đến {player + 25}"
                return hint
            else:
                print("Kiểm tra thất bại, trừ 1 lượt")
                time.sleep(1)
                return -1
        case 17:
            pass
        case 18:
            if random.randint(1, 10) == 1:
                print("Bạn đã trúng $10")
                time.sleep(2)
                return True
            print("Bạn không trúng thưởng")
            time.sleep(2)
            return False
        case 19:
            print(f"Số tiền bạn đang có: {money}")
            bet = int_input("Nhập số tiền bạn muốn cược (tối đa $10): ", 1, min(10, money))
            hints[hint][1] = bet
            player = int_input("Nhập số bạn muốn cược: ", left, right)

            if player == CPU:
                print(f"Chính xác, tiền thưởng x{right - left + 1}")
                money += bet * (right - left + 1)
                return -1
            print("Không chính xác")
            return -1
        case 20:
            print(f"Số tiền bạn đang có: {money}")
            m = int_input("Nhập số tiền bạn muốn đổi (tối đa $10): ", 2, min(10, money))

            hints[hint][1] = m
            return m // 2

def hint_in_guesing(hint, CPU, left, right, turns):
        if hint:
            res = use_hint(hint, CPU, left, right)
            if isinstance(res, str):
                    print(res)
                    time.sleep(2)
                    return res, turns
            elif isinstance(res, int):
                    print(f"Đã thêm {res} lượt đoán")
                    time.sleep(2)
                    return None, turns + res
            elif isinstance(res, list):
                    delete_s = ''.join(str(i) + " " for i in res)
                    print(f"Đã loại bỏ các số: {delete_s}")
                    hint = f"Loại bỏ các số: {delete_s}"
                    time.sleep(2)
                    return hint, turns
            else:
                    print("Bạn không còn gợi ý nào")
                    time.sleep(2)
                    return hint, turns

def guesing(left, right, CPU, hint, turns, mode):
        if turns == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            if mode == 4:
                print(f"Bạn đã thua! Số đúng là {CPU / 10}")
            else:
                print(f"Bạn đã thua! Số đúng là {CPU}")
            return -1
        
        os.system('cls' if os.name == 'nt' else 'clear')
        if mode in (1, 2, 3):
            print(f"MYSTERY: Đoán số bí ẩn từ {left} đến {right}")
        elif mode == 4:
            print(f"Đoán số từ {left // 10} đến {max(right // 10, left // 10 + 1)}")
        else:
            print(f"Đoán số từ {left} đến {right}")

        print(f"Lượt còn lại: {turns}")
        if hint:
            if mode == 5:
                print(f"Gợi ý: **VÔ HIỆU HÓA")
                new_turns = hints[hint][1] // 2 if hints[hint][1] != -1 else 0
                print(f"Đã đổi thành {new_turns} lượt chơi thêm")
                print("-"*50)
                print("\tNhấn Enter để tiếp tục...")
                while True:
                    if keyboard.is_pressed('enter'):
                        break
                time.sleep(0.2)
                return guesing(left, right, CPU, None, turns + new_turns, mode)
            if hint in hints:
                print(f"Gợi ý (gõ \"HINT\"): {hints[hint][0]}")
                if mode == 4:
                    print("Gợi ý được dùng theo số nguyên (VD: 12 - 24 -> 120 - 240)")
            else:
                print(f"Gợi ý: {hint}")
        
        print("-"*50)
        if mode == 4:
            player = input(f"Nhập 1 số từ {left // 10} đến {max(right // 10, left // 10 + 1)}: ")
        else:
            player = input(f"Nhập 1 số từ {left} đến {right}: ")
        if player.upper() == "HINT":
            # if mode == 4:
                # hint, turns = hint_in_guesing(hint, CPU, left*10, right*10, turns)
                # print("Nhập số tròn (VD: 52.8 -> 528)")
            # else:
            #     hint, turns = hint_in_guesing(hint, CPU, left, right, turns)
            hint, turns = hint_in_guesing(hint, CPU, left, right, turns)
            return guesing(left, right, CPU, hint, turns, mode)
        
        if mode == 4:
            try:
                player = int(float(player)*10)
            except ValueError:
                return guesing(left, right, CPU, hint, turns, mode)
        else:
            try:
                player = int(player)
            except ValueError:
                return guesing(left, right, CPU, hint, turns, mode)

        #Hàm bình thường so sánh lớn hơn và bé hơn
        def all_positive(left, right, CPU, hint, turns):
            if player < CPU:
                print("Lớn hơn!")
                time.sleep(1)
                return guesing(max(player + 1, left), right, CPU, hint, turns - 1, mode)
                
            elif player > CPU:
                print("Nhỏ hơn!")
                time.sleep(1)
                return guesing(left, min(player - 1, right), CPU, hint, turns - 1, mode)

            else:
                print("Chúc mừng! Bạn đã đoán đúng số.")
                time.sleep(1)
                return turns - 1

        #Hàm tổng hiệu: hint_1 là số bất kỳ trong khoaảng (1;100) và là tham số
        def mystery_1(left, right, CPU, hint, turns):
            if player != CPU:
                choices = random.randint(1, 3)
                hint_1 = random.randint(1, 100)
                if choices == 1:
                    print(f"Tổng các chữ số trong hiệu của {hint_1} và số cần tìm: {sum(int(i) for i in str(abs(hint_1 - CPU)))}")
                elif choices == 2:
                    print(f"Tổng các chữ số trong tổng của {hint_1} và số cần tìm: {sum(int(i) for i in str(hint_1 + CPU))}")
                else:
                    print(f"Tổng các chữ số trong tích của {hint_1} và số cần tìm: {sum(int(i) for i in str(abs(hint_1 * CPU)))}")
                time.sleep(5)
                return guesing(left, right, CPU, hint, turns - 1, mode)
            else:
                print("Chúc mừng! Bạn đã đoán đúng số.")
                time.sleep(1)
                return turns - 1

        #Hàm công thức bí ẩn, với định nghĩa của các công thức lần lượt theo
        def mystery_2(left, right, CPU, hint, turns):
            if player != CPU:
                def sum_mys(num, type):
                    res = 0
                    for i in str(num):
                        if i == "0":
                            res = res // 2
                            continue
                        match type:
                            case 1:
                                res += int(i)**2
                            case 2:
                                res *= int(i)
                            case 3:
                                res += int(i) // 2
                    return res
                
                typee = random.randint(1, 3)
                hint_2 = random.randint(1,100)
                print(f"Dạng {typee}: Nếu số cần tìm là {sum_mys(CPU, typee)} thì {hint_2} là {sum_mys(hint_2, typee)}")
                time.sleep(5)
                return guesing(left, right, CPU, hint, turns - 1, mode)
            else:
                print("Chúc mừng! Bạn đã đoán đúng số.")
                time.sleep(1)
                return turns - 1
        
        def mystery_3(left, right, CPU, hint, turns, i):
            if player != CPU:
                hint_3 = random.randint(1, 100)
                print(f"Với {i = } thì số cần tìm là {str(CPU*i)[-1]} và {hint_3} là {str(hint_3*i)[-1]}")
                if turns in (1, 2, 3):
                    if player < CPU:
                        print("Số bạn đoán đang nhỏ hơn!")
                        time.sleep(7)
                        return guesing(max(player + 1, left), right, CPU, hint, turns - 1, mode)
                    elif player > CPU:
                        print("Số bạn đoán đang lớn hơn!")
                        time.sleep(7)
                        return guesing(left, min(player - 1, right), CPU, hint, turns - 1, mode)
                time.sleep(7)
                return guesing(left, right, CPU, hint, turns - 1, mode)
            else:
                print("Chúc mừng! Bạn đã đoán đúng số.")
                time.sleep(1)
                return turns - 1
        
        def float_1point(left, right, CPU, hint, turns):
            if player < CPU:
                print("Lớn hơn!")
                time.sleep(1)
                return guesing(max(player + 1, left), right, CPU, hint, turns - 1, mode)
                
            elif player > CPU:
                print("Nhỏ hơn!")
                time.sleep(1)
                return guesing(left, min(player - 1, right), CPU, hint, turns - 1, mode)

            else:
                print("Chúc mừng! Bạn đã đoán đúng số.")
                time.sleep(1)
                return turns - 1

        if mode == 0 or mode == 5:
            return all_positive(left, right, CPU, hint, turns)
        if mode == 1:
            return mystery_1(left, right, CPU, hint, turns)
        if mode == 2:
            return mystery_2(left, right, CPU, hint, turns)
        if mode == 3:
            return mystery_3(left, right, CPU, hint, turns, random.randint(1, 10))
        if mode == 4:
            return float_1point(left, right, CPU, hint, turns)
        
def guesing_2(left, right, left2, right2, CPU, CPU2, hint, turns, mode):
        if turns == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            if mode == 2:
                print(f"Bạn đã thua! Số đúng là {CPU} và {CPU2}")
            else:
                print(f"Bạn đã thua! Số đúng là {CPU}")
            return -1
        
        os.system('cls' if os.name == 'nt' else 'clear')
        if right != left2:
            print(f"Đoán số trong khoảng [{left}, {right}], [{left2}, {right2}]")
        else:
            print(f"Đoán số từ {left} đến {right2}")

        print(f"Lượt còn lại: {turns}")
        if hint:
            if hint in hints:
                print(f"Gợi ý (gõ \"HINT\"): {hints[hint][0]}")
            else:
                print(f"Gợi ý: {hint}")
        
        print("-"*50)
        if mode == 2:
            player = input(f"Nhập 1 số trong mỗi khoảng [{left}, {right}], [{left2}, {right2}] (mẫu: A B): ")
        else:
            if right != left2:
                player = input(f"Nhập 1 số trong khoảng [{left}, {right}], [{left2}, {right2}]")
            else:
                player = input(f"Nhập 1 số từ {left} đến {right2}: ")
        if player.upper() == "HINT":
            if CPU2:
                CPU_choice = int_input("Lựa số cần dùng gợi ý (1/2): ", 1, 2)
                if CPU_choice == 2:
                    hint, turns = hint_in_guesing(hint, CPU2, left2, right2, turns)
                    hint = hint + " (2)"
                else:
                    hint, turns = hint_in_guesing(hint, CPU, left, right, turns)
                    hint = hint + " (1)"
                return guesing_2(left, right, left2, right2, CPU, CPU2, hint, turns, mode)
            
            hint, turns = hint_in_guesing(hint, CPU, left, right, turns)
            return guesing_2(left, right, left2, right2, CPU, CPU2, hint, turns, mode)
        
        if mode == 2:
            try:
                num_player = list(map(int, player.split()))
                if len(num_player) != 2:
                    raise ValueError
            except ValueError:
                print("Vui lòng nhập 2 số hợp lệ, cách nhau bằng dấu cách.")
                time.sleep(2)
                return guesing_2(left, right, left2, right2, CPU, CPU2, hint, turns, mode)
        else:
            try:
                player = int(player)
            except ValueError:
                return guesing_2(left, right, left2, right2, CPU, CPU2, hint, turns, mode)
        
        def continuous_interger(left, right, left2, right2, CPU, hint, turns):
            if abs(player) < abs(CPU):
                print(f"Số thuộc khoảng [{left}, {min(right, - abs(player) - 1)}], [{max(left2, abs(player) + 1)}, {right2}]")
                time.sleep(1)
                return guesing_2(left, min(right, - abs(player) - 1), max(left2, abs(player) + 1), right2, CPU, hint, turns - 1, mode)
            elif abs(player) > abs(CPU):
                print(f"Số thuộc khoảng [{max(left, - abs(player) + 1)}, {min(right2, abs(player) - 1)}]")
                time.sleep(1)
                return guesing_2(left, right, left2, right2, CPU, hint, turns - 1, mode)
            else:
                player = int_input(f"Kết quả cuối cùng là {CPU} hay -{CPU}? ", -CPU, CPU)
                if player == CPU:
                    print("Chính xác")
                    time.sleep(1)
                    return turns - 1
                else:
                    print("Sai, bạn bị mất thêm 1 lượt")
                    time.sleep(1)
                    return turns - 2
        
        def disrupt_interger(left, right, left2, right2, CPU, CPU2, hint, turns):
            arr = [0, 0, 0]
            if num_player[0] < CPU:
                arr[0] += 1
            elif num_player[0] == CPU:
                arr[1] += 1
            else:
                arr[2] += 1
            if num_player[1] < CPU2:
                arr[0] += 1
            elif num_player[1] == CPU2:
                arr[1] += 1
            else:
                arr[2] += 1
            
            if arr[1] == 2:
                print("Chính xác")
                time.sleep(1)
                return turns - 1
            
            if arr[1] == 1:
                print("Đang có 1 số đúng")
                time.sleep(2)
                return guesing_2(left, right, left2, right2, CPU, CPU2, hint, turns - 1, mode)
            
            if arr[0] == 2:
                left = max(left, num_player[0] + 1)
                left2 = max(left2, num_player[1] + 1)
            
            if arr[2] == 2:
                right = min(right, num_player[0] - 1)
                right2 = min(right2, num_player[1] - 1)

            print(np.random.choice([f"Có {arr[0]} số nhỏ hơn", f"Có {arr[1]} số chính xác", f"Có {arr[2]} số lớn hơn"], p = [0.45, 0.1, 0.45]))
            time.sleep(2)
            return guesing_2(left, right, left2, right2, CPU, CPU2, hint, turns - 1, mode)

        if mode == 1:
            return continuous_interger(left, 0, 0, right2, CPU, None, hint, turns)
        elif mode == 2:
            return disrupt_interger(left, right, left2, right2, CPU, CPU2, hint, turns)

def guesing_boss_1(left, right, CPU, hint, turns, max_right, points):
        if points >= 50:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Bạn đã thắng! Số mục tiêu là {CPU}")
            time.sleep(1)
            return turns
        
        if turns == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Bạn đã thua! Số mục tiêu là {CPU}")
            return -1
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"*MISSION: Đạt 50 điểm: {points}/50")
        print("(Đoán số càng gần số mục tiêu càng được nhiều điểm)")
        print(f"Lượt còn lại: {turns}")
        if hint:
            if hint in hints:
                print(f"Gợi ý (gõ \"HINT\"): {hints[hint][0]}")
            else:
                print(f"Gợi ý: {hint}")
        
        print("-"*50)
        player = input(f"Nhập 1 số bất kỳ từ 1 đến {max_right}: ")
        if player.upper() == "HINT":
            hint, turns = hint_in_guesing(hint, CPU, left, right, turns)
            return guesing_boss_1(left, right, CPU, hint, turns, max_right, points)
        
        try:
            player = int(player)
        except ValueError:
            return guesing_boss_1(left, right, CPU, hint, turns, max_right, points)
        
        def cum_pts(left, right, CPU, hint, turns, points):
            def left_right(CPU, player, pct):
                if CPU - max_right * pct < 0:
                    left = CPU - max_right * pct + max_right
                    right = CPU + max_right * pct
                    return 0 < player < right or left < player <= max_right 
                elif CPU + max_right * pct > max_right:
                    left = CPU - max_right * pct
                    right = CPU + max_right * pct - max_right
                    return 0 < player < right or left < player <= max_right 
                else:
                    left = CPU - max_right * pct
                    right = CPU + max_right * pct
                    return left < player < right

            if not left_right(CPU, player, 0.25):
                print("-1 điểm")
                time.sleep(1)
                return guesing_boss_1(left, right, CPU, hint, turns - 1, max_right, points - 1)
            
            if not left_right(CPU, player, 0.05):
                print("0 điểm")
                time.sleep(1)
                return guesing_boss_1(left, right, CPU, hint, turns - 1, max_right, points)
            
            if not left_right(CPU, player, 0.005):
                print("1 điểm")
                time.sleep(1)
                return guesing_boss_1(left, right, CPU, hint, turns - 1, max_right, points + 1)
            
            if not left_right(CPU, player, 0.0005):
                print("2 điểm")
                time.sleep(1)
                return guesing_boss_1(left, right, CPU, hint, turns - 1, max_right, points + 2)
            
            if player != CPU:
                print("3 điểm")
                time.sleep(1)
                return guesing_boss_1(left, right, CPU, hint, turns - 1, max_right, points + 3)
            else:
                print("15 điểm")
                time.sleep(1)
                return guesing_boss_1(left, right, CPU, hint, turns - 1, max_right, points + 15)
        
        return cum_pts(left, right, CPU, hint, turns, points)

def stage_normal(left = 1, right = 100, hint = None, turns = None, round = 0, mode = 0):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Stage {round}/8")
    time.sleep(1)
    CPU = random.randint(left, right)
    return guesing(left, right, CPU, hint, turns, mode)

def stage_normal_4(left = 0, right = 100, hint = None, turns = None, round = 0, mode = 4):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Stage {round}/8")
    print("Nhập số thực có 1 dấu chấm động (VD: 12.3)")
    print("\tNhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)
    CPU = random.randint(left, right)
    return guesing(left, right, CPU, hint, turns, mode)

def stage_hard(left = -100, right = 0, left2 = 0, right2 = 100, hint = None, turns = None, round = 0, mode = 0):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Stage {round}/8")
    time.sleep(1)
    CPU = random.randint(left, right)
    if mode == 2:
        CPU2 = random.randint(left2, right2)
        return guesing_2(left, right, left2, right2, CPU, CPU2, hint, turns, mode)
    return guesing_2(left, 0, 0, right2, CPU, None, hint, turns, mode)

def stage_boss(left = 0, right = 100, hint = None, turns = None, period = 0, round = 8, max_right = 0):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Stage {round}/8")
    print("-"*30)
    print(f"Giai Đoạn {period}")
    time.sleep(1)
    CPU = random.randint(left, right)
    return guesing_boss_1(left, right, CPU, hint, turns, max_right, 0)

def stage_end(turns, moneys, hint, passed):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("{0}\t\t\t\t{1}".format("Thưởng qua màn:", f" ${passed}"))
    print("{0}\t\t\t{1}".format(f"Thưởng {turns} lượt dư:", f" ${turns}"))
    if hint:
        pay = 0
        if hint in (14, 19, 20):
            pay = hints[hint][1]
            moneys -= pay
            hints[hint][1] = -1
        # print("{0}\t\t\t\t{1}".format("Phí gợi ý:", f"-${pay}"))
    print("{0}\t{1}".format(f"${moneys}: Thưởng $1 lời mỗi $5 (tối đa $5):", f" ${min(moneys//5, 5)}")) 
    if hint:
        print("\t(Gợi ý hết hiệu lực)")
    moneys += passed + turns + min(moneys//5, 5)
    print(" "*37, "-"*8)
    print("{0}\t\t\t{1}".format("Tổng tiền hiện có:", f" ${moneys}"))
    print("\tNhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    return None, moneys

def print_item_shopping():
    dt = {}
    while len(dt) < 3:
        item = np.random.choice(list(hints.keys()), p=probility)
        if item not in dt:
            dt[item] = hints[item][1]
            print(f"{item}. {hints[item][0]} - ${hints[item][1] if hints[item][1] != -1 else 'Free'}")
    return dt

def shoptime(hint = None, moneys = 0):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Số tiền hiện có: ${moneys}")
    print("Vật phẩm hiện có: ")
    dt = print_item_shopping()
    print("-"*30)
    while True:
        x = input("Nhập hàng mua/ Enter (thoát): ")
        match x:
            case x if x.isdigit() and int(x) in dt:
                x = int(x)
                if dt[x] == -1:
                    if x == 14:
                        hint = int(14)
                        print("Đã mua chức năng, chỉ dùng trong lượt chơi")
                        time.sleep(1)
                        return hint, moneys
                    
                    elif x == 19:
                        hint = int(19)
                        print("Đã mua vé cược, dùng trong lượt chơi")
                        time.sleep(1)
                        return hint, moneys
                    
                    elif x == 20:
                        hint = int(20)
                        print("Đã mua chức năng, chỉ dùng trong lượt chơi")
                        time.sleep(1)
                        return hint, moneys
                    
                elif x == 18:
                    if moneys < 1:
                        print("Không đủ tiền")
                        continue
                    print("Đã chơi roulette với giá $1")
                    if use_hint(18, 0, 0, 0):
                        moneys += 10
                    print(f"Số tiền còn lại: ${moneys}")
                    return None, money - 1

                moneys -= dt[x]
                if moneys < 0:
                    print("Không đủ tiền")
                    moneys += dt[x]
                    continue
                else:
                    hint = int(x)
                    print(f"Đã mua {hints[hint][0]} với giá ${hints[hint][1]}")
                    print(f"Số tiền còn lại: ${moneys}")
                    time.sleep(1)
                    return hint, moneys

            case _ if keyboard.is_pressed('enter'):
                return hint, moneys

hint, money, turns_left = None, 0, 0

# Main program
def MainGame():
    global hint, money, turns_left
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Chào mừng đến với trò chơi đoán số!")
    print("Bạn sẽ có 8 vòng để đoán số trong khoảng nhất định.")
    print("Mỗi vòng bạn sẽ có số lượt đoán cho sẵn.")
    print("Bạn có thể mua gợi ý để giúp bạn đoán đúng số.")
    print("Mỗi vòng có thể mua và dùng tối đa 1 gợi ý.")
    print("\tNhấn Enter để bắt đầu...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)

    # Stage 1
    random.seed(random.randint(1, 1000))
    turns_left = stage_normal(1, 100, turns = 10, round = 1, mode = 0)
    if turns_left < 0:
        return False
    
    random.seed(random.randint(1, 1000))
    hint, money = stage_end(turns_left, money, hint, 1)
    time.sleep(0.2)
    hint, money = shoptime(hint, money)
    print("Nhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)
    
    # Stage 2
    turns_left = stage_normal(1, 250, hint, turns = 10, round = 2, mode = 0)
    if turns_left < 0:
        return False
    
    random.seed(random.randint(1, 1000))
    hint, money = stage_end(turns_left, money, hint, 1)
    time.sleep(0.2)
    hint, money = shoptime(hint, money)
    print("Nhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)

    # Stage 3
    if random.randint(1, 2) == 1:
        turns_left = stage_normal(1, 100, hint, turns = 5, round = 6, mode = 5)
    else:
        turns_left = stage_normal_4(0, 500, hint, turns = 8, round = 6, mode = 4)
    if turns_left < 0:
        return False
    
    random.seed(random.randint(1, 1000))
    hint, money = stage_end(turns_left, money, hint, 2)
    time.sleep(0.2)
    hint, money = shoptime(hint, money)
    print("Nhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)    
    
    # Stage 4
    turns_left = stage_hard(1, 250, 251, 500, hint, turns = 15, round = 4, mode = 2)
    if turns_left < 0:
        return False
    
    random.seed(random.randint(1, 1000))
    hint, money = stage_end(turns_left, money, hint, 3)
    time.sleep(0.2)
    hint, money = shoptime(hint, money)
    print("Nhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)
    
    # Stage 5
    turns_left = stage_normal(1, 500, hint, turns = 8, round = 5, mode = 0)
    if turns_left < 0:
        return False
    
    random.seed(random.randint(1, 1000))
    hint, money = stage_end(turns_left, money, hint, 1)
    time.sleep(0.2)
    hint, money = shoptime(hint, money)
    print("Nhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)
    
    # Stage 6
    turns_left = stage_normal(1, 100, hint, turns = 10, round = 3, mode = random.randint(1, 3))
    if turns_left < 0:
        return False
    
    random.seed(random.randint(1, 1000))
    hint, money = stage_end(turns_left, money, hint, 2)
    time.sleep(0.2)
    hint, money = shoptime(hint, money)
    print("Nhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)

    # Stage 7
    if random.randint(1, 2) == 1:
        turns_left = stage_normal(1, 250, hint, turns = 5, round = 7, mode = 5)
    else:
        turns_left = stage_normal_4(0, 1000, hint, turns = 8, round = 7, mode = 4)
    if turns_left < 0:
        return False
    
    random.seed(random.randint(1, 1000))
    hint, money = stage_end(turns_left, money, hint, 2)
    time.sleep(0.2)
    
    #Stage 8.1
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Stage 8/8")
    print("-"*50)
    print("Vòng này gồm 2 giai đoạn, và số lượt chơi được dùng chung cho cả 2 giai đoạn")
    print("Bạn có thể mua gợi ý ở đầu giai đoạn 2")
    print("LƯU Ý: Sau khi mua hàng số tiền dư không thể quy đổi thành lượt chơi tiếp")
    print()
    print(f"Số tiền bạn đang có: {money}")
    pay = int_input("Nhập số tiền bạn muốn quy đổi thành lượt chơi ($1 = 2 lượt thêm): ", 1, money)
    new_turns = 2*pay
    money -= pay
    print("-"*50)
    print(f"Đã đổi thành {2*pay} lượt chơi thêm")
    print(f"Bạn còn ${money}")
    time.sleep(1.5)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("----- Quy luật tính điểm -----")
    print("Đoán đúng số  : +15")
    print("Khoảng +- 5   : +3")
    print("Khoảng +- 50  : +2")
    print("Khoảng +- 500 : +1")
    print("Khoảng +- 2500: +0")
    print("Còn lại       : -1")

    print("\nNhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)

    turns_left = stage_boss(1, 10000, None, 30 + new_turns, 1, 8, 10000)
    if turns_left < 0:
        return False
    
    # Stage 8.2
    random.seed(random.randint(1, 1000))
    os.system('cls' if os.name == 'nt' else 'clear')
    print("{0}\t\t\t\t{1}".format("Chưa qua màn:", " $0"))
    print("{0}\t\t\t{1}".format(f"Không thưởng lượt dư:", f" $0"))
    print("{0}\t{1}".format(f"${money}: Thưởng $1 lời mỗi $5 (tối đa $5):", f" ${min(money//5, 5)}")) 
    money += min(money//5, 5)
    print(" "*37, "-"*8)
    print("{0}\t\t\t{1}".format("Tổng tiền hiện có:", f" ${money}"))
    print("-"*50)
    print("{0}\t\t\t{1}".format("Số lượt chơi còn lại:", f" {turns_left} lượt"))
    print("\tNhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)
    hint, money = shoptime(hint, money)
    print("\tNhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)

    os.system('cls' if os.name == 'nt' else 'clear')
    print("----- Quy luật tính điểm -----")
    print("Đoán đúng số   : +15")
    print("Khoảng +- 50   : +3")
    print("Khoảng +- 500  : +2")
    print("Khoảng +- 5000 : +1")
    print("Khoảng +- 25000: +0")
    print("Còn lại        : -1")

    print("\nNhấn Enter để tiếp tục...")
    while True:
        if keyboard.is_pressed('enter'):
            break
    time.sleep(0.2)
    
    turns_left = stage_boss(1, 100000, hint, turns_left, 2, 8, 100000)
    if turns_left < 0:
        return False
    
    hint, money = stage_end(turns_left, money, hint)
    time.sleep(0.2)
    print(f"Chúc mừng, bạn đã thắng được ${money}!")
    return True

# MainGame()