# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:54:46 2023

"""


import cv2
import numpy as np
from IPython.display import Image, display
import csv
from matplotlib import pyplot as plt

# 画像を表示する関数
def imshow(img):
    ret, encoded = cv2.imencode(".png", img)
    display(Image(encoded))


# 外れ値を除外する関数（dataを基準にしてdata2も除外）
def remove_outliers(data, data2, threshold=1.5):
    mean = np.mean(data)
    std = np.std(data)
    data_cleaned = []
    data2_cleaned = []
    for x, y in zip(data, data2):
        if abs(x - mean) < threshold * std:
            data_cleaned.append(x)
            data2_cleaned.append(y)
    return data_cleaned, data2_cleaned


def detect_ellipses(path):
    # 画像を読み込む
    img = cv2.imread(path)
    
    # 画像をグレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    average = np.mean(np.array(gray))  # 画素値の平均を計算
    if average < 128:  # Assuming the background is black (average < 128)
        gray = 255 - gray  # Invert the pixel values
        
    # 2値化処理
    ret, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # モルフォロジー演算によるノイズ除去
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # sure backgroundのマーカーを作成
    sure_bg = cv2.dilate(bin_img, kernel, iterations=3)

    # 距離変換を行い sure foregroundのマーカーを作成
    dist = cv2.distanceTransform(bin_img, cv2.DIST_L2, 5)

    ret, sure_fg = cv2.threshold(dist, 0.3 * dist.max(), 255, cv2.THRESH_BINARY)
    sure_fg = sure_fg.astype(np.uint8)  # float32 -> uint8
    
    # 不明な領域を作成
    unknown = cv2.subtract(sure_bg, sure_fg)

    # マーカーの作成
    ret, markers = cv2.connectedComponents(sure_fg)
    
    markers += 1
    markers[unknown == 255] = 0

    # Watershedを適用
    markers = cv2.watershed(img, markers)

    labels = np.unique(markers)
    
    ellipses = []
    for label in labels[2:]:
        target = np.where(markers == label, 255, 0).astype(np.uint8)
        contours, hierarchy = cv2.findContours(target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ellipses.append(contours[0])
    
    # 検出した楕円を画像に描画
    img_with_ellipses = img.copy()
    cv2.drawContours(img_with_ellipses, ellipses, -1, color=(0, 0, 255), thickness=2)
    imshow(img_with_ellipses)
            
    # 特徴量をCSVファイルに保存
    csv_file_name = "ellipse_detail.csv"
    
    with open(csv_file_name, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Object No.", "面積", "周囲長", "円形度", "縦横比", "面積比"])
        writer.writerows(detail_list)
    
    # 面積と周囲長の外れ値を除外
    area_list, perimeter_list = remove_outliers([r[1] for r in detail_list], [r[2] for r in detail_list])

    # 面積と円形度の外れ値を除外
    _, circularity_list = remove_outliers([r[1] for r in detail_list], [r[3] for r in detail_list])
    
    # 面積と周囲長の散布図を表示
    plt.scatter(area_list, perimeter_list, color='blue')
    plt.xlabel('面積')
    plt.ylabel('周囲長')
    plt.title('面積 vs 周囲長 散布図')
    plt.show()
    
    # 面積と円形度の相関グラフを表示
    plt.scatter(area_list, circularity_list, color='blue')
    plt.xlabel('面積')
    plt.ylabel('円形度')
    plt.title('面積 vs 円形度 相関グラフ')
    plt.show()
    

if __name__=="__main__":
    path = "sample1.png"
    #path = "covid19-1.jpg"
    detect_ellipses(path)
