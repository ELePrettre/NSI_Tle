# -*- coding: cp1252 -*-
################################################################################
#                                                                              #
#                                 Hanoi                                        #
#                                                                              #
#                         Jeu reprenant le principe                            #
#                            des tours de Hanoi                                #
#                         avec solution automatique                            #
#                                                                              #
#                           language : Python 2.6                              #
#                         auteur : Guillaume Michon                            #
#                            date : 10/10/2012                                 #
#                                                                              #
################################################################################
from tkinter import *
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk # pensez à installer PILLOW

       
class Disque():
    """Définition d'un Objet représentant un disque."""
    def __init__(self,image,canvas):
        self.imageSprite = image
        self.imageID = None
        self.canvas = canvas
        self.coordX = 0
        self.coordY = 0
        self.largeur = image.width()
        self.hauteur = image.height()
        #----------------------------
        self.coordArretMonter = 50
        self.coordArretDescente = 0
        self.coordArretHorizontale = 0
        self.sensMouvementHorizontale = 0
        #-----------------------------

    def Place(self):
        """Dessine le sprite du disque à ses coordonnées par ancrage nord."""
        self.imageID = self.canvas.create_image(self.coordX,self.coordY,anchor=N,image=self.imageSprite)

    def DessineSprite(self):
        """Redessine le sprite du disque à ses nouvelles coordonnées."""
        self.canvas.coords(self.imageID,self.coordX,self.coordY)

#-------------------------------------------------------------------------------
def Initialisation(x=1):
    """Initialisation des variables et mise en forme graphique."""
    global tabTours,selection1,selection2,pause,coupsEffectues,nbrCoups

    # selection1 et selection2 contiendront les 2 tours sélectionnée à la souris
    selection1, selection2 = None, None
    pause = True
    
    etatBoutSol.set(0)
    boutSolution.config(state=ACTIVE)
    
    airDessin.delete(ALL)
    airDessin.create_image(264,204,image=imageFond)
    airDessin.create_image(40,100,image=imageTour,anchor=NW)
    airDessin.create_image(200,100,image=imageTour,anchor=NW)    
    airDessin.create_image(360,100,image=imageTour,anchor=NW)
    mess = "Nombre minimum de mouvements  : "+str((2**nbrDisques.get())-1)
    coups_mini = airDessin.create_text(250,340,text=mess,font="Arial 13 bold ",fill='light blue')

    nbrCoups = 0
    coupsEffectues = airDessin.create_text(250,360,text="Nombre de déplacements effectués : "
                                      +str(nbrCoups),font="Arial 13 bold ",fill='light green')

    #Les 3 tours sont représentée par leur axe en x et un tableau pour les disques qu'elles contiennent
    tabTours = [[100,[]],[260,[]],[420,[]]]
    
    CreationDisques()
    airDessin.bind('<Button-1>',ClickSouris)

#-------------------------------------------------------------------------------    
def CreationDisques():
    """Création des Objets disques en fonction du nombre choisi.
    Par Défaut ils sont mis dans la 1ère tour."""
    
    for n in range(nbrDisques.get(),0,-1):
        disque = Disque(tabDisques[n-1],airDessin)
        disque.coordX = 100
        disque.coordY = 280-((nbrDisques.get()-n)*20)
        disque.Place()
        tabTours[0][1].append(disque)

