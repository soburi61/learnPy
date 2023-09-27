'''
一部コード,コメントにchatGPTを活用
'''

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import datetime
import matplotlib.pyplot as plt
#------定義------
# 重要度、締切日（日付）、タスクの軽さを入力変数とします

def calculate_priority(name, importance_value, deadline_date, lightness_value):
    # 重要度、締切日（日付）、タスクの軽さを入力変数とします
    importance = ctrl.Antecedent(np.arange(0, 11, 1), 'importance')
    deadline = ctrl.Antecedent(np.arange(0, 11, 1), 'deadline')
    lightness = ctrl.Antecedent(np.arange(0, 11, 1), 'lightness')

    # 優先度を出力変数とします
    priority = ctrl.Consequent(np.arange(0, 101, 1), 'priority')

    # 各変数のファジィ集合を定義します
    importance['low'] = fuzz.trimf(importance.universe, [0, 0, 5])
    importance['medium'] = fuzz.trimf(importance.universe, [0, 5, 10])
    importance['high'] = fuzz.trimf(importance.universe, [5, 10, 10])

    deadline['near'] = fuzz.trimf(deadline.universe, [0, 0, 5])
    deadline['medium'] = fuzz.trimf(deadline.universe, [0, 5, 10])
    deadline['far'] = fuzz.trimf(deadline.universe, [5, 10, 10])

    lightness['light'] = fuzz.trimf(lightness.universe, [0, 0, 5])
    lightness['medium'] = fuzz.trimf(lightness.universe, [0, 5, 10])
    lightness['heavy'] = fuzz.trimf(lightness.universe, [5, 10, 10])

    priority['low'] = fuzz.trimf(priority.universe, [0, 0, 50])
    priority['medium'] = fuzz.trimf(priority.universe, [0, 50, 100])
    priority['high'] = fuzz.trimf(priority.universe, [50, 100, 100])

    # ルールを定義します
    rule1 = ctrl.Rule(importance['low'] | deadline['far'] | lightness['light'], priority['low'])
    rule2 = ctrl.Rule(importance['medium'] | deadline['medium'] | lightness['medium'], priority['medium'])
    rule3 = ctrl.Rule(importance['high'] | deadline['near'] | lightness['heavy'], priority['high'])

    # ルールを制御システムに追加します
    priority_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

    # 制御システムをシミュレーションに接続します
    priority_eval = ctrl.ControlSystemSimulation(priority_ctrl)

    # 具体的な入力値を設定します
    priority_eval.input['importance'] = importance_value
    # 締切日を日付または時間形式から数値に変換し、適切な値を設定します
    current_date = datetime.datetime.now()  # 現在の日付を取得
    days_until_deadline = (deadline_date - current_date).days
    # 締切日までの日数を0から10の範囲にスケーリングします
    deadline_scaled = min(max(days_until_deadline / 10, 0), 10)
    priority_eval.input['deadline'] = deadline_scaled
    priority_eval.input['lightness'] = lightness_value

    # 優先度を計算します
    priority_eval.compute()
    
    # プロットして結果を可視化する
    priority.view(sim=priority_eval)
    # グラフにタイトルを追加します
    plt.title(name)
    
    # グラフを表示します
    plt.show()

    # 優先度を返します
    return priority_eval.output['priority']


# タスクを優先度順に並び替える関数を定義します
def sort_tasks(task_list):
    # ラムダでソートを定義
    task_list.sort(key=lambda x: calculate_priority(x["name"], x["importance"], x["deadline_date"], x["lightness"]), reverse=True)
    return task_list


# タスクのリストを定義します
tasks = [
    {"name": "タスクA", "importance": 8, "deadline_date": datetime.datetime(2023, 10, 15), "lightness": 7},
    {"name": "タスクB", "importance": 5, "deadline_date": datetime.datetime(2023, 10, 10), "lightness": 5},
    {"name": "タスクC", "importance": 7, "deadline_date": datetime.datetime(2023, 10, 5), "lightness": 9},
    {"name": "タスクD", "importance": 9, "deadline_date": datetime.datetime(2023, 10, 20), "lightness": 3},
]

# タスクを優先度順に並び替えて結果を取得します
sorted_tasks = sort_tasks(tasks)

# 優先度順に並び替えたタスクを表示します
for i, task in enumerate(sorted_tasks, start=1):
    print(f"タスク{i}: 名前({task['name']}), 重要度({task['importance']}), 締切日({task['deadline_date']}), 軽さ({task['lightness']})")

