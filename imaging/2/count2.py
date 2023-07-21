# 必要なライブラリをインポート
import cv2
import numpy as np
from skimage.transform import hough_ellipse

# 画像の読み込み
frame = cv2.imread('sample1.png')

# グレースケールに変換
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# エッジ検出 (Canny)
canny_gray = cv2.Canny(gray, 100, 200)

# hough_ellipse()関数に渡すために2次元配列に変換
cimg = np.array(canny_gray)

# skimage.transform.hough_ellipse()を使用して楕円の検出を実行
# 具体的なパラメータは、状況に応じて調整する必要があります
result = hough_ellipse(cimg, accuracy=4,threshold=10, min_size=8, max_size=19)

# 検出された楕円のパラメータ（x, y, 半径x, 半径y）を抽出
circles = []
for ellipse in result:
    y, x, radius_y, radius_x = ellipse[1], ellipse[2], ellipse[3], ellipse[4]
    circles.append([x, y, radius_x, radius_y])

# 検出された楕円を元の画像に描画
for i in circles:
    cv2.ellipse(frame, (i[0], i[1]), (i[2], i[3]), 0, 0, 360, (0, 255, 0), 2)

# 検出された楕円の数を数える
j = len(circles)

# 画像上に検出された楕円の数を表示
fontType = cv2.FONT_HERSHEY_COMPLEX
cv2.putText(frame, 'Total: ' + str(j), (30, 30), fontType, 1, (0, 0, 0), 1, cv2.LINE_AA)

# 検出結果を表示
cv2.imshow('', frame)

# 結果を保存
cv2.imwrite('hough_ellipse.png', frame)

# キー入力を待ち、全てのウィンドウを閉じる
cv2.waitKey(0)
cv2.destroyAllWindows()
print(j)