#-------------------------------------------------------------------------------
def ClickSouris(event):
    """Gestion des 2 sélections à la souris.
    Selection 1 = tour de départ qui contient le disque que l'on veut déplacer
    Selection 2 = tour de déstination de ce disque."""
    global selection1,selection2,disqueEnMouvement

    # clique sur la 1ère tour ?
    if event.x >= 40 and event.x <= 160 and event.y >= 100 and event.y <= 310:
        tourSelectionnee = tabTours[0]

    # 2ème ?
    elif event.x >= 200 and event.x <= 320 and event.y >= 100 and event.y <= 310:
        tourSelectionnee = tabTours[1]

    # 3ème ?
    elif event.x >= 360 and event.x <= 480 and event.y >= 100 and event.y <= 310:
        tourSelectionnee = tabTours[2]
  
    # Aucune donc on sort
    else:
        return

    #-- Si on ne connait pas la tour de départ
    if selection1 == None:
        #- Si la tour sélectionnée n'est pas vide
        if tourSelectionnee[1] != []:
            # cette tour devient la tour de départ
            selection1 = tourSelectionnee
            # son dernier disque devient le disque à mettre en mouvement
            disqueEnMouvement = selection1[1][-1]
            # on le lève un petit peu
            disqueEnMouvement.coordY -= 20
            disqueEnMouvement.DessineSprite()
    #-- Si on connait la tour de départ
    else:
        # cette tour devient la tour de déstination
        selection2 = tourSelectionnee
        #- Si c'est la même que la tour de départ
        if selection2 == selection1:
            # on redescend le disque en mouvement
            disqueEnMouvement.coordY += 20
            disqueEnMouvement.DessineSprite()
            # on réinitialise les sélections et on sort
            selection1, selection2 = None, None
            return
        #- Sinon on détermine les coordonnées de déplacement du disque et on le met en mouvement
        else:
            coordsDeplacementDisque(selection1,selection2)

#-------------------------------------------------------------------------------
def coordsDeplacementDisque(tourDepart,tourArrivee):
    """Détermination des coordonnées d'arret en translation horizontale et verticale descendante du
    du disque en mouvement en fonction des 2 tours concernées."""
    global selection2,pause

    #-- Si la tour de destination n'est pas vide
    if tourArrivee[1] != []:
        disqueDestination = tourArrivee[1][-1]
        #- Si la largeur de son dernier disque est supérieur à celle du disque en mouvement
        if disqueDestination.largeur > disqueEnMouvement.largeur:
            # la coord d'arret en descente de ce dernier est égale à celle du disque de destination moins sa hauteur
            disqueEnMouvement.coordArretDescente = disqueDestination.coordY - 20
        #- Sinon la 2ème sélection n'est pas valide
        else:
            selection2 = None
            return
    #-- Sinon on pose le disque en  mouvement sur la tour vide
    else:
        disqueEnMouvement.coordArretDescente = 280

    # la différence des axes des tours donne le sens de déplacement
    if tourArrivee[0] - tourDepart[0] > 0:
        disqueEnMouvement.sensMouvementHorizontale = 1
    else:
        disqueEnMouvement.sensMouvementHorizontale = -1

    # le disque s'arretera quand son centre sera sur l'axe de la tour de destination
    disqueEnMouvement.coordArretHorizontale = tourArrivee[0]

    # on met ajour les tableau des tours
    tourArrivee[1].append(disqueEnMouvement)
    tourDepart[1].remove(disqueEnMouvement)

    # On met le disque en mouvement
    airDessin.unbind('<Button-1>')
    pause = False
    Mouvement()    

#-------------------------------------------------------------------------------    
def Mouvement():
    """Mise en mouvement du dernier disque de la 1ère tour selectionnée."""
    global nbrCoups,selection1,selection2

    # Tant qu'il n'est ni en haut ni au dessus de la tour de destination, on le monte
    if (disqueEnMouvement.coordY != disqueEnMouvement.coordArretMonter) and (disqueEnMouvement.coordX != disqueEnMouvement.coordArretHorizontale):
        disqueEnMouvement.coordY -= 10
    # Quand il est en haut
    else:
        # Tant qu'il n'est pas au dessus de sa tour de destination, on le déplace
        if disqueEnMouvement.coordX != disqueEnMouvement.coordArretHorizontale:
            disqueEnMouvement.coordX += disqueEnMouvement.sensMouvementHorizontale * 10
        # Quand il est au dessus de la tour 
        else:
            # Tant qu'il n'est pas en bas, on le descend
            if disqueEnMouvement.coordY != disqueEnMouvement.coordArretDescente:
                disqueEnMouvement.coordY += 10
            # Le disque est placé
            else:
                nbrCoups += 1
                airDessin.itemconfigure(coupsEffectues,text="Nombre de déplacements effectués : "+str(nbrCoups))
                # Si on est en mode solution, on passe au déplacement suivant
                if etatBoutSol.get() == 1:
                    DeplacementAuto()
                    return
                # Sinon on vérifie si le but est atteind
                Verification()
                selection1, selection2 = None, None                
                airDessin.bind('<Button-1>',ClickSouris)
                return
    disqueEnMouvement.DessineSprite()
    if not pause:
        fen.after(25,Mouvement)

