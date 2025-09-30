'''
CÁC THAM SỐ:
    X là đáp án
    Y là số đoán
    f là số gợi ý từ Status
    a,b,z là số thành phần của X  (z là số thực sau dấu phẩy)
    c,d,z2 là số thành phần của Y (z2 là số thực sau dấu phẩy)
    F là gợi ý từ Hint
'''

# -------------------------
# CÁC MÀN CHƠI
# -------------------------

import random
import numpy as np
from DATA import HINT_GROUPS

class Stage:
    def __init__(self, left, right, turn, status = "Nhập số", round = 0, money = 0 ):
        self.left = left
        self.right = right
        # self.X = random.randint(left, right) → luôn random số mới, nên tham số X ở đầu vẫn đang… thừa (không dùng đến).
        self.X = random.randint(left, right)
        self.turn = turn
        self.status = status
        self.round = round

    def kt_so(self, player_input):
        try:
            y = int(player_input)     #input() → lệnh cho console chứ không phải GUI => trong GUI nên lược input
            return y
        except ValueError:
            return None

    #chỗ def so_sanh(self) không cần ghi tham số Y: def so_sanh(self, Y) vì đã có hàm kt_so
    def so_sanh(self, Y):
        if Y is None:  # nhập không hợp lệ
            self.status = "Bạn phải nhập số nguyên!"
            return False

        self.turn -= 1
        if Y == self.X:
            self.status = "Bingo!"
            return True
        else:
            return False


class Rut_gon(Stage):   #class rút gọn khoảng đoán, dùng cho màn 1,3
    def so_sanh(self,Y):
        is_win = super().so_sanh(Y)

        if not is_win:
            if self.X < Y:
                self.status = f"{Y} lớn hơn số cần tìm"
                self.right = min(Y-1, self.right)
            else:
                self.status = f"{Y} bé hơn số cần tìm"
                self.left = max(Y+1, self.left)
        return is_win

class Hai_khoang(Stage):    #dùng cho màn 4
    def __init__(self,left, right, turn, status, round, left2, right2):
        super().__init__(left, right, turn, status, round)   #vậy dù cần lấy X từ Stage thì vẫn không cần phải thêm nó vào hàm super() vì đã có random đè
        self.left2 = left2
        self.right2 = right2
        self.X2 = random.randint(left2, right2)

    def kt_so(self, player_input):
        try:
            y, y2 = map(int, player_input.split())
            return y, y2
        except ValueError:
            self.status = "Vui lòng nhập 2 số hợp lệ, cách nhau bằng dấu cách."
            return None

    #Lưu ý nhớ truyền tham số Y,Y2 qua kt_so trước rồi bắt đầu dùng hàm so sánh
    def so_sanh(self,Y,Y2):      #override lại hàm so_sanh ở lớp cha

        if Y is None or Y2 is None:  # nhập không hợp lệ
            self.status = "Bạn phải nhập đủ 2 số nguyên: <A><space><B>!"
            return False

        elif Y == self.X and Y2 == self.X2:
            self.status = "Bingo!"
            return True

        else:
            # Phân loại trường hợp để thông báo:
            arr = [0, 0, 0]
            # arr[0]: số lần người chơi đoán nhỏ hơn x/x2.
            # arr[1]: số lần đoán bằng x/x2.
            # arr[2]: số lần đoán lớn hơn x/x2.
            if self.X > Y:
                arr[0] += 1
            elif self.X == Y:
                arr[1] += 1
            else:
                arr[2] += 1

            if self.X2 > Y2:
                arr[0] += 1
            elif self.X2 == Y2:
                arr[1] += 1
            else:
                arr[2] += 1

            #Các loại thông báo:
            if arr[2] == 2:  # cả hai số đều lớn hơn
                self.right = max(self.left, min(Y - 1, self.right))
                self.right2 = max(self.left2, min(Y2 - 1, self.right2))
                self.status = f"Cả {Y} và {Y2} đều lớn hơn số cần đoán"

            elif arr[0] == 2:  # cả hai số đều nhỏ hơn
                self.left = min(self.right, max(Y + 1, self.left))
                self.left2 = min(self.right2, max(Y2 + 1, self.left2))
                self.status = f"Cả {Y} và {Y2} đều nhỏ hơn số cần đoán"

            else:
                self.status = np.random.choice(
                    [f"Có 1 số nhỏ hơn", f"Có 1 số lớn hơn"],
                    p = [0.5,0.5]
                )

            if arr[1] == 1:
                self.status +="\nĐang có 1 số đúng"

            self.turn -= 1
            return False


