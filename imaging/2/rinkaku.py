# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 14:13:02 2023

"""

import cv2
import numpy as np
from IPython.display import Image, display
from matplotlib import pyplot as plt


def imshow(img):
    """ndarray 配列をインラインで Notebook 上に表示する。
    """
    ret, encoded = cv2.imencode(".png", img)
    display(Image(encoded))


# 画像を読み込む。
img = cv2.imread("sample1.png")

# グレースケール形式に変換する。
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 大津の手法で2値化する。
ret, bin_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# ノイズを削除する。
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel, iterations=2)
imshow(bin_img)

# sure background 領域を抽出する。
sure_bg = cv2.dilate(bin_img, kernel, iterations=3)
imshow(sure_bg)
# 距離マップを作成する。
dist = cv2.distanceTransform(bin_img, cv2.DIST_L2, 5)
imshow(dist)

# sure foreground 領域を抽出する。
ret, sure_fg = cv2.threshold(dist, 0.3 * dist.max(), 255, cv2.THRESH_BINARY)
sure_fg = sure_fg.astype(np.uint8)  # float32 -> uint8
imshow(sure_fg)

# 前景か背景か判断できない領域を抽出する。
unknown = cv2.subtract(sure_bg, sure_fg)
imshow(unknown)
# sure foreground にたいして、ラベル付を行う。
ret, markers = cv2.connectedComponents(sure_fg)

# 前景か背景か判断できない領域はラベル0
markers += 1
markers[unknown == 255] = 0

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(markers, cmap="tab20b")
plt.show()
# watershed アルゴリズムを適用する。
markers = cv2.watershed(img, markers)

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(markers, cmap="tab20b")
plt.show()
labels = np.unique(markers)

coins = []
for label in labels[2:]:  # 0:背景ラベル １：境界ラベル は無視する。

    # ラベル label の領域のみ前景、それ以外は背景となる2値画像を作成する。
    target = np.where(markers == label, 255, 0).astype(np.uint8)

    # 作成した2値画像に対して、輪郭抽出を行う。
    contours, hierarchy = cv2.findContours(
        target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    coins.append(contours[0])

# 輪郭を描画する。
cv2.drawContours(img, coins, -1, color=(0, 0, 255), thickness=2)
imshow(img)

# 各コインの特徴量を計算
# for i, coin_contour in enumerate(coins):
#     # 面積を計算
#     area = cv2.contourArea(coin_contour)

#     # 周囲長を計算
#     perimeter = cv2.arcLength(coin_contour, True)

#     # 円形度（面積に対する円の面積比）を計算
#     circularity = (4 * np.pi * area) / (perimeter ** 2)

#     # 外接矩形を計算
#     x, y, w, h = cv2.boundingRect(coin_contour)

#     # 縦横比を計算
#     aspect_ratio = w / h

#     # 特徴量を表示
#     print(f"Coin {i+1}:")
#     print(f"  面積: {area}")
#     print(f"  周囲長: {perimeter}")
#     print(f"  円形度: {circularity}")
#     print(f"  縦横比: {aspect_ratio}")
    