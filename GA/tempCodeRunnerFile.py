import random
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import numpy
import csv


#----GA設定-----
#選択法 トーナメント選択
N = 50 # 個体数
NGEN = 400 # 止める世代数
MUTPB = 0.2 # 個体が突然変異する確率
INDPB = 0.1 # MUTPBの確率で突然変異した個体の各遺伝子が突然変異する確率
CXPB = 0.5 # 選択された個体群のうちどれだけの割合のペアが交叉を行うかの確率
CXTYPE = 2 # 1は一点交叉 2は2点交叉 3は一様交叉
CXINDPB = 0.8 # 一様交叉の場合の各遺伝子の交叉確率
TOURNSIZE = 10  # トーナメントサイズ 大きいと選択圧が高くなる
#---------------
# ナップサック問題の設定
def load_items(file_name):
    # ファイルからアイテムを読み込む
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
MAX_WEIGHT = 30 # 制限
#--------------------
# 適応度関数の定義
def evaluate(individual):
    # 適応度を評価する
    weight = 0  # 重さの初期値
    value = 0  # 価値の初期値
    for item, included in zip(ITEMS, individual):
        if included:
            weight += item[0]  # アイテムの重さを加算
            value += item[1]  # アイテムの価値を加算
            if weight > MAX_WEIGHT:  # 重量が最大重量を超えた場合
                return 0,  # 重量オーバーの場合は価値を0とする
    return value,  # 重量が最大重量を超えない場合は価値を返す

# 遺伝的アルゴリズムの設定
creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # 最大化適応度の作成
creator.create("Individual", list, fitness=creator.FitnessMax)  # 個体の作成

toolbox = base.Toolbox()  # ツールボックスの作成
toolbox.register("attr_bool", random.randint, 0, 1)  # 0または1のランダムな整数を生成する関数を登録
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(ITEMS))  # 個体の初期化関数を登録
toolbox.register("population", tools.initRepeat, list, toolbox.individual)  # 個体群の初期化関数を登録
toolbox.register("evaluate", evaluate)  # 評価関数を登録
if CXTYPE == 1:
    toolbox.register("mate", tools.cxTwoPoint)  # 交叉を行う関数を登録(2点交叉)
elif CXTYPE == 2:
    toolbox.register("mate", tools.cxOnePoint)  # 交叉を行う関数を登録(1点交叉)
else:
    toolbox.register("mate", tools.cxUniform, indpb=CXINDPB)

toolbox.register("mutate", tools.mutFlipBit, indpb=INDPB)  # 突然変異を行う関数を登録(突然変異する個体の各遺伝子を確率で反転)
toolbox.register("select", tools.selTournament, tournsize=TOURNSIZE)  # トーナメント選択を行う関数を登録

def main():
    # メイン関数
    random.seed(39)
    pop = toolbox.population(n=N) 
    hof = tools.HallOfFame(1) # 一番適応度が高い個体

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=stats, halloffame=hof, verbose=True)

    # 平均値の推移のグラフを描画
    gen = log.select("gen")
    avg = log.select("avg")

    # グラフ描画部分
    plt.plot(gen, avg, label="Average Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.yticks(numpy.arange(int(min(avg)), int(max(avg))+1, step=1))  # 目盛りを設定

    plt.title("Fitness Evolution")
    plt.legend()
    plt.show()

    return pop, log, hof

# メイン関数の実行
if __name__ == "__main__":
    pop, log, hof = main()
    best_ind = hof[0]
    print("Best Individual: ", best_ind)
    print("Best Fitness: ", best_ind.fitness.values[0])