class Anh_xa(Stage):  #Dùng cho stage 2,6,5
    def so_sanh(self,Y):
        is_win = super().so_sanh(Y)

        if not is_win:
            typee = random.randint(1, 3)
            a = random.randint(1, 10)

            if self.round == 6:
                def sum_mys(num, type):     #Hàm tính các số ánh xạ
                    if type == 2:
                        res = 1
                    else:
                        res = 0
                    for i in str(num):
                        match type:
                            case 1:
                                res += int(i) ** 2       #tổng bình phương các số thành phần
                            case 2:
                                res *= int(i)            #tích các số thành phần
                            case 3:
                                res += int(i) // 2       #thương nguyên các số thành phần
                    return res

                self.status = f"Dạng {typee}: Nếu ánh xạ của số cần tìm là {sum_mys(self.X, typee)} thì ánh xạ của {Y} là {sum_mys(Y, typee)}"

            if self.round == 2:
                def diff(lst):   #Hàm trừ các số
                    if not lst:
                        return 0
                    res = lst[0]
                    for i in lst[1:]:
                        res -= i
                    return res

                def mult(lst):   #Hàm nhân các số
                    if not lst:
                        return 0
                    res = lst[0]
                    for i in lst[1:]:
                        res *= i
                    return res

                if typee == 1:      #Tổng của hiệu
                    self.status = f"Tổng các chữ số trong hiệu của {Y} và số cần tìm = {sum(int(i) for i in str(abs(Y - self.X)))}"

                elif typee == 2:  # Hiệu của tổng
                    digits = list(int(i) for i in str(abs(Y + self.X)))
                    self.status = f"Hiệu các chữ số trong tổng của {Y} và số cần tìm = {diff(digits)}"

                elif typee == 3: # Tích của tích
                    digits = list(int(i) for i in str(abs(Y * self.X)))
                    self.status = f"Tích các chữ số trong tích của {Y} và số cần tìm = {mult(digits)}"

            if self.round == 5:
                self.status = f"Với a = {a} thì số cần tìm trở thành {str(self.X*a)[-1]} và {Y} trở thành {str(Y*a)[-1]}"

        return is_win

class Float(Stage):       #Lưu ý màn này sẽ cần chỉnh lại random của x = left, right *10
    def __init__(self, left, right, turn, status, round):
        super().__init__(left, right, turn, status, round)
        self.X = random.randint(left*10, right*10)

    def kt_so(self, player_input):
        try:
            y = int(float(player_input)*10)     #input() → lệnh cho console chứ không phải GUI => trong GUI nên lược input
            return y
        except ValueError:
            return None

    def so_sanh(self,Y):
        is_win = super().so_sanh(Y)

        if not is_win:
            if self.X < Y:
                self.status = f"{Y/10} lớn hơn số cần tìm"

            else:
                self.status = f"{Y/10} bé hơn số cần tìm"
        return is_win

