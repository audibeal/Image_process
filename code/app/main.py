from ExtractionTray import *

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def checkFormatJPG(filePath):
    extension=filePath.split('.')[-1]
    if extension == "jpg" or extension == "JPG":
        return True
    return False


def main():
    print("Hello user.")
    while True:
        # Choice of the image to process
        img = input("Which image ?\n>>")
        if img == "quit":
            print("Closing the app...\nGood bye user.")
            return
        if img == "?":
            print("Liste of the commands :")
            print(">>?  -- Print the app help.")
            print(">>quit -- Close the app.")
            print(">>path2file -- Image processing on the image path2file.")
            continue
        if not checkFileExistance(img):
            print("Error !\nThis file doesn't exist.")
            continue
        # Now we have check that the file exist
        # Now let's check if it is a jpg file.
        if not checkFormatJPG(img):
            print("Erreur !\nIncorrect format. The specified file has to to be extended by .jpg or .JPG")
            continue
        print("Image Processing ...")
        print(">> Tray extraction ...")
        image = cv2.imread(img)
        liste_corners = []
        for i, (x, y) in enumerate(find_angulars(img)):
            print("Point {} : (".format(i), x, ", ", y, ")")
            cv2.circle(image, (x, y), 25, (0, 0, 255), -1)
            liste_corners.append((x, y))

        cv2.namedWindow('Detected Angulars', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Detected Angulars', 600, 400)


        cv2.imshow("Detected Angulars", image)
        cv2.waitKey(1)


        confirm = None
        while  not (confirm == "y" or confirm == "n"):
            confirm = input("Confirm ?  y/n\n")
        cv2.destroyWindow('Detected Angulars')
        if confirm == "n":
            liste_corners = find_angulars_manualy(cv2.imread(img))

        print(liste_corners)





main()