#-------------------------------------------------------------------------------
def Verification():
    """Vérifie si le but du jeu est atteind."""

    # Si le nombre de disques dans la dernière tour est égal au nombre de disque au départ, la partie est gagné
    if len(tabTours[2][1]) == nbrDisques.get():
        # A-t-on fait plus de coups que le nombre minimum nécessaire
        if nbrCoups > (2**nbrDisques.get())-1:
            diff = nbrCoups - ((2**nbrDisques.get())-1)
            message ="   Bien mais il y a %s coups de trop\n\nVoulez-vous rejouer ?\n"%(str(diff))
        # si le minimum de déplacement est respecté
        else:
            message ="   Trouvé !\n en %s coups minimum   \n\n   Voulez-vous rejouer ?   \n"%(str(nbrCoups))

        boite1 = showinfo(fen,title='Question ?',icone="icone_hanoi.ico",pos='+280+180',
                                mess=message,buttons=['Oui','Non'],bg_f='orange',
                                bg_l='gold',bg_b='maroon',fg_b='ivory',quit_opt=0)
        if(boite1.go()):
            Initialisation()
        else:
            Quitter()

#-------------------------------------------------------------------------------
def Solution():
    """Départ de l'algorithme de solution automatique."""
    global tabCouplesTours

    # On remet tout a l'initiale
    Initialisation()
    etatBoutSol.set(1)
    boutSolution.config(state=DISABLED)
    # tableau contenant les couples [tourDepart,tourArrivee], ce sont des indexs
    tabCouplesTours = []

    Recursivite(nbrDisques.get(),0,1,2) # 0,1,2 -> les indexs des tours dans tabTours
    fen.after(500,DeplacementAuto)
    
#-------------------------------------------------------------------------------
def Recursivite(nombreDisques,tourDepart,tourTransition,tourArrivee):
    """Fonction à double récursivité permettant de remplir le tableau de couples [tourDepart,tourArrivee]."""
    if nombreDisques>0:
        Recursivite(nombreDisques-1,tourDepart,tourArrivee,tourTransition)
        tabCouplesTours.append((tourDepart,tourArrivee))
        Recursivite(nombreDisques-1,tourTransition,tourDepart,tourArrivee)
        
#-------------------------------------------------------------------------------
def DeplacementAuto():
    """Fontion qui sélectionne le disque à mettre en mouvement de la tour de départ du couple [tourDepart,tourArrivee]
     vers la tour de destination."""
    global disqueEnMouvement

    if nbrCoups < len(tabCouplesTours):
        # Comme on a reinitialisé, la variable nbrCoups vaut zéro
        # elle est incrémentée lorsque le disque courant à atteind son but
        couple = tabCouplesTours[nbrCoups] #couple = [tourDepart,tourArrivee]

        # couple[0] -> tourDepart(son index dans tabTours)
        # tabTours[couple[0]][1] -> pour accéder au tableau des disques de cette tour
        # tabTours[couple[0]][1][-1] -> pour accéder au dernier disque de cette tour
        disqueEnMouvement = tabTours[couple[0]][1][-1]

        # on détermine les coordonnées de déplacement du disque et on le met en mouvement
        coordsDeplacementDisque(tabTours[couple[0]],tabTours[couple[1]])
    else:
        etatBoutSol.set(0)

