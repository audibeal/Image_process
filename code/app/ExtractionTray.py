import cv2

liste_corners = []
img = None

def find_angulars(img):
    return [(906, 2400), (3199, 2272), (3109, 315), (726, 472)]


def click_event(event, x, y, flags, params):

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        #print(x, ' ', y)
        liste_corners.append((x, y))
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.circle(img, (x, y), 25, (0, 0, 255), -1)
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('Corner finding', img)

    # checking for right mouse clicks
    if event==cv2.EVENT_RBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.circle(img, (x, y), 25, (0, 0, 255), -1)
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('Corner finding', img)


def find_angulars_manualy(image):
    """
    To do
    """
    global img
    img = image
    global liste_corners
    liste_corners = []
    # reading the image

    # displaying the image
    cv2.namedWindow('Corner finding',cv2.WINDOW_NORMAL)
    cv2.imshow('Corner finding', img)

    # setting mouse hadler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('Corner finding', click_event)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    # close the window
    cv2.destroyAllWindows()
    return liste_corners[:4]
