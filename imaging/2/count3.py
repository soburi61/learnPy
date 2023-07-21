# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 13:37:54 2023

"""

import matplotlib.pyplot as plt

from skimage import data, color, img_as_ubyte
from skimage.feature import canny
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
from skimage.color import rgb2gray,rgba2rgb
image_rgb = plt.imread('sample1.png')
image_gray = rgb2gray(rgba2rgb(image_rgb))
edges = canny(image_gray,sigma=1.0,low_threshold=0.1, high_threshold=0.8)

fig, ax = plt.subplots(dpi=140)
ax.imshow(edges, cmap=plt.cm.gray)
plt.savefig('fabric_mark_ellipse_edge.jpg',dpi=130)
result = hough_ellipse(edges, accuracy=4, threshold=1,
                       min_size=8, max_size=30)
result.sort(order='accumulator')


best = list(result[-1])
yc, xc, a, b = [int(round(x)) for x in best[1:5]]
orientation = best[5]


# Draw the ellipse on the original image
cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
# Draw the edge (white) and the resulting ellipse (red)
edges = color.gray2rgb(img_as_ubyte(edges))
edges[cy, cx] = (250, 0, 0)

fig2, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(8, 4),
                                sharex=True, sharey=True,dpi=150)

ax1.set_title('Original picture')
ax1.imshow(image_rgb)

ax2.set_title('Edge (white) and result (red)')
ax2.imshow(edges)
plt.savefig("daen_hough.jpg",dpi=100)
plt.show()