#-------------------------------------------------------------------------------        
def Regle():
    """Affichage des règles du jeu et mise en pause."""
    global pause

    pause = True
    message = "Règles du jeux :\n\nLe but est de déplacer tous les disques de la tour gauche vers la tour droite\n\
et ce sans violer les règles suivantes :\n\n\
1/ On ne peut déplacer qu'un disque à la fois\n\
2/ Un disque ne peut se poser sur un disque plus petit que lui\n"

    boite = showinfo(fen,title='Tours de Hanoï',icone="icone_hanoi.ico",pos='+280+180',
                           mess=message,buttons=['ok'],bg_f='orange',bg_l='gold',
                           bg_b='maroon',fg_b='ivory',justify=LEFT)
    if(boite.go()):
        pause = False
        if selection2 or etatBoutSol.get() :
            Mouvement()

#-------------------------------------------------------------------------------
def Quitter():
    """Quitte le jeu"""
    fen.quit()    
    fen.destroy()

#-------------------------------------------------------------------------------    
fen = Tk()
fen.title("Hanoi")
fen.iconbitmap("icone_hanoi.ico")
fen.resizable(0,0)

#------------------------------ L'interface --------------------------------------
#--- le cadre principal 
interface = Frame(fen,relief="ridge", borderwidth=3,bg='light green')
interface.pack()

#--- les sous-cadres
cadreNbrDisc  = Frame(interface,bg='light blue',relief="ridge", borderwidth=3)
cadreNbrDisc.grid(row=1,column=1)
cadreBouttons = Frame(interface,bg='light green',relief="ridge", borderwidth=3)
cadreBouttons.grid(row=1,column=2,rowspan=2)

#--- la règle nombre de disques
Label(cadreNbrDisc,text="Nombre de disques :",bg='light blue',
      font="Arial 11 bold").grid(row=1,column=1)
nbrDisques = IntVar()
disques = Scale(cadreNbrDisc,from_=1,to=8,length=420,orient=HORIZONTAL,
                tickinterval=1,variable=nbrDisques,command=Initialisation,
                bg='light blue',activebackground='blue',troughcolor='ivory')
disques.grid(row=2,column=1)

#--- les 4 boutons de droite 
Button(cadreBouttons,text="Initialiser",
       command=Initialisation,font="Arial 11 bold",bg='blue',fg='ivory',
       activebackground='ivory',activeforeground='blue').grid(row=1,column=1,padx=2,pady=2, sticky="nsew")

etatBoutSol = IntVar()
boutSolution = Checkbutton(cadreBouttons,text='Solution',bg='red',fg='ivory',
                           activebackground='ivory',activeforeground='red',
                           selectcolor='red',variable=etatBoutSol,command=Solution,
                           indicatoron=0,font='Arial 11 bold')
boutSolution.grid(row=2,column=1,padx=2,pady=2,sticky="nsew")

Button(cadreBouttons,text="Quitter",bg='black',fg='ivory',activebackground='ivory',
       activeforeground='black',command=Quitter,font="Arial 11 bold").grid(row=3,column=1,padx=2,pady=2,sticky="nsew")

Button(cadreBouttons,text="Règles",bg='dark violet',fg='ivory',activebackground='ivory',
       activeforeground='dark violet',command=Regle,font="Arial 11 bold").grid(row=4,column=1,padx=2,pady=2,sticky="nsew")

#-------------------------------------------------------------------------------
airDessin = Canvas(fen,width=520,height=400,bg='ivory',relief="raised", borderwidth=3)
airDessin.pack()

imageFondHanoi = Image.open("fond2.jpg")
imageFond = ImageTk.PhotoImage(imageFondHanoi)

imageTour = PhotoImage(file="tour.gif")
imageDisque8 = PhotoImage(file="disque8.gif")
imageDisque7 = PhotoImage(file="disque7.gif")
imageDisque6 = PhotoImage(file="disque6.gif")
imageDisque5 = PhotoImage(file="disque5.gif")
imageDisque4 = PhotoImage(file="disque4.gif")
imageDisque3 = PhotoImage(file="disque3.gif")
imageDisque2 = PhotoImage(file="disque2.gif")
imageDisque1 = PhotoImage(file="disque1.gif")
tabDisques = [imageDisque1,imageDisque2,imageDisque3,imageDisque4,imageDisque5,imageDisque6,imageDisque7,imageDisque8]

Initialisation()

fen.mainloop()
