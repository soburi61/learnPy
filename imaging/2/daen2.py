# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 13:58:42 2023

"""

import cv2
import math
import numpy as np

def main():
    img = cv2.imread('sample1.png', cv2.IMREAD_COLOR)

    # グレイスケール化
    gray1 = cv2.bitwise_and(img[:,:,0], img[:,:,1])
    gray1 = cv2.bitwise_and(gray1, img[:,:,2])

    # 二値化
    _, binimg = cv2.threshold(gray1, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    binimg = cv2.bitwise_not(binimg)

    # 結果画像の黒の部分を灰色にする。
    bimg = binimg // 4 + 255 * 3 //4
    resimg = cv2.merge((bimg,bimg,bimg)) 

    # 輪郭取得
    contours,hierarchy =  cv2.findContours(binimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(contours):
        # 楕円フィッティング
        ellipse = cv2.fitEllipse(cnt)
        print(ellipse)

        cx = int(ellipse[0][0])
        cy = int(ellipse[0][1])

        # 楕円描画
        resimg = cv2.ellipse(resimg,ellipse,(255,0,0),2)
        cv2.drawMarker(resimg, (cx,cy), (0,0,255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=1)
        cv2.putText(resimg, str(i+1), (cx+3,cy+3), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,80,255), 1,cv2.LINE_AA)

    cv2.imshow('resimg',resimg)
    cv2.waitKey()

if __name__ == '__main__':
    main()