class Score(Stage):
    def __init__(self,left, right, turn, status, round, S = 0):
        super().__init__(left, right, turn, status, round)   #vậy dù cần lấy X từ Stage thì vẫn không cần phải thêm nó vào hàm super() vì đã có random đè
        self.S = S
        self.phase = 1

    def calc_range(self, x, k, N):      #modulo
        #x = số bí mật,
        #k = bán kính phạm vi (ví dụ 25),
        #N = max_right + 1 (tổng số phần tử trong vòng).

        left = (x - k) % N                  # left và right theo modulo
        right = (x + k) % N

        if left <= right:
            # không bị vòng qua biên
            return list(range(left, right + 1))
        else:
            # bị vòng qua biên (chia làm 2 đoạn)
            return list(range(left, N)) + list(range(0, right + 1))

    def so_sanh_phrase1(self,Y):
        if self.S >= 50:
            self.status = "Chúc mừng!! Bạn đã thắng được boss"
            return True
        if Y == self.X:
            # Đây chỉ là “đoán trúng”, nhưng ta vẫn muốn cộng điểm chứ không thắng ngay
            self.S += 10
            self.status = "Bạn đoán chính xác! +10 điểm"
            return False
            #if not is_right:
        if Y in self.calc_range(self.X, 5, 10001):
            self.S += 5
            self.status = f"Bạn được cộng 5 điểm \n(Nằm trong khoảng ± 5)"
        elif Y in self.calc_range(self.X, 50, 10001):
            self.S += 2
            self.status = f"Bạn được cộng 2 điểm \n(Nằm trong khoảng ± 50)"
        elif Y in self.calc_range(self.X, 500, 10001):
            self.S += 1
            self.status = f"Bạn được cộng 1 điểm \n(Nằm trong khoảng ± 500)"
        elif Y in self.calc_range(self.X, 3000, 10001):
            self.S += 0
            self.status = f"Bạn được cộng 0 điểm \n(Nằm trong khoảng ± 3000)"
        else:
            self.S -= 1
            self.status = f"Bạn bị trừ 1 điểm \n(Đoán quá xa so với kết quả)"

        self.turn -=1

    def so_sanh_phrase2(self, Y):
        self.right = 100000

        if self.S >= 50:
            self.status = "Chúc mừng!! Bạn đã thắng được boss"
            return True

        if Y == self.X:
            # Đây chỉ là “đoán trúng”, nhưng ta vẫn muốn cộng điểm chứ không thắng ngay
            self.S += 10
            self.status = "Bạn đoán chính xác! +10 điểm"
            return False
            #if not is_right:
        if Y in self.calc_range(self.X, 50, 100001):
            self.S += 5
            self.status = f"Bạn được cộng 5 điểm \n(Nằm trong khoảng ± 50)"
        elif Y in self.calc_range(self.X, 500, 100001):
            self.S += 2
            self.status = f"Bạn được cộng 2 điểm \n(Nằm trong khoảng ± 500)"
        elif Y in self.calc_range(self.X, 5000, 100001):
            self.S += 1
            self.status = f"Bạn được cộng 1 điểm \n(Nằm trong khoảng ± 5000)"
        elif Y in self.calc_range(self.X, 30000, 100001):
            self.S += 0
            self.status = f"Bạn được cộng 0 điểm \n(Nằm trong khoảng ± 30000)"
        else:
            self.S -= 1
            self.status = f"Bạn bị trừ 1 điểm \n(Đoán quá xa so với kết quả)"

        self.turn -=1

    def so_sanh(self, Y):
        """
        Gọi hàm này trong game. Nó tự động chuyển từ phase 1 sang phase 2.
        """
        # ---- PHA 1 ----
        if self.phase == 1:
            win = self.so_sanh_phrase1(Y)
            # Nếu chưa đủ điểm và đã hết lượt -> chuyển pha 2
            if self.turn <= 0 and self.S < 50:
                # reset thông số cho phase 2
                self.phase = 2
                self.turn  = 30           # số lượt mới (tùy bạn muốn)
                self.right = 100000       # mở rộng giới hạn
                self.X = random.randint(self.left, self.right)
                self.status = ("Bạn chưa đủ 50 điểm. "
                               "Bắt đầu Phase 2 với phạm vi lớn hơn!")
            return win

        # ---- PHA 2 ----
        else:
            return self.so_sanh_phrase2(Y)

# -------------------------
# MONEY
# -------------------------
class Money():
    def __init__(self, tien=0):
        self.tien = tien
        
    def earn(self, value):
        self.tien += value

    def spend(self, value):
        if self.tien >= value:
            self.tien -= value
            return True
        return False

    def thong_bao(self):     #khỏi cần thông báo return từng dòng mà lấy ra thành một hàm riêng để thông báo
        return f"${self.tien}"

# -------------------------
# HINT
# -------------------------

