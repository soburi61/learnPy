import csv
# ナップサック問題の設定
def load_items(file_name):
    items = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            weight, value = map(int, row)
            items.append((weight, value))
    return items

# ファイルからアイテムを読み込む
ITEMS = load_items("c:\git\learnPy\GA\items.csv")
MAX_WEIGHT = 30 # ナップサックの容量

# 重さと価値を分ける
WEIGHTS = [item[0] for item in ITEMS] # 各アイテムの重さ
VALUES = [item[1] for item in ITEMS] # 各アイテムの価値

def knapsack_dp_with_items(MAX_WEIGHT, WEIGHTS, VALUES):
    n = len(WEIGHTS)
    # 動的計画法のテーブル初期化
    K = [[0 for x in range(MAX_WEIGHT + 1)] for x in range(n + 1)]

    # ナップサック問題を解く
    for i in range(1, n + 1):
        for w in range(1, MAX_WEIGHT + 1):
            if WEIGHTS[i-1] <= w:
                # アイテムを追加する場合としない場合で最大の価値を選択
                K[i][w] = max(VALUES[i-1] + K[i-1][w-WEIGHTS[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]

    # 最適なアイテムの組み合わせを決定
    w = MAX_WEIGHT
    chosen_items = [0] * n
    for i in range(n, 0, -1):
        if K[i][w] != K[i-1][w]:
            chosen_items[i-1] = 1
            w -= WEIGHTS[i-1]

    return chosen_items, K[n][MAX_WEIGHT]

# ナップサック問題の解を計算し、結果を出力
individual, fitness = knapsack_dp_with_items(MAX_WEIGHT, WEIGHTS, VALUES)
print("Best Individual: ", individual)
print("Best Fitness: ", fitness)
