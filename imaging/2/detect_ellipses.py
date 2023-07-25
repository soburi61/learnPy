# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 14:13:02 2023

"""

import cv2
import numpy as np
from IPython.display import Image, display
from PIL import ImageOps
import numpy as np
from matplotlib import pyplot as plt
import csv


def imshow(img):#表示
    ret, encoded = cv2.imencode(".png", img)
    display(Image(encoded))


def remove_outliers(data, data2, threshold=1.5):#dataを基準に外れ値を除外する
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
    ret, bin_img = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # モルフォロジー演算によるノイズ除去
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, iterations=2)
    #imshow(bin_img)
    
    # sure backgroundのマーカーを作成
    sure_bg = cv2.dilate(bin_img, kernel, iterations=3)
    #imshow(sure_bg)

    # 距離変換を行い sure foregroundのマーカーを作成
    dist = cv2.distanceTransform(bin_img, cv2.DIST_L2, 5)
    #imshow(dist)

    ret, sure_fg = cv2.threshold(
        dist, 0.3 * dist.max(), 255, cv2.THRESH_BINARY)
    sure_fg = sure_fg.astype(np.uint8)  # float32 -> uint8
    #imshow(sure_fg)
    
    # 不明な領域を作成
    unknown = cv2.subtract(sure_bg, sure_fg)
    #imshow(unknown)

    # マーカーの作成
    ret, markers = cv2.connectedComponents(sure_fg)
    
    markers += 1
    markers[unknown == 255] = 0
    
    # fig, ax = plt.subplots(figsize=(6, 6))
    # ax.imshow(markers, cmap="tab20b")
    # plt.show()

    # Watershedを適用
    markers = cv2.watershed(img, markers)
    
    # fig, ax = plt.subplots(figsize=(6, 6))
    # ax.imshow(markers, cmap="tab20b")
    # plt.show()
    labels = np.unique(markers)
    
    ellipses = []
    for label in labels[2:]:
        target = np.where(markers == label, 255, 0).astype(np.uint8)
        contours, hierarchy = cv2.findContours(
            target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ellipses.append(contours[0])
    
    # 検出した楕円を画像に描画
    # img_mark=img.copy()
    # cv2.drawContours(img_mark, ellipses, -1, color=(0, 0, 255), thickness=2)
    # imshow(img_mark)
    
    ellipses_to_draw=[] #条件にあった円
    detail_list=[] #すべての円の詳細
    # 各コインの特徴量を計算
    for i, ellipse_contour in enumerate(ellipses):
        area = cv2.contourArea(ellipse_contour)  # 面積を計算
        perimeter = cv2.arcLength(ellipse_contour, True)  # 周囲長を計算
        circularity = (4 * np.pi * area) / (perimeter ** 2)  # 円形度を計算
        x, y, w, h = cv2.boundingRect(ellipse_contour)  # 外接矩形を計算
        aspect_ratio = w / h  # 縦横比を計算
        area_ratio = area/(w*h) #外接短形の面積と抽出物体の面積比
        # 特徴量を表示
        # print(f"Object No.{i+1}:")
        # print(f"  面積: {area}")
        # print(f"  周囲長: {perimeter}")
        # print(f"  円形度: {circularity}")
        # print(f"  縦横比: {aspect_ratio}")
        # print(f"  面積比: {area_ratio}")
        if 100 <= area <= 200 and perimeter >= 50 and circularity <= 0.86:
            ellipses_to_draw.append(ellipse_contour)
            #print("  条件に合致")
        detail_list.append(
            [i + 1, area, perimeter, circularity, aspect_ratio, area_ratio])
        
    print(f"オブジェクトの数:{i+1}個")
    print("----------")
    print("面積:100~200px,周囲長:50以上,真円度:0.86以下のオブジェクトをマーク")
    # 条件を満たす楕円を元の画像に描画
    img_with_ellipses = img.copy()
    cv2.drawContours(
        img_with_ellipses, ellipses_to_draw, -1, 
        color=(0, 0, 255), thickness=2)
    imshow(img_with_ellipses)
            
    # 特徴量をCSVファイルに保存
    csv_file_name = "ellipse_detail.csv"
    
    with open(csv_file_name, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ["Object No.", "面積", "周囲長", "円形度", "縦横比", "面積比"])
        writer.writerows(detail_list)
    
    area_list,perimeter_list=remove_outliers(
        [r[1] for r in detail_list],[r[2] for r in detail_list])
    _,circularity_list=remove_outliers(
        [r[1] for r in detail_list],[r[3] for r in detail_list])
    
    plt.scatter(area_list, perimeter_list, color='blue')
    plt.xlabel('面積')
    plt.ylabel('周囲長')
    plt.title('面積 vs 周囲長 散布図')
    plt.show()
    
    # グラフを表示
    plt.scatter(area_list,circularity_list, color='blue')
    plt.xlabel('面積')
    plt.ylabel('円形度')
    plt.title('面積 vs 円形度 相関グラフ')
    plt.show()
    
    
if __name__=="__main__":
    path = "sample1.png"
    #path = "covid19-1.jpg"
    detect_ellipses(path)
