# 重さと価値の定義

ITEMS = [(4, 12), (2, 2), (2, 1), (1, 1), (10, 4)]  # 各アイテムは(重さ, 価値)

# 重さと価値を分ける
WEIGHTS = [item[0] for item in ITEMS] # 各アイテムの重さ
VALUES = [item[1] for item in ITEMS] # 各アイテムの価値
MAX_WEIGHT = 15 # 制限  # ナップサックの容量

# 動的計画法によるナップサック問題の解法
def knapsack_dp(MAX_WEIGHT, WEIGHTs, VALUES):
    n = len(WEIGHTs)
    K = [[0 for x in range(MAX_WEIGHT + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(MAX_WEIGHT + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif WEIGHTs[i-1] <= w:
                K[i][w] = max(VALUES[i-1] + K[i-1][w-WEIGHTs[i-1]],  K[i-1][w])
            else:
                K[i][w] = K[i-1][w]

    return K[n][MAX_WEIGHT]

# ナップサック問題の解を計算
print(knapsack_dp(MAX_WEIGHT, WEIGHTs, VALUES))