class Hint():
    def __init__(self):
        self.inventory = []
        self.message = [] #Nếu muốn dùng nhiều hint trong 1 stage, nên biến self.message thành list

    def buy_hint(self, hint_buy:str, tien:"class_Money"):
        # Nếu đã mua rồi thì không cho mua lại
        if hint_buy in self.inventory:
            return False, "Bạn đã mua hint này rồi!"
        # Tìm hint trong Data
        for nest_category in HINT_GROUPS.values():
            if hint_buy in nest_category["items"]: #vd như sum, even,...
                cost = nest_category["items"][hint_buy]["cost"]

                if cost == -1:
                    self.inventory.append(hint_buy)
                    return True, f"Đã mua hint: {hint_buy}"

                if tien.spend(cost):
                    self.inventory.append(hint_buy)
                    return True, f"Đã mua hint: {hint_buy}"
                else:
                    return False, "Không đủ tiền!"
        return False, "Hint không tồn tại!"

    def use_1_hint(self, stage_obj:"class_Stage(thông_số)",apply, f_val,Y):
        if not self.inventory:
            return "Bạn chưa mua hint này!"

        self.message = [] #reset mỗi vòng

        def is_prime(n):
            return n in (2, 3, 5, 7)

        if stage_obj.round ==4:
            if not f_val:  # chưa nhập khoảng
                return "Vui lòng nhập '1' (khoảng 1) hoặc '2' (khoảng 2) để chọn số cần hint."
            try:
                choice = int(f_val)
            except ValueError:
                return "Khoảng phải là số 1 hoặc 2!"
            if choice == 1:
                X_target = stage_obj.X
            elif choice == 2:
                X_target = stage_obj.X2
            else:
                return "Khoảng không hợp lệ! Nhập 1 hoặc 2."
        else:
            X_target = stage_obj.X

        #gợi ý cộng lượt chơi
        if apply == "add1":
            stage_obj.turn += 1
            self.message.append(f"Được +1 lượt")
        elif apply == "add2":
            stage_obj.turn += 2
            self.message.append(f"Được +2 lượt")
        elif apply == "add3":
            stage_obj.turn += 3
            self.message.append(f"Được +3 lượt")

        #gợi ý về X
        elif apply == "sum":
            self.message.append(f"Tổng các chữ số là {sum(int(i) for i in str(X_target))}")
        elif apply == "even":
            self.message.append(f"Số chữ số chẵn là {sum(1 for i in str(X_target) if int(i) % 2 == 0)}")
        elif apply == "odd":
            self.message.append(f"Số chữ số lẻ là {sum(1 for i in str(X_target) if int(i) % 2 != 0)}")
        elif apply == "max":
            self.message.append(f"Chữ số lớn nhất là {max(int(i) for i in str(abs(X_target)))}")
        elif apply == "min":
            self.message.append(f"Chữ số nhỏ nhất là {min(int(i) for i in str(abs(X_target)))}")
        elif apply == "prime":
            self.message.append(f"Số chữ số là số nguyên tố (thuộc (2,3,5,7)) là {sum(1 for i in str(X_target) if is_prime(int(i)))}")
        elif apply == "last":
            self.message.append(f"Chữ số cuối là {str(X_target)[-1]}")
        elif apply == "first":
            self.message.append(f"Chữ số đầu là {str(X_target)[0]}")

        # gợi ý về khoảng giá trị
        elif apply == "check10":
            self.message.append("Nhập số đoán bạn muốn kiểm tra trong khoảng +-10:")
            try:
                F = int(f_val)
            except Exception:
                self.message.append("Giá trị kiểm tra không hợp lệ.")
                return "\n".join(self.message)
            if F - 10 <= X_target <= F + 10:
                self.message.append(f"Số thuộc khoảng {F - 10} đến {F + 10}")
            else:
                self.message.append(f"Kiểm tra thất bại, trừ 1 lượt")
                

        elif apply == "check25":
            self.message.append("Nhập số đoán bạn muốn kiểm tra trong khoảng +-25:")
            try:
                F = int(f_val)
            except Exception:
                self.message.append("Giá trị kiểm tra không hợp lệ.")
                return "\n".join(self.message)
            if F - 25 <= X_target <= F + 25:
                self.message.append(f"Số thuộc khoảng {F - 25} đến {F + 25}")
            else:
                self.message.append(f"Kiểm tra thất bại, trừ 1 lượt")

        # gợi ý về tiền thưởng
        elif apply == "roulette":
            if random.randint(1, 10) == 1:
                stage_obj.money.earn(10)
                self.message.append("Bạn đã trúng $10")
            else:
                self.message.append("Bạn không trúng thưởng")

        elif apply == "bet":
            self.message.append("Nhập số tiền bạn muốn cược ($2 <= Bet <= $10)")
            try:
                F = int(f_val)
            except Exception:
                self.message.append("Giá trị kiểm tra không hợp lệ.")
                return "\n".join(self.message)
            if 2<=F<=10:
                if stage_obj.so_sanh(Y):
                    stage_obj.money.earn(F * (stage_obj.right - stage_obj.left + 1))
                    self.message.append(f"Chính xác, tiền thưởng x khoảng đoán = {stage_obj.money.thong_bao()}")
                else:
                    self.message.append("Sai")
            else:
                self.message.append("Ngoài số tiền cho phép")

        elif apply == "exchange":
            self.message.append("Nhập số tiền bạn muốn đổi ($2 <= Exchange <= $10):")
            try:
                F = int(f_val)
            except Exception:
                self.message.append("Giá trị kiểm tra không hợp lệ.")
                return "\n".join(self.message)
            if 10>=F>=2 and stage_obj.money.spend(F):
                stage_obj.turn += F//2
                self.message.append(f"Được +{F//2}lượt")
            else:
                self.message.append("Ngoài số tiền cho phép")
        return "\n".join(self.message)
