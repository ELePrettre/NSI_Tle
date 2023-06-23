# -*- coding:Latin-1 -*-
from Tkinter import *


class boite_dialogTk(Toplevel):
    """ Boite de dialogue à choix multiples personnalisable"""
    def __init__(self,root=None,title='',icone=None,pos='',mess='',buttons=[],
                 bg_f='grey',bg_l='grey',fg_l='black',bg_b='grey',fg_b='black',
                 font_l='Century 13 bold',font_b='Arial 13 bold',
                 relief_l='ridge',relief_b='ridge',justify=CENTER,quit_opt = None):

        Toplevel.__init__(self,bg=bg_f)
        self.title(title)        
        self.iconbitmap(icone)
        self.resizable(0,0)
        self.wait_visibility()
        self.grab_set()
        self.transient(self.master)
        self.focus_force()

        self.quit_opt = quit_opt     
        nb_but = len(buttons)
        self.buttons = buttons
        
        Label(self,text=mess,font=font_l,
              bg=bg_l,fg=fg_l,relief=relief_l,borderwidth=5,
              justify=justify).grid(row=1,column=1,columnspan=nb_but)
        
        self.num = 0
        for num in range(len(buttons)):
            texte = buttons[num]
            b = Button(self,text=texte,font=font_b,bg=bg_b,fg=fg_b,
               activebackground=fg_b,activeforeground=bg_b,
                      command =(lambda self=self, num=num: self.done(num)))
            b.config(relief=relief_b, borderwidth=6)
            b.grid(row=2,column=num+1)
             
        self.geometry(pos)
        
        if self.quit_opt != None:
                        
            self.protocol("WM_DELETE_WINDOW",lambda self=self,num=self.quit_opt:self.done(num))
##            print "\nSi appui sur croix :\nIndice dans le tableau : %s\nOption : %s"%(str(self.quit_opt),
##                                                                                  buttons[self.quit_opt])
        else:
            self.protocol("WM_DELETE_WINDOW",lambda:None)
##            print "\nSi appui sur croix : Aucun effet !"
        
            
    def go(self):
        
        self.mainloop()
        self.destroy()
        
        if self.num == 0:           
            return 1
        elif self.num == 1:
            return 0
        else :
            return self.num  # Si la boite a trois boutons par exemple
            

    def done(self,num):
        
##        print "Indice du bouton pressé dans le tableau : %s\nOption : %s"%(str(num),self.buttons[num])
        self.num = num
        self.quit()


if __name__=='__main__':
 
    def aide():
        boite = boite_dialogTk(fen,title='Aide sur le fonctionnement',icone='',pos='+200+40',
                               mess=message_aide,buttons=['Ok'],
                               bg_f='maroon',bg_l='light blue',fg_l='navy',
                               bg_b='light green',fg_b='dark green',justify=LEFT)
        boite.go()
 
    def test1():
        message = "\n  La partie est terminée !  \n\
  Vous avez 15 230 points \n\
  Voulez-vous sauvegarder votre score ? \n\n"
        boite1 = boite_dialogTk(fen,title='Sauvegarde ?...',icone='',pos='+320+160',
                               mess=message,buttons=['Sauvegarder','Quitter'],
                               bg_f='pink',bg_l='gold',fg_l='navy',
                               bg_b='black',fg_b='white',
                               font_l='arial 16',font_b='century 13',
                               relief_l='groove',relief_b='raised')
        var = boite1.go()
        print "valeur renvoyée : ",var
        if var==1:
            message = "\n Score enregistrer. \n Voulez-vous rejouer ?  \n"
            boite2 = boite_dialogTk(fen,title='Rejouer ?...',icone='',pos='+320+160',
                               mess=message,buttons=['Oui','Non'],
                               bg_f='white',bg_l='violet',fg_l='black',
                               bg_b='white',fg_b='black',
                               relief_l='sunken',relief_b='solid',quit_opt=0)
            var = boite2.go()
            print "valeur renvoyée : ",var
            if var == 0:
                fen.destroy()
        
    def test2():
        global top,message_aide
        top = Toplevel(fen)
        top.title("Test 3")
        top.wait_visibility()
        top.grab_set()
        top.transient(fen)
        top.focus_force()
        top.geometry('+200+50')
        t = Text(top,font='Arial 13 bold')
        t.insert(END,message_aide)
        
        scroll = Scrollbar(top,command=t.yview)
        t.configure(yscrollcommand=scroll.set)
        
        t.grid(row=1,column=1)
        scroll.grid(row=1,column=2,sticky=S+N)
        
        top.protocol("WM_DELETE_WINDOW",boite_3bouttons)
        
    def boite_3bouttons():
        global top
        message="\n Vous n'avez pas sauvegardé votre document ! \n"
        boite3 = boite_dialogTk(fen,title='Attention !',icone='',pos='+320+160',
                               mess=message,buttons=['Sauvegarder','Quitter','Annuler'],
                               bg_f='black',bg_l='white',fg_l='black',
                               bg_b='maroon',fg_b='white',
                               relief_l='sunken',relief_b='raised',quit_opt=2)
        var = boite3.go()
        print "valeur renvoyée : ",var
        if var == 1:
            boite_confirm = boite_dialogTk(fen,title='Confirmation',icone='',pos='+320+160',
                               mess='  Sauvegarde effectuée !  ',buttons=['Ok'],
                               bg_f='black',bg_l='white',fg_l='black',
                               bg_b='maroon',fg_b='white',
                               font_b='arial 11 bold', 
                               relief_l='flat',relief_b='raised')
                       
            if var == boite_confirm.go() :
                print "valeur renvoyée : ",var
                top.destroy()
                
        elif var == 0:
            top.destroy()

        elif var == 2:
            top.focus_force()

    
    fen = Tk()
    fen.geometry('+50+50')
    top = None
    message_aide="Boîte de dialogue personnalisée à choix multiples  \n\n\
Liste des arguments :   \n\n\
1/ root      = la fenêtre qui l'invoque\n\
2/ title     = le titre\n\
3/ icone     = l'icône\n\
4/ pos       = position de la fenêtre\n\
5/ mess      = le texte à afficher\n\
6/ buttons[] = tableau de chaînes des choix possibles  \n\
7/ bg_f      = couleur de fond de la fenêtre\n\
8/ bg_l      = couleur de fond du texte\n\
9/ fg_l      = couleur du texte\n\
10/ bg_b     = couleur de fond des boutons\n\
11/ fg_b     = couleur du texte des boutons\n\
12/ font_l   = police du texte\n\
13/ font_b   = police des boutons\n\
14/ relief_l = type de relief du texte\n\
15/ relief_b = type de relief des boutons\n\
16/ justify  = alignement du texte\n\
17/ quit_opt = indice du choix par défaut si fermeture par la 'croix'\n\n\
Après l'instanciation de la boite\n\
faire un appel à la méthode 'go() qui renverra :'\n\
1 pour le premier bouton\n\
0 pour le deuxième(vrai ou faux : choix binaire le plus courant)\n\
l'index du tableau 'buttons[]pour les autres cas'\n\n"
    
    but_aide = Button(fen,text='Aide',command=aide)
    but_aide.grid(row=1,sticky='nsew')
    but_test1 = Button(fen,text='Test 2 boutons',command=test1)
    but_test1.grid(row=2,sticky='nsew')
    but_test2 = Button(fen,text='Test 3 boutons',command=test2)
    but_test2.grid(row=3,sticky='nsew')
    but_quit = Button(fen,text='Quitter',command=fen.destroy)
    but_quit.grid(row=4,sticky='nsew')
    fen.mainloop()
