import random
from deap import base, creator, tools, algorithms
import numpy
# ナップサック問題の設定
ITEMS = [(4, 12), (2, 2), (2, 1), (1, 1), (10, 4)]  # 各アイテムは(重さ, 価値)
MAX_WEIGHT = 15 # 制限

# 適応度関数の定義
def evaluate(individual):
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
toolbox.register("mate", tools.cxTwoPoint)  # 交叉を行う関数を登録
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)  # 突然変異を行う関数を登録
toolbox.register("select", tools.selTournament, tournsize=3)  # 選択を行う関数を登録

# メイン関数
def main():
    random.seed(64)
    pop = toolbox.population(n=50)  # 初期個体群の生成
    hof = tools.HallOfFame(1)  # Hall of Fameの設定
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)  # 統計情報の設定
    stats.register("avg", numpy.mean)  # 平均の統計情報を登録
    stats.register("min", numpy.min)  # 最小値の統計情報を登録
    stats.register("max", numpy.max)  # 最大値の統計情報を登録

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, halloffame=hof, verbose=True)  # 遺伝的アルゴリズムの実行

    return pop, log, hof  # 最終的な個体群、ログ、Hall of Fameを返す

if __name__ == "__main__":
    pop, log, hof = main()  # メイン関数の実行
    best_ind = hof[0]  # 最良個体を取得
    print("Best Individual: ", best_ind)  # 最良個体の表示
    print("Best Fitness: ", best_ind.fitness.values[0])  # 最良個体の適応度の表示

