#opencvをインポートします。
import cv2 
import numpy as np
#フォントの指定
fontType = cv2.FONT_HERSHEY_COMPLEX
#検出する画像の読み込み
frame = cv2.imread('sample1.png')
#1チャンネル（白黒画像に変換）
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#Cannyにてエッジ検出処理（やらなくてもよい）
canny_gray = cv2.Canny(gray,100,200)    
#結果の書き込み
cv2.imwrite('totyu.png',canny_gray)   
#houghで使う画像の指定、後で変えたりする際に変数してしておくと楽。
cimg = canny_gray

j = 1
#hough関数
circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,
                           1,10,param1=120,param2=10,
                           minRadius=8,maxRadius=19)
    # param1 ; canny()エッジ検出機に渡される２つの閾値のうち、大きいほうの閾値0
    # param2 ; 円の中心を検出する際の投票数の閾値、小さくなるほど、より誤検出が起こる可能性がある。
    # minRadius ; 検出する円の最小値
    # maxRadius ; 検出する円の最大値

#検出された際に動くようにする。
if circles is not None and len(circles) > 0:
    #型をfloat32からunit16に変更：整数のタイプになるので、後々トラブルが減る。
    circles = np.uint16(np.around(circles))
    
    for i in circles[0,:]:
        # 外側の円を描く
        cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
        # 中心の円を描く
        cv2.circle(frame,(i[0],i[1]),2,(0,0,255),2)
        # 円の数を数える
        j = j + 1
#円の合計数を表示
cv2.putText(frame,'Total :'+str(j), (30,30), fontType, 1, (0, 0, 0), 1, cv2.LINE_AA)
#結果画像の表示
cv2.imshow('',frame)      
#結果の書き込み
cv2.imwrite('hough_circle.png',frame)   

#キー入力を待つ
cv2.waitKey(0)
#全ての開いたウインドウ閉じる
cv2.destroyAllWindows()