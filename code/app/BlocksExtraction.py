import cv2
import numpy as np


EPS = 0.01

class Cercle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __eq__(self, other):
        a = (abs(self.x -other.x) <= EPS )
        b = (abs(self.y -other.y) <= EPS )
        c = (abs(self.r -other.r) <= EPS )
        return (a and b and c)

    def distance(self, other):
        return ((self.x-other.x)**2 + (self.y-other.y)**2)**(0.5)

    def cercles_dans(self, liste):
        """
        Retourne True si un cercle de liste a son milieu à l'interieur du cercle self.
        """
        for c in liste:
            d = self.distance(c)
            if d < self.r:
                return True
        return False

    def nombre_cercles_dans(self, liste):
        """
        Retourne le nombre de cercles de liste dont le centre est dans self.
        """
        res = 0
        for c in liste:
            d = self.distance(c)
            if d < self.r:
                res += 1
        return res




class ExtractionBlocs:
    def __init__(self, img):
        self.VERBOSE = False
        self.image = cv2.imread(img)
        self.rayon_minimum = 29
        self.erosion = 1
        self.dilatation = 4
        self.lo = np.array([0, 150, 50])
        self.hi = np.array([179, 200, 300])
        self.noyau_erosion = np.ones((5,5),np.uint8)
        self.noyau_dilatation = np.ones((5,5),np.uint8)
        self.tolerance_rayon = 0
        self.k = 1
        self.seuil_canny_bas = 0
        self.seuil_canny_haut = 50
        self.suppression_cercles = True
        self.dilatation_cercles = 1
        self.dilatation_canny = 1


    def save_img(self, img, titre):
        if self.VERBOSE:
            cv2.imwrite("results/" +titre+".jpg", img)

    def seuillage_init(self, img):
        return cv2.inRange(cv2.cvtColor(img, cv2.COLOR_BGR2HSV), self.lo, self.hi)

    def inv_pixels(self, img):
        """
        Inverse les pixels de img (le noir devient blanc et le blanc devient noir.)
        """
        img_c = img.copy()
        img[img_c == 0] = 255
        img[img_c == 255] = 0

    def erosion_(self, img):
        return cv2.erode(img,self.noyau_erosion,iterations = self.erosion)

    def dilatation_(self, img):
        return cv2.dilate(img,self.noyau_dilatation,iterations = self.dilatation)

    def generer_cercles(self, masque):
        res = []
        for elem in cv2.findContours(masque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]:
            ((x, y), rayon) = cv2.minEnclosingCircle(elem)
            res.append(Cercle(x, y, rayon))
        return res

    def filtrer_petits_rayons(self, liste_cercles):
        i = len(liste_cercles)
        while i != 0:
            elem = liste_cercles[i-1]
            if elem.r < self.rayon_minimum + self.tolerance_rayon:
                liste_cercles.remove(elem)
            i = i - 1

    def filtrer_cercles_imbiques(self, liste_cercles, liste_cercles_init):
        hyper = 95
        nouv = []
        for i in range(len(liste_cercles)):
            b = True
            for j in range(len(liste_cercles)):
                if liste_cercles[i] != liste_cercles[j]:
                    d = liste_cercles[i].distance(liste_cercles[j])
                    if d > max(liste_cercles[i].r, liste_cercles[j].r) :
                        continue
                    else:
                        if liste_cercles[i].r < liste_cercles[j].r:
                            b = self.fonction_alex(liste_cercles[i], liste_cercles, liste_cercles_init) # b = False
                            break
            if b:
                nouv.append(liste_cercles[i])
        return nouv

    def fonction_alex(self, petit_cercle,liste_cercles, liste_cercles_init):
        """
        Retroune True si le petit_cercle est le deuxième plus grand cercle à l'interieur d'un grand cercle de liste_cercles_init
        """
        return False


    def ajouter_cercles_oublies(self, liste_cercles_nouv, liste_cercles_init):
        nouv = liste_cercles_nouv.copy()
        for alex in liste_cercles_init:
            if alex.cercles_dans(liste_cercles_nouv):
                pass
            else:
                nouv.append(alex)
        return nouv

    def nouv_f(self, liste_cercles_final, liste_cercles_init, liste_cercles_interm):
        res = liste_cercles_final.copy()
        hyper = 95
        for c_init in liste_cercles_init:
            if c_init.r >= hyper:
                # 2 cas possibles, 1 cercle dedans ou plus
                if c_init.nombre_cercles_dans(liste_cercles_final) >= 2:
                    pass
                else:
                    # 1 cercle, je dois ajouter le deuxième.
                    n_liste = []
                    for c in liste_cercles_interm:
                        d = c_init.distance(c)
                        if d < c_init.r:
                            n_liste.append(c)
                    if len(n_liste) >=2:
                        n_liste.sort(reverse=True, key=lambda cer: cer.r)
                        res.append(n_liste[1])
        return res

    def nouv_ff(self, liste_c):
        hyper = 50
        eps = 10
        res = []
        d = []
        for i in range(len(liste_c)):
            for j in range(i+1, len(liste_c)):
                c1 = liste_c[i]
                c2 = liste_c[j]
                if c1.distance(c2) < c1.r+c2.r + eps and c1.r < hyper and c2.r < hyper:
                        res.append(Cercle((c1.x+c2.x)/2, (c1.y+c2.y)/2, c1.r+c2.r) )
                        d.append(c1)
                        d.append(c2)
        for c in liste_c:
            test = True
            for g in d:
                if g == c:
                    test = False
            if test:
                res.append(c)
        return res


    def main(self):

        img = self.image
        seuil = self.seuillage_init(img)
        self.save_img(seuil, "Threshold")

        erode = self.erosion_(seuil)
        dilate = self.dilatation_(erode)
        self.save_img(seuil, "Erosion")
        self.save_img(seuil, "Dilatation")

        masque = cv2.bitwise_and(img, img, mask=dilate)
        self.save_img(masque, "Mask")

        liste_cercles_init = self.generer_cercles(dilate)
        self.filtrer_petits_rayons(liste_cercles_init)

        prem_res = img.copy()
        for c in liste_cercles_init:
            cv2.circle(prem_res, (int(c.x), int(c.y)), int(c.r), (0, 255, 255), 2)
        self.save_img(prem_res, "ResInit")

        masque_gris = gray_=cv2.cvtColor(masque, cv2.COLOR_BGR2GRAY)
        self.save_img(masque_gris, "GrayMask")

        if self.k != 1:
            masque_gris=cv2.blur(masque_gris, (self.k, self.k))
            self.save_img(masque_gris, "BlurGrayMask")

        img_canny = cv2.Canny(masque_gris, self.seuil_canny_bas, self.seuil_canny_haut)
        self.save_img(img_canny, "Canny")

        if self.suppression_cercles:
            cimg = cv2.cvtColor(img_canny,cv2.COLOR_GRAY2BGR)
            img_canny_sans_cercles = np.zeros_like(img_canny)
            cercles_a_supprimer = cv2.HoughCircles(img_canny,cv2.HOUGH_GRADIENT,1,11, param1=5,param2=12,minRadius=0,maxRadius=8)
            if cercles_a_supprimer is not None:
                circles = np.uint16(np.around(cercles_a_supprimer))
                for i in circles[0,:]:
                    # draw the outer circle
                    cv2.circle(img_canny_sans_cercles,(i[0],i[1]),i[2], 255)
                    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                img_canny_sans_cercles = cv2.dilate(img_canny_sans_cercles,np.ones((5,5),np.uint8),iterations = self.dilatation_cercles)
            self.inv_pixels(img_canny_sans_cercles)
            img_canny = cv2.bitwise_and(img_canny, img_canny, mask=img_canny_sans_cercles)
            if self.VERBOSE:
                self.save_img(img_canny, "CannyWhithoutCercle")
            if self.VERBOSE:
                self.save_img(cimg, "DetectedCircles")

            img_canny_dilatee = cv2.dilate(img_canny,np.ones((5,5),np.uint8),iterations = self.dilatation_canny)
            self.inv_pixels(img_canny_dilatee)
            self.save_img(img_canny_dilatee, "DilatedCannyFilter")

        nouv_filtre = cv2.bitwise_and(masque, masque, mask=img_canny_dilatee)
        self.save_img(nouv_filtre, "NewMask")

        gris = cv2.cvtColor(nouv_filtre,cv2.COLOR_BGR2GRAY)
        seuillage_ = cv2.threshold(gris,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
        self.inv_pixels(seuillage_)

        self.save_img(seuillage_, "NewThreshold")


        if self.suppression_cercles:
            img_canny_sans_cercles_ = np.zeros_like(seuillage_)
            if cercles_a_supprimer is not None:
                circles = np.uint16(np.around(cercles_a_supprimer))
                for i in circles[0,:]:
                    # draw the outer circle
                    cv2.circle(img_canny_sans_cercles_,(i[0],i[1]),i[2], 255, -1)
                img_canny_sans_cercles_ = cv2.dilate(img_canny_sans_cercles_,np.ones((5,5),np.uint8),iterations = self.dilatation_cercles)
            seuillage_ = cv2.addWeighted(seuillage_,1,img_canny_sans_cercles_,1,0)
            if self.VERBOSE:
                self.save_img(seuillage_, "NouveauSeuillageSansCercles")


        param1 = 1
        seuillage_ = cv2.erode(seuillage_,np.ones((5,5),np.uint8),iterations = param1)
        if param1 > 0:
            self.save_img(seuillage_,"NouveauSeuillageErod")



        liste_cercles_nouv = self.generer_cercles(seuillage_)
        cliste_cercles_nouv = liste_cercles_nouv.copy()

        # filtrage des petites cercles
        self.filtrer_petits_rayons(liste_cercles_nouv)
        # filtrage des cercles imbriqués
        liste_cercles_nouv = self.filtrer_cercles_imbiques(liste_cercles_nouv, liste_cercles_init)
        # cercles oubliés
        liste_cercles_nouv = self.ajouter_cercles_oublies(liste_cercles_nouv, liste_cercles_init)
        # nouv
        liste_cercles_nouv = self.nouv_f(liste_cercles_nouv, liste_cercles_init, cliste_cercles_nouv)
        liste_cercles_nouv = self.nouv_ff(liste_cercles_nouv)

        res = img.copy()
        for c in liste_cercles_nouv:
            cv2.circle(res, (int(c.x), int(c.y)), int(c.r), (0, 255, 255), 2)
        cv2.imwrite("results/FinalResult.jpg", res)


def extract(img):
    extraction = ExtractionBlocs(img)
    extraction.main()
