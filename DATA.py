STAGE = {
    1:[1,100,10,1],
    2:[1,100,10,2],
    3:[1,500,8,3],
    4:[1,250,15,4,251,500],
    5:[1,250,10,5],
    6:[1,500,10,6],
    7:[1,1000,10,7],
    8:[1,10000,20,8],
}

# DATA.py
HINT_GROUPS = {               #gọi dict[key] giống như list[index], key đóng vai trò như index trong dict
    "digit": {   # Nhóm 1: Phân tích chữ số       #group = HINT_GROUP.values =dict digit
        "label": "Phân tích chữ số",              #hint_key = dict label, dict items
        "items": {                                
            "sum":     {"desc": "Tổng các chữ số",       "cost": 4},
            "even":    {"desc": "Đếm chữ số chẵn",      "cost": 2},
            "odd":     {"desc": "Đếm chữ số lẻ",        "cost": 2},
            "max":     {"desc": "Chữ số lớn nhất",      "cost": 5},
            "min":     {"desc": "Chữ số nhỏ nhất",      "cost": 5},
            "prime":   {"desc": "Chữ số nguyên tố",     "cost": 2},
            "first":   {"desc": "Tiết lộ chữ số đầu",   "cost": 10},
            "last":    {"desc": "Tiết lộ chữ số cuối",  "cost": 5},
        }
    },
    "range": {  # Nhóm 2: Khoảng giá trị
        "label": "Khoảng giá trị",
        "items": {
            "check10": {"desc": "Kiểm tra ±10",          "cost": 7},
            "check25": {"desc": "Kiểm tra ±25",          "cost": 4},
        }
    },
    "turn": {   # Nhóm 3: Thêm lượt
        "label": "Thêm lượt",
        "items": {
            "add1": {"desc": "Tặng 1 lượt", "cost": 1},
            "add2": {"desc": "Tặng 2 lượt", "cost": 3},
            "add3": {"desc": "Tặng 3 lượt", "cost": 6},
        }
    },
    "money": {  # Nhóm 4: Tiền & may rủi
        "label": "Tiền & Cược",
        "items": {
            "roulette": {"desc": "Roulette 10% trúng $10", "cost": 1},
            "bet":      {"desc": "Vé cược xN khi trúng",   "cost": -1},
            "exchange": {"desc": "Đổi $2 = 1 lượt",        "cost": -1},
        }
    }
}

'''         """CHỈ CẦN NHẬP THAM SỐ X"""
hint = { 1: ["Tổng các chữ số", 4],                           #digit
         2: ["Số chữ số chẵn", 2],                           #digit
         3: ["Số chữ số lẻ", 2],                             #digit
         4: ["Chữ số lớn nhất", 5],                          #digit
         5: ["Chữ số nhỏ nhất", 5],                          #digit
         
         6: ["Số chữ số lớn hơn bằng 5", 3],                    #bỏ 
         
         7: ["Số chữ số là số nguyên tố", 2],                #digit
         8: ["Tiết lộ chữ số cuối", 5],                      #digit
         9: ["Tiết lộ chữ số đầu", 10],                      #digit
         
         
             """TÁC ĐỘNG ĐẾN STAGE(TURN)"""
         10: ["Miễn phí 1 lượt đoán", 1],                    #turn
         11: ["Miễn phí 2 lượt đoán", 3],                    #turn
         12: ["Miễn phí 3 lượt đoán", 6],                    #turn
         
         13: ["- 50%", 4],                                      #bỏ 
             
             """CHỈ CẦN NHẬP THAM SỐ X"""
         14: ["Loại bỏ 1 khoảng sai", -1],                   #range
         15: ["Kiểm tra số trong khoảng +-10", 7],           #range
         16: ["Kiểm tra số trong khoảng +-25", 4],           #range
         
         17: ["A fun fact", 1],                                 #bỏ
             
             """TÁC ĐỘNG ĐẾN STAGE(MONEY)"""
         18: ["Roulette (10% nhận $10)", 1],                 #money
         19: ["Vé cược (dùng trong lượt)", -1],              #money
         20: ["Đổi tiền thành lượt chơi ($2 = 1 lượt)", -1]  #money
         }
'''
