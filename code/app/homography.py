import numpy as np
import cv2
from scipy.spatial import distance

def trie(x):
    a = sorted(x,key =  lambda x : np.linalg.norm(x))
    if(a[1][0] > a[2][0]):
        save_1, save_2 = a[1], a[2]
        a[1], a[2] = save_2, save_1
    return np.array([a[0],a[1], a[2], a[3]])


def locate_tray(img, point_corner):
    point_corner = trie(point_corner)
    height = int(distance.euclidean(point_corner[0], point_corner[1]))
    weight = int(distance.euclidean(point_corner[0], point_corner[2]))
    if (height < weight):
        point_arriver = np.array([[0,0], [0, height], [weight, 0], [weight, height]])
    else:
        point_arriver = np.array([[0, weight], [height, weight], [0, 0], [height, 0]])
    h, status = cv2.findHomography(point_corner, point_arriver)
    im_dst = cv2.warpPerspective(img, h, (img.shape[1], img.shape[0]))
    return im_dst[0: min(weight, height), 0: max(weight,height)]



def homog(liste_corners, img):
    point = np.array(liste_corners)
    img1 = cv2.imread(img, 3)
    img1 = locate_tray(img1, point)
    cv2.imwrite("results/" + img.split('.')[-2].split("/")[-1]  +".jpg", img1)
