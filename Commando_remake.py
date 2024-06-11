"""
Créateur : Charles Mailley
Jeu : Commando
Reprise d'un jeu déjà existant (miniclip)
"""
import tkinter
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import time

#import sys
# sys.setrecursionlimit(sys.getrecursionlimit() * 5)
import function as function # pip install function
import pygame  # pip install pygame
import keyboard  # pip install keyboard
import random
from PIL import ImageTk, Image, ImageOps  # pip install pillow
import math
from math import *
import os.path

# import threading


# A la fin mettre tout dans un try
# Dans le except, on reportera l'erreur
print('La modification, suppression ou déplacement des images peut générer une erreur. NE PAS LES DEPLACER !')
print('La modification, suppression ou déplacement des sons peut générer une erreur. NE PAS LES DEPLACER !')
print('La modification du fichier config.txt peut générer une erreur. En cas de doute, suprimez le.')


# Definition de toutes les images du jeu ainsi que les parametres des objets de classe
class ImageGame:  # Camp de gauche
    def __init__(self, menu: Menu, m) -> None: #m: MusiqueGame

        def createImgGrise(img) -> Image:
            # Convertie en RGB + transparent
            rgba = img.convert('RGBA')
            # Recupere tous les couleurs de pixel de l'image
            datas = rgba.getdata()
            # Liste des nouvellez couleurs de l'image
            newData = []
            # Pour chaque pixel
            for item in datas:
                # Calcule de la nuance de gris
                L = round(item[0] * 299 / 1000 + item[1] * 587 / 1000 + item[2] * 114 / 1000)
                # Enregistrement de la nouvelle valeur
                item = (L, L, L, 255)
                # Si la valeur est le noir (0, 0, 0)
                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    # On applique le fond transparent
                    newData.append((255, 255, 255, 0))
                else:
                    # Sinon on applique la nuance de gris trouvé
                    newData.append(item)
            # Application des nouvelles couleur sur l'image
            rgba.putdata(newData)
            # Ajout de la nouvell image dans le dico
            return rgba

        def firstLettreMaj(mot: str) -> str:
            return mot[0].upper() + mot[1:]

        # Nom du dossier image
        root = "Image"
        # Dictionnaire contenant toutes les images
        i = {}
        # Dictionnaire contenant les images de couleur grise
        l = {}

        # Pour chaque dossier Image
        for dossier in os.listdir(root):

            # IMAGE/DOSSIER/Dossier_entitee/Dossier_MOV/list(IMG)
            if dossier in ["P-Player", "P-Mob_Ami", "P-Mob_Ennemi", "P-Boss"]:
                listEntitee = {}
                # Pour chaque dossier d'entité
                for dossierEntitee in os.listdir(root + "/" + dossier):
                    listMovement = {}
                    # Pour chaque dossier de mouvement
                    for dossierMovement in os.listdir(root + "/" + dossier + "/" + dossierEntitee):
                        listImages = []
                        nomMovement = dossierMovement.split("-")[-1]
                        imgGris = None
                        # On met toutes les images dans un dico
                        chaminIMG = root + "/" + dossier + "/" + dossierEntitee + "/" + dossierMovement
                        for nomIMG in os.listdir(chaminIMG):
                            # Chargement de l'image et save dans le dico avecc la clé à son nom
                            listImages += [Image.open(chaminIMG + '/' + nomIMG)]
                            # Si on est dans un des dossiers de la liste
                            if dossier in ['P-Mob_Ami', 'P-Mob_Ennemi', 'P-Boss'] and imgGris is None and nomMovement == "move" :
                                # Creation des images de nuance gris dans un noueau dico
                                imgGris = createImgGrise(Image.open(chaminIMG + '/' + nomIMG))
                                l[dossierEntitee] = imgGris
                        listMovement[nomMovement] = listImages
                    listEntitee[dossierEntitee] = listMovement
                i[dossier] = listEntitee

            # IMAGE/DOSSIER/list(IMG)
            else:
                # Pour chaque image contenu dans un dossier
                for nomIMG in os.listdir(root + "/" + dossier):
                    nomfinal = firstLettreMaj(nomIMG.replace('.png', '').replace('.PNG', ''))
                    # Pour les dossier à ouvrir avec Tkinter
                    if dossier[0] == 'T':
                        # Chargement de l'image et save dans le dico avecc la clé à son nom
                        i[nomfinal] = PhotoImage(file=root + '/' + dossier + '/' + nomIMG)
                    elif dossier[0] == 'P':
                        # Chargement de l'image et save dans le dico avecc la clé à son nom
                        i[nomfinal] = Image.open(root + '/' + dossier + '/' + nomIMG)
                        # Si on est dans un des dossiers de la liste
                        if dossier in ['P-Structure']:
                            # Creation des images de nuance gris dans un noueau dico
                            l[nomfinal] = createImgGrise(Image.open(root + '/' + dossier + '/' + nomIMG))

            menu.upgradeProgressbar()
        menu.upgradeProgressbar()

        self.i = i


        # Caracteristique du player
        self.dic_player = {
            # x_velo, y_velo, listImagePlayer, deco, Bruitage        # bonus Vitesse de tir, degat, vie a voir
            'M': [6, 12, i['P-Player']["Homme"], i['Deco_Vie_M'], m.Bruit_Joueur['M']],
            'F': [6, 12, i['P-Player']["Femme"], i['Deco_Vie_F'], m.Bruit_Joueur['F']]}
        # Caracteristique des armes
        self.dic_arme = {
            # [freqTir, imageArme, imageArmeBras, munitions], [velocity, damage, imageBalle, imgExplose],
                # [BruitArme], [BruitBalle]
            'ALX_W30': [[45, i['ALX_W30'], i['Bras_ALX_W30'], 40], [13, 18, i['Shape_3972']],
                        m.Bruit_Arme['ALX_W30'][0], m.Bruit_Arme['ALX_W30'][1]],
            'Barreti': [[30, i['Barreti'], i['Bras_Barreti'], 'Infini'], [11, 3, i['Balle1']],
                        m.Bruit_Arme['Barreti'][0], m.Bruit_Arme['Barreti'][1]],
            'Cult_Silence': [[20, i['Cult_Silence'], i['Bras_Cult_Silence'], 'Infini'], [11, 6, i['Balle1']],
                             m.Bruit_Arme['Cult_Silence'][0], m.Bruit_Arme['Cult_Silence'][1]],
            'Dragon_Destructor': [[40, i['Dragon_Destructor'], i['Bras_Dragon_Destructor'], 10],
                                  [8, 75, i['Shape_187']],
                                  m.Bruit_Arme['Dragon_Destructor'][0], m.Bruit_Arme['Dragon_Destructor'][1]],
            'DA_Moonshadow': [[75, i['DA_Moonshadow'], i['Bras_DA_Moonshadow'], 35], [13, 33, i['Missile_burst']],
                              m.Bruit_Arme['DA_Moonshadow'][0], m.Bruit_Arme['DA_Moonshadow'][1]],
            'Dominator': [[20, i['Dominator'], i['Bras_Dominator'], 25], [14, 18, i['Craft_Missile']],
                          m.Bruit_Arme['Dominator'][0], m.Bruit_Arme['Dominator'][1]],
            'Logan_35': [[45, i['Logan_35'], i['Bras_Logan_35'], 50], [15, 18, i['Shape_3972']],
                         m.Bruit_Arme['Logan_35'][0], m.Bruit_Arme['Logan_35'][1]],
            'MCP_Avenger': [[8, i['MCP_Avenger'], i['Bras_MCP_Avenger'], 300], [22, 5, i['Glenos_G_160']],
                            m.Bruit_Arme['MCP_Avenger'][0], m.Bruit_Arme['MCP_Avenger'][1]],
            'MK_150': [[5, i['MK_150'], i['Bras_MK_150'], 300], [20, 5, i['C25_Marrugo']],
                       m.Bruit_Arme['MK_150'][0], m.Bruit_Arme['MK_150'][1]],
            'MC_5': [[55, i['MC_5'], i['Bras_MC_5'], 'Infini'], [13, 7, i['Balle1']],
                     m.Bruit_Arme['MC_5'][0], m.Bruit_Arme['MC_5'][1]],
            'Nayberg_NS30': [[45, i['Nayberg_NS30'], i['Bras_Nayberg_NS30'], 30], [10, 28, i['Shape_1346']],
                             m.Bruit_Arme['Nayberg_NS30'][0], m.Bruit_Arme['Nayberg_NS30'][1]],
            'Pequeno_R25': [[50, i['Pequeno_R25'], i['Bras_Pequeno_R25'], 25], [16, 20, i['Shape_1382']],
                            m.Bruit_Arme['Pequeno_R25'][0], m.Bruit_Arme['Pequeno_R25'][1]],
            'P25_Maisto': [[40, i['P25_Maisto'], i['Bras_P25_Maisto'], 25], [12, 38, i['Shape_1343']],
                           m.Bruit_Arme['P25_Maisto'][0], m.Bruit_Arme['P25_Maisto'][1]],
            'PA_4514': [[55, i['PA_4514'], i['Bras_PA_4514'], 15], [16, 33, i['Missile_burst']],
                        m.Bruit_Arme['PA_4514'][0], m.Bruit_Arme['PA_4514'][1]],
            'SG_200': [[10, i['SG_200'], i['Bras_SG_200'], 200], [15, 5, i['Balle1']],
                       m.Bruit_Arme['SG_200'][0], m.Bruit_Arme['SG_200'][1]],
            'Shape_3556': [[40, i['Shape_3556'], i['Bras_Shape_3556'], 15], [17, 35, i['Craft_Missile']],
                           m.Bruit_Arme['Shape_3556'][0], m.Bruit_Arme['Shape_3556'][1]],
            'TI_Prescision': [[4, i['TI_Prescision'], i['Bras_TI_Prescision'], 350], [25, 5, i['Glenos_G_160']],
                              m.Bruit_Arme['TI_Prescision'][0], m.Bruit_Arme['TI_Prescision'][1]],
            'vide': [[0, None, None, 0]]}




        # Caracteristique des mob gentils
        Mini_Mob_G = i['Mob_G']
        dG = i["P-Mob_Ami"]
        self.dic_mob_gentil = {
            # [velocity, frectir, health, imageMobe, imgGris, x_min, x_max, y_min, y_max, ImageMini, nbPoint, pos_y],
            # [velocityBballe, damage, imageBalle, imgExplose], [BruitArme], [BruitBalle]
            0: [[3, 50, 250, dG['Grenadier'], l['Grenadier'], 180, 200, 200, 100, Mini_Mob_G, 0, 0],
                [12, 2, i['Balle1']],
                m.Bruit_Mob_gentil[0][0], m.Bruit_Mob_gentil[0][1]],
            1: [[1.5, 75, 230, dG['Crewman'], l['Crewman'], 200, 200, 200, 100, Mini_Mob_G, 0, 0],
                [9, 5, i['Shape_1346']],
                m.Bruit_Mob_gentil[1][0], m.Bruit_Mob_gentil[1][1]],
            2: [[4, 45, 290, dG['Marksman'], l['Marksman'], 200, 200, 200, 100, Mini_Mob_G, 0, 0], [14, 3, i['Balle2']],
                m.Bruit_Mob_gentil[2][0], m.Bruit_Mob_gentil[2][1]],
            3: [[3, 60, 280, dG['CamionLeger'], l['CamionLeger'], 180, 200, 200, 100, Mini_Mob_G, 0, 0],
                [13, 7, i['Balle1']],
                m.Bruit_Mob_gentil[3][0], m.Bruit_Mob_gentil[3][1]],
            4: [[1.6, 55, 275, dG['CamionMini'], l['CamionMini'], 200, 200, 200, 100, Mini_Mob_G, 0, 0],
                [11, 8, i['Missile_burst']],
                m.Bruit_Mob_gentil[4][0], m.Bruit_Mob_gentil[4][1]],
            5: [[1.5, 70, 255, dG['Char'], l['Char'], 180, 200, 200, 100, Mini_Mob_G, 0, 0],
                [12, 12, i['Glenos_G_160']],
                m.Bruit_Mob_gentil[5][0], m.Bruit_Mob_gentil[5][1]],
            6: [[2, 80, 270, dG['CharMoyen'], l['CharMoyen'], 180, 200, 200, 100, Mini_Mob_G, 0, 0],
                [9, 10, i['Shape_1382']],
                m.Bruit_Mob_gentil[6][0], m.Bruit_Mob_gentil[6][1]],
            7: [[1.8, 90, 250, dG['TankLourd'], l['TankLourd'], 180, 200, 200, 100, Mini_Mob_G, 0, 0],
                [8, 15, i['Shape_187']],
                m.Bruit_Mob_gentil[7][0], m.Bruit_Mob_gentil[7][1]],
            8: [[1.5, 100, 290, dG['BlindeeCanonLong'], l['BlindeeCanonLong'], 180, 200, 200, 100, Mini_Mob_G, 0, 0],
                [7, 15, i['Shape_1343']],
                m.Bruit_Mob_gentil[8][0], m.Bruit_Mob_gentil[8][1]],
            9: [[2.0, 100, 425, dG['Avion_Aigle'], l['Avion_Aigle'], 0, 350, -50, 200, Mini_Mob_G, 0, -225],
                [10, 50, i['Shape_187']],
                m.Bruit_Mob_gentil[9][0], m.Bruit_Mob_gentil[9][1]],
            10: [[1.0, 20, 375, dG['Corvette'], l['Corvette'], 200, 80, -80, 100, Mini_Mob_G, 0, -225],
                 [7, 5, i['Shape_1343']],
                 m.Bruit_Mob_gentil[10][0], m.Bruit_Mob_gentil[10][1]]}

        # Caracteristique des mob mechants
        Mini_Mob_D = i['Mob_D']
        dM = i["P-Mob_Ennemi"]
        self.dic_mob_mechant = {
            # [velocity, frectir, health, imageMobe, imgGris, x_min, x_max, y_min, y_max, ImageMini, nbPoint, pos_y],
            # [velocityBballe, damage, imageBalle, , imgExplose], [BruitArme], [BruitBalle]
            0: [[-1.9, 40, 25, dM['Rebel_Soldier_fusee'], l['Rebel_Soldier_fusee'], 150, 180, 100, 200, Mini_Mob_D, 10, 0], [7, 20, i['Shape_3972']],
                m.Bruit_Mob_mechant[0][0], m.Bruit_Mob_mechant[0][1]],
            1: [[-2.2, 60, 35, dM['Rebel_Soldier_grenade'], l['Rebel_Soldier_grenade'], 160, 180, 100, 200, Mini_Mob_D, 25, 0], [12, 23, i['Balle1']],
                m.Bruit_Mob_mechant[1][0], m.Bruit_Mob_mechant[1][1]],
            2: [[-2.4, 50, 55, dM['Rebel_Soldier_Stielhandgranate'], l['Rebel_Soldier_Stielhandgranate'], 175, 180, 100, 200, Mini_Mob_D, 150, 0], [14, 25, i['Balle1']],
                m.Bruit_Mob_mechant[2][0], m.Bruit_Mob_mechant[2][1]],
            3: [[-2.0, 75, 65, dM['Rebel_Soldier_Rifle'], l['Rebel_Soldier_Rifle'], 165, 180, 100, 200, Mini_Mob_D, 200, 0], [12, 35, i['C25_Marrugo']],
                m.Bruit_Mob_mechant[3][0], m.Bruit_Mob_mechant[3][1]],
            4: [[-1.8, 70, 85, dM['Rebel_Soldier_Bazooka'], l['Rebel_Soldier_Bazooka'], 185, 180, 100, 200, Mini_Mob_D, 250, 0], [13, 40, i['Balle2']],
                m.Bruit_Mob_mechant[4][0], m.Bruit_Mob_mechant[4][1]],
            5: [[-1.6, 80, 15, dM['Rebel_Soldier_Mini_Gun'], l['Rebel_Soldier_Mini_Gun'], 185, 180, 100, 200, Mini_Mob_D, 300, 0], [14, 30, i['Shape_1343']],
                m.Bruit_Mob_mechant[5][0], m.Bruit_Mob_mechant[5][1]],
            6: [[-1.4, 35, 20, dM['Rebel_Soldier_mortier'], l['Rebel_Soldier_mortier'], 190, 180, 100, 200, Mini_Mob_D, 400, 0], [15, 50, i['Glenos_G_160']],
                m.Bruit_Mob_mechant[6][0], m.Bruit_Mob_mechant[6][1]],
            7: [[-2.0, 100, 100, dM['Allen_ONeill'], l['Allen_ONeill'], 200, 350, -100, 150, Mini_Mob_D, 400, 0], [10, 50, i['Shape_1382']],
                m.Bruit_Mob_mechant[7][0], m.Bruit_Mob_mechant[7][1]],
            8: [[-1.0, 20, 150, dM['Bazooka_Soldier'], l['Bazooka_Soldier'], 150, 150, -100, 200, Mini_Mob_D, 650, 0], [7, 5, i['Craft_Missile']],
                m.Bruit_Mob_mechant[8][0], m.Bruit_Mob_mechant[8][1]],
            9: [[-1.6, 80, 80, dM['Allen_Mecha'], l['Allen_Mecha'], 155, 180, 100, 200, Mini_Mob_D, 300, 0], [14, 30, i['Shape_1343']],
                m.Bruit_Mob_mechant[9][0], m.Bruit_Mob_mechant[9][1]],
            10: [[-1.6, 80, 80, dM['Morden_Robot'], l['Morden_Robot'], 155, 180, 100, 200, Mini_Mob_D, 300, 0], [14, 30, i['Shape_1343']],
                m.Bruit_Mob_mechant[9][0], m.Bruit_Mob_mechant[9][1]],
            11: [[-1.9, 40, 25, dM['Landeseek'], l['Landeseek'], 150, 180, 100, 200, Mini_Mob_D, 10, 0], [7, 20, i['Shape_3972']],
                m.Bruit_Mob_mechant[0][0], m.Bruit_Mob_mechant[0][1]],
            12: [[-2.2, 60, 35, dM['Machinegun_Unit'], l['Machinegun_Unit'], 160, 180, 100, 200, Mini_Mob_D, 25, 0], [12, 23, i['Balle1']],
                m.Bruit_Mob_mechant[1][0], m.Bruit_Mob_mechant[1][1]],
            13: [[-2.4, 50, 55, dM['KT_21'], l['KT_21'], 175, 180, 100, 200, Mini_Mob_D, 150, 0], [14, 25, i['Balle1']],
                m.Bruit_Mob_mechant[2][0], m.Bruit_Mob_mechant[2][1]],
            14: [[-2.0, 75, 65, dM['Bradley_Ptolemai'], l['Bradley_Ptolemai'], 165, 180, 100, 200, Mini_Mob_D, 200, 0], [12, 35, i['C25_Marrugo']],
                m.Bruit_Mob_mechant[3][0], m.Bruit_Mob_mechant[3][1]],
            15: [[-1.6, 80, 15, dM['Di_Cokka'], l['Di_Cokka'], 185, 180, 100, 200, Mini_Mob_D, 300, 0], [14, 30, i['Shape_1343']],
                m.Bruit_Mob_mechant[5][0], m.Bruit_Mob_mechant[5][1]],
            16: [[-1.4, 35, 20, dM['M_15A_Bradley'], l['M_15A_Bradley'], 190, 180, 100, 200, Mini_Mob_D, 400, 0], [15, 50, i['Glenos_G_160']],
                m.Bruit_Mob_mechant[6][0], m.Bruit_Mob_mechant[6][1]],
            17: [[-2.0, 100, 100, dM['Shoe_Brown'], l['Shoe_Brown'], 175, 350, -100, 150, Mini_Mob_D, 400, 0], [10, 50, i['Shape_1382']],
                m.Bruit_Mob_mechant[7][0], m.Bruit_Mob_mechant[7][1]],
            18: [[-1.0, 20, 150, dM['Flying_Tara'], l['Flying_Tara'], 250, 125, -100, 200, Mini_Mob_D, 650, -225], [7, 5, i['Craft_Missile']],
                m.Bruit_Mob_mechant[8][0], m.Bruit_Mob_mechant[8][1]],
            19: [[-1.6, 80, 80, dM['Ptolemaic_Tara'], l['Ptolemaic_Tara'], 155, 180, 100, 200, Mini_Mob_D, 300, -225], [14, 30, i['Shape_1343']],
                m.Bruit_Mob_mechant[9][0], m.Bruit_Mob_mechant[9][1]],
            20: [[-1.6, 80, 80, dM['MH_6J_Masknell_V1'], l['MH_6J_Masknell_V1'], 155, 180, 100, 200, Mini_Mob_D, 300, -225], [14, 30, i['Shape_1343']],
                 m.Bruit_Mob_mechant[9][0], m.Bruit_Mob_mechant[9][1]],
            21: [[-2.0, 75, 65, dM['MH_6J_Masknell_V2'], l['MH_6J_Masknell_V2'], 165, 180, 100, 200, Mini_Mob_D, 200, -225], [12, 35, i['C25_Marrugo']],
                m.Bruit_Mob_mechant[3][0], m.Bruit_Mob_mechant[3][1]]}

        # Caracteristique des boss
        Mini_Boss = i['Boss']
        dM = i["P-Boss"]
        self.dic_boss = {
            # [velocity, frectir, health, imageMobe, imgGris, x_min, x_max, y_min, y_max, ImageMini, nbPoint, pos_y],
            # [velocityBballe, damage, imageBalle, , imgExplose], [BruitArme], [BruitBalle]
            1: [[-2, 80, 700, dM['Scientist'], l['Scientist'], 155, 400, 100, 100, Mini_Boss, 1250, 0],
                [17, 40, i['Craft_Missile']], m.Bruit_Boss[1][0], m.Bruit_Boss[1][1]],
            2: [[-1.5, 100, 600, dM['Mars_People'], l['Mars_People'], 330, 180, 50, 75, Mini_Boss, 1250, 0],
                [16, 55, i['Shape_1382']], m.Bruit_Boss[2][0], m.Bruit_Boss[2][1]],
            3: [[-2.5, 35, 500, dM['Slug_Square'], l['Slug_Square'], 190, 280, 100, 0, Mini_Boss, 1250, 0],
                [15, 60, i['Glenos_G_160']], m.Bruit_Boss[3][0], m.Bruit_Boss[3][1]]}



        # Caracteristique des bases
        self.dic_base = {
            # imageBase, imgGris, health, nbpoint, biblioMob, imageMini, sonsBase
            'BaseD': [i['BaseD'], l['BaseD'], 1500, 1250, self.dic_mob_mechant, i['Base_D'], m.Bruit_Base['BaseD']],
            'BaseG': [i['BaseG'], l['BaseG'], 1500, 1250, self.dic_mob_gentil, i['Base_G'], m.Bruit_Base['BaseG']]}
        # Caracteristique des tour gentils
        self.dic_tour_G = {
            # [frectir, health, imageTour, imgGris, x_min, x_max, y_min, y_max, ImageMini, imageSocle, nbPoint],
            # [velocityBballe, damage, imageBalle, imgExplose], [BruitArme], [BruitBalle]
            'Tourelle1': [
                [25, 1000, i['Tourelle1_G'], l['Tourelle1_G'], 425, 425, 200, 200, i['Tour_G'], i['Socle_G'], 1000],
                [13, 5, i['Balle1']],
                m.Bruit_Tourelle_G['Tourelle1'][0], m.Bruit_Tourelle_G['Tourelle1'][1]],
            'Tourelle2': [
                [30, 1000, i['Tourelle2_G'], l['Tourelle2_G'], 200, 200, 200, 200, i['Tour_G'], i['Socle_G'], 1000],
                [10, 10, i['Balle2']],
                m.Bruit_Tourelle_G['Tourelle1'][0], m.Bruit_Tourelle_G['Tourelle1'][1]]}
        # Caracteristique des tour mechants
        self.dic_tour_D = {
            # [frectir, health, imageTour, imgGris, x_min, x_max, y_min, y_max, ImageMini, imageSocle, nbPoint],
            # [velocityBballe, damage, imageBalle, imgExplose], [BruitArme], [BruitBalle]
            'Tourelle1': [
                [25, 1000, i['Tourelle1_D'], l['Tourelle1_D'], 425, 425, 200, 200, i['Tour_D'], i['Socle_D'], 1000],
                [13, 5, i['Balle1']],
                m.Bruit_Tourelle_D['Tourelle1'][0], m.Bruit_Tourelle_D['Tourelle1'][1]],
            'Tourelle2': [
                [30, 1000, i['Tourelle2_D'], l['Tourelle2_D'], 450, 450, 200, 450, i['Tour_D'], i['Socle_D'], 1000],
                [10, 10, i['Balle2']],
                m.Bruit_Tourelle_D['Tourelle1'][0], m.Bruit_Tourelle_D['Tourelle1'][1]]}
        # Caracteristique des objets
        self.dic_objet = {
            # 0 pour les armes infini          1-5 pour les armes             6-9 pour les objets
            # image, effetmunition, effetsoin, effetmoney, numArme, sonsObjet
            0: [i['Munition'], 99999, 0, 0, None, m.Bruit_Objet[0]],
            6: [i['Conserve'], 0, 50, 0, None, m.Bruit_Objet[6]],
            7: [i['Fruit'], 0, 100, 0, None, m.Bruit_Objet[7]],
            8: [i['Sushi'], 0, 200, 0, None, m.Bruit_Objet[8]],
            9: [i['Bague'], 0, 0, 1750, None, m.Bruit_Objet[9]]}
        # Catalogue des armes
        self.dic_page = {
            'weapA': ['Pequeno_R25', 'Dragon_Destructor', 'TI_Prescision', 'ALX_W30', 'P25_Maisto', [350, 95]],
            'weapB': ['Cult_Silence', 'MC_5', None, None, None, [350 + 40 * 1, 95]],
            'weapC': ['SG_200', None, None, None, None, [350 + 40 * 2, 95]],
            'weapD': ['PA_4514', 'Shape_3556', None, None, None, [350 + 40 * 3, 95]],
            'weapE': ['MCP_Avenger', 'MK_150', 'TI_Prescision', None, None, [350 + 40 * 4, 95]],
            'weapF': ['Dominator', 'DA_Moonshadow', None, None, None, [350 + 40 * 5, 95]],
            'weapG': ['Nayberg_NS30', 'P25_Maisto', None, None, None, [350 + 40 * 6, 95]],
            'weapH': ['Pequeno_R25', 'ALX_W30', 'Dragon_Destructor', None, None, [350 + 40 * 7, 95]],
            'weapI': ['Logan_35', None, None, None, None, [350 + 40 * 8, 95]]}


############FIN###########FIN###########FIN###########FIN###########FIN###########FIN###########FIN


# Definition de tous les textes du jeux pour toutes les langues
class Text:
    def __init__(self, menu: Menu) -> None:
        # Parametre de Text
        self.menu = menu
        self.l = 0
        self.langue = ['Francais', 'Anglais']
        self.miniLangue = ['fr', 'ang']

        # Les fonts en fonction de leur taille
        self.f22 = Font(family="Rockwell Nova Cond", weight="bold", size=22, slant='roman', underline=0, overstrike=0)
        self.f23 = Font(family="Rockwell Nova Cond", weight="bold", size=23, slant='roman', underline=0, overstrike=0)
        self.fd1 = Font(family="Rockwell Nova Cond", weight="bold", size=25, slant='roman', underline=0, overstrike=0)
        self.fd2 = Font(family="Rockwell Nova Cond", weight="bold", size=25, slant='roman', underline=0, overstrike=0)
        self.f25 = Font(family="Rockwell Nova Cond", weight="bold", size=25, slant='roman', underline=0, overstrike=0)
        self.f20 = Font(family="Rockwell Nova Cond", weight="bold", size=20, slant='roman', underline=0, overstrike=0)
        self.f15 = Font(family="Rockwell Nova Cond", weight="bold", size=15, slant='roman', underline=0, overstrike=0)
        self.f17 = Font(family="Rockwell Nova Cond", weight="bold", size=17, slant='roman', underline=0, overstrike=0)
        self.f30 = Font(family="Rockwell Nova Cond", weight="bold", size=30, slant='roman', underline=0, overstrike=0)
        self.f40 = Font(family="Rockwell Nova Cond", weight="bold", size=40, slant='roman', underline=0, overstrike=0)
        self.f24 = Font(family="Rockwell Nova Cond", weight="bold", size=24, slant='roman', underline=0, overstrike=0)
        self.f13 = Font(family="Rockwell Nova Cond", weight="bold", size=13, slant='roman', underline=0, overstrike=0)

        # Couleur du texte
        self.c = '#FA8000'
        self.c1 = 'black'
        self.c2 = "#08081B"
        self.c3 = "#85201C"
        self.c4 = "#f19191"
        self.c5 = "#8d987b"
        self.c6 = "#29231c"

        # Menu Principal
        self.text = ['PAYS', 'COUNTRY']
        self.MP_box1 = ['JOUER', "PLAY"]
        self.MP_box2 = ['OPTION', "OPTION"]
        self.MP_box3 = ['? AIDE', "? HELP"]
        self.MP_box4 = ['SCORE', "SCORE"]
        self.MP_box5 = ['FUIR', "EXIT"]
        self.MP_box6 = ['RETOUR', "BACK"]
        self.MP_box7 = ['LANCER', "START"]


        # Menu Help
        self.helpTitle = ['Bienvenu dans l\'aide:', "Welcome in the help:"]
        self.helpExplanation = ["Objectif du jeu :\n Vous etes le P bleu \n- Detruitre les rouges\n- Proteger les "
                                "verts \n- Eviter de mourir  \n\n Pour les commandes, utiliser l'autre bouton pause "
                                "ou allez dans les options du menu principal \n\nPour changer d'etage : appuier 3 "
                                "fois sur la toche s'accroupir",
                                "Game Objective :\n You are the blue P \n- Destroy red camp\n- Protecte green camp\n"
                                "- Don't dei \n\n The commandes, use bouton pause or go in otion menu\n\n"
                                "to change floors : press the crouch key 3 times"]
        self.H_b1 = ["Vous", "You"]
        self.H_b2 = ["Vos alliés à protéger", 'Your allies to protect']
        self.H_b3 = ["Les vilains à éliminer", 'Villains to eliminate']

        # Menu scores
        self.scoreTitle = ['Liste des scores', "Rank Score"]
        self.score1 = ['\n\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n', '\n\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n']
        self.score2 = ['NOM\n', "NAME\n"]
        self.score3 = ['SCORE\n', "SCORE\n"]
        self.score4 = ['SEXE\n', "SEXE\n"]

        # Menu Option
        self.optionTitle = ['OPTION DE JEU', "GAME OPTION"]

        self.t_move1 = ["Déplacement 1", "Move 1"]
        self.t_move2 = ["Déplacement 2", "Move 2"]
        self.t_tomber = ['Tomber (x3)', 'Fall (x3)']
        self.t_allier = ['Renfort', "Forward"]
        self.t_changerArme = ["Changer arme", 'Select Weapon']
        self.t_tirer = ["Tirer", 'Shoot']
        self.t_aide = ['Aide', 'Help']
        self.t_pause = ['Pause', "Pause"]
        self.t_viser = ["Viser", 'Aim']

        self.sons = ['Reglage des bruitages', 'Sound effects adjustment']
        self.mus = ['Reglage de la musique', 'Music setting ']
        self.changeTouche = ['Appuyer sur la nouvelle touche', "Press the new key..."]
        self.defautTouche = ['Touche par défaut', 'Default keys']

        # Pop Up
        self.txtPopTitre = ["NOUVEAU PERSONNAGE", "CREATE NEW CHARACTER"]
        self.txtPopT1 = ['Nom :', 'Name g:']
        self.texPop1 = ['Pseudo invalide', 'Nickname invalid']
        self.texPop2 = ['Pseudo trop long', 'Nickname too long']
        self.texPop3 = ['Pseudo interdit', 'Nickname prohibited']
        self.txtCancel = ["RETOUR", "CANCEL"]
        self.txtConfirm = ['CONTINER', "CONFIRM"]

        # Menu Play
        self.nomMun = ['Munitions : ', 'Ammunition : ']
        self.mMission = ['CHOIX MISSION', 'SELECT MISSION']
        self.mArme = ['CHOIX ARME', 'WEAPON SELECT']
        self.mInventaire = ['INVENTAIRE', 'INVENTORY']
        self.mM1 = ['1 ETAGE', '1 FLOOR']
        self.mM2 = ['2 ETAGES', '2 FLOORS']
        self.mM3 = ['3 ETAGES', '3 FLOORS']


        # Interface du jeu
        self.indicMun = ['Infini', 'Loop']
        self.retMP = ['Retour menu principal', 'Back to main menu']
        self.play = ['clic sur play pour continuer', 'click on play to continue']
        self.indicbaseD = ["base ennemie", "ennemie base"]
        self.indicbaseG = ["base alliee", "alliee base"]
        self.spam = ['spammer SPACE pour passer', "spamme SPACE to skip"]
        self.win = ["Gagné", "You win"]
        self.lost = ['Perdu', 'You lost']
        self.end1 = ['Vous avez ', 'you ']
        self.end2 = ['Score finale de ', 'Final score by ']
        self.end3 = ['Debut : ', 'Start at : ']
        self.end4 = ['Fin : ', 'End at : ']

    def changeLangage(self, langue: str) -> None:
        if self.miniLangue.index(langue) != self.l:
            self.l = self.miniLangue.index(langue)
            self.menu.menu_pricipal()

    # Definition de tous les sons du jeu ainsi que ses reglage


class MusiqueGame:
    def __init__(self, windows: Tk, menu: Menu):
        self.windows = windows
        self.menu = menu
        pygame.mixer.init()
        menu.upgradeProgressbar()

        # partie musique
        self.arretMusique = False
        self.PosBarMus = 1
        self.m = []

        # Chargement des musiques
        nomMus = [['Battle_for_honor', 0.1, 143], ['Black_Hole', 0.1, 196], ['Centaury', 0.1, 202],
                  ['Game', 0.1, 64], ['Indian_Express', 0.1, 64],
                  ['Requiem', 0.1, 68], ['Retro_Gaming_Level', 0.1, 149],
                  ["Commando_Original-Mission-1_1", 0.1, 39],
                  ["Commando_Original-Mission-1_2", 0.1, 41],
                  ["Commando_Original-Mission-1_3", 0.1, 44],
                  ["Commando_Original-Mission-2_1", 0.1, 42],
                  ["Commando_Original-Mission-2_2", 0.1, 32],
                  ["Commando_Original-Mission-2_3", 0.1, 41],
                  ["Commando_Original-Mission-2_4", 0.1, 39],
                  ["Commando_Original-Mission-3_1", 0.1, 44],
                  ["Commando_Original-Mission-3_2", 0.1, 44],
                  ["Commando_Original-Mission-3_3", 0.1, 44],
                  ["Commando_Original-Mission-4_1", 0.1, 42],
                  ["Commando_Original-Mission-4_2", 0.1, 42],
                  ["Commando_Original-Mission-4_3", 0.1, 41],
                  ["Commando_Original-Mission-4_4", 0.1, 39],
                  ["Commando_Original-t_acceuil", 0.1, 10]
                  ]
        for nom, volume, time in nomMus:
            self.m += [[pygame.mixer.Sound("Sons/Musique/" + nom + ".ogg"), volume, time]]
            menu.upgradeProgressbar()

        # partie bruitage
        self.arretBruit = False
        self.PosBarBruit = 1
        b = {}

        # Chargement des bruitages
        nomSons = [
            ['Boss', [['spawn1', 0.1], ['spawn2', 0.1], ['spawn3', 0.1]]],
            ['Bouton', [['clic', 0.1], ['bip', 0.1]]],
            ['ArmeSpawn', [['recharge1', 0.1], ['recharge2', 0.1], ['recharge3', 0.1], ['recharge4', 0.1],
                           ['recharge5', 0.1], ['recharge6', 0.1], ['recharge7', 0.15], ['recharge8', 0.1],
                           ['recharge9', 0.1], ['recharge10', 0.1], ['recharge11', 0.2], ['recharge12', 0.15],
                           ['recharge13', 0.15], ['recharge14', 0.1], ['recharge15', 0.1], ['recharge16', 0.1]]],
            ['BalleDestroy/Arme', [['impact1', 0.05], ['impact4', 0.05], ['impact5', 0.05], ['impact9', 0.05],
                                   ['impact10', 0.05]]],
            ['BalleDestroy/Mob', [['impact2', 0.05], ['impact3', 0.05], ['impact6', 0.05], ['impact7', 0.05],
                                  ['impact8', 0.05]]],
            ['BalleSpawn/Arme', [['ALX_W30', 0.05], ['Cult_Silence', 0.08], ['DA_Moonshadow', 0.07],
                                 ['Dominator', 0.09], ['Barreti', 0.04], ['Dragon_Destructor', 0.3], ['SG_200', 0.3],
                                 ['Logan_35', 0.08], ['MC_5', 0.09], ['MCP_Avenger', 0.1], ['MK_150', 0.1],
                                 ['Nayberg_NS30', 0.1], ['P25_Maisto', 0.08], ['PA_4514', 0.1], ['Pequeno_R25', 0.08],
                                 ['Shape_3556', 0.09], ['TI_Prescision', 0.2]]],
            ['BalleSpawn/Mob', [['C25_Marrugo', 0.1], ['Craft_Missile', 0.1], ['Glenos_G_160', 0.1],
                                ['Image_Balle', 0.1], ['Image_Boulet', 0.1], ['missile_burst', 0.1], ['Shape_187', 0.1],
                                ['Shape_1343', 0.1], ['Shape_1346', 0.1], ['Shape_1382', 0.1], ['Shape_3972', 0.1]]],
            ['MobDamage', [['health', 0.04], ['touche1', 0.03], ['touche2', 0.03], ['touche3', 0.03], ['touche4', 0.03],
                           ['touche5', 0.03], ['touche6', 0.03], ['touche7', 0.03]]],
            ['MobDed', [['Humain1', 0.08], ['Humain2', 0.08], ['Humain3', 0.08], ['Humain4', 0.08], ['Humain5', 0.08],
                        ['Humain6', 0.07], ['DestructionBase', 0.1], ['DestructionChar', 0.3],
                        ['DestructionTour', 0.09]]],
            ['MobMove', [['moteurAvion1', 0.05], ['moteurAvion2', 0.25], ['moteurTank', 0.02]]],
            ['Objet', [['spawnItem', 0.08], ['dedItem', 0.07], ['eatItem', 0.3]]],
            ['Player', [['marche', 0.09], ['marcheSilence', 0.22], ['damagePlayer', 0.05], ['saut', 0.1],
                        ['envoyeTroupe', 0.1], ['dedPlayer', 0.4], ['upHealth', 0.09]]]]

        for dossier, listSons in nomSons:
            for nom, volume in listSons:
                b[nom] = [pygame.mixer.Sound("Sons/Bruit/" + dossier + '/' + nom + ".ogg"), volume]
            menu.upgradeProgressbar()
        self.b = b

        self.Bruit_Joueur = {
            # move, damage, ded, envoyetroupe, jump, accroupie
            'M': [b['marche'], b['damagePlayer'], b['dedPlayer'], b['envoyeTroupe'], b['saut'], b['marcheSilence']],
            'F': [b['marche'], b['damagePlayer'], b['dedPlayer'], b['envoyeTroupe'], b['saut'], b['marcheSilence']]}
        # bruitage d'arme vide bulletDestroy
        self.Bruit_Arme = {
            # [spawnArme], [spawnBalle, * exploseBalle]
            'ALX_W30': [b['recharge7'], [b['ALX_W30'], None]],
            'Barreti': [b['recharge16'], [b['Barreti'], None]],
            'Cult_Silence': [b['recharge13'], [b['Cult_Silence'], None]],
            'Dragon_Destructor': [b['recharge10'], [b['Dragon_Destructor'], b['impact5']]],
            'DA_Moonshadow': [b['recharge12'], [b['DA_Moonshadow'], b['impact1']]],
            'Dominator': [b['recharge11'], [b['Dominator'], None]],
            'Logan_35': [b['recharge1'], [b['Logan_35'], None]],
            'MCP_Avenger': [b['recharge9'], [b['MCP_Avenger'], None]],
            'MK_150': [b['recharge8'], [b['MK_150'], None]],
            'MC_5': [b['recharge14'], [b['MC_5'], None]],
            'Nayberg_NS30': [b['recharge7'], [b['Nayberg_NS30'], b['impact4']]],
            'Pequeno_R25': [b['recharge4'], [b['Pequeno_R25'], b['impact9']]],
            'P25_Maisto': [b['recharge6'], [b['P25_Maisto'], b['impact10']]],
            'PA_4514': [b['recharge5'], [b['PA_4514'], None]],
            'SG_200': [b['recharge15'], [b['SG_200'], None]],
            'Shape_3556': [b['recharge3'], [b['Shape_3556'], None]],
            'TI_Prescision': [b['recharge2'], [b['TI_Prescision'], None]]}
        self.Bruit_Mob_gentil = {
            # [* move, damage, ded], [spawnBalle, * exploseBalle]
            0: [[None, b['touche7'], b['Humain1']], [b['Image_Balle'], None]],
            1: [[None, b['touche1'], b['Humain2']], [b['Shape_3972'], None]],
            2: [[None, b['touche7'], b['Humain3']], [b['Image_Boulet'], None]],
            3: [[b['moteurTank'], b['touche1'], b['Humain4']], [b['Image_Balle'], None]],
            4: [[None, b['touche2'], b['DestructionChar']], [b['missile_burst'], None]],
            5: [[None, b['touche1'], b['DestructionChar']], [b['Glenos_G_160'], None]],
            6: [[None, b['touche4'], b['DestructionChar']], [b['Shape_1382'], None]],
            7: [[None, b['touche5'], b['DestructionChar']], [b['Shape_187'], None]],
            8: [[b['moteurTank'], b['touche6'], b['DestructionChar']], [b['Shape_1343'], b['impact3']]],
            9: [[b['moteurAvion1'], b['touche3'], b['DestructionChar']], [b['Shape_187'], None]],
            10: [[b['moteurAvion2'], b['touche5'], b['DestructionChar']], [b['Shape_1382'], b['impact8']]]}
        self.Bruit_Mob_mechant = {
            # [* move, damage, ded], [spawnBalle, - exploseBalle]
            0: [[None, b['touche7'], b['Humain5']], [b['Shape_3972'], None]],
            1: [[None, b['touche1'], b['Humain6']], [b['Image_Balle'], None]],
            2: [[None, b['touche7'], b['Humain4']], [b['Image_Balle'], None]],
            3: [[None, b['touche2'], b['DestructionChar']], [b['C25_Marrugo'], None]],
            4: [[None, b['touche3'], b['DestructionChar']], [b['Image_Boulet'], None]],
            5: [[None, b['touche7'], b['Humain3']], [b['Glenos_G_160'], None]],
            6: [[None, b['touche6'], b['Humain2']], [b['Shape_1382'], None]],
            7: [[b['moteurAvion2'], b['touche5'], b['DestructionChar']], [b['Craft_Missile'], None]],
            8: [[b['moteurAvion1'], b['touche6'], b['DestructionChar']], [b['Shape_1343'], None]],
            9: [[None, b['touche4'], b['DestructionChar']], [b['Shape_1382'], None]]}
        self.Bruit_Boss = {
            # [* move, damage, ded, spawn], [spawnBalle, - exploseBalle]
            1: [[None, b['touche2'], b['DestructionChar'], b['spawn1']], [b['Craft_Missile'], b['impact7']]],
            2: [[None, b['touche6'], b['DestructionChar'], b['spawn2']], [b['Shape_1382'], b['impact2']]],
            3: [[None, b['touche5'], b['DestructionChar'], b['spawn3']], [b['Glenos_G_160'], b['impact6']]]}
        self.Bruit_Objet = {
            # spawn, ded
            0: [b['spawnItem'], b['dedItem'], b['eatItem']],
            1: [b['spawnItem'], b['dedItem'], b['eatItem']],
            2: [b['spawnItem'], b['dedItem'], b['eatItem']],
            3: [b['spawnItem'], b['dedItem'], b['eatItem']],
            4: [b['spawnItem'], b['dedItem'], b['eatItem']],
            5: [b['spawnItem'], b['dedItem'], b['eatItem']],
            6: [b['spawnItem'], b['dedItem'], b['eatItem']],
            7: [b['spawnItem'], b['dedItem'], b['eatItem']],
            8: [b['spawnItem'], b['dedItem'], b['eatItem']],
            9: [b['spawnItem'], b['dedItem'], b['eatItem']]}
        self.Bruit_Base = {
            # damage, ded, heale
            'BaseD': [b['touche5'], b['DestructionBase'], b['health']],
            'BaseG': [b['touche5'], b['DestructionBase'], b['health']]}
        self.Bruit_Tourelle_G = {
            # [damage, ded], [spawnBalle, * exploseBalle]
            'Tourelle1': [[b['touche4'], b['DestructionTour']], [b['Image_Balle'], None]],
            'Tourelle2': [[b['touche4'], b['DestructionTour']], [b['Image_Boulet'], None]]}
        self.Bruit_Tourelle_D = {
            # [damage, ded], [spawnBalle, * exploseBalle]
            'Tourelle1': [[b['touche4'], b['DestructionTour']], [b['Image_Balle'], None]],
            'Tourelle2': [[b['touche4'], b['DestructionTour']], [b['Image_Boulet'], None]]}

    # Action Musical M1
    # Demarre une nouvelle musique
    def MusiqueStart(self, newMusique):
        # Repetition=n-1, temps d'ecoute, temps ouverture musique : 5000=5 seconde  mettre -1 pour repetition infini
        # Modifier le volume : set_volume va entre 0.00 à 1.00
        # On peut recuperer le volume du son et on peut demander la duree de la musique
        pygame.mixer.stop()
        demarage = 0
        self.volumeMus = newMusique[1]
        self.Musique = newMusique[0]
        self.Musique.play(-1, 0, demarage)
        self.volumeMusique(self.PosBarMus)
        if self.arretMusique:
            self.Musique.stop()

    # Action Musical M2
    def volumeMusique(self, vol):
        self.PosBarMus = float(vol)
        self.Musique.set_volume(round(self.volumeMus * self.PosBarMus, 3))

    # Action Musical M3
    # Stopper la musique en cour
    def StopMusique(self, event=True):
        self.Musique.stop()
        self.arretMusique = True
        self.windows.bind_all('<' + self.menu.config.allTouche['mus'] + '>', self.PlayMusique)
        try:
            self.menu.config.canvas.itemconfig(self.menu.config.Musique_Logo, image=self.menu.dataImg.i['rondRouge'])
        except:
            pass

    # Action Musical M4
    # Reprendre la musique en cour
    def PlayMusique(self, event=False):
        self.Musique.play()
        self.arretMusique = False
        self.windows.bind_all('<' + self.menu.config.allTouche['mus'] + '>', self.StopMusique)
        try:
            self.menu.config.canvas.itemconfig(self.menu.config.Musique_Logo, image=self.menu.dataImg.i['rondVert'])
        except:
            pass

    # Action Musical B1
    # Demarre un bruitage
    def Bruit_Touche(self, bruit, epicentre="Menu", zonePlayer=None):
        # Les bruit ne sactive que si non descativé et si visible par le joueur
        if not self.arretBruit:
            try:
                if epicentre == "Menu" and zonePlayer == None:
                    self.Bruitage = bruit[0]
                    self.volumeBrut = bruit[1]
                    self.Bruitage.play()
                    self.volumeBruit(self.PosBarBruit)
                elif zonePlayer[0] < epicentre[0] < zonePlayer[2] and zonePlayer[1] < epicentre[1] < zonePlayer[3] and \
                        bruit[0].get_num_channels() < 1:
                    self.Bruitage = bruit[0]
                    self.volumeBrut = bruit[1]
                    self.Bruitage.play()
                    self.volumeBruit(self.PosBarBruit)
            except:
                print('ERROR dans la fonction Bruit_Touche')
                print(zonePlayer, epicentre)

    # Action Musical B4
    def volumeBruit(self, vol):
        try:
            self.PosBarBruit = float(vol)
            self.Bruitage.set_volume(round(self.volumeBrut * self.PosBarBruit, 2))
        except:
            print("AttributeError: 'NoneType' object has no attribute 'set_volume'")

    # Action Musical B2
    # Desactive les bruits
    def Stop_Bruit(self, event=True):
        self.windows.bind_all('<' + self.menu.config.allTouche['bruit'] + '>', self.Play_Bruit)
        self.arretBruit = True
        try:
            self.menu.config.canvas.itemconfig(self.menu.config.Bruitage_Logo, image=self.menu.dataImg.i['rondRouge'])
        except:
            pass

    # Action Musical B3
    # Reactivation des bruits
    def Play_Bruit(self, event=False):
        self.windows.bind_all('<' + self.menu.config.allTouche['bruit'] + '>', self.Stop_Bruit)
        self.arretBruit = False
        try:
            self.menu.config.canvas.itemconfig(self.menu.config.Bruitage_Logo, image=self.menu.dataImg.i['rondVert'])
        except:
            pass


# Utilisation de fichiers
# Reglage du volume du son
# Reglage des touches et des scores qui sont sauvé dans un fichier
class Config:
    def __init__(self, window, menu, dataImg, dataMus, txt):
        # Recuperation des arguments
        self.window = window
        self.menu = menu
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.txt = txt

        # recuperation des touches du fichier
        self.recupTouche()
        self.docScore()

    # Cree ou recupere le fichier config.txt au debut du programme
    # Permet aussi de reinitialiser le fichier a 0
    def recupTouche(self, reset=0):  # reset = 1 ou reset sinon reset = None/0
        # Regarde si le fichier existe
        os.path.isfile("Doc/config.txt")
        # Si non on cree le fichier et le complete avec la liste des touches de bases
        if not os.path.isfile("Doc/config.txt") or reset == 1:
            allTouche = [
                "up1 : z ",
                "up2 : Up ",
                "down1 : s ",
                "down2 : Down ",
                "left1 : q ",
                "left2 : Left ",
                "right1 : d ",
                "right2 : Right ",
                "bruit : l ",
                "mus : m ",
                "spawner1 : space ",
                "spawner2 : t ",
                "weapon1 : a ",
                "weapon2 : e ",
                "shoot : Return ",
                "help : h ",
                "pause : p "]
            # Ecrit la config dse touches dans le fichier config.txt
            with open("Doc/config.txt", "w") as configtouche:
                for nbMot in allTouche:
                    configtouche.write(nbMot + "\n")
        # Le fichier existe maintenant obligatoirement.
        # On recupere les infos du fichier qu'on attibut dans self.allTouche
        self.allTouche = {
            'up1': None,
            'up2': None,
            'down1': None,
            'down2': None,
            'left1': None,
            'left2': None,
            'right1': None,
            'right2': None,
            'bruit': None,
            'mus': None,
            'spawner1': None,
            'spawner2': None,
            'weapon1': None,
            'weapon2': None,
            'shoot': None,
            'help': None,
            'pause': None
        }
        with open("Doc/config.txt", "r") as configtouche:
            for cle in self.allTouche:
                ligne = configtouche.readline()
                ligne = ligne.split(' ')
                self.allTouche[cle] = ligne[2]
        # On a plus besoin du fichier, on le ferme
        # Verification que le fichier n'est pas cassee
        for cle in self.allTouche:
            if self.allTouche[cle] == None or self.allTouche[cle] == "":
                self.recupTouche(1)
                break

    # Modifie et enregistre la nouvelle touche voulu
    def modifConfig(self, cle):
        # On regarde la ligne à modifier
        with open("Doc/config.txt", "r") as configtouche:
            text = 0
            ligne = -1
            while cle != text:
                ligne += 1
                text = configtouche.readline()
                text = text.split(' ')
                text = text[0]
        # recuperation du fichier integrale
        file = open("Doc/config.txt", "r")
        document = file.readlines()
        file.close()
        # Modification de la ligne
        document[ligne] = cle + " : " + self.allTouche[cle] + " \n"
        file = open("Doc/config.txt", "w")
        file.writelines(document)
        file.close()


    # Ecran pour modifier les parametres
    def reglage(self, canvas: tkinter.Canvas) -> None:

        # Décalage en x et y possible si on est en pleine partie.
        self.canvas = canvas
        Xdecal, Ydecal = 0, 0
        try:
            if canvas == self.menu.game.canvas:
                co = canvas.coords(self.menu.game.FrameMiniMap)
                Xdecal, Ydecal = abs(co[0] - 920), abs(co[1] - 15)
        except:
            pass

        ########## Bruitage ##########
        # Placement et définition de la couleur du voyant : Bruitage
        imgRond = self.dataImg.i['RondVert'] if self.menu.dataMus.arretBruit else self.dataImg.i['RondVert']
        self.Bruitage_Logo = canvas.create_image(695 + Xdecal, 460 + Ydecal, image=imgRond)
        # Creation du scale : Bruitage
        scaleBrut = Scale(canvas, from_=0, to=10, resolution=0.01, activebackground='red', orient=HORIZONTAL,
                          command=self.dataMus.volumeBruit, showvalue=0, width=15, length=200, label=self.txt.sons[self.txt.l])
        scaleBrut.set(self.dataMus.PosBarBruit)
        scaleBrut.pack()
        self.sousWindowBrut = canvas.create_window(820 + Xdecal, 460 + Ydecal, anchor='center', window=scaleBrut)
        # Affiche l'image d'une touche : Bruitage
        self.touche_bruit = canvas.create_image(650 + Xdecal, 460 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        # Mise en place de la lettre : Bruitage
        self.lettre_bruit = imgButton(self.menu, canvas, 650 + Xdecal, 460 + Ydecal, None, None,
                                      lambda touche: self.selectTouche(touche='bruit'), 'c', self.allTouche['bruit'],
                                      font=25 + int(round(25 / len(self.allTouche['bruit']) - 25)))

        ########## Musique ##########
        # Placement et définition de la couleur du voyant : Musique
        imgRond = self.dataImg.i['RondVert'] if self.menu.dataMus.arretMusique else self.dataImg.i['RondVert']
        self.Musique_Logo = canvas.create_image(695 + Xdecal, 520 + Ydecal, image=imgRond)
        # Creation du scale : Musique
        scaleMus = Scale(canvas, from_=0, to=10, resolution=0.01, activebackground='red', orient=HORIZONTAL,
                         command=self.dataMus.volumeMusique, showvalue=0, width=15, length=200, label=self.txt.mus[self.txt.l])
        scaleMus.set(self.dataMus.PosBarMus)
        scaleMus.pack()
        self.sousWindowMus = canvas.create_window(820 + Xdecal, 520 + Ydecal, anchor='center', window=scaleMus)
        # Affiche l'image d'une touche : Musique
        self.touche_mus = canvas.create_image(650 + Xdecal, 520 + Ydecal, image=self.dataImg.i['Touche'],anchor='c')
        # Mise en place de la lettre : Musique
        self.lettre_mus = imgButton(self.menu, canvas, 650 + Xdecal, 520 + Ydecal, None, None,
                                    lambda touche: self.selectTouche(touche='mus'), 'c', self.allTouche['mus'],
                                    font=25 + int(round(25 / len(self.allTouche['mus']) - 25)))

        ########## Boutons par défaut ##########
        self.touche_default = imgButton(self.menu, canvas, 100 + Xdecal, 520, self.dataImg.i['BoutonDefault'],
                                        self.dataImg.i['BoutonDefaultPass'], lambda event: self.default(), 'center')
        self.touche_default_txt = canvas.create_text(100 + Xdecal, 520 + Ydecal, font=self.txt.f15, fill=self.txt.c3,
                                                     state='disabled', anchor='center', text=self.menu.txt.defautTouche[self.txt.l])

        ########## Pause ##########
        # Affiche l'image d'une touche
        self.touche_pause = canvas.create_image(150 + Xdecal, 460 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        # Mise en place de la lettre
        self.lettre_pause = imgButton(self.menu, canvas, 150 + Xdecal, 460 + Ydecal, None, None,
                                      lambda touche: self.selectTouche(touche='pause'), 'c', self.allTouche['pause'],
                                      font=25 + int(round(25 / len(self.allTouche['pause']) - 25)))
        # Legende de la touche
        self.touche_pause_txt = canvas.create_text(110 + Xdecal, 460 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                     state='disabled', anchor='e', text=self.menu.txt. t_pause[self.txt.l])

        ########## Aide ##########
        # Affiche l'image d'une touche
        self.touche_help = canvas.create_image(150 + Xdecal, 400 + Ydecal,
                                               image=self.dataImg.i['Touche'], anchor='c')
        # Mise en place de la lettre
        self.lettre_help = imgButton(self.menu, canvas, 150 + Xdecal, 400 + Ydecal, None, None,
                                     lambda touche: self.selectTouche(touche='help'), 'c', self.allTouche['help'],
                                     font=25 + int(round(25 / len(self.allTouche['help']) - 25)))
        # Legende de la touche
        self.touche_help_txt = canvas.create_text(110 + Xdecal, 400 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                     state='disabled', anchor='e', text=self.menu.txt.t_aide[self.txt.l])

        ########## Move plache 1 ##########
        # Legende des touches
        self.touche_move1_txt = canvas.create_text(300 + Xdecal, 210 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                  state='disabled', anchor='n', text=self.menu.txt.t_move1[self.txt.l])
        # Sauter
        self.touche_up1 = canvas.create_image(300 + Xdecal, 120 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_up1 = imgButton(self.menu, canvas, 300 + Xdecal, 120 + Ydecal, None, None,
                                    lambda touche: self.selectTouche(touche='up1'), 'c', self.allTouche['up1'],
                                    font=25 + int(round(25 / len(self.allTouche['up1']) - 25)))
        # # S'accroupir
        self.touche_down1 = canvas.create_image(300 + Xdecal, 180 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_down1 = imgButton(self.menu, canvas, 300 + Xdecal, 180 + Ydecal, None, None,
                                      lambda touche: self.selectTouche(touche='down1'), 'c', self.allTouche['down1'],
                                      font=25 + int(round(25 / len(self.allTouche['down1']) - 25)))
        # Aller à gauche
        self.touche_left1 = canvas.create_image(240 + Xdecal, 180 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_left1 = imgButton(self.menu, canvas, 240 + Xdecal, 180 + Ydecal, None, None,
                                      lambda touche: self.selectTouche(touche='left1'), 'c', self.allTouche['left1'],
                                      font=25 + int(round(25 / len(self.allTouche['left1']) - 25)))
        # Aller à droite
        self.touche_right1 = canvas.create_image(360 + Xdecal, 180 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_right1 = imgButton(self.menu, canvas, 360 + Xdecal, 180 + Ydecal, None, None,
                                       lambda touche: self.selectTouche(touche='right1'), 'c', self.allTouche['right1'],
                                       font=25 + int(round(25 / len(self.allTouche['right1']) - 25)))

        ########## Move plache 2 ##########
        # Legende des touches
        self.touche_move2_txt = canvas.create_text(650 + Xdecal, 210 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                   state='disabled', anchor='n', text=self.menu.txt.t_move2[self.txt.l])
        # Sauter
        self.touche_up2 = canvas.create_image(650 + Xdecal, 120 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_up2 = imgButton(self.menu, canvas, 650 + Xdecal, 120 + Ydecal, None, None,
                                    lambda touche: self.selectTouche(touche='up2'), 'c', self.allTouche['up2'],
                                    font=25 + int(round(25 / len(self.allTouche['up2']) - 25)))
        # S'accroupir
        self.touche_down2 = canvas.create_image(650 + Xdecal, 180 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_down2 = imgButton(self.menu, canvas, 650 + Xdecal, 180 + Ydecal, None, None,
                                      lambda touche: self.selectTouche(touche='down2'), 'c', self.allTouche['down2'],
                                      font=25 + int(round(25 / len(self.allTouche['down2']) - 25)))
        # Aller à gauche
        self.touche_left2 = canvas.create_image(590 + Xdecal, 180 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_left2 = imgButton(self.menu, canvas, 590 + Xdecal, 180 + Ydecal, None, None,
                                      lambda touche: self.selectTouche(touche='left2'), 'c', self.allTouche['left2'],
                                      font=25 + int(round(25 / len(self.allTouche['left2']) - 25)))
        # Aller à droite
        self.touche_right2 = canvas.create_image(710 + Xdecal, 180 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_right2 = imgButton(self.menu, canvas, 710 + Xdecal, 180 + Ydecal, None, None,
                                       lambda touche: self.selectTouche(touche='right2'), 'c', self.allTouche['right2'],
                                       font=25 + int(round(25 / len(self.allTouche['right2']) - 25)))

        ########## Viser ##########
        # Legende des touches
        self.touche_viser_txt = canvas.create_text(150 + Xdecal, 310 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                   state='disabled', anchor='n', text=self.menu.txt.t_viser[self.txt.l])
        # Avec le mouvement de la sourie
        self.mouseAim = canvas.create_image(150 + Xdecal, 280 + Ydecal, image=self.dataImg.i['MouseAim'])

        ########## Tirer ##########
        # Legende des touches
        self.touche_tirer_txt = canvas.create_text(480 + Xdecal, 310 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                   state='disabled', anchor='n', text=self.menu.txt.t_tirer[self.txt.l])
        # Avec le clic droit de la sourie
        self.mouseRight = canvas.create_image(450 + Xdecal, 280 + Ydecal, image=self.dataImg.i['MouseRight'])
        # Avec une touche du clavier
        self.touche_shoot = canvas.create_image(510 + Xdecal, 280 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_shoot = imgButton(self.menu, canvas, 510 + Xdecal, 280 + Ydecal, None, None,
                                      lambda touche: self.selectTouche(touche='shoot'), 'c', self.allTouche['shoot'],
                                      font=25 + int(round(25 / len(self.allTouche['shoot']) - 25)))

        ########## Changer arme ##########
        # Legende des touches
        self.touche_arme_txt = canvas.create_text(760 + Xdecal, 310 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                   state='disabled', anchor='n', text=self.menu.txt.t_changerArme[self.txt.l])
        # Avec la molette de la sourie
        self.mouseCenter = canvas.create_image(700 + Xdecal, 280 + Ydecal,
                                               image=self.dataImg.i['MouseCenter'])
        # Avec une première touche du clavier
        self.touche_weapon1 = canvas.create_image(760 + Xdecal, 280 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_weapon1 = imgButton(self.menu, canvas, 760 + Xdecal, 280 + Ydecal, None,
                                        None, lambda touche: self.selectTouche(touche='weapon1'), 'c', self.allTouche['weapon1'],
                                        font=25 + int(round(25 / len(self.allTouche['weapon1']) - 25)))
        # Avec une seconde touche du clavier
        self.touche_weapon2 = canvas.create_image(820 + Xdecal, 280 + Ydecal,
                                                  image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_weapon2 = imgButton(self.menu, canvas, 820 + Xdecal, 280 + Ydecal, None,
                                        None, lambda touche: self.selectTouche(touche='weapon2'), 'c', self.allTouche['weapon2'],
                                        font=25 + int(round(25 / len(self.allTouche['weapon2']) - 25)))

        ########## Tomber ##########
        # Legende des touches
        self.touche_tomber_txt = canvas.create_text(310 + Xdecal, 395 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                  state='disabled', anchor='n', text=self.menu.txt.t_tomber[self.txt.l])
        # Avec une première touche du clavier
        self.touche_fall1 = canvas.create_image(280 + Xdecal, 370 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_fall1 = canvas.create_text(280 + Xdecal, 370 + Ydecal, font=self.txt.fd1,
                                               fill=self.txt.c1, anchor='center', text=self.allTouche['down1'])
        # Avec une seconde touche du clavier
        self.touche_fall2 = canvas.create_image(340 + Xdecal, 370 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_fall2 = canvas.create_text(340 + Xdecal, 370 + Ydecal, font=self.txt.fd2,
                                               fill=self.txt.c1, anchor='center', text=self.allTouche['down2'])
        # Change la taille des touches imprimé en noir
        self.txt.fd1.config(size=(25 + int(round(25 / len(self.allTouche['down1']) - 25))))
        self.txt.fd2.config(size=(25 + int(round(25 / len(self.allTouche['down2']) - 25))))

        ########## Appeller alliers ##########
        # Legende des touches
        self.touche_allier_txt = canvas.create_text(620 + Xdecal, 395 + Ydecal, font=self.txt.f20, fill=self.txt.c4,
                                                  state='disabled', anchor='n', text=self.menu.txt.t_allier[self.txt.l])
        # Avec une première touche du clavier
        self.touche_spawner1 = canvas.create_image(590 + Xdecal, 370 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_spawner1 = imgButton(self.menu, canvas, 590 + Xdecal, 370 + Ydecal, None,
                                         None, lambda touche: self.selectTouche(touche='spawner1'), 'c', self.allTouche['spawner1'],
                                         font=25 + int(round(25 / len(self.allTouche['spawner1']) - 25)))
        # Avec une seconde touche du clavier
        self.touche_spawner2 = canvas.create_image(650 + Xdecal, 370 + Ydecal, image=self.dataImg.i['Touche'], anchor='c')
        self.lettre_spawner2 = imgButton(self.menu, canvas, 650 + Xdecal, 370 + Ydecal, None,
                                         None, lambda touche: self.selectTouche(touche='spawner2'), 'c', self.allTouche['spawner2'],
                                         font=25 + int(round(25 / len(self.allTouche['spawner2']) - 25)))




        # Liste des objets présent ici pour suppression
        self.listTouche = [
            # Bruitage
            self.Bruitage_Logo, self.sousWindowBrut, self.touche_bruit, self.lettre_bruit,
            # Musique
            self.Musique_Logo, self.sousWindowMus, self.touche_mus, self.lettre_mus,
            # Touche par defaut
            self.touche_default, self.touche_default_txt,
            # Pause
            self.touche_pause, self.lettre_pause, self.touche_pause_txt,
            # Aide
            self.touche_help, self.lettre_help, self.touche_help_txt,
            # Move 1
            self.touche_move1_txt, self.touche_up1, self.lettre_up1, self.touche_down1, self.lettre_down1,
            self.touche_left1, self.lettre_left1, self.touche_right1, self.lettre_right1,
            # Move 2
            self.touche_move2_txt, self.touche_up2, self.lettre_up2, self.touche_down2, self.lettre_down2,
            self.touche_left2, self.lettre_left2, self.touche_right2, self.lettre_right2,
            # Viser
            self.touche_viser_txt, self.mouseAim,
            # Tirer
            self.touche_tirer_txt, self.mouseRight, self.touche_shoot, self.lettre_shoot,
            # Changer arme
            self.touche_arme_txt, self.mouseCenter, self.touche_weapon1, self.lettre_weapon1, self.touche_weapon2, self.lettre_weapon2,
            # Tomber
            self.touche_tomber_txt, self.touche_fall1, self.lettre_fall1, self.touche_fall2, self.lettre_fall2,
            # Appeller alliers
            self.touche_allier_txt, self.touche_spawner1, self.lettre_spawner1, self.touche_spawner2, self.lettre_spawner2,
        ]






    # Player a selectionner une action dont il faut changer la touche
    def selectTouche(self, touche):
        self.touche = touche
        self.window.bind('<Key>', self.newTouche)
        Xdecal, Ydecal = 0, 0
        try:
            if self.canvas == self.menu.game.canvas:
                co = self.canvas.coords(self.menu.game.FrameMiniMap)
                Xdecal, Ydecal = abs(co[0] - 920), abs(co[1] - 15)
        except:
            pass
        try:
            self.canvas.delete(self.indicNexTouche)
        except:
            pass
        self.indicNexTouche = self.canvas.create_text(345 + Xdecal, 100 + Ydecal, font=self.txt.f25, fill=self.txt.c,
                                                      anchor='w', text=self.txt.changeTouche[self.txt.l])

    # Player a saisie sa nouvelle touche
    def newTouche(self, event):
        newTouch = event.keysym
        try:
            self.menu.windows.unbind_all('<' + self.allTouche[self.touche] + '>')
        except:
            pass
        for cle in self.allTouche:
            if self.allTouche[cle] == newTouch:
                self.allTouche[cle] = self.allTouche[self.touche]
                # Modification du fichier
                self.modifConfig(cle)
                break
        self.allTouche[self.touche] = newTouch
        # Modification du fichier
        self.modifConfig(self.touche)
        self.removeTouche()
        self.reglage(self.canvas)
        self.window.unbind('<Key>')
        self.canvas.delete(self.indicNexTouche)
        try:
            self.menu.game.reactive_touche()
            self.menu.game.desactive_touche()
        except:
            pass

    # Remet les touches par defauts
    def default(self):
        self.menu.windows.unbind_all('<' + self.allTouche['mus'] + '>')
        self.menu.windows.unbind_all('<' + self.allTouche['bruit'] + '>')
        # Auto modification à la place de recuperation des donnees
        self.recupTouche(1)
        self.removeTouche()
        self.reglage(self.canvas)
        try:
            self.menu.game.desactive_touche()
            self.menu.game.reactive_touche()
            self.menu.game.desactive_touche()
        except:
            pass
        self.menu.windows.bind_all('<' + self.allTouche['mus'] + '>', self.dataMus.StopMusique)
        self.menu.windows.bind_all('<' + self.allTouche['bruit'] + '>', self.dataMus.Stop_Bruit)

    # Supprime l'ecran de configuration
    def removeTouche(self) -> None:
        for element in self.listTouche:
            try:
                self.canvas.delete(element.bouton)
            except:
                self.canvas.delete(element)

        self.window.unbind('<Key>')
        try:
            self.canvas.delete(self.menu.config.indicNexTouche)
        except:
            pass

    # Regarde si le fichier existe
    def docScore(self, reset=0):
        os.path.isfile("Doc/score.txt")
        # Si non on cree le fichier et le complete avec la liste des touches de bases
        if not os.path.isfile("Doc/score.txt") or reset == 1:
            # Ecrit la config dse touches dans le fichier config.txt
            with open("Doc/score.txt", "w") as configscore:
                pass

    # Affiche les 10 meilleurs scores
    def Score(self) -> None:
        # On regarde le nombre de ligne
        file = open("Doc/score.txt", "r")
        totLigne = len(file.readlines())
        file.close()

        # On recupere les 10 meilleurs joueurs
        with open("Doc/score.txt", "r") as configScore:
            score = [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1],
                     [-1, -1], ]
            nbligne = 0
            while nbligne < totLigne:
                player = configScore.readline().split(' ')
                if int(player[1]) > score[-1][0]:
                    score[9][0] = int(player[1])
                    score[9][1] = nbligne
                    score.sort(reverse=True)
                nbligne += 1

        # Creation des labels
        score2 = self.txt.score2[self.txt.l]
        score3 = self.txt.score3[self.txt.l]
        score4 = self.txt.score4[self.txt.l]
        self.menu.canvas.create_text(135, 77, text=self.txt.score1[self.txt.l], font=self.txt.f23, fill=self.txt.c4,
                                     anchor='nw')
        nom = self.menu.canvas.create_text(175, 117, text=score2, font=self.txt.f23, fill=self.txt.c4, anchor='nw',
                                           width=300)
        sexe = self.menu.canvas.create_text(545, 117, text=score4, font=self.txt.f23, fill=self.txt.c4, anchor='nw', )
        point = self.menu.canvas.create_text(625, 117, text=score3, font=self.txt.f23, fill=self.txt.c4, anchor='nw',
                                             width=300)

        # On affiche les 10 meilleurs trouvé
        file = open("Doc/score.txt", "r")
        document = file.readlines()
        for numligne in score:
            if numligne[0] == -1 or totLigne == 0:
                ligne = ['None', 'None', 'None']
            else:
                ligne = document[numligne[1]].split(' ')
            score2 += str(ligne[0]) + '\n'
            score3 += str(ligne[1]) + '\n'
            score4 += ligne[2] + '\n'
            self.menu.canvas.itemconfig(nom, text=score2)
            self.menu.canvas.itemconfig(point, text=score3)
            self.menu.canvas.itemconfig(sexe, text=score4)
        file.close()

    # Ajoute un nouveau score à la liste
    def addScore(self, newScore):
        # newScore = "nom score sexe mission debut fin \n"
        # On affiche les 10 meilleurs trouvé
        file = open("Doc/score.txt", "r")
        document = file.readlines()
        file.close()
        document += [newScore + " \n"]
        # ajout un nouveau score au fichier
        file = open("Doc/score.txt", "w")
        file.writelines(document)
        file.close()


# Toute entitie de la game sont regroupee dans des camps
class Camp:
    def __init__(self, game, canvas, couleur, pos_x, pos_y, menu, windows, nbBase, nb_vie, dataImg, dataMus):
        # Recuperation des informations
        self.game = game
        self.canvas = canvas
        self.couleur = couleur
        self.pos_x = pos_x  # Point de spawn en x
        self.pos_y = pos_y  # Point de spawn en y
        self.menu = menu
        self.windows = windows
        self.nbBase = nbBase
        self.dataImg = dataImg
        self.dataMus = dataMus

        # Creation des groupes de sprite pour chaque categorie
        self.all_mob = pygame.sprite.Group()
        self.all_ball = pygame.sprite.Group()
        self.all_tourelle = pygame.sprite.Group()
        self.all_base = pygame.sprite.Group()

        # Creation des caractreristique d'une base
        self.nb_vie = nb_vie
        self.quit_game = False
        self.stepHeal = 1
        self.txt = self.game.txt

        # Creation du joueur

        if couleur == "blue":
            # Les prix pour engager des mercenaires
            self.etape = [[1000, None, False], [1500, None, False], [2000, None, False], [2500, None, False],
                          [3000, None, False], [3500, None, False], [4000, None, False], [4500, None, False],
                          [5000, None, False], [5500, None, False], [6000, None, False]]
            self.scoreMutilple = [500, 500]

            self.all_players = pygame.sprite.Group()
            # x_velo, y_velo, imagePlayer, imagePlayerBas, IconPlayer, Bruitage
            self.Cararc_Joueur = self.dataImg.dic_player[self.game.sexe]
            self.score = self.game.DollardDeBase
            self.totalScore = self.score
            self.ID_vie_restant = self.canvas.create_text(80, 40, text="X" + str(self.nb_vie), font=self.txt.f20,
                                                          fill=self.txt.c)
            self.ID_score = self.canvas.create_text(200, 40, text="$" + str(self.score), font=self.txt.f20,
                                                    fill=self.txt.c)
            self.set_loot(0)
            self.ID_cadre = self.canvas.create_image(160, 55, image=self.Cararc_Joueur[3])
            self.ID_pseudo = self.canvas.create_text(5, 5, text=self.game.pseudo, font=self.txt.f15, fill=self.txt.c,
                                                     anchor='nw')
            self.ID_stepHeal = self.canvas.create_rectangle(5, 85, 5 + 310 * self.totalScore / (20000 * self.stepHeal),
                                                            88, fill='orange')
            self.player = self.invoqueJoueur()
        # Creation des mechants
        else:
            self.all_item = pygame.sprite.Group()

        # Creation des bases, tourelles et platformes
        self.nbBase = nbBase
        pos_carte = self.canvas.bbox(self.game.ID_background)
        if self.couleur == "blue":
            caracTour1 = self.dataImg.dic_tour_G['Tourelle1']
            caracTour2 = self.dataImg.dic_tour_G['Tourelle2']
            caracBase = self.dataImg.dic_base['BaseG']
        else:
            caracTour1 = self.dataImg.dic_tour_D['Tourelle1']
            caracTour2 = self.dataImg.dic_tour_D['Tourelle2']
            caracBase = self.dataImg.dic_base['BaseD']

        for id_etage in range(self.nbBase):
            # ImageGame, MusiqueGame, menu, game, camp, canvas, pos_x, pos_y, caracBase, caracTour
            self.all_base.add(
                Base(self.dataImg, self.dataMus, self.menu, self.game, self, self.canvas, self.pos_x,
                     self.pos_y + pos_carte[1] + 660 * id_etage, caracBase, id_etage, caracTour2))
            if id_etage > 0:
                for hauteur in range(1050, 1201, 150):  # Creation de deux platforme de chaque coté
                    self.game.all_platforme.add(Platforme(self.game, self, self.canvas, self.pos_x - (hauteur + 200),
                                                          self.pos_y + 900 + pos_carte[
                                                              1] + 660 * 1 * id_etage - hauteur,
                                                          self.dataImg.i['Platforme']))
            for nbtour in range(500, 2001, 500):
                (Tourelle(self.dataImg, self.dataMus, self.menu, self.game, self, self.canvas,
                          (abs(self.pos_x - nbtour)),
                          self.pos_y + pos_carte[1] + 660 * id_etage, True, caracTour1))

    # Exemple:
    #  self.player = Player(ImageGame, MusiqueGame, game, camp, canvas, pseudo, health, pos_x, pos_y, Cararc_Joueur)
    def invoqueJoueur(self):
        self.player = Player(self.dataImg, self.dataMus, self.game, self, self.canvas, "Admin", self.game.nbPv,
                             self.pos_x, self.pos_y+30, self.Cararc_Joueur)
        # Deplace  la minimap, le cardre, le sexe du joueur, les scores et le nb vie du player
        co = self.canvas.coords(self.game.FrameMiniMap)
        x, y = -abs(co[0] - 920), -abs(co[1] - 15)
        self.canvas.move(self.game.FrameMiniMap, x, y)
        self.canvas.move(self.ID_cadre, x, y)
        self.canvas.move(self.ID_vie_restant, x, y)
        self.canvas.move(self.ID_score, x, y)
        self.canvas.move(self.ID_stepHeal, x, y)
        return self.player

    def set_loot(self, nbpoint):
        self.score += nbpoint
        if nbpoint > 0:
            self.totalScore += nbpoint
            # Gagne des vie
            if self.totalScore >= 30000 * self.stepHeal:
                self.stepHeal += 1
                self.nb_vie += 1
                # Son d'apparition de l'ame
                self.dataMus.Bruit_Touche(self.dataMus.b['upHealth'], 'Menu', None)
                self.canvas.itemconfigure(self.ID_vie_restant, text="X" + str(self.nb_vie))
            coordsX, coordsY = -self.player.x_decalPlayer, -self.player.y_decalPlayer
            self.canvas.delete(self.ID_stepHeal)
            self.ID_stepHeal = self.canvas.create_rectangle(5 + coordsX, 85 + coordsY,
                                                            5 + coordsX + 310 * self.totalScore / (
                                                                        20000 * self.stepHeal), 88 + coordsY,
                                                            fill='orange')
        self.canvas.itemconfigure(self.ID_score, text="$" + str(self.score))
        for num in range(len(self.etape)):
            if self.score >= self.etape[num][0] and self.etape[num][2] is False:
                self.etape[num][1] = self.game.canvas_bar.create_image(40 + 85 * num, 55,
                                                                       image=self.dataImg.i['Filtre_vert'])
                self.etape[num][2] = True

    # Peut mettre fin au jeu
    def resurection(self):
        self.nb_vie -= 1
        self.canvas.scan_dragto(0, 0)
        self.x_decalPlayer = 0
        self.y_decalPlayer = 0
        self.player = self.invoqueJoueur()
        self.canvas.itemconfigure(self.ID_vie_restant, text="X" + str(self.nb_vie))

        # Fonction appartenant a tous les objets differents

    class Global():
        def __init__(self):
            self.numImg = 0
            self.dossier = None

        # Mise en mouvement de l'objet
        def animation(self, dossier, miror=False):
            if self.dossier != dossier:
                self.dossier = dossier
                self.numImg = 0

            # Passe à l'image suivante
            self.numImg += 1

            # Verifie si on a atteint lla fin du dossier
            if self.numImg >= len(dossier):
                # Remettre l'animation au depart
                self.numImg = 0

            # Modifier l'image précédente par la suivante en fonction du sens de deplacement
            if miror == False:
                self.img = ImageTk.PhotoImage(dossier[self.numImg])
                self.canvas.itemconfigure(self.ID_visual, image=self.img, anchor='s')
            else:
                self.img = ImageTk.PhotoImage(ImageOps.mirror(dossier[self.numImg]))
                self.canvas.itemconfigure(self.ID_visual, image=self.img, anchor='s')






# Fonction appartenant a tous les objets differents
class Entity():
    def __init__(self):
        self.numImg = 0
        self.dossier = None

    # Mise en mouvement de l'objet
    def animation(self, dossier, miror=False):
        if self.dossier != dossier:
            self.dossier = dossier
            self.numImg = -1

        # Passe à l'image suivante
        self.numImg += 1

        # Verifie si on a atteint lla fin du dossier
        if self.numImg >= len(dossier):
            # Remettre l'animation au depart
            self.numImg = -1

        # Modifier l'image précédente par la suivante en fonction du sens de deplacement
        if miror == False:
            self.img = ImageTk.PhotoImage(dossier[self.numImg])
            self.canvas.itemconfigure(self.ID_visual, image=self.img, anchor='s')
        else:
            self.img = ImageTk.PhotoImage(ImageOps.mirror(dossier[self.numImg]))
            self.canvas.itemconfigure(self.ID_visual, image=self.img, anchor='s')








# Une base peut se prendre des degats  (impact: animation, vie et barre de vie) et mettre fin a la partie
class Tourelle(pygame.sprite.Sprite):
    def __init__(self, dataImg, dataMus, menu, game, camp, canvas, pos_x, pos_y, socle, caracTour):
        super().__init__()
        # Recuperation des liens de connections et autres infos
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.menu = menu
        self.game = game
        self.camp = camp
        self.canvas = canvas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.socle = socle

        # Recuperation des caracteristique : [[frectir, health, imageTour, imgGris, x_min, x_max, y_min, y_max, ImageMini, imageSocle, nbPoint],
        # [velocityBballe, damage, imageBalle], [BruitArme], [BruitBalle]]
        self.frectir = caracTour[0][0]
        self.health = caracTour[0][1]
        self.imageTourModele = caracTour[0][2]
        self.imageGris = caracTour[0][3]
        self.x_min = caracTour[0][4]
        self.x_max = caracTour[0][5]
        self.y_min = caracTour[0][6]
        self.y_max = caracTour[0][7]
        self.imageMini = caracTour[0][8]
        self.imageSocle = caracTour[0][9]
        self.nbPoint = caracTour[0][10]

        # Recuperation des sons
        # [damage, ded], [spawnBalle, exploseBalle]
        self.bruitDamage = caracTour[2][0]
        self.bruitDed = caracTour[2][1]

        self.caracBullet = caracTour[1]
        self.SonsBullet = caracTour[3]

        self.couleur = camp.couleur
        self.frectir_ini = self.frectir
        self.max_health = self.health
        self.renfort = False

        self.camp.all_tourelle.add(self)

        # Creation des caracteristiques d'une base
        self.rechargement = False
        self.rotat = 0
        self.imageTour = ImageTk.PhotoImage(self.imageTourModele.rotate(self.rotat))
        if self.socle is True:  # Si c'est une tourelle normal, on lui ajout un socle sinon elle est deja sur une base
            self.ID_socle = self.canvas.create_image(self.pos_x - 10, self.pos_y, image=self.imageSocle, anchor='s')
            coords = self.canvas.bbox(self.ID_socle)
            self.ID_max_health = self.canvas.create_rectangle(coords[0] + 25, coords[1] + 75,
                                                              (coords[0] + 25 + (coords[2] - coords[
                                                                  0] - 50) * self.health / self.max_health),
                                                              coords[1] + 65, fill="gray")
            self.ID_health = self.canvas.create_rectangle(coords[0] + 25, coords[1] + 75,
                                                          (coords[0] + 25 + (coords[2] - coords[
                                                              0] - 50) * self.health / self.max_health),
                                                          coords[1] + 65, fill=self.couleur)

            # point d'attache au sol, x = pos_x+demi longueur de l'image+marge du cadre y = coord_y[3]+20+marge du cadre
            self.ID_tourelle_mini = self.game.canvasMiniMap.create_image(5 + self.pos_x // 15.3, 9 + coords[3] // 16.5,
                                                                         anchor='s', image=self.imageMini)

        # Creation image de la Tourelle et ses PV
        self.ID_visual = self.canvas.create_image(self.pos_x + 15, self.pos_y - 200, anchor='c', image=self.imageTour)

    # Cherche un cible puis lui tire dessus
    def cherche_cible(self):
        coords = self.canvas.bbox(self.ID_visual)
        shooter_x = coords[0] + (coords[2] - coords[0]) / 2
        shooter_y = coords[1] + (coords[3] - coords[1]) / 2
        en_joue = self.game.ennemieDetection(self, 'tour', self.rechargement)
        # Le mob a le choit entre tirer, recharger et avancer
        A = self.canvas.coords(self.ID_visual)
        if en_joue:
            B = [en_joue[1], en_joue[2]]
            self.se_potiononne(A, B)
            Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, shooter_x, shooter_y,
                   en_joue[1], en_joue[2], self.caracBullet, self.SonsBullet)
            Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, shooter_x, shooter_y,
                   en_joue[1], en_joue[2] + 150, self.caracBullet, self.SonsBullet)
            Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, shooter_x, shooter_y,
                   en_joue[1], en_joue[2] - 150, self.caracBullet, self.SonsBullet)
            self.rechargement = True
        else:
            self.frectir -= 1
            if self.frectir <= 0:
                self.frectir, self.rechargement = self.frectir_ini, False
            elif not self.rechargement and self.rotat != 0:
                A = self.canvas.bbox(self.ID_visual)
                self.se_potiononne(A, A)
                self.rotat = 0

    # positionne le cannon dans l'axe du tir
    def se_potiononne(self, A, B):
        try:
            rotat = -round(math.atan((B[1] - A[1]) / (B[0] - A[0])) * 57)  # A : la tourelle, B : la cible
        except ZeroDivisionError:
            rotat = 180
        if A[0] <= B[0] and self.couleur != 'blue':
            rotat += 180
        elif A[0] >= B[0] and self.couleur != 'red':
            rotat += 180
        if self.rotat != rotat:
            self.rotat = rotat
            self.changeImg(self.imageTourModele)

    def changeImg(self, img='normal'):
        if img == 'normal':
            img = self.imageTourModele
        self.imageTour = ImageTk.PhotoImage(img.rotate(angle=self.rotat, expand=True))
        self.canvas.itemconfigure(self.ID_visual, image=self.imageTour)

    # Perde de la vie
    def damage(self, damage):
        self.health -= damage
        if self.socle is True:
            self.canvas.delete(self.ID_health)
            coords = self.canvas.bbox(self.ID_socle)
            self.ID_health = self.canvas.create_rectangle(coords[0] + 25, coords[1] + 75,
                                                          (coords[0] + 25 + (coords[2] - coords[
                                                              0] - 50) * self.health / self.max_health),
                                                          coords[1] + 65, fill=self.couleur)
        if self.health <= self.max_health // 2 and not self.renfort and self.couleur != 'blue' and len(
                self.game.campB.all_base) > 0:
            # Envoi un boss en renfort
            self.renfort = True
            nomBase = []
            for nbBase in self.game.campB.all_base:
                nomBase += [nbBase]
            numbase = nomBase[random.randint(0, len(nomBase) - 1)]
            for base in self.game.campB.all_base:
                if base == numbase:
                    carac = base.dataImg.dic_boss[random.randint(1, len(base.dataImg.dic_boss))]
                    Boss(base.dataImg, base.dataMus, base.game, base.camp, base.canvas, abs(base.pos_x - 10),
                         base.pos_y, base.id_etage, carac)
                    break
        elif random.randint(0, 2) == 0:
            # Son des degats prit
            bruit = self.game.positionSons(self.ID_visual)
            self.dataMus.Bruit_Touche(self.bruitDamage, bruit[0], bruit[1])
        if self.health <= 0:
            self.remove()
        else:
            # Grisement de l'image
            self.changeImg(self.imageGris)
            self.canvas.after(200, self.changeImg)

    # Supprime la balle et son image peut mettre fin au jeu
    def remove(self):
        self.camp.all_tourelle.remove(self)
        if self.couleur != 'blue':
            self.game.campA.set_loot(self.nbPoint)
            if self.socle is True:
                coord = self.canvas.coords(self.ID_socle)
                for nbObjet in range(5, 11, 2):
                    carac = [None]
                    while carac[0] == None or carac[1] == 'Infini':
                        numOjet = random.randint(0, len(self.game.dataImg.dic_objet) - 1)
                        carac = self.game.dataImg.dic_objet[numOjet]
                    Item(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, coord[0], coord[1], carac,
                         nbObjet)
        if self.socle is True:
            self.canvas.delete(self.ID_max_health)
            self.canvas.delete(self.ID_health)
            self.canvas.delete(self.ID_socle)
            self.game.canvasMiniMap.delete(self.ID_tourelle_mini)
        self.camp.nbBase -= 1
        # Son de la mort
        bruit = self.game.positionSons(self.ID_visual)
        self.dataMus.Bruit_Touche(self.bruitDed, bruit[0], bruit[1])
        self.canvas.delete(self.ID_visual)


class Base(pygame.sprite.Sprite):
    def __init__(self, dataImg, dataMus, menu, game, camp, canvas, pos_x, pos_y, caracBase, id_etage, caracTour):
        super().__init__()
        # Recuperation des liens de connections et autres infos
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.menu = menu
        self.game = game
        self.camp = camp
        self.canvas = canvas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id_etage = id_etage

        # Recuperation des caracteristique : [imageBase, imgGris, health, nbpoint, biblioMob, imageMini, sonsBase]
        self.imgModele = caracBase[0]
        self.imgGris = caracBase[1]
        self.health = caracBase[2]
        self.nbPoint = caracBase[3]
        self.biblioMob = caracBase[4]
        self.imageMini = caracBase[5]

        # Recuperation des sons  :  damage, ded, heale
        self.bruitDamage = caracBase[6][0]
        self.bruitDed = caracBase[6][1]
        self.bruitHealth = caracBase[6][2]

        self.max_health = self.health
        self.couleur = self.camp.couleur
        self.dic_clas_Mob = self.dataImg.dic_mob_gentil if self.couleur == "blue" else self.dataImg.dic_mob_mechant

        pos_carte = self.canvas.bbox(self.game.ID_background)
        self.renfort1 = False
        self.renfort2 = False
        self.renfort3 = False

        # Creation image de la Base et ses PV
        self.imgVisual = ImageTk.PhotoImage(self.imgModele)
        self.ID_visual = self.canvas.create_image(self.pos_x, self.pos_y + 10, anchor='s', image=self.imgVisual)
        coords = self.canvas.bbox(self.ID_visual)
        self.ID_max_health = self.canvas.create_rectangle(coords[0] + 50, coords[1] + 175,
                                                          (coords[0] + 50 + (coords[2] - coords[
                                                              0] - 100) * self.health / self.max_health),
                                                          coords[1] + 165, fill="gray")
        self.ID_health = self.canvas.create_rectangle(coords[0] + 50, coords[1] + 175,
                                                      (coords[0] + 50 + (coords[2] - coords[
                                                          0] - 100) * self.health / self.max_health),
                                                      coords[1] + 165, fill=self.couleur)
        # point d'attache au sol, x = pos_x+demi longueur de l'image+marge du cadre y = coord_y[3]+6+marge du cadre
        self.ID_base_mini = self.game.canvasMiniMap.create_image(5 + abs(-10 + self.pos_x // 15.3),
                                                                 8 + coords[3] // 16.5, anchor='s',
                                                                 image=self.imageMini)

        self.all_tour = pygame.sprite.Group()
        depX = depY = 170
        for k in range(self.camp.nbBase):
            depX, depY = depX - 100, depY - 100
            self.all_tour.add(
                Tourelle(self.dataImg, self.dataMus, self.menu, self.game, self.camp, self.canvas, self.pos_x,
                         self.camp.pos_y + depY + pos_carte[1] + 660 * id_etage, k, caracTour))

    # Supprime la balle et son image peut mettre fin au jeu
    def remove(self):
        if self.couleur != 'blue':
            self.game.campA.set_loot(self.nbPoint)
            coord = self.canvas.bbox(self.ID_visual)
            for nbObjet in range(6, 11, 1):
                carac = [None]
                while carac[0] == None or carac[1] == 'Infini':
                    numOjet = random.randint(0, len(self.game.dataImg.dic_objet) - 1)
                    carac = self.game.dataImg.dic_objet[numOjet]
                Item(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, coord[2], coord[3] - 55,
                     carac, nbObjet)
        if self in self.camp.all_base:
            self.camp.all_base.remove(self)
        # Son de la mort
        bruit = self.game.positionSons(self.ID_visual)
        bruit[0][1] -= 50
        self.dataMus.Bruit_Touche(self.bruitDed, bruit[0], bruit[1])
        self.canvas.delete(self.ID_visual)
        self.canvas.delete(self.ID_max_health)
        self.canvas.delete(self.ID_health)
        self.game.canvasMiniMap.delete(self.ID_base_mini)
        for tour in self.all_tour:
            tour.remove()
        # Remove aussi les tourelles de la base
        self.camp.nbBase -= 1
        self.dataMus.MusiqueStart(self.dataMus.m[random.randint(0, len(self.dataMus.m) - 1)])

    def changeImg(self, img='normal'):
        if img == 'normal':
            img = self.imgModele
        self.imgVisual = ImageTk.PhotoImage(img)
        self.canvas.itemconfigure(self.ID_visual, image=self.imgVisual)

    def damage(self, damage):
        coords = self.canvas.bbox(self.ID_visual)
        if self.couleur != 'blue':
            self.game.campA.set_loot(1)
        self.health -= damage
        self.canvas.delete(self.ID_health)
        self.ID_health = self.canvas.create_rectangle(coords[0] + 50, coords[1] + 175,
                                                      (coords[0] + 50 + (coords[2] - coords[
                                                          0] - 100) * self.health / self.max_health),
                                                      coords[1] + 165, fill=self.couleur)

        if self.health <= self.max_health // 2 and not self.renfort1 and self.couleur != 'blue':
            # Envoi boss1 en renfort
            self.renfort1 = True
            nomBase = []
            for nbBase in self.game.campB.all_base:
                nomBase += [nbBase]
            numbase = nomBase[random.randint(0, len(nomBase) - 1)]
            for base in self.game.campB.all_base:
                if base == numbase:
                    carac = base.dataImg.dic_boss[random.randint(1, len(base.dataImg.dic_boss))]
                    Boss(base.dataImg, base.dataMus, base.game, base.camp, base.canvas, abs(base.pos_x - 10),
                         base.pos_y, base.id_etage, carac)
                    break
        elif self.health <= self.max_health // 4 and not self.renfort2 and self.couleur != 'blue':
            # Envoi boss1 en renfort
            self.renfort2 = True
            nomBase = []
            for nbBase in self.game.campB.all_base:
                nomBase += [nbBase]
            numbase = nomBase[random.randint(0, len(nomBase) - 1)]
            for base in self.game.campB.all_base:
                if base == numbase:
                    carac = base.dataImg.dic_boss[random.randint(1, len(base.dataImg.dic_boss))]
                    Boss(base.dataImg, base.dataMus, base.game, base.camp, base.canvas, abs(base.pos_x - 10),
                         base.pos_y, base.id_etage, carac)
                    break
        elif self.health <= self.max_health * 3 // 4 and not self.renfort3 and self.couleur != 'blue':
            # Envoi boss1 en renfort
            self.renfort3 = True
            nomBase = []
            for nbBase in self.game.campB.all_base:
                nomBase += [nbBase]
            numbase = nomBase[random.randint(0, len(nomBase) - 1)]
            for base in self.game.campB.all_base:
                if base == numbase:
                    carac = base.dataImg.dic_boss[random.randint(1, len(base.dataImg.dic_boss))]
                    Boss(base.dataImg, base.dataMus, base.game, base.camp, base.canvas, abs(base.pos_x - 10),
                         base.pos_y, base.id_etage, carac)
                    break
        elif random.randint(0, 2) == 0:
            # Son des degats prit
            bruit = self.game.positionSons(self.ID_visual)
            self.dataMus.Bruit_Touche(self.bruitDamage, bruit[0], bruit[1])
        if self.health <= 0:
            self.remove()
        else:
            # Grisement de l'image
            self.changeImg(self.imgGris)
            self.canvas.after(200, self.changeImg)

    def soinPlayer(self):
        coordBase = self.canvas.bbox(self.ID_visual)
        coordPlayer = self.canvas.bbox(self.camp.player.ID_visual)
        pointPlayer = self.canvas.coords(self.camp.player.ID_visual)
        if coordBase[2] + self.camp.player.x_velo > coordPlayer[0] and coordBase[3] >= pointPlayer[1] >= coordBase[1]:
            # Son des soins
            bruit = self.game.positionSons(self.ID_visual)
            bruit[0][1] -= 1000
            self.camp.player.damage(-self.game.campA.player.max_health // 1500, self.bruitHealth, bruit[0], bruit[1])


# Un player peut se depalcer sur les 4 axes, tirer, envoyer des troupes, changer d'arme ainsi que se prendre des degats et mettre fin a la partie
class Player(pygame.sprite.Sprite, Entity):
    def __init__(self, dataImg, dataMus, game, camp, canvas, pseudo, health, pos_x, pos_y, Cararc_Joueur):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)
        # Recuperation des liens de connections et autres infos
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.game = game
        self.camp = camp
        self.canvas = canvas
        self.pseudo = pseudo
        self.max_health = health
        self.pos_x = pos_x
        self.pos_y = pos_y

        # Recuperation des caracteristique : [x_velo, y_velo, listImagePlayer, deco, Bruitage]
        self.x_velo = Cararc_Joueur[0]
        self.y_velo = Cararc_Joueur[1]

        self.imgs_x = Cararc_Joueur[2]["x"]
        self.imgs_y = Cararc_Joueur[2]["y"]
        self.imgs_p = Cararc_Joueur[2]["Player_Place"]
        self.imgs_arme = Cararc_Joueur[2]["ArmeBras"]

        #self.imageSexeBase = Cararc_Joueur[2]######
        #self.imageSexeBasBase = Cararc_Joueur[3]#####

        # Recuperation des sons
        # move, damage, ded, envoyetroupe, jump, accroupie
        self.movePlayer = Cararc_Joueur[4][0]
        self.damagePlayer = Cararc_Joueur[4][1]
        self.dedPlayer = Cararc_Joueur[4][2]
        self.envoyeTroupePlayer = Cararc_Joueur[4][3]
        self.jumpPlayer = Cararc_Joueur[4][4]
        self.accroupiePlayer = Cararc_Joueur[4][5]

        # Sincronisation des touches
        self.game.windows.bind_all('<KeyRelease-' + self.game.config.allTouche['spawner1'] + '>', self.lancer_troupe)
        self.game.windows.bind_all('<KeyRelease-' + self.game.menu.config.allTouche['spawner2'] + '>',
                                   self.lancer_troupe)
        self.game.windows.bind_all('<Triple-KeyRelease-' + self.game.config.allTouche['down1'] + '>',
                                   lambda sens: self.change_etage(sens=1))
        self.game.windows.bind_all('<Triple-KeyRelease-' + self.game.config.allTouche['down2'] + '>',
                                   lambda sens: self.change_etage(sens=1))
        self.game.windows.bind_all('<MouseWheel>', self.changer_arme)
        self.game.windows.bind_all('<KeyRelease-' + self.game.config.allTouche['weapon1'] + '>',
                                   lambda lettre: self.changer_arme(lettre=self.game.config.allTouche['weapon1']))
        self.game.windows.bind_all('<KeyRelease-' + self.game.config.allTouche['weapon2'] + '>',
                                   lambda lettre: self.changer_arme(lettre=self.game.config.allTouche['weapon2']))

        # Creation des caracteristiques d'un joueur
        #self.imageSexeMode = self.imageSexeBase
        self.txt = self.game.txt
        self.couleur = self.camp.couleur
        self.health = int(self.max_health // 1.5)
        self.numEtage = round(self.pos_y / 660)
        self.retarder = -ceil(self.x_velo / 1.5)
        self.saute = False
        self.limite = 0
        self.deplacement_Y = False
        self.deplacement_YM = False
        self.estbas = False
        self.nesautepas = True
        self.y_decalPlayer = 0
        self.y_decalPlayerNew = 0
        self.x_decalPlayer = 0
        self.initChangeEtage = True
        self.camp.all_players.add(self)
        self.posHealthLeft, self.posHealthRight = 60, 250
        self.posHealthTop, self.posHealthFloor = 60, 75
        self.choixArme = self.game.choixArme

        # Variable annimation player
        self.dirLeft = False
        self.play = True
        self.run = False
        self.gravite = False

        # Gestion des munitions, des armes et objet d'arme
        self.dicoMunition = {
            'munition_Arme0': self.dataImg.dic_arme[self.choixArme[0]][0][3],
            'munition_Arme1': self.dataImg.dic_arme[self.choixArme[1]][0][3],
            'munition_Arme2': self.dataImg.dic_arme[self.choixArme[2]][0][3],
            'munition_Arme3': self.dataImg.dic_arme[self.choixArme[3]][0][3],
            'munition_Arme4': self.dataImg.dic_arme[self.choixArme[4]][0][3],
            'munition_Arme5': self.dataImg.dic_arme[self.choixArme[5]][0][3]}
        self.dicoMunitionMax = {
            'munition_Arme0': self.dataImg.dic_arme[self.choixArme[0]][0][3],
            'munition_Arme1': self.dataImg.dic_arme[self.choixArme[1]][0][3],
            'munition_Arme2': self.dataImg.dic_arme[self.choixArme[2]][0][3],
            'munition_Arme3': self.dataImg.dic_arme[self.choixArme[3]][0][3],
            'munition_Arme4': self.dataImg.dic_arme[self.choixArme[4]][0][3],
            'munition_Arme5': self.dataImg.dic_arme[self.choixArme[5]][0][3]}
        self.num_arme = 0
        carac = self.dataImg.dic_arme[self.choixArme[self.num_arme]]
        self.ID_munition = self.canvas.create_text(400, 65, text=str(self.dicoMunitionMax['munition_Arme0']),
                                                   font=self.txt.f30, fill=self.txt.c)
        self.logoArme = self.canvas.create_image(430, 40, image=carac[0][1])
        for k in range(1, 6):
            self.dataImg.dic_objet[k] = [eval('self.game.Arme' + str(k)),
                                         self.dicoMunitionMax['munition_Arme' + str(k)], 0, 0, k,
                                         dataMus.Bruit_Objet[k]]

        # Creation image du joueur et ses PV
        self.img = ImageTk.PhotoImage(self.imgs_x[1])
        self.ID_visual = self.canvas.create_image(self.pos_x, self.pos_y, anchor='s', image=self.img)
        self.ID_health = self.canvas.create_rectangle(self.posHealthLeft, self.posHealthFloor, (
                    self.posHealthLeft + self.posHealthRight * self.health / self.max_health), self.posHealthTop,
                                                      fill="green")
        self.ID_nbVie = self.canvas.create_text(185, 67, text=str(self.health) + '/' + str(self.max_health),
                                                font=self.txt.f15, fill=self.txt.c)
        # Creation de l'arme de base du joueur
        self.newArme(self.num_arme, self.pos_x, self.pos_y)

        coords = self.canvas.bbox(self.ID_visual)
        self.ID_player_mini = self.game.canvasMiniMap.create_image(4 + 1 + self.pos_x // 15.3, 10 + coords[3] // 16.5,
                                                                   anchor='s', image=self.dataImg.i['Payer'])
        self.chooseAnnimation()

    # Un joueur peut se prendre des degats et en distribuer.
    def damage(self, damage, sons=None, emmetteur=None, zone=None):
        if self.health + (-damage) > self.max_health:
            if self.health < self.max_health:
                damage = ((self.health + (-damage)) - self.max_health)
            else:
                return
        self.health -= damage
        self.canvas.delete(self.ID_health)
        co = self.canvas.coords(self.game.FrameMiniMap)
        Xdecal, Ydecal = abs(co[0] - 920), abs(co[1] - 15)
        self.ID_health = self.canvas.create_rectangle(self.posHealthLeft + Xdecal, self.posHealthFloor + Ydecal,
                                                      (
                                                                  self.posHealthLeft + Xdecal + self.posHealthRight * self.health / self.max_health),
                                                      Ydecal + self.posHealthTop, fill="green")
        self.canvas.itemconfigure(self.ID_nbVie, text=str(self.health) + '/' + str(self.max_health))
        self.canvas.tag_raise(self.ID_nbVie)
        if sons == None:
            # Son des degats
            bruit = self.game.positionSons(self.ID_visual)
            sons = self.damagePlayer
            emmetteur = bruit[0]
            zone = bruit[1]
        if sons != 0:
            self.dataMus.Bruit_Touche(sons, emmetteur, zone)
        if self.health <= 0:
            self.remove()

    # Supprime le joueur et son arme
    def remove(self):
        # Son du player qui meurt
        bruit = self.game.positionSons(self.ID_visual)
        self.dataMus.Bruit_Touche(self.dedPlayer, bruit[0], bruit[1])

        # Si le joueur peut encore resussiter
        if self.camp.nb_vie > 0:
            # Deconnection du player au jeu
            self.camp.all_players.remove(self)
            # Ajout un filtre gris sur l'encran principal, la mini map et la barre de soldat
            FiltreP1 = self.canvas.create_image(450 - self.x_decalPlayer, 300 - self.y_decalPlayer, image=self.dataImg.i['Filtre_Pause'])
            FiltreP2 = self.game.canvas_bar.create_image(450, 150, image=self.dataImg.i['Filtre_Pause'])
            # affiche une image de la mort
            coord = self.canvas.coords(self.ID_visual)
            crane = self.canvas.create_image(coord[0], self.numEtage*660-400, image=self.dataImg.i['DedPlayer'])
            # supprime tous les elements visuel lié au player
            self.canvas.delete(self.ID_health)
            self.canvas.delete(self.arme.ID_arme)
            self.canvas.delete(self.ID_munition)
            self.canvas.delete(self.logoArme)
            self.canvas.delete(self.ID_nbVie)
            # Met le player au premier plan, maj de l'ecran et temps d'attente
            self.canvas.tag_raise(self.ID_visual)
            # Deplace la minimap en dehors de l'ecran (reviens par defaut mais jsp pourquoi)
            self.canvas.move(self.game.FrameMiniMap, 1000, 1000)
            self.canvas.update()
            time.sleep(3)
            self.canvas.move(self.game.FrameMiniMap, -1000, -1000)
            # Suppression des filtres et image
            self.canvas.delete(crane)
            self.canvas.delete(FiltreP1)
            self.game.canvas_bar.delete(FiltreP2)
            self.canvas.delete(self.ID_visual)
            self.game.canvasMiniMap.delete(self.ID_player_mini)
            # Creation d'un nouveau player
            self.camp.resurection()
        else:
            # Fin du jeu
            self.camp.quit_game = True

    # Deplace les objets relatif a la fenetre du joueur
    def deplace_affichage(self, x, y):
        self.canvas.move(self.logoArme, x, y)
        self.canvas.move(self.ID_munition, x, y)
        self.canvas.move(self.ID_nbVie, x, y)
        self.canvas.move(self.ID_health, x, y)
        self.canvas.move(self.camp.ID_vie_restant, x, y)
        self.canvas.move(self.camp.ID_score, x, y)
        self.canvas.move(self.camp.ID_cadre, x, y)
        self.canvas.move(self.camp.ID_pseudo, x, y)
        self.canvas.move(self.camp.ID_stepHeal, x, y)
        self.canvas.move(self.game.ID_Pause.bouton, x, y)
        self.canvas.move(self.game.ID_Help.bouton, x, y)
        self.canvas.move(self.game.FrameMiniMap, x, y)




    def chooseAnnimation(self, dirLeft=False):
        if self.play:
            # Si saute
            if self.saute:
                self.animation(self.imgs_y, self.dirLeft)

            # Si gravitee
            elif self.gravite:
                self.animation(self.imgs_x, self.dirLeft)

            # Si marche
            elif self.run and not self.estbas:
                self.animation(self.imgs_x, self.dirLeft)

            # Si accroupie
            elif self.estbas and self.run:
                self.animation(self.imgs_y, self.dirLeft)

            # Si eccroupe ne cout pas et sens du corp different
            elif self.estbas and dirLeft != self.dirLeft:
                self.animation(self.imgs_y, self.dirLeft)

            # Player a l'arret
            elif not self.estbas:
                self.animation(self.imgs_p, self.dirLeft)

            self.canvas.after(200, self.chooseAnnimation, self.dirLeft)





        # Deplace le Player a Droite ou a Gauche en fonction de sa vitesse, si n'est pas a une extremitee deplace aussi la fenetre
    def move_x_Player(self):
        # PARAMETRAGE
        Val_Pos = Val_Colli = signe = Val_x_decP = pos_carte = coordinates = actionL = actionR = 0
        if keyboard.is_pressed(self.game.config.allTouche['left1']) or keyboard.is_pressed(
                self.game.config.allTouche['left2']):
            coordinates, pos_carte, actionL, base = self.canvas.bbox(self.ID_visual), self.canvas.bbox(
                self.game.ID_background), True, 'campA'
            signe, Val_Pos, Val_Colli, Val_x_decP = -1, pos_carte[0] < coordinates[0], self.collision_base(
                base), self.x_decalPlayer < 0
        if keyboard.is_pressed(self.game.config.allTouche['right1']) or keyboard.is_pressed(
                self.game.config.allTouche['right2']):
            coordinates, pos_carte, actionR, base = self.canvas.bbox(self.ID_visual), self.canvas.bbox(
                self.game.ID_background), True, 'campB'
            signe, Val_Pos, Val_Colli, Val_x_decP = 1, coordinates[2] < pos_carte[2] - 50, self.collision_base(
                base), self.x_decalPlayer > -4635
        # ACTION
        if Val_Pos and not Val_Colli and actionL != actionR:
            self.run = True
            self.canvas.move(self.ID_visual, signe * self.x_velo, 0)
            self.canvas.move(self.arme.ID_arme, signe * self.x_velo, 0)
            self.game.canvasMiniMap.move(self.ID_player_mini, signe * self.x_velo * 360 / 5580, 0)
            if pos_carte[0] + 450 <= coordinates[0] and pos_carte[2] - 450 >= coordinates[2] and Val_x_decP:
                # Deplace le canvas puis les images d'affichage
                self.canvas.scan_dragto(self.x_decalPlayer, self.y_decalPlayer, gain=1)
                self.x_decalPlayer = self.x_decalPlayer + int(self.x_velo) * -signe
                self.deplace_affichage(signe * self.x_velo, 0)

            coordJ = self.canvas.bbox(self.ID_visual)
            if self.estbas:
                bruit = self.game.positionSons(self.ID_visual)
                self.dataMus.Bruit_Touche(self.accroupiePlayer, bruit[0], bruit[1])
            elif self.platformisee() or (float(self.pos_y) <= coordJ[3] and not self.saute):
                bruit = self.game.positionSons(self.ID_visual)
                self.dataMus.Bruit_Touche(self.movePlayer, bruit[0], bruit[1])
        elif self.run == True:
            self.run = False

    # player s'accroupie si touche activee et se releve lorsque touche desactivee
    def down_downUp(self):
        # PARAMETRAGE
        if (keyboard.is_pressed(self.game.config.allTouche['down1']) or keyboard.is_pressed(self.game.config.allTouche['down2'])) and not self.estbas and not self.saute and self.nesautepas:
            self.estbas = True
            self.x_velo += self.retarder
            self.canvas.move(self.arme.ID_arme, 0, 20)
            if not self.dirLeft:
                self.img = ImageTk.PhotoImage(self.imgs_y[0])
            else:
                self.img = ImageTk.PhotoImage(ImageOps.mirror(self.imgs_y[0]))
            self.canvas.itemconfigure(self.ID_visual, image=self.img)



        elif self.estbas and not (keyboard.is_pressed(self.game.config.allTouche['down1']) or keyboard.is_pressed(self.game.config.allTouche['down2'])):
            self.estbas = False
            self.x_velo -= self.retarder
            self.canvas.move(self.arme.ID_arme, 0, -20)
            self.animation(self.imgs_y, self.dirLeft)




    # Deplace le player vers le haut
    def jump(self, event):
        touche = (keyboard.is_pressed(self.game.config.allTouche['up1']) or keyboard.is_pressed(
            self.game.config.allTouche['up2']))
        coordJ = self.canvas.bbox(self.ID_visual)
        if ((touche and self.saute) or (touche and coordJ[3] == self.pos_y) or (
                self.pos_y > coordJ[3] > self.pos_y - 100) or (touche and self.platformisee())) and not self.estbas:
            if coordJ[3] == self.pos_y or self.platformisee():
                self.saute = True
                self.nesautepas = False
                bruit = self.game.positionSons(self.ID_visual)
                self.dataMus.Bruit_Touche(self.jumpPlayer, bruit[0], bruit[1])
                self.limite = coordJ[3] - 200
            if self.saute:
                self.canvas.move(self.ID_visual, 0, -self.y_velo)
                self.canvas.move(self.arme.ID_arme, 0, -self.y_velo)
                self.game.canvasMiniMap.move(self.ID_player_mini, 0, -round(self.y_velo * 120 / 1980, 2))
                if coordJ[3] < self.limite:
                    self.saute = False
        else:
            self.saute = False

    def change_etage(self, event=False, sens=0):
        coordJ = self.canvas.bbox(self.ID_visual)
        # PARAMETRAGE
        teste1 = False
        if sens == -1:  # montee
            teste1 = (coordJ[3] <= (self.numEtage - 1) * 660 and self.numEtage > 1) or not self.initChangeEtage
            self.game.windows.unbind_all('<Triple-KeyRelease-' + self.game.config.allTouche['down1'] + '>')
            self.game.windows.unbind_all('<Triple-KeyRelease-' + self.game.config.allTouche['down2'] + '>')
        elif sens == 1:  # descente
            teste1 = self.numEtage < self.game.nbBase and (float(self.pos_y) == coordJ[3] or not self.initChangeEtage)
        # ACTION
        if teste1:
            if self.initChangeEtage:
                self.initChangeEtage = False
                self.pos_y += sens * 660
                self.y_decalPlayerNew += 660 * sens
            if (self.y_decalPlayer + self.y_velo * sens) * -sens < self.y_decalPlayerNew * sens:
                if sens == -1:
                    accelere = 2
                    self.game.canvasMiniMap.move(self.ID_player_mini, 0, round(sens * self.y_velo * 120 / 1980, 2))
                else:
                    accelere = 1
                self.deplacement_Y = True
                self.canvas.scan_dragto(self.x_decalPlayer, self.y_decalPlayer, gain=1)
                self.y_decalPlayer -= self.y_velo * sens * accelere
                self.deplace_affichage(0, sens * self.y_velo * accelere)
            elif (self.y_decalPlayer + self.y_velo * sens) * -sens >= self.y_decalPlayerNew * sens:
                self.deplacement_Y = False
                self.deplacement_YM = False
                self.numEtage += 1 * sens
                self.initChangeEtage = True
                self.game.windows.bind_all('<Triple-KeyRelease-' + self.game.config.allTouche['down1'] + '>',
                                           lambda sens: self.change_etage(sens=1))
                self.game.windows.bind_all('<Triple-KeyRelease-' + self.game.config.allTouche['down2'] + '>',
                                           lambda sens: self.change_etage(sens=1))

    def gravity(self):
        coordJ = self.canvas.bbox(self.ID_visual)
        if not self.platformisee() and float(self.pos_y) > coordJ[3] and not self.saute:
            self.canvas.move(self.ID_visual, 0, self.y_velo)
            self.canvas.move(self.arme.ID_arme, 0, self.y_velo)
            self.game.canvasMiniMap.move(self.ID_player_mini, 0, round(self.y_velo * 120 / 1980, 2))
            coordJ = self.canvas.bbox(self.ID_visual)
            deplacement = self.pos_y - coordJ[3]
            if coordJ[3] + self.y_velo > float(self.pos_y) > coordJ[3] - self.y_velo and deplacement != 0:
                self.canvas.move(self.ID_visual, 0, deplacement)
                self.canvas.move(self.arme.ID_arme, 0, deplacement)
                coordMJ = self.game.canvasMiniMap.coords(self.ID_player_mini)
                deplacementMJ = round(coordMJ[1], -1) - coordMJ[1]
                self.game.canvasMiniMap.move(self.ID_player_mini, 0, deplacementMJ)
        elif not self.saute and not self.nesautepas and self.initChangeEtage:
            self.nesautepas = True
        if (coordJ[3] <= (self.numEtage - 1) * 660 and self.numEtage > 1) or self.deplacement_YM:
            self.deplacement_YM = True
            self.canvas.move(self.ID_visual, 0, -self.y_velo)
            self.canvas.move(self.arme.ID_arme, 0, -self.y_velo)
            self.change_etage(False, -1)

    # Recherche si le joueur est sur une platforme
    def platformisee(self):
        for platforme in self.game.all_platforme:
            J = self.canvas.bbox(self.ID_visual)
            T = self.canvas.bbox(platforme.ID_platforme)
            y_veloJ = self.y_velo
            # Collision avec le socle
            if (T[1] - y_veloJ <= J[3] <= T[1] + y_veloJ) and (T[0] < J[0] < T[2] or T[0] < J[2] < T[2]):
                deplacement = T[1] - J[3]
                if T[1] != J[3] and not self.saute:
                    self.canvas.move(self.ID_visual, 0, deplacement)
                    self.canvas.move(self.arme.ID_arme, 0, deplacement)
                return True
        return False

    # Verifie que le joueur ne touche pas une base
    def collision_base(self, side):
        for base in eval('self.game.' + side + '.all_base'):
            J = self.canvas.bbox(self.ID_visual)
            B = self.canvas.bbox(base.ID_visual)
            x_veloJ = self.game.campA.player.x_velo
            # Collision avec la base
            if (B[1] <= J[1] <= B[3] or B[1] < J[3] <= B[3]) and (B[0] < J[0] < B[2] or B[0] < J[2] + x_veloJ < B[2]):
                deplacement = B[0] - J[2]
                if deplacement > 0:
                    self.canvas.move(self.ID_visual, deplacement, 0)
                    self.canvas.move(self.arme.ID_arme, deplacement, 0)
                return True
        return False

    def lancer_troupe(self, event):
        if self.camp.score >= 1000:
            bruit = self.game.positionSons(self.ID_visual)
            self.dataMus.Bruit_Touche(self.envoyeTroupePlayer, bruit[0], bruit[1])
            nbEnvoi = 0
            for num in range(len(self.camp.etape)):
                if self.camp.etape[num][2]:
                    self.game.canvas_bar.delete(self.camp.etape[num][1])
                    self.camp.etape[num][2] = False
                    nbEnvoi += 1
                    self.game.liste += [num]
            # Paie les troupes et les envoies
            self.camp.set_loot(-(self.camp.scoreMutilple[0] + nbEnvoi * self.camp.scoreMutilple[1]))
            self.camp.set_loot(0)

        # PARTIE ARME

    ###########ARME###########ARME###########ARME###########ARME###########ARME###########ARME###########ARME
    # Creation de l'arme demandé
    def newArme(self, numero, pos_x, pos_y):
        nom = self.choixArme[numero]
        carac = self.dataImg.dic_arme[nom]
        # self.arme = Arme(canvas, game, camp, pos_x, pos_y, velocity, freqTir, damage, imageArme, imageBalle)
        self.arme = Arme(self.dataImg, self.dataMus, self.canvas, self.game, self.camp, self, pos_x, pos_y - 50,
                         carac)
        self.canvas.itemconfig(self.logoArme, image=carac[0][1])

    # Diminu le nombre de balle de l'arme
    def enleveMunition(self, numero):
        nbMunition = 'munition_Arme' + str(numero)
        nom = self.choixArme[numero]
        # print(self.dicoMunition)
        if numero in [0, 1, 2, 3, 4, 5]:
            for nbArme, name in enumerate(self.choixArme):
                if nbArme != 0 and nom == name and self.dicoMunition[nbMunition] > 0 and self.dicoMunition[
                    nbMunition] != self.txt.indicMun[self.txt.l]:
                    self.dicoMunition[nbMunition] -= 1
                    self.canvas.itemconfigure(self.ID_munition, text=str(self.dicoMunition[nbMunition]) + "/"
                                                                     + str(self.dicoMunitionMax[nbMunition]))
                    return True
                elif self.dicoMunition[nbMunition] == self.txt.indicMun[self.txt.l]:
                    self.canvas.itemconfigure(self.ID_munition, text=str(self.dicoMunitionMax[nbMunition]))
                    return True
        return False

    # Change l'arme du joueur
    def changer_arme(self, event=None, lettre=None):
        if lettre == None:
            lettre = self.game.config.allTouche['weapon1']
        for maxArme in range(6):
            if maxArme == 0 or self.choixArme[self.num_arme] == None or self.choixArme[self.num_arme] == 'vide':
                try:
                    delta = event.delta
                except:
                    delta = 0
                if delta > 0 or lettre != self.game.config.allTouche['weapon1']:
                    if self.num_arme > 0:
                        self.num_arme -= 1
                    else:
                        self.num_arme = 5
                else:
                    if self.num_arme < 5:
                        self.num_arme += 1
                    else:
                        self.num_arme = 0
            else:
                break
        coords = self.canvas.coords(self.ID_visual)
        self.canvas.delete(self.arme.ID_arme)
        self.newArme(self.num_arme, coords[0], coords[1])
        self.rechercheArmePortee()

    # Regarde l'arme que porte le joueur pour afficher les munitions retantes ainsi que l'arme
    def rechercheArmePortee(self):
        numero = self.num_arme
        bnMunition = 'munition_Arme' + str(numero)
        for nbArme, name in enumerate(self.choixArme):
            if numero == nbArme and self.dicoMunition[bnMunition] != self.txt.indicMun[self.txt.l]:
                self.canvas.itemconfigure(self.ID_munition, text=str(self.dicoMunition[bnMunition]) + "/"
                                                                 + str(self.dicoMunitionMax[bnMunition]))
                return numero
            elif self.dicoMunition[bnMunition] == self.txt.indicMun[self.txt.l]:
                self.canvas.itemconfigure(self.ID_munition, text=self.dicoMunitionMax[bnMunition])
        return 0


class Arme():
    def __init__(self, dataImg, dataMus, canvas, game, camp, player, pos_x, pos_y, carac_Arme):
        # Recuperation des liens de connections et autres infos
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.canvas = canvas
        self.game = game
        self.camp = camp
        self.player = player
        self.pos_x = pos_x
        self.pos_y = pos_y

        # Recuperation des caracteristique : [freqTir, imageArme, imageArmeBras], [velocity, damage, imageBalle], [BruitArme], [BruitBalle]
        self.freqTir = carac_Arme[0][0]
        self.imageArmeModele0 = carac_Arme[0][2].convert("RGBA")

        # Recuperation des sons
        # [spawnArme, [spawnBalle, exploseBalle]]
        spawnArme = carac_Arme[2]

        self.caracBullet = carac_Arme[1]
        self.SonsBullet = carac_Arme[3]

        self.recharge = 0
        self.maintienTir = False
        self.game.windows.bind_all('<Button-1>', self.debutTir)
        self.game.windows.bind_all('<ButtonRelease-1>', self.finTir)

      #  self.imageCorpsModele0 = self.player.imageSexeMode
     #   self.imageCorpsModele1 = ImageOps.mirror(self.player.imageSexeMode)
      #  self.orienteCorp = self.imageCorpsModele0

        self.imageArmeModele1 = ImageOps.mirror(self.imageArmeModele0)
        self.rotat = 0
        self.imageArme = ImageTk.PhotoImage(self.imageArmeModele0)
        self.ID_arme = self.canvas.create_image(self.pos_x, self.pos_y, image=self.imageArme)

        try:
            # Son d'apparition de l'ame
            bruit = self.game.positionSons(self.ID_arme)
            self.dataMus.Bruit_Touche(spawnArme, bruit[0], bruit[1])
        except:
            pass

    # Debut de la salve de tir
    def debutTir(self, event):
        self.maintienTir = True

    # Fin de la salve de tir
    def finTir(self, event):
        self.maintienTir = False

    # Possiblilitee de tirer
    def rechargement(self):
        if self.recharge <= 0:
            # Vise
            self.se_potiononne()
            # ToR pour shooter
            touche = (self.maintienTir or keyboard.is_pressed(self.game.config.allTouche['shoot']))
            if touche:
                # Enleve une munition s'il y a puis tir et remonte l'arme
                if self.camp.player.enleveMunition(self.camp.player.num_arme):
                    self.shoot()
                    self.debutrecharge()
        else:
            # Recharge et abesse l'arme
            self.recharge -= 1
            self.imgRecharge()

    # deplace imgArme de 0 degre nord au curseur
    def imgRecharge(self):
        # Incremente le degré de rechargement
        self.rotat += self.decalRecharge
        # Rotation de l'arme
        self.imageArme = ImageTk.PhotoImage(self.image.rotate(angle=self.rotat, expand=True))
        self.canvas.itemconfigure(self.ID_arme, image=self.imageArme)

    # Deplace imgArem a 0 degre nord
    def debutrecharge(self):
        # Recuperation des coordonnées de la sourie et du player
        x_decalage, y_decalage = self.player.x_decalPlayer, self.player.y_decalPlayer
        coordArme = self.canvas.coords(self.ID_arme)
        coordmouse = [(self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()) - x_decalage,
                      self.canvas.winfo_pointery() - self.canvas.winfo_rooty() - y_decalage]

        # Calcule du degré de la sourie sur un cercle trigo
        try:
            decalage = -round(math.atan((coordmouse[1] - coordArme[1]) / (coordmouse[0] - coordArme[0])) * 57)
        except ZeroDivisionError:
            if coordArme[1] >= coordmouse[1]:
                decalage = -90
            else:
                decalage = 90

        # Sens de decalage de l'arme apres tir
        if coordArme[0] >= coordmouse[0]:
            self.image = self.imageArmeModele1
            self.rotat = -self.freqTir * 2 + decalage
        else:
            self.image = self.imageArmeModele0
            self.rotat = self.freqTir * 2 + decalage
        self.decalRecharge = 0

        # Rotation de l'arme
        self.imgRecharge()

        # Sens de rechargement de l'arme
        self.decalRecharge = round(self.freqTir * 2 / self.freqTir)
        if coordArme[0] <= coordmouse[0]:
            self.decalRecharge = -self.decalRecharge

    # Tire une balle
    def shoot(self):
        self.recharge = self.freqTir
        coords = self.canvas.coords(self.ID_arme)
        x_decalage, y_decalage = self.player.x_decalPlayer, self.player.y_decalPlayer
        pos_x_mouse = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx() - x_decalage
        pos_y_mouse = self.canvas.winfo_pointery() - self.canvas.winfo_rooty() - y_decalage
        Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, coords[0],
               coords[1], pos_x_mouse, pos_y_mouse, self.caracBullet, self.SonsBullet)

    # positionne le cannon dans l'axe du tir
    def se_potiononne(self):
        x_decalage, y_decalage = self.player.x_decalPlayer, self.player.y_decalPlayer
        coordArme = self.canvas.coords(self.ID_arme)
        coordmouse = [(self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()) - x_decalage,
                      self.canvas.winfo_pointery() - self.canvas.winfo_rooty() - y_decalage]
        self.canvas.update()
        if coordArme == []:
            coordArme = [0, 0]
        try:
            rotat = -round(math.atan(
                (coordmouse[1] - coordArme[1]) / (coordmouse[0] - coordArme[0])) * 57)  # A : la tourelle, B : la cible
        except ZeroDivisionError:
            if coordArme[1] >= coordmouse[1]:
                rotat = -90
            else:
                rotat = 90


        if coordArme[0] >= coordmouse[0]:
            image = self.imageArmeModele1
            self.player.dirLeft = True
        else:
            image = self.imageArmeModele0
            self.player.dirLeft = False
        if self.rotat != rotat:
            # Rotation de l'arme
            self.rotat = rotat
            self.imageArme = ImageTk.PhotoImage(image.rotate(angle=self.rotat, expand=True))
            self.canvas.itemconfigure(self.ID_arme, image=self.imageArme)
            # Rotation du joueur
           # self.newJoueurImage = ImageTk.PhotoImage(orienteCorp.rotate(angle=0, expand=True))
           # self.canvas.itemconfigure(self.player.ID_visual, image=self.newJoueurImage)
          #  self.orienteCorp = orienteCorp


# Un mob peut se deplacer, tirer, se faire tirer dessus et mourrir
class Mob(pygame.sprite.Sprite, Entity):
    def __init__(self, dataImg, dataMus, game, camp, canvas, pos_x, pos_y, id_etage, Carac_Mob, numMob="nul"):
        pygame.sprite.Sprite.__init__(self)
        Entity.__init__(self)
        # Recuperation des liens de connections et autres infos
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.game = game
        self.camp = camp
        self.canvas = canvas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id_etage = id_etage  # 0, 1 ou 2
        self.Carac_Mob = Carac_Mob

        self.camp.all_mob.add(self)

        #print(numMob)

        # Recuperation des caracteristique :
        #           [velocity, frectir, health, imageMobe, imgGris, x_min, x_max, y_min, y_max, ImageMini, nbPoint, pos_y],
        #           [velocityBballe, damage, imageBalle], [BruitArme], [BruitBalle]
        self.velocity = Carac_Mob[0][0]
        self.frectir = Carac_Mob[0][1]
        self.health = Carac_Mob[0][2]
        self.imgGris = Carac_Mob[0][4]
        self.x_min = Carac_Mob[0][5]
        self.x_max = Carac_Mob[0][6]
        self.y_min = Carac_Mob[0][7]
        self.y_max = Carac_Mob[0][8]
        self.ImageMini = Carac_Mob[0][9]
        self.nbPoint = Carac_Mob[0][10]
        self.pos_y += Carac_Mob[0][11]


        # annimation
        self.imgMove = Carac_Mob[0][3]["move"]
        self.imgDeath = Carac_Mob[0][3]["death"]
        self.imgReload = Carac_Mob[0][3]["reload"]
        self.dossier = self.imgMove
        self.imgModele = Carac_Mob[0][3]["move"][0]

        self.moved = True
        self.intervalle = 200
        self.play = True
        self.isDed = False
        self.countDed = 0

        # Recuperation des sons
        # [move, damage, ded], [spawnBalle, exploseBalle]
        self.bruitMove = Carac_Mob[2][0]
        self.bruitDamage = Carac_Mob[2][1]
        self.bruitDed = Carac_Mob[2][2]

        self.caracBullet = Carac_Mob[1]
        self.SonsBullet = Carac_Mob[3]

        # Creation des caracteristiques d'un mob
        self.couleur = self.camp.couleur
        self.rechargement = False
        self.max_health = self.health
        self.frectir_ini = self.frectir

        # Creation image du joueur et ses PV ainsi que son score
        self.img = ImageTk.PhotoImage(self.imgMove[0])
        self.ID_visual = self.canvas.create_image(self.pos_x + 50, self.pos_y, anchor='s', image=self.img)
        coords = self.canvas.bbox(self.ID_visual)
        self.ID_max_health = self.canvas.create_rectangle(coords[0], coords[1], (coords[0] + (coords[2] - coords[
            0]) * self.max_health / self.max_health), coords[1] - 5, fill="gray")
        self.ID_health = self.canvas.create_rectangle(coords[0], coords[1],
                                                      (coords[0] + (coords[2] - coords[
                                                          0]) * self.health / self.max_health), coords[1] - 5,
                                                      fill=self.couleur)
        # point d'attache au sol, x = pos_x+demi longueur de l'image+marge du cadre y = coord_y[3]+6+marge du cadre
        self.ID_mob_mini = self.game.canvasMiniMap.create_image(5 + abs(-10 + self.pos_x // 15.3),
                                                                9 + coords[3] // 16.5, anchor='s', image=self.ImageMini)
        self.chooseAnnimation()


    def chooseAnnimation(self):
        # Si est mort
        if self.isDed:
            self.animation(self.imgDeath, False)
            self.countDed += 1
            if len(self.imgDeath) == self.countDed:
                # Active l'animation de mort
                # Supprime definitivement le mob
                self.canvas.delete(self.ID_visual)
        # Si en mouvement
        elif self.moved:
            # Change l'image pendant le deplacement en fonction du sens
            self.animation(self.imgMove, False)
        # Si recharge
        elif self.rechargement:
            # Change l'image pendant le deplacement en fonction du sens
            self.animation(self.imgReload, False)
        # Activation du programe en boucle
        if len(self.imgDeath) != self.countDed:
            self.canvas.after(self.intervalle, self.chooseAnnimation)



    def remove(self):
        self.isDed = True
        # Chance de lacher un objet et ajout du score si est un enemie
        if self.couleur != 'blue':
            self.game.campA.set_loot(self.nbPoint)
            coord = self.canvas.bbox(self.ID_visual)
            pos_carte = self.canvas.bbox(self.game.ID_background)
            if random.randint(0, 3) == 0 and coord[2] < + pos_carte[2]:
                carac = [None]
                while carac[0] == None or carac[1] == 'Infini':
                    numOjet = random.randint(0, len(self.game.dataImg.dic_objet) - 1)
                    carac = self.game.dataImg.dic_objet[numOjet]
                Item(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, coord[2], coord[3], carac)
        # Son de la mort
        bruit = self.game.positionSons(self.ID_visual)
        self.dataMus.Bruit_Touche(self.bruitDed, bruit[0], bruit[1])
        # Supprime les infos et de vie du mob
        self.camp.all_mob.remove(self)
        self.canvas.delete(self.ID_max_health)
        self.canvas.delete(self.ID_health)
        self.game.canvasMiniMap.delete(self.ID_mob_mini)


    def se_deplace(self):
        coords = self.canvas.bbox(self.ID_visual)
        shooter_x = coords[0] + (coords[2] - coords[0]) / 2
        shooter_y = coords[1] + (coords[3] - coords[1]) / 2
        en_joue = self.game.ennemieDetection(self, 'mob', self.rechargement)
        # Le mob a le choit entre tirer, recharger et avancer
        if en_joue:
            self.moved = False
            if self.bruitMove != None:
                self.bruitMove[0].stop()
            Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, shooter_x, shooter_y,
                   en_joue[1], en_joue[2], self.caracBullet, self.SonsBullet)
            self.rechargement = True
        elif self.rechargement is False:
            self.canvas.move(self.ID_visual, self.velocity, 0)
            self.canvas.move(self.ID_max_health, self.velocity, 0)
            self.canvas.move(self.ID_health, self.velocity, 0)
            self.game.canvasMiniMap.move(self.ID_mob_mini, self.velocity / 15.5, 0)
            self.moved = True
            pos_carte = self.canvas.bbox(self.game.ID_background)
            # Son de deplacement
            if self.bruitMove != None:
                bruit = self.game.positionSons(self.ID_visual)
                self.dataMus.Bruit_Touche(self.bruitMove, bruit[0], bruit[1])
            if coords[0] > pos_carte[2] or coords[0] < pos_carte[0] - 50:
                id_etage = 0
                if self.id_etage == 0 and self.game.nbBase > 1:
                    id_etage = 1
                elif self.id_etage == 1 and self.game.nbBase == 3:
                    id_etage = 2
                pos_y = self.camp.pos_y + pos_carte[1] + 660 * id_etage
                # Fait disparaitre le mob et en crée un nouveau avec les memes caracteristique a l'etage du bas
                self.remove()
                Mob(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self.pos_x, pos_y, id_etage,
                    self.Carac_Mob)

        else:
            self.frectir -= 1
            if self.frectir <= 0:
                self.frectir, self.rechargement = self.frectir_ini, False

    def changeImg(self, img='normal'):
        if img == 'normal':
            img = self.imgModele
        self.imgVisual = ImageTk.PhotoImage(img)
        self.canvas.itemconfigure(self.ID_visual, image=self.imgVisual)

    def damage(self, damage):
        coords = self.canvas.bbox(self.ID_visual)
        self.health -= damage
        self.canvas.delete(self.ID_health)
        self.ID_health = self.canvas.create_rectangle(coords[0], coords[1], (
                coords[0] + (coords[2] - coords[0]) * self.health / self.max_health), coords[1] - 5, fill=self.couleur)
        if random.randint(0, 3) == 0:
            # Son des degats prit
            bruit = self.game.positionSons(self.ID_visual)
            self.dataMus.Bruit_Touche(self.bruitDamage, bruit[0], bruit[1])
        if self.health <= 0:
            # Le mob n'a plus de vie, il disparait
            self.remove()
        else:
            # Grisement de l'image
            self.changeImg(self.imgGris)
            self.canvas.after(200, self.changeImg)


class Boss(Mob):
    def __init__(self, dataImg, dataMus, game, camp, canvas, pos_x, pos_y, id_etage, Carac_Mob):
        super().__init__(dataImg, dataMus, game, camp, canvas, pos_x, pos_y, id_etage, Carac_Mob)
        dataMus.Bruit_Touche(Carac_Mob[2][3], "Menu", None)

    def remove(self):
        self.isDed = True
        # Chance de lacher un objet et ajout du score si est un enemie
        if self.couleur != 'blue':
            self.game.campA.set_loot(self.nbPoint)
            coord = self.canvas.bbox(self.ID_visual)
            pos_carte = self.canvas.bbox(self.game.ID_background)
            for nbObjet in range(6, 15, 2):
                carac = [None]
                while carac[0] == None or carac[1] == 'Infini':
                    numOjet = random.randint(0, len(self.game.dataImg.dic_objet) - 1)
                    carac = self.game.dataImg.dic_objet[numOjet]
                Item(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, coord[2], coord[3],
                     carac), nbObjet
        # Son de la mort
        bruit = self.game.positionSons(self.ID_visual)
        self.dataMus.Bruit_Touche(self.bruitDed, bruit[0], bruit[1])
        # Supprime le mob
        self.camp.all_mob.remove(self)
        self.canvas.delete(self.ID_max_health)
        self.canvas.delete(self.ID_health)
        self.game.canvasMiniMap.delete(self.ID_mob_mini)

    def se_deplace(self):
        coords = self.canvas.bbox(self.ID_visual)
        shooter_x = coords[0] + (coords[2] - coords[0]) / 2
        shooter_y = coords[1] + (coords[3] - coords[1]) / 2
        en_joue = self.game.ennemieDetection(self, 'mob', self.rechargement)
        # Le mob a le choit entre tirer, recharger et avancer
        if en_joue:
            self.moved = False
            if self.bruitMove != None:
                self.bruitMove[0].stop()
            Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, shooter_x + 100,
                   shooter_y, en_joue[1], en_joue[2], self.caracBullet, self.SonsBullet)
            Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, shooter_x - 100,
                   shooter_y, en_joue[1], en_joue[2], self.caracBullet, self.SonsBullet)
            Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, shooter_x,
                   shooter_y + 100, en_joue[1], en_joue[2], self.caracBullet, self.SonsBullet)
            Bullet(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self, shooter_x,
                   shooter_y - 100, en_joue[1], en_joue[2], self.caracBullet, self.SonsBullet)

            self.rechargement = True
        elif self.rechargement is False:
            self.moved = True
            self.canvas.move(self.ID_visual, self.velocity, 0)
            self.canvas.move(self.ID_max_health, self.velocity, 0)
            self.canvas.move(self.ID_health, self.velocity, 0)
            self.game.canvasMiniMap.move(self.ID_mob_mini, self.velocity / 15.5, 0)
            pos_carte = self.canvas.bbox(self.game.ID_background)
            # Son de deplacement
            if self.bruitMove != None:
                bruit = self.game.positionSons(self.ID_visual)
                self.dataMus.Bruit_Touche(self.bruitMove, bruit[0], bruit[1])
            if coords[0] > pos_carte[2] or coords[0] < pos_carte[0] - 50:
                id_etage = 0
                if self.id_etage == 0 and self.game.nbBase > 1:
                    id_etage = 1
                elif self.id_etage == 1 and self.game.nbBase == 3:
                    id_etage = 2
                pos_y = self.camp.pos_y + pos_carte[1] + 660 * id_etage
                # Fait disparaitre le mob et en crée un nouveau avec les memes caracteristique a l'etage du bas
                self.remove()
                Boss(self.dataImg, self.dataMus, self.game, self.camp, self.canvas, self.pos_x, pos_y, id_etage,
                     self.Carac_Mob)
        else:
            self.frectir -= 1
            if self.frectir <= 0:
                self.frectir, self.rechargement = self.frectir_ini, False


# Une balle peut se deplacer et peut faire des degat puis disparaitre
class Bullet(pygame.sprite.Sprite):
    def __init__(self, dataImg, dataMus, game, camp, canvas, tireur, shooter_x, shooter_y, cible_x, cible_y,
                 caracBullet, SonsBullet):
        super().__init__()
        # Recuperation des liens de connections et autres infos
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.game = game
        self.camp = camp
        self.canvas = canvas
        self.tireur = tireur
        self.shooter_x = shooter_x
        self.shooter_y = shooter_y
        self.cible_x = cible_x
        self.cible_y = cible_y

        self.camp.all_ball.add(self)

        # Recuperation des caracteristique : velocity, damage, imageBalle
        self.velocity = caracBullet[0]
        self.degat = caracBullet[1]
        self.imageBalleBase = caracBullet[2]

        # Recuperation des sons
        bruitSpawn = SonsBullet[0]
        self.bruiExplose = SonsBullet[1]

        # Creation des caracteristiques d'une balle
        self.touche = False
        self.couleur = self.camp.couleur

        if self.cible_x == self.shooter_x and self.cible_y == self.shooter_y:
            self.x_velo = 0
            self.y_velo = 1
        else:
            self.x_velo = (-(self.shooter_x - self.cible_x) / max(abs(-(self.shooter_x - self.cible_x)), abs(
                -(self.shooter_y - self.cible_y)))) * self.velocity
            self.y_velo = (-(self.shooter_y - self.cible_y) / max(abs(-(self.shooter_x - self.cible_x)), abs(
                -(self.shooter_y - self.cible_y)))) * self.velocity
        if self.x_velo > 0:
            self.imageBalle = ImageTk.PhotoImage(self.imageBalleBase)
        else:
            self.imageBalle = ImageTk.PhotoImage(self.imageBalleBase.rotate(180))

        # Creation image du joueur et ses PV ainsi que son score
        self.ID_visual = self.canvas.create_image(self.shooter_x, self.shooter_y, image=self.imageBalle)

        # Son d'apparition de la balle
        bruit = self.game.positionSons(self.ID_visual)
        self.dataMus.Bruit_Touche(bruitSpawn, bruit[0], bruit[1])

    def est_tiree(self):
        coords = self.canvas.coords(self.ID_visual)
        self.canvas.move(self.ID_visual, self.x_velo, self.y_velo)
        touched = self.game.ennemieDetection(self, 'bullet')
        if (coords[0] > (self.shooter_x + self.canvas.winfo_width()) or coords[0] < (
                self.shooter_x - self.canvas.winfo_width())) or (
                coords[1] > (self.shooter_y + self.canvas.winfo_height() / 2) or coords[1] < (
                self.shooter_y - 2 * self.canvas.winfo_height() / 2)) or touched:
            self.remove()

    # Supprime la balle et son image
    def remove(self):
        # Son d'explotion de la balle si roquette
        if self.bruiExplose != None:
            bruit = self.game.positionSons(self.ID_visual)
            self.dataMus.Bruit_Touche(self.bruiExplose, bruit[0], bruit[1])
        self.camp.all_ball.remove(self)
        self.canvas.delete(self.ID_visual)


class Platforme(pygame.sprite.Sprite):
    def __init__(self, game, camp, canvas, x_pos, y_pos, image):
        super().__init__()
        # Recuperation des informations
        self.game = game
        self.camp = camp
        self.canvas = canvas
        self.x_pos = abs(x_pos)
        self.y_pos = abs(y_pos)
        self.image = image
        # Creation image de la Platforme
        self.ID_platforme = self.canvas.create_image(self.x_pos + 50, self.y_pos, image=self.image)


class Item(pygame.sprite.Sprite):
    def __init__(self, dataImg, dataMus, game, camp, canvas, pos_x, pos_y, carac_Item, velo_x=5):
        super().__init__()
        # Recuperation des liens de connections et autres infos
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.game = game
        self.camp = camp
        self.canvas = canvas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velo_x = velo_x

        self.camp.all_item.add(self)

        # Recuperation des caracteristique : [image, effetmunition, effetsoin, effetmoney, numArme, sonsObjet]
        self.image = carac_Item[0]
        self.effetmunition = carac_Item[1]
        self.effetsoin = carac_Item[2]
        self.effetmoney = carac_Item[3]
        self.numArme = carac_Item[4]

        # Parametre de l'item
        self.statue = 'normal'
        self.hauteur = 'nonAtteind'
        self.velo_y = 4
        self.Dedtime = round(time.time() + 20)

        if self.pos_y < 660:
            self.sol = self.camp.pos_y
        elif self.pos_y > 1320:
            self.sol = 20 + self.camp.pos_y + 660 * 2
        else:
            self.sol = 20 + self.camp.pos_y + 660

        # Creation image de l'item
        self.ID_visual = self.canvas.create_image(self.pos_x, self.pos_y, image=self.image,
                                                  disabledimage=self.dataImg.i['H'
                                                                               'iddenItem'])

        # Recuperation des sons
        spawnItem = carac_Item[5][0]
        self.dedItem = carac_Item[5][1]
        self.eatItem = carac_Item[5][2]

        # Son sapawn objet
        bruit = self.game.positionSons(self.ID_visual)
        self.dataMus.Bruit_Touche(spawnItem, bruit[0], bruit[1])

    # Propultion de l'item à son spawn
    def jumping(self):
        if self.hauteur == 'nonAtteind':
            if self.canvas.bbox(self.ID_visual)[0] <= 100:
                self.velo_x = 0
            self.canvas.move(self.ID_visual, -self.velo_x, -self.velo_y)
            if self.canvas.bbox(self.ID_visual)[1] < self.sol - 250:
                self.hauteur = 'Atteind'
        else:
            self.gravity()

    # Redescent a la fin du saut
    def gravity(self):
        if self.canvas.bbox(self.ID_visual)[3] < self.sol:
            if self.canvas.bbox(self.ID_visual)[0] <= 100:
                self.velo_x = 0
            self.canvas.move(self.ID_visual, -self.velo_x // 2, self.velo_y)
        else:
            self.checkPlayer()

    # Verifie si le joueur touche l'item
    def checkPlayer(self):
        # clignote 3 seconde avant de disparaitre
        if round(time.time()) > self.Dedtime - 3 and self.statue == 'normal':
            self.statue = 'place'
            self.clignoter()
        P = self.canvas.bbox(self.game.campA.player.ID_visual)
        I = self.canvas.bbox(self.ID_visual)
        if P == None:
            P = [I[3], I[2], I[1], I[0]]
        if ((I[0] < P[0] < I[2] or I[0] < P[2] < I[2]) and (
                I[1] < P[1] < I[3] or I[1] < P[3] < I[3])) or (
                (P[0] < I[0] < P[2] or P[0] < I[2] < P[2]) and (
                P[1] < I[1] < P[3] or P[1] < I[3] < P[3])):
            self.regeneration()
        # Sinon il est l'heure de disparaitre
        elif round(time.time()) > self.Dedtime:
            self.remove(self.dedItem)

    # Previent qu'ik va bientot disparaitre
    def clignoter(self):
        if self.statue == 'place':
            self.statue = 'no_place'
            self.canvas.itemconfigure(self.ID_visual, state=DISABLED)
        else:
            self.statue = 'place'
            self.canvas.itemconfigure(self.ID_visual, state=NORMAL)
        if (round(time.time()) < self.Dedtime or self.game.pause) \
                and not self.game.campA.quit_game and not self.game.campB.quit_game:
            self.canvas.after(200, self.clignoter)

    # Appplique un des trois effet de l'item
    def regeneration(self):
        if self.effetsoin > 0:
            self.game.campA.player.damage(-self.effetsoin, sons=0)
        if self.effetmoney > 0:
            self.game.campA.set_loot(self.effetmoney)
        saisie = True
        if self.effetmunition > 0:
            if self.effetmunition == 99999:
                self.numArme = self.game.campA.player.rechercheArmePortee()
            saisie = self.rechercheNumArme()
        if saisie:
            self.game.campA.player.rechercheArmePortee()
            self.remove(self.eatItem)

        # Remet au max les minutions

    def rechercheNumArme(self):
        bnMunition = 'munition_Arme' + str(self.numArme)
        if self.game.campA.player.dicoMunitionMax[bnMunition] != self.game.campA.player.dicoMunition[bnMunition]:
            self.game.campA.player.dicoMunition[bnMunition] = self.game.campA.player.dicoMunitionMax[bnMunition]
            return True
        return False

    # Supprime l'item
    def remove(self, son):
        # Son sapawn objet
        bruit = self.game.positionSons(self.ID_visual)
        self.dataMus.Bruit_Touche(son, bruit[0], bruit[1])
        self.camp.all_item.remove(self)
        self.canvas.delete(self.ID_visual)


class Game:
    def __init__(self, windows, menu, canvas, canvas_bar, dataImg, dataMus, txt, config, ID_background, nbBase, nb_vie,
                 DollardDeBase, nbPv, choixArme, difficulteeIA, sexe, pseudo):
        # Recuperation des informations
        self.windows = windows
        self.menu = menu
        self.canvas = canvas
        self.canvas_bar = canvas_bar
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.txt = txt
        self.config = config
        self.ID_background = ID_background
        self.nbBase = nbBase
        self.nb_vie = nb_vie
        self.DollardDeBase = DollardDeBase
        self.nbPv = nbPv
        self.choixArme = choixArme
        self.difficulteeIA = difficulteeIA
        self.sexe = sexe
        self.pseudo = pseudo

        self.gamefinished = False
        # Trie les musique et demarre la premiere musique de jeu
        random.shuffle(self.dataMus.m)
        self.timeMus = 0
        self.numMus = 0
        self.reloadMus = round(time.time())

        # Creation de la mini map
        self.canvasMiniMap = Canvas(self.canvas, bg="grey", bd=0, highlightthickness=0, cursor="cross")
        self.FrameMiniMap = self.canvas.create_window(920, 15, anchor='ne', width=360 + 4 * 2, height=120 + 9,
                                                      window=self.canvasMiniMap)
        self.MiniCarte = self.canvasMiniMap.create_image(0, 0, anchor='nw', image=self.dataImg.i['Carte'])

        self.timeGame1 = time.strftime('%d %b %Y à %H:%M:%S ', time.localtime())

        # Duréé minimal d'une boucle de jeu
        self.refresh = 0.004

        self.config = self.menu.config

        # Creation des caracteristiques d'une game
        self.pos_carte = self.canvas.bbox(ID_background)
        self.all_platforme = pygame.sprite.Group()

        for k in range(1, 6):
            if self.choixArme[k] == None:
                self.choixArme[k] = 'vide'
        self.Arme1 = eval('self.dataImg.i["' + str(self.choixArme[1]) + '"]')
        self.Arme2 = eval('self.dataImg.i["' + str(self.choixArme[2]) + '"]')
        self.Arme3 = eval('self.dataImg.i["' + str(self.choixArme[3]) + '"]')
        self.Arme4 = eval('self.dataImg.i["' + str(self.choixArme[4]) + '"]')
        self.Arme5 = eval('self.dataImg.i["' + str(self.choixArme[5]) + '"]')

        # # Creation des deux camp d'une game
        # game, canvas, couleur, pos_x, pos_y, menu, windows, nbBase, nb_vie, dataImg, dataMus
        self.campA = Camp(self, canvas, 'blue', self.pos_carte[0] + 70, 510.0, self.menu, self.windows,
                          self.nbBase, nb_vie, self.dataImg, self.dataMus)
        self.campB = Camp(self, canvas, 'red', self.pos_carte[2] - 70, 510.0, self.menu, self.windows,
                          self.nbBase, nb_vie, self.dataImg, self.dataMus)

        # Partie pause et help et end
        self.pause = False
        self.windows.bind_all('<' + self.config.allTouche['pause'] + '>', self.jeu_Pause)
        self.windows.bind_all('<Escape>', self.jeu_Pause)
        self.windows.bind_all('<' + self.config.allTouche['help'] + '>', self.help)
        self.ID_Pause = imgButton(self, self.canvas, 50, 460, self.dataImg.i['Bouton_Pause'], None,
                                  lambda event: self.jeu_Pause())
        self.ID_Help = imgButton(self, self.canvas, 50, 505, self.dataImg.i['Bouton_Help'], None,
                                 lambda event: self.help())

        self.windows.bind_all('<Button-1>', self.campA.player.arme.debutTir)
        self.windows.bind_all('<ButtonRelease-1>', self.campA.player.arme.finTir)

        self.liste = []
        self.timeEnvoi = 0
        self.renvoi_interface()
        self.a = 1
        self.b = 1
        self.introduction()

    # Gere toutes les deplacement du jeu
    def update(self, canvas):
        if not self.pause:

            # Chargement de la musique
            if self.reloadMus == round(time.time()):
                self.dataMus.MusiqueStart(self.dataMus.m[self.numMus])
                self.timeMus = self.dataMus.m[self.numMus][2]
                self.reloadMus = round(time.time() + self.timeMus)
                self.numMus += 1
                if self.numMus == len(self.dataMus.m) - 1:
                    self.numMus = -1

            # Player se deplace a gauche ou/et a droite
            self.campA.player.move_x_Player()
            # Player s'accroupie
            self.campA.player.down_downUp()
            # Player saut
            self.campA.player.jump(False)
            # Player subie la gravitee
            self.campA.player.gravity()
            # Phase ou le joueur change d'etage
            if self.campA.player.deplacement_Y and not self.campA.player.deplacement_YM:
                self.campA.player.change_etage(False, 1)
            # Si je player maintient la sourie enfoncee

            # if self.maintienTir:
            #  self.campA.player.arme.shoot(False)
            self.campA.player.arme.rechargement()

            # Envoi des alliee a intervalle irregulier quand possible
            if len(self.liste) > 0:
                self.timeEnvoi -= 1
                if self.timeEnvoi < 0:
                    self.spawn_gentil(self.campA)
                    self.timeEnvoi = random.randint(200, 400)
            # Tente de faire apparaitre un ennemie
            self.spawner(self.campB)

            # Met en action tous les entitees cree du jeu
            for projectile in self.campA.all_ball:
                projectile.est_tiree()
            for projectile in self.campB.all_ball:
                projectile.est_tiree()
            for troupe in self.campA.all_mob:
                troupe.se_deplace()
            for troupe in self.campB.all_mob:
                troupe.se_deplace()
            for tourelle in self.campA.all_tourelle:
                tourelle.cherche_cible()
            for tourelle in self.campB.all_tourelle:
                tourelle.cherche_cible()
            for base in self.campA.all_base:
                base.soinPlayer()
            for item in self.campB.all_item:
                item.jumping()

        # actionne la fin du jeu
        if len(self.campB.all_tourelle) <= 0 and len(self.campB.all_mob) <= 0:
            self.campB.quit_game = True
        elif len(self.campA.all_tourelle) <= 0 and len(self.campA.all_mob) <= 0:
            self.campA.quit_game = True

        # Regarde si le jeu est fini
        if self.campA.quit_game or self.campB.quit_game:
            self.end()
        # Sinon rafraichie l'ecran de jeu
        else:
            # ralentir pour la visibilitee humaine

            time.sleep(self.refresh)
            self.canvas.update()
            # Le jeu n'est pas fini



    # Algorithme pour faire apparaitre un ennemie
    def spawner(self, campB):
        for base in campB.all_base:
            if random.randint(0, self.difficulteeIA) == 0:
                num = random.randint(0, len(self.dataImg.dic_mob_mechant) - 1)
                carac = base.dic_clas_Mob[num]
                Mob(base.dataImg, base.dataMus, base.game, base.camp, base.canvas, abs(base.pos_x - 10), base.pos_y,
                    base.id_etage, carac, "M-" + str(num))

    def spawn_gentil(self, campA):
        numMob = random.randint(0, len(self.liste) - 1)
        for base in campA.all_base:
            carac = base.dic_clas_Mob[self.liste[numMob]]
            Mob(base.dataImg, base.dataMus, base.game, base.camp, base.canvas, abs(base.pos_x - 10), base.pos_y,
                base.id_etage, carac, "G-" + str(self.liste[numMob]))
        del self.liste[numMob]
        if len(self.liste) > 31:
            numMob = random.randint(0, len(self.liste) - 1)
            for base in campA.all_base:
                carac = base.dic_clas_Mob[self.liste[numMob]]
                Mob(base.dataImg, base.dataMus, base.game, base.camp, base.canvas, abs(base.pos_x - 10), base.pos_y,
                    base.id_etage, carac)
            del self.liste[numMob]
        if random.randint(0, 1) == 0:
            self.renvoi_interface()

    def positionSons(self, emetteur):
        emetteur = self.canvas.coords(emetteur)
        zonePlayer = [float(-self.campA.player.x_decalPlayer), float(-self.campA.player.y_decalPlayer),
                      float(-self.campA.player.x_decalPlayer + self.canvas.winfo_width()),
                      float(-self.campA.player.y_decalPlayer + self.canvas.winfo_height())]
        return [emetteur, zonePlayer]

    # Remet au premier plan l'interface de l'utilisateur
    def renvoi_interface(self):
        self.canvas.tag_raise(self.campA.player.ID_visual)
        self.canvas.tag_raise(self.campA.player.arme.ID_arme)
        self.canvas.tag_raise(self.campA.player.logoArme)
        self.canvas.tag_raise(self.campA.player.ID_munition)
        self.canvas.tag_raise(self.campA.ID_vie_restant)
        self.canvas.tag_raise(self.campA.ID_score)
        self.canvas.tag_raise(self.campA.ID_cadre)
        self.canvas.tag_raise(self.campA.player.ID_health)
        self.canvas.tag_raise(self.campA.player.ID_nbVie)
        self.canvas.tag_raise(self.ID_Pause.bouton)
        self.canvas.tag_raise(self.ID_Help.bouton)
        self.canvasMiniMap.tag_raise(self.campA.player.ID_player_mini)

    # ennemieDetection(keeper='self', ID='ID_keeper', section='soldat', reload=False)
    def ennemieDetection(self, keeper, section, reloading=False):
        if not reloading:
            # Parametre secondaire de la fonction
            ob1 = keeper.canvas.bbox(keeper.ID_visual)
            actived, pos_x, pos_y = False, None, None
            opposingCamp = keeper.game.campB if keeper.couleur == 'blue' else keeper.game.campA
            search = ['mob', 'player']
            search = search + ['tour'] if section == 'mob' else (
                search + ['base', 'tour'] if section == 'bullet' else search)
            # Le but de cette fonction
            espece = [['player', self.campA.all_players], ['mob', opposingCamp.all_mob],
                      ['tour', opposingCamp.all_tourelle], ['base', opposingCamp.all_base]]
            for num, all_ in espece:
                if num in search and not actived:
                    if num == 'player' and keeper.couleur == "blue":
                        continue
                    for ele in all_:
                        ob2 = self.canvas.bbox(ele.ID_visual)
                        try:
                            x_min, x_max, y_min, y_max = keeper.x_min, keeper.x_max, keeper.y_min, keeper.y_max
                        except:
                            x_min, x_max, y_min, y_max = 0, 0, 0, 0
                        if (ob1[0] - x_min <= ob2[2] <= ob1[2] + x_max and ob1[1] - y_min <= ob2[1] <= ob1[
                            3] + y_max) or (
                                ob2[0] - x_min <= ob1[2] <= ob2[2] + x_max and ob2[1] - y_min <= ob1[1] <= ob2[
                            3] + y_max):
                            if section == 'bullet':
                                ele.damage(keeper.degat)
                            actived = True
                            pos_x = ob2[0] + (ob2[2] - ob2[0]) / 2
                            pos_y = ob2[1] + (ob2[3] - ob2[1]) / 2
                            break
            # End fonction
            if actived == True:
                return [actived, pos_x, pos_y]
        return False

    def reactive_touche(self):
        self.windows.bind_all('<' + self.config.allTouche['mus'] + '>', self.dataMus.StopMusique)
        self.windows.bind_all('<' + self.config.allTouche['bruit'] + '>', self.dataMus.Stop_Bruit)
        self.windows.bind_all('<' + self.config.allTouche['pause'] + '>', self.jeu_Pause)
        self.windows.bind_all('<' + self.config.allTouche['help'] + '>', self.help)

        self.windows.bind_all('<KeyRelease-' + self.config.allTouche['spawner1'] + '>', self.campA.player.lancer_troupe)
        self.windows.bind_all('<KeyRelease-' + self.menu.config.allTouche['spawner2'] + '>',
                              self.campA.player.lancer_troupe)
        self.windows.bind_all('<Triple-KeyRelease-' + self.config.allTouche['down1'] + '>',
                              lambda sens: self.campA.player.change_etage(sens=1))
        self.windows.bind_all('<Triple-KeyRelease-' + self.config.allTouche['down2'] + '>',
                              lambda sens: self.campA.player.change_etage(sens=1))
        self.windows.bind_all('<KeyRelease-' + self.config.allTouche['weapon1'] + '>',
                              lambda lettre: self.campA.player.changer_arme(lettre=self.config.allTouche['weapon1']))
        self.windows.bind_all('<KeyRelease-' + self.config.allTouche['weapon2'] + '>',
                              lambda lettre: self.campA.player.changer_arme(lettre=self.config.allTouche['weapon2']))
        self.windows.bind_all('<MouseWheel>', self.campA.player.changer_arme)

        self.windows.bind_all('<Button-1>', self.campA.player.arme.debutTir)
        self.windows.bind_all('<ButtonRelease-1>', self.campA.player.arme.finTir)

    # On regarde si le jeu n'est pas fini sinon on annime
    def desactive_touche(self):
        self.windows.unbind_all('<KeyRelease-' + self.config.allTouche['spawner1'] + '>')
        self.windows.unbind_all('<KeyRelease-' + self.config.allTouche['spawner2'] + '>')
        self.windows.unbind_all('<KeyRelease-' + self.config.allTouche['weapon1'] + '>')
        self.windows.unbind_all('<KeyRelease-' + self.config.allTouche['weapon2'] + '>')
        self.windows.unbind_all('<Triple-KeyRelease-' + self.config.allTouche['down1'] + '>')
        self.windows.unbind_all('<Triple-KeyRelease-' + self.config.allTouche['down2'] + '>')

        self.windows.unbind('<Button-1>')
        self.windows.unbind('<ButtonRelease-1>')
        self.windows.unbind_all('<MouseWheel>')

        self.windows.unbind_all('<' + self.config.allTouche['help'] + '>')
        self.windows.unbind_all('<' + self.config.allTouche['pause'] + '>')
        self.windows.unbind_all('<Escape>')

    def Reprise_Game(self, event=False):
        self.pause = False
        self.canvas.delete(self.Filtre_Pause1)
        self.canvas_bar.delete(self.Filtre_Pause2)
        self.canvasMiniMap.delete(self.Filtre_Pause3)
        self.canvas.delete(self.Logo_Pause.bouton)

        self.canvas_bar.delete(self.labIndication.bouton)
        self.canvas.delete(self.Button_Mp.bouton)
        try:
            self.config.removeTouche()

        except:
            pass
        try:
            self.canvas.delete(self.labIndic.bouton)
        except:
            pass
        self.windows.bind_all('<' + self.config.allTouche['pause'] + '>', self.jeu_Pause)
        self.windows.bind_all('<' + self.config.allTouche['help'] + '>', self.help)
        self.windows.bind_all('<Escape>', self.jeu_Pause)
        self.reactive_touche()

        for item in self.campB.all_item:
            item.Dedtime += (round(time.time()) - self.dureePause)

    def jeu_Pause(self, event=False):
        # Arret du jeu
        self.dureePause = round(time.time())
        self.pause = True
        self.campA.player.arme.maintienTir = False
        self.desactive_touche()
        self.windows.bind_all('<' + self.config.allTouche['pause'] + '>', self.Reprise_Game)
        self.windows.bind_all('<Escape>', self.Reprise_Game)

        co = self.canvas.coords(self.FrameMiniMap)
        Xdecal, Ydecal = abs(co[0] - 920), abs(co[1] - 15)

        self.Filtre_Pause1 = self.canvas.create_image(450 + Xdecal, 300 + Ydecal, image=self.dataImg.i['Filtre_Pause'])
        self.Filtre_Pause2 = self.canvas_bar.create_image(450, 150, image=self.dataImg.i['Filtre_Pause'])
        self.Filtre_Pause3 = self.canvasMiniMap.create_image(100, 100, image=self.dataImg.i['Filtre_Pause'])

        # Ajout des labels de pause
        self.Logo_Pause = imgButton(self.menu, self.canvas, 450 + Xdecal, 280 + Ydecal, self.dataImg.i['Pause_Logo'],
                                    None, lambda event: self.Reprise_Game())
        self.labIndication = imgButton(self.menu, self.canvas_bar, 450, 50, None, None,
                                       lambda event: self.Reprise_Game(), None, self.txt.play[self.txt.l], 25)
        self.Button_Mp = imgButton(self.menu, self.canvas, 175 + Xdecal, 30 + Ydecal, None, None,
                                   lambda event: self.exit(), None, self.txt.retMP[self.txt.l], 25)

        # Ajout du reglage du son lors de l'ajout de la musique
        self.config.reglage(self.canvas)

    def help(self, event=False):
        self.jeu_Pause()
        self.windows.bind_all('<' + self.config.allTouche['help'] + '>', self.Reprise_Game)
        self.canvas.delete(self.Logo_Pause.bouton)
        try:
            self.config.removeTouche()
        except:
            pass
        co = self.canvas.coords(self.FrameMiniMap)
        Xdecal, Ydecal = abs(co[0] - 920), abs(co[1] - 15)

        self.Logo_Pause = imgButton(self.menu, self.canvas, 150 + Xdecal, 330 + Ydecal, self.dataImg.i['Help_Logo'],
                                    None, lambda event: self.Reprise_Game())
        self.labIndic = imgButton(self.menu, self.canvas, 290 + Xdecal, 100 + Ydecal, None, None,
                                  lambda event: self.Reprise_Game(),
                                  'nw', self.txt.helpExplanation[self.txt.l], 22, 600)

    def end(self):
        self.jeu_Pause()
        self.canvas.delete(self.Logo_Pause.bouton)
        self.canvas_bar.delete(self.labIndication.bouton)
        self.canvas.delete(self.Button_Mp.bouton)
        try:
            self.config.removeTouche()
        except:
            pass
        if self.campB.quit_game and not self.gamefinished:

            self.timeGame2 = time.strftime('%d %b %Y à %H:%M:%S ', time.localtime())
            self.gamefinished = True
            self.decision = self.txt.win[self.txt.l]
            # Enregistre le nouveau score si c'est gagnee
            newScore = self.pseudo + " " + str(
                self.campA.totalScore) + " " + self.sexe + ' ' + self.menu.mission + " " + self.timeGame1 + ' ' + self.timeGame2 + ' ' + " ".join(
                self.choixArme)
            self.config.addScore(newScore)

        elif not self.gamefinished:
            self.decision = self.txt.lost[self.txt.l]
            self.timeGame2 = time.strftime('%d %b %Y à %H:%M:%S ', time.localtime())
            self.gamefinished = True

        co = self.canvas.coords(self.FrameMiniMap)
        Xdecal, Ydecal = abs(co[0] - 920), abs(co[1] - 15)
        self.Button_Mp = imgButton(self.menu, self.canvas, 445 + Xdecal, 200 + Ydecal, self.dataImg.i['Game_Over'],
                                   None, lambda event: self.exit())
        self.labIndic = imgButton(self.menu, self.canvas, 445 + Xdecal, 350 + Ydecal, None, None,
                                  lambda event: self.exit(), 'n',
                                  self.txt.end1[self.txt.l] + self.decision + "\n" + self.txt.end2[
                                      self.txt.l] + self.pseudo + ' : ' + str(self.campA.totalScore) + '\n' +
                                  self.txt.end3[self.txt.l] + self.timeGame1 + "\n" + self.txt.end4[
                                      self.txt.l] + self.timeGame2, 25, 600)

        self.desactive_touche()
        self.canvas.update()

    # Metre fin au jeu
    def exit(self, event=False):
        self.menu.running = False
        self.desactive_touche()
        pygame.mixer.stop()

    def skipIntro(self, event=False):
        self.skip = True

    def introduction(self):
        self.skip = False

        # Si on stop le jeu momentanement
        self.jeu_Pause()
        # Suppression des labels genant
        x = y = -2000
        try:
            self.config.removeTouche()
        except:
            pass
        self.canvas.move(self.Logo_Pause.bouton, x, y)
        self.canvas.move(self.Filtre_Pause1, x, y)
        self.canvas_bar.move(self.Filtre_Pause2, x, y)
        self.canvasMiniMap.move(self.Filtre_Pause3, x, y)
        self.canvas.move(self.Button_Mp.bouton, x, y)
        self.canvas_bar.move(self.labIndication, 0, -300)
        self.canvas_bar.itemconfig(self.labIndication.bouton, text=self.txt.spam[self.txt.l])
        self.windows.bind_all('<' + self.config.allTouche['spawner1'] + '>', self.skipIntro)
        decalage = 0
        self.canvas.update()
        self.desactive_touche()
        # Montre les bases ennemies
        self.label_indic_base = self.canvas.create_text(5315, 520, text=self.txt.indicbaseD[self.txt.l],
                                                        font=self.txt.f20, fill=self.txt.c)
        self.fleche = self.canvas.create_image(5315, 400, image=self.dataImg.i['Fleche_Droite'])
        for nbEtage in range(self.nbBase):
            self.canvas.scan_dragto(-465, decalage)
            self.canvas.update()
            decalage -= 70
            self.canvas.move(self.fleche, 0, 700)
            self.canvas.move(self.label_indic_base, 0, 700)
            for k in range(200):
                if self.skip:
                    break
                time.sleep(0.01)
        self.canvas.move(self.label_indic_base, -5080, -750)
        self.canvas.move(self.fleche, -5080, -750)
        # Montre les bases alliee
        self.canvas.itemconfig(self.label_indic_base, text=self.txt.indicbaseG[self.txt.l])
        self.canvas.itemconfig(self.fleche, image=self.dataImg.i['Fleche_Gauche'])
        decalage += 70
        for nbEtage in range(self.nbBase):
            self.canvas.scan_dragto(0, decalage)
            self.canvas.update()
            decalage += 70
            self.canvas.move(self.fleche, 0, -660)
            self.canvas.move(self.label_indic_base, 0, -660)
            for k in range(200):
                if self.skip:
                    break
                time.sleep(0.01)

        # Remet l'ecran a sa place en cas de probleme
        self.canvas.scan_dragto(0, 0)
        self.canvas_bar.move(self.labIndication, 450, 50)
        self.canvas_bar.itemconfig(self.labIndication.bouton, text=self.txt.play[self.txt.l])
        self.windows.unbind_all('<' + self.config.allTouche['spawner1'] + '>')
        self.windows.bind_all('<Button-1>', self.Reprise_Game)


class Menu:
    def __init__(self, windows: Tk) -> None:
        # Recuperation de arguments
        self.windows = windows

        # Chargement des resources
        self.loadPackage()

        # Parametres de l'objet
        self.running = False
        self.windows.protocol("WM_DELETE_WINDOW", self.quit_game)
        self.windows.bind_all('<' + self.config.allTouche['mus'] + '>', self.dataMus.StopMusique)
        self.windows.bind_all('<' + self.config.allTouche['bruit'] + '>', self.dataMus.Stop_Bruit)

        # Commencement dans le menu principal
        self.dataMus.MusiqueStart(self.dataMus.m[random.randint(0, len(self.dataMus.m) - 1)])
        self.menu_pricipal()

        # Pour les phases de test
        #self.jeuRapide()

    # Cherche a supprimer la frame precedante
    def delFrame(self) -> None:
        try:
            self.frame.destroy()
            self.windows.unbind('<Key>')
        except:
            pass

    # Affiche les elements de la frame et du canvas
    def watchCanvas(self) -> None:
        self.canvas.pack()
        self.frame.pack(expand=YES)

    # Chargement des images, musique et configuration
    def loadPackage(self) -> None:
        # Frame et canvas pour le chargement des données
        self.frame = Frame(self.windows, bg="#08081B", bd=0, relief=SUNKEN)
        self.canvas = Canvas(self.frame, width=930, height=660, bg="#0C0101", bd=0, highlightthickness=0,
                             cursor="cross")

        # Fond d'ecran de chargement
        img = PhotoImage(file="Image/T-Backgroung/loading.png")
        self.canvas.create_image(465, 330, image=img)

        # Barre de progression
        font = Font(family="Rockwell Nova Cond", weight="bold", size=15)
        self.label_Affichage = self.canvas.create_text(475, 610, text="0%", anchor='center', fill="white", font=font)
        self.bar = ttk.Progressbar(self.frame, orient=HORIZONTAL, length=500, mode='determinate', cursor='rtl_logo')
        self.bar.pack(pady=20)
        self.canvas.create_window(475, 640, anchor='center', window=self.bar)

        # Faire apparaitre les elements
        self.watchCanvas()
        self.canvas.update()

        # Etape de la Barre de progression
        etape = 64
        self.pourcentBar = 100 % etape
        self.bar['value'] += self.pourcentBar
        self.factorBar = 100 // etape

        # Chargement des ressources
        self.txt = Text(self)
        self.dataMus = MusiqueGame(self.windows, self)
        self.dataImg = ImageGame(self, self.dataMus)
        self.config = Config(self.windows, self, self.dataImg, self.dataMus, self.txt)

    # Augmente la barre de progression
    def upgradeProgressbar(self) -> None:
        self.pourcentBar += self.factorBar
        self.bar['value'] += self.factorBar
        self.canvas.itemconfig(self.label_Affichage, text=str(self.pourcentBar) + '%')
        self.canvas.update()

    def menu_pricipal(self, event: bool=False) -> None:
        self.delFrame()
        # Creation de la Frame et du canvas et ses parametres
        self.frame = Frame(self.windows, bg="#08081B", bd=0, relief=SUNKEN)
        self.canvas = Canvas(self.frame, width=930, height=660, bg="#0C0101", bd=0, highlightthickness=0,
                             cursor="cross")
        pos_bout = 380

        # Image et titre du jeu
        self.canvas.create_image(465, 330, image=self.dataImg.i['Commando_Menu_Principal'])
        self.canvas.create_image(465, 250, image=self.dataImg.i['BMP_Titre'])

        # Choix de la langue du jeu
        self.canvas.create_text(100, 610, text=self.txt.text[self.txt.l], font=self.txt.f20, fill=self.txt.c3, width=700)
        imgButton(self, self.canvas, 50, 640, self.dataImg.i['FlagAnglais'], self.dataImg.i['FlagAnglaisN'],
                  lambda event: self.txt.changeLangage('ang'))
        imgButton(self, self.canvas, 150, 640, self.dataImg.i['FlagFrancais'], self.dataImg.i['FlagFrancaisN'],
                  lambda event: self.txt.changeLangage('fr'))

        # Creation des boutons
        imgButton(self, self.canvas, 450, pos_bout, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.parametre_jeu(), textBT=self.txt.MP_box1[self.txt.l], font=self.txt.f22)
        imgButton(self, self.canvas, 450, pos_bout + 60 * 1, self.dataImg.i['B_vide'],
                  self.dataImg.i['B_vide_True'], lambda event: self.option(), textBT=self.txt.MP_box2[self.txt.l], font=self.txt.f22)
        imgButton(self, self.canvas, 450, pos_bout + 60 * 2, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.help(), textBT=self.txt.MP_box3[self.txt.l], font=self.txt.f22)
        imgButton(self, self.canvas, 450, pos_bout + 60 * 3, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.score(), textBT=self.txt.MP_box4[self.txt.l], font=self.txt.f22)
        imgButton(self, self.canvas, 450, pos_bout + 60 * 4, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.windows.destroy(), textBT=self.txt.MP_box5[self.txt.l], font=self.txt.f22)
        self.watchCanvas()

    def option(self, event: bool=False) -> None:
        self.delFrame()
        # Frame et canvas
        self.frame = Frame(self.windows, bg="#08081B", bd=0, relief=SUNKEN)
        self.canvas = Canvas(self.frame, width=930, height=660, bg="#0C0101", bd=0, highlightthickness=0,
                             cursor="cross")

        # Background, titre du jeu et bouton menu
        self.canvas.create_image(464, 330, image=self.dataImg.i['Commando_Menu_Principal'])
        self.canvas.create_text(450, 50, text=self.txt.optionTitle[self.txt.l], font=self.txt.f40, fill=self.txt.c4, width=700)
        imgButton(self, self.canvas, 465, 620, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.menu_pricipal(), textBT=self.txt.MP_box6[self.txt.l], font=self.txt.f22)

        # Apparition les elements de configuration
        self.config.reglage(self.canvas)
        self.watchCanvas()

    # Donne des indication au joueur
    def help(self, event: bool=False) -> None:
        self.delFrame()
        # Frame et canvas
        self.frame = Frame(self.windows, bg="#08081B", bd=0, relief=SUNKEN)
        self.canvas = Canvas(self.frame, width=930, height=660, bg="#0C0101", bd=0, highlightthickness=0,
                             cursor="cross")

        # Background, titre du jeu et bouton menu
        self.canvas.create_image(464, 330, image=self.dataImg.i['Commando_Menu_Principal'])
        self.canvas.create_text(500, 40, text=self.txt.helpTitle[self.txt.l], font=self.txt.f40, fill=self.txt.c4,
                                width=700)
        imgButton(self, self.canvas, 465, 620, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.menu_pricipal(), textBT=self.txt.MP_box6[self.txt.l], font=self.txt.f22)

        # label texte avec les explications
        self.canvas.create_image(464, 330, image=self.dataImg.i['Planche_aide'])
        self.canvas.create_text(464, 220, text=self.txt.H_b1[self.txt.l], font=self.txt.f25, fill=self.txt.c4, width=700)
        self.canvas.create_text(464, 370, text=self.txt.H_b2[self.txt.l], font=self.txt.f25, fill=self.txt.c4, width=700)
        self.canvas.create_text(464, 520, text=self.txt.H_b3[self.txt.l], font=self.txt.f25, fill=self.txt.c4, width=700)

      #  self.canvas.create_text(450, 350, text=self.txt.helpExplanation[self.txt.l], font=self.txt.f24, fill=self.txt.c,
       #                         anchor='center', width=500)
        self.watchCanvas()

    # Consulation des scores des precedants joueur
    def score(self) -> None:
        self.delFrame()
        # Frame et canvas
        self.frame = Frame(self.windows, bg="#08081B", bd=0, relief=SUNKEN)
        self.canvas = Canvas(self.frame, width=930, height=660, bg="#0C0101", bd=0, highlightthickness=0)

        # Background, titre du jeu et bouton menu
        self.canvas.create_image(464, 330, image=self.dataImg.i['Commando_Menu_Principal'])
        self.canvas.create_image(464, 365, image=self.dataImg.i['Plache_Scores'])
        self.canvas.create_text(450, 45, text=self.txt.scoreTitle[self.txt.l], font=self.txt.f40, fill=self.txt.c4,
                                anchor='center')
        imgButton(self, self.canvas, 465, 620, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.menu_pricipal(), textBT=self.txt.MP_box6[self.txt.l], font=self.txt.f22)

        # Affiche les scores
        self.config.Score()
        self.watchCanvas()

    # Le joueur choisie ses armes et son niveau
    def parametre_jeu(self, event: bool=False) -> None:
        self.delFrame()
        # Frame et canvas
        self.frame = Frame(self.windows, bg="#08081B", bd=0, relief=SUNKEN)
        self.canvas = Canvas(self.frame, width=930, height=660, bg="#0C0101", bd=0, highlightthickness=0, cursor="cross")

        # Fond d'ecran ainsi que bouton Menu et Jeu
        self.canvas.create_image(464, 331, image=self.dataImg.i['Bg_Parametre_Jeu'])
        imgButton(self, self.canvas, 465, 620, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.menu_pricipal(), textBT=self.txt.MP_box6[self.txt.l], font=self.txt.f22)
        imgButton(self, self.canvas, 740, 620, self.dataImg.i['B_vide'], self.dataImg.i['B_vide_True'],
                  lambda event: self.jeu(), textBT=self.txt.MP_box7[self.txt.l], font=self.txt.f22)

        # Label de l'ecran en fonction de la langue
        self.canvas.create_text(150, 50, text=self.txt.mMission[self.txt.l], font=self.txt.f25, fill=self.txt.c6, anchor='center')
        self.canvas.create_text(500, 50, text=self.txt.mArme[self.txt.l], font=self.txt.f25, fill=self.txt.c5, anchor='center')
        self.canvas.create_text(800, 50, text=self.txt.mInventaire[self.txt.l], font=self.txt.f25, fill=self.txt.c5, anchor='center')
        self.canvas.create_text(150, 100, text=self.txt.mM1[self.txt.l], font=self.txt.f17, fill=self.txt.c5, anchor='center')
        self.canvas.create_text(150, 280, text=self.txt.mM2[self.txt.l], font=self.txt.f17, fill=self.txt.c5, anchor='center')
        self.canvas.create_text(150, 465, text=self.txt.mM3[self.txt.l], font=self.txt.f17, fill=self.txt.c5, anchor='center')

        # Pour chaque arme du jeu, si c'est une arme a munition infini : met le texte dans la langue choisi
        for arme in self.dataImg.dic_arme:
            if self.dataImg.dic_arme[arme][0][3] in ['Infini', 'Loop'] and self.dataImg.dic_arme[arme][0][3] != \
                    self.txt.indicMun[self.txt.l]:
                self.dataImg.dic_arme[arme][0][3] = self.txt.indicMun[self.txt.l]

        # Choix niveau
        x = 61
        y1, y2, y3 = 185, 370, 555
        self.Choix, self.numEtage, self.IA = '1A', 1, 0
        self.Jeux_1A = imgButton(self, self.canvas, x * 1, y1, self.dataImg.i['M_Niveau_1'],
                                 self.dataImg.i['M_Niveau_1_True'],
                                 lambda numMission: self.select_mission(numMission="1A"))
        self.Jeux_1B = imgButton(self, self.canvas, x * 2, y1, self.dataImg.i['M_Niveau_1'],
                                 self.dataImg.i['M_Niveau_1_True'],
                                 lambda numMission: self.select_mission(numMission="1B"))
        self.Jeux_1C = imgButton(self, self.canvas, x * 3, y1, self.dataImg.i['M_Niveau_1'],
                                 self.dataImg.i['M_Niveau_1_True'],
                                 lambda numMission: self.select_mission(numMission="1C"))
        self.Jeux_1D = imgButton(self, self.canvas, x * 4, y1, self.dataImg.i['M_Niveau_1'],
                                 self.dataImg.i['M_Niveau_1_True'],
                                 lambda numMission: self.select_mission(numMission="1D"))
        self.Jeux_2A = imgButton(self, self.canvas, x * 1, y2, self.dataImg.i['M_Niveau_2'],
                                 self.dataImg.i['M_Niveau_2_True'],
                                 lambda numMission: self.select_mission(numMission="2A"))
        self.Jeux_2B = imgButton(self, self.canvas, x * 2, y2, self.dataImg.i['M_Niveau_2'],
                                 self.dataImg.i['M_Niveau_2_True'],
                                 lambda numMission: self.select_mission(numMission="2B"))
        self.Jeux_2C = imgButton(self, self.canvas, x * 3, y2, self.dataImg.i['M_Niveau_2'],
                                 self.dataImg.i['M_Niveau_2_True'],
                                 lambda numMission: self.select_mission(numMission="2C"))
        self.Jeux_2D = imgButton(self, self.canvas, x * 4, y2, self.dataImg.i['M_Niveau_2'],
                                 self.dataImg.i['M_Niveau_2_True'],
                                 lambda numMission: self.select_mission(numMission="2D"))
        self.Jeux_3A = imgButton(self, self.canvas, x * 1, y3, self.dataImg.i['M_Niveau_3'],
                                 self.dataImg.i['M_Niveau_3_True'],
                                 lambda numMission: self.select_mission(numMission="3A"))
        self.Jeux_3B = imgButton(self, self.canvas, x * 2, y3, self.dataImg.i['M_Niveau_3'],
                                 self.dataImg.i['M_Niveau_3_True'],
                                 lambda numMission: self.select_mission(numMission="3B"))
        self.Jeux_3C = imgButton(self, self.canvas, x * 3, y3, self.dataImg.i['M_Niveau_3'],
                                 self.dataImg.i['M_Niveau_3_True'],
                                 lambda numMission: self.select_mission(numMission="3C"))
        self.Jeux_3D = imgButton(self, self.canvas, x * 4, y3, self.dataImg.i['M_Niveau_3'],
                                 self.dataImg.i['M_Niveau_3_True'],
                                 lambda numMission: self.select_mission(numMission="3D"))
        self.select_mission(False, '1A')

        # Choix des armes
        self.catalog = []
        self.pos = [[790, 180], [770, 255], [790, 330], [770, 410], [770, 490]]
        self.choixArme = ["Barreti", None, None, None, None, None]
        self.armeChoisi = [[False, None, None], [False, None, None], [False, None, None], [False, None, None],
                           [False, None, None]]
        self.dataImg.i['vide'] = None  # Variable pour quand un des emplacements d'arme est vide

        # Arme de base
        self.Cercle_0 = self.canvas.create_image(765, 107, image=self.dataImg.i['BMP_Cercle_Sombre'])
        self.Arme0 = self.canvas.create_image(765, 107, image=self.dataImg.i['Barreti'])
        self.Alpha_Filtre = self.canvas.create_image(350, 95, image=self.dataImg.i['P_Alpha_Filtre'])

        # boutons des pages d'arme
        x, y, c = 350, 95, 40
        self.BoutonA = imgButton(self, self.canvas, x + c * 0, y, self.dataImg.i['P_A'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapA']))
        self.BoutonB = imgButton(self, self.canvas, x + c * 1, y, self.dataImg.i['P_B'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapB']))
        self.BoutonC = imgButton(self, self.canvas, x + c * 2, y, self.dataImg.i['P_C'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapC']))
        self.BoutonD = imgButton(self, self.canvas, x + c * 3, y, self.dataImg.i['P_D'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapD']))
        self.BoutonE = imgButton(self, self.canvas, x + c * 4, y, self.dataImg.i['P_E'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapE']))
        self.BoutonF = imgButton(self, self.canvas, x + c * 5, y, self.dataImg.i['P_F'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapF']))
        self.BoutonG = imgButton(self, self.canvas, x + c * 6, y, self.dataImg.i['P_G'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapG']))
        self.BoutonH = imgButton(self, self.canvas, x + c * 7, y, self.dataImg.i['P_H'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapH']))
        self.BoutonI = imgButton(self, self.canvas, x + c * 8, y, self.dataImg.i['P_I'], self.dataImg.i['P_select'],
                                 lambda weaps: self.page(weaps=self.dataImg.dic_page['weapI']))
        self.page(self.dataImg.dic_page['weapA'])
        self.watchCanvas()

        # Apparition du pop-up pour le choix du sexe et du pseudo
        self.sexe = ""
        self.pseudo = ""
        self.filtre = self.canvas.create_image(450, 350, image=self.dataImg.i['Filtre_Pause'])
        PopUp(self.windows, self, self.dataImg, self.dataMus, self.txt)

    # Player a choisie une mission
    def select_mission(self, event: bool=False, numMission: str='') -> None:
        # Efface la derniere mission selectionnee
        btn, img = eval('self.Jeux_' + self.Choix + ".bouton"), eval(
            'self.dataImg.i["M_Niveau_' + str(self.numEtage) + '"]')
        self.canvas.itemconfig(btn, image=img)

        # Affiche la nouvelle mission
        self.Choix, self.numEtage, self.IA = numMission, int(numMission[0]), ord(numMission[1]) - ord("A")
        btn = eval('self.Jeux_' + numMission + ".bouton")
        self.canvas.itemconfig(btn, image=self.dataImg.i['M_Niveau_Select'])

        #  Configure la mission
        self.background = self.dataImg.i['Carte1new']
        self.nb_vie = 1 * self.numEtage
        self.nbBase = 1 * self.numEtage
        self.difficulteeIA = 300 - 50 * self.IA
        self.DollardDeBase = 3750 + 250 * self.IA
        self.nbPv = 1000 * self.numEtage
        self.mission = numMission

    # Afficher une nouvelle page d'arme
    def page(self, weaps: list) -> None:
        self.nettoye_page()
        x, y, xc, yc = 345, 160, 110, 80
        self.Alpha_Filtre = self.canvas.create_image(weaps[5][0], weaps[5][1], image=self.dataImg.i['P_Alpha_Filtre'])

        weap = []
        for arme in weaps:
            if arme is not None and type(arme) != type([]):
                weap += [[self.dataImg.i[arme], self.dataImg.i[arme + '_Sombre'], arme,
                          arme + '\n\n' + self.txt.nomMun[self.txt.l] +
                          str(self.dataImg.dic_arme[arme][0][3])]]
            else:
                weap += [[None], [None], [None]]

        if weap[0][0] != None:
            self.catalog += [[imgButton(self, self.canvas, x, y + yc * 0, weap[0][0], weap[0][1],
                                        lambda arme: self.ajout_arme(arme=weap[0][2]), 'w'),
                              self.canvas.create_text(x + xc * 3, y + yc * 0, anchor='e', justify='right',
                                                      text=weap[0][3], font=self.txt.f13, fill=self.txt.c4)]]
        if weap[1][0] != None:
            self.catalog += [[imgButton(self, self.canvas, x, y + yc * 1, weap[1][0], weap[1][1],
                                        lambda arme: self.ajout_arme(arme=weap[1][2]), 'w'),
                              self.canvas.create_text(x + xc * 3, y + yc * 1, anchor='e', justify='right',
                                                      text=weap[1][3], font=self.txt.f13, fill=self.txt.c4)]]
        if weap[2][0] != None:
            self.catalog += [[imgButton(self, self.canvas, x, y + yc * 2, weap[2][0], weap[2][1],
                                        lambda arme: self.ajout_arme(arme=weap[2][2]), 'w'),
                              self.canvas.create_text(x + xc * 3, y + yc * 2, anchor='e', justify='right',
                                                      text=weap[2][3], font=self.txt.f13, fill=self.txt.c4)]]
        if weap[3][0] != None:
            self.catalog += [[imgButton(self, self.canvas, x, y + yc * 3, weap[3][0], weap[3][1],
                                        lambda arme: self.ajout_arme(arme=weap[3][2]), 'w'),
                              self.canvas.create_text(x + xc * 3, y + yc * 3, anchor='e', justify='right',
                                                      text=weap[3][3], font=self.txt.f13, fill=self.txt.c4)]]
        if weap[4][0] != None:
            self.catalog += [[imgButton(self, self.canvas, x, y + yc * 4, weap[4][0], weap[4][1],
                                        lambda arme: self.ajout_arme(arme=weap[4][2]), 'w'),
                              self.canvas.create_text(x + xc * 3, y + yc * 4, anchor='e', justify='right',
                                                      text=weap[4][3], font=self.txt.f13, fill=self.txt.c4)]]

    # Supprimer la page d'arme precedante
    def nettoye_page(self) -> None:
        self.canvas.delete(self.Alpha_Filtre)
        for img, text in self.catalog:
            self.canvas.delete(img.bouton)
            self.canvas.delete(text)
        self.catalog = []

    # Une arme a ete selectionnee
    def ajout_arme(self, event: bool=False, arme: str='') -> None:
        num, x, y = None, None, None
        for ele in range(len(self.armeChoisi)):
            if not self.armeChoisi[ele][0] and arme not in self.choixArme:
                num, x, y = ele, self.pos[ele][0], self.pos[ele][1]
                break
        if num != None:
            img1, img2 = eval('self.dataImg.i["' + arme + '"]'), eval('self.dataImg.i["' + arme + '_Sombre"]')
            self.armeChoisi[num][0], self.choixArme[num + 1] = True, arme
            self.armeChoisi[num][1] = self.canvas.create_image(x, y, image=self.dataImg.i['BMP_Cercle_Sombre'])
            self.armeChoisi[num][2] = imgButton(self, self.canvas, x, y, img1, img2,
                                                lambda eleveArme: self.envele_arme(eleveArme=arme))

    # Le joueur ne veut plus d'une des armes qu'il a choisi
    def envele_arme(self, event: bool=False, eleveArme: str='') -> None:
        for k in range(len(self.armeChoisi)):
            if self.armeChoisi[k][0] and eleveArme in self.choixArme[k + 1]:
                self.canvas.delete(self.armeChoisi[k][1])
                self.canvas.delete(self.armeChoisi[k][2].bouton)
                self.choixArme[k + 1] = None
                self.armeChoisi[k][0], self.armeChoisi[k][1], self.armeChoisi[k][2] = False, None, None
                break

    # Pour le phases de test
    def jeuRapide(self) -> None:
        self.background = self.dataImg.i['Carte1new']
        self.nb_vie, self.nbBase, self.DollardDeBase, self.nbPv = 5, 1, 10000, 5000
        self.difficulteeIA, self.mission = 300, 'test'
        self.choixArme = ['Barreti', 'Pequeno_R25', 'MK_150', 'TI_Prescision', 'P25_Maisto', 'Dragon_Destructor']
        self.pseudo, self.sexe = "Admin", "M"
        self.jeu()

    # Cretion d'une partie
    def jeu(self, event: bool=False) -> None:
        self.delFrame()
        # Frame et canvas
        self.frame = Frame(windows, bg="#0C0101", bd=0, relief=SUNKEN)
        self.canvas = Canvas(self.frame, width=930, height=550, bg="#0C0101", bd=0, highlightthickness=0,
                             cursor="cross")
        self.canvas_bar = Canvas(self.frame, width=930, height=110, bg="grey", bd=0, highlightthickness=0,
                                 cursor="cross")

        # Background
        self.ID_Bar = self.canvas_bar.create_image(460, 55, image=self.dataImg.i['Canvasbar'])
        self.ID_background = self.canvas.create_image(2790, 1000, image=self.background)
        self.watchCanvas()
        self.canvas_bar.pack()

        # Debut du jeu avec tout les parametre chosit
        self.game = Game(self.windows, self, self.canvas, self.canvas_bar, self.dataImg, self.dataMus, self.txt,
                         self.config,
                         self.ID_background, self.nbBase, self.nb_vie, self.DollardDeBase, self.nbPv, self.choixArme,
                         self.difficulteeIA, self.sexe, self.pseudo)

        # Tand que sa tourne, le jeu continue
        self.running = True
        self.end = False
        while self.running:
            self.game.update(self.game.canvas)
        if self.end:
            self.quit_game()
        else:
            self.dataMus.MusiqueStart(self.dataMus.m[random.randint(0, len(self.dataMus.m) - 1)])
            self.menu_pricipal()

    # Fermeture de la fenetre
    def quit_game(self) -> None:
        if self.running is True:
            self.running = False
            self.end = True
        else:
            print('FIN REUSSIE', self.running)
            pygame.quit()
            self.windows.destroy()


class PopUp:
    def __init__(self, window: Tk, menu: Menu, dataImg: ImageGame, dataMus: MusiqueGame, txt: Text) -> None:
        # Recuperation des arguments
        self.window = window
        self.menu = menu
        self.dataImg = dataImg
        self.dataMus = dataMus
        self.txt = txt

        # Creation de la fenetre et ses parametres
        self.notName = ['Dieu', 'Dieux', 'Admin', 'Admins', 'Administrator', 'Master', 'God', '.', '!']
        self.popUp = Toplevel(self.window)
        self.popUp.title("Commando Assaut - Pop-up")
        self.popUp.config(background="#4065A4")
        self.popUp.resizable(width=False, height=False)
        width = 400
        height = 280
        posX = self.popUp.winfo_screenwidth()
        posY = self.popUp.winfo_screenheight()
        self.popUp.geometry("%dx%d+%d+%d" % (width, height, (posX - width) / 2, (posY - height) / 2))
        self.popUp.protocol("WM_DELETE_WINDOW", self.canceled)
        self.menu.windows.bind_all('<Return>', self.confirmed)

        # Frame, canvas et fond d'ecran
        self.frame = Frame(self.popUp, bg="#08081B", bd=0, relief=SUNKEN)
        self.canvas = Canvas(self.frame, width=400, height=280, bg="#0C0101", bd=0, highlightthickness=0,
                             cursor="cross")
        self.ID_background = self.canvas.create_image(0, 0, image=self.dataImg.i['PopUp'])

        # Les textes
        self.labeTitre = self.canvas.create_text(200, 20, text=self.txt.txtPopTitre[self.txt.l], font=txt.f20,
                                                 fill=self.txt.c4, anchor='center')
        self.labelNom = self.canvas.create_text(75, 170, text=self.txt.txtPopT1[self.txt.l], font=txt.f20,
                                                fill=self.txt.c4, anchor='center', width=300)
        self.labelError = self.canvas.create_text(200, 205, text="", font=txt.f20, fill=self.txt.c4, anchor='center')

        # Les boutons
        self.buttonH = imgButton(self, self.canvas, 150, 95, self.dataImg.i['LogoM0'], None, lambda event: self.homm(), 'c')
        self.buttonF = imgButton(self, self.canvas, 250, 95, self.dataImg.i['LogoF0'], None, lambda event: self.femm(), 'c')


        self.cancel = imgButton(self, self.canvas, 120, 240, self.dataImg.i['B_vide_mini'], self.dataImg.i['B_vide_mini_True'],
                                lambda event: self.canceled(), 'c')
        self.cancel_txt = self.canvas.create_text(130, 240, font=self.txt.f17, fill=self.txt.c3,
                                                     state='disabled', anchor='center', text=self.menu.txt.txtCancel[self.txt.l])
        self.confirm = imgButton(self, self.canvas, 290, 240, self.dataImg.i['B_vide_mini'], self.dataImg.i['B_vide_mini_True'],
                                 lambda event: self.confirmed(), 'c')
        self.confirm_txt = self.canvas.create_text(300, 240, font=self.txt.f17, fill=self.txt.c3,
                                                     state='disabled', anchor='center', text=self.menu.txt.txtConfirm[self.txt.l])


        # La boite de saisie
        self.entry = Entry(self.popUp, font=txt.f15, bg=self.txt.c2, insertwidth=3, insertbackground='white',
                           fg="White", bd=5, relief=SUNKEN, exportselection=0)
        self.sousWindow = self.canvas.create_window(225, 170, anchor='center', window=self.entry)
        self.entry.focus_set()

        # Faire apparaitre les elements
        self.canvas.pack()
        self.frame.pack(expand=YES)

        # Choix sexe preselectionne
        self.homm()

        # Freeze l'ecran de jeu
        self.popUp.transient(self.window)
        self.popUp.grab_set()
        self.window.wait_window(self.popUp)

    # Si player selectionne l'homme
    def homm(self) -> None:
        if self.menu.sexe == 'F':
            self.canvas.itemconfig(self.buttonF.bouton, image=self.dataImg.i['LogoF0'])
        self.menu.sexe = 'M'
        self.canvas.itemconfig(self.buttonH.bouton, image=self.dataImg.i['LogoM1'])

    # Si player selectionne la femme
    def femm(self) -> None:
        if self.menu.sexe == 'M':
            self.canvas.itemconfig(self.buttonH.bouton, image=self.dataImg.i['LogoM0'])
        self.menu.sexe = 'F'
        self.canvas.itemconfig(self.buttonF.bouton, image=self.dataImg.i['LogoF1'])

    # Pour revenir au menu principal
    def canceled(self, event: bool=True) -> None:
        self.popUp.destroy()
        self.menu.menu_pricipal()

    # Verification du nom et du sexe et fin du popUp
    def confirmed(self, event: bool=None) -> None:
        self.menu.pseudo = self.entry.get()
        if not self.menu.pseudo.isascii() or len(self.menu.pseudo) <= 0:
            self.canvas.itemconfig(self.labelError, text=self.txt.texPop1[self.txt.l])
            return
        self.menu.pseudo = list(self.menu.pseudo.lower())
        self.menu.pseudo[0] = self.menu.pseudo[0].upper()
        self.menu.pseudo = "".join(self.menu.pseudo)
        if len(self.menu.pseudo) > 20:
            self.canvas.itemconfig(self.labelError, text=self.txt.texPop2[self.txt.l])
            return
        elif self.menu.pseudo in self.notName:
            self.canvas.itemconfig(self.labelError, text=self.txt.texPop3[self.txt.l])
            return
        self.menu.windows.unbind_all('<Return>')
        self.menu.canvas.delete(self.menu.filtre)
        self.popUp.destroy()


class imgButton:
    def __init__(self, menu: Menu, canvas: tkinter.Canvas, x: int, y: int, image: tkinter.PhotoImage, activeimage: tkinter.PhotoImage,
                 function: function, anchor: str=None, text: str=None, font: Font or int=15, width: int=None, textBT: str="", fill: str="#85201C") -> None:
        # Image-Bouton
        if text == None:
            self.bouton = canvas.create_image(x, y, image=image, activeimage=activeimage, anchor=anchor)
            canvas.create_text(x, y, text=textBT, font=font, fill=fill, width=width, state="disabled")


        # Texte-bouton
        else:
            font = 8 if font < 8 else font
            font = ("Rockwell Nova Cond", font)
            self.bouton = canvas.create_text(x, y, font=font, fill=fill, anchor=anchor, text=text, activefill='red',
                                             width=width)

        # Transformation en bouton
        canvas.tag_bind(self.bouton, '<Button-1>', lambda bruit: menu.dataMus.Bruit_Touche(bruit=menu.dataMus.b['bip']))
        canvas.tag_bind(self.bouton, '<Button-1>', function, add='+')
        canvas.tag_bind(self.bouton, '<Enter>', lambda bruit: menu.dataMus.Bruit_Touche(bruit=menu.dataMus.b['clic']))


if __name__ == '__main__':
    # Creation de la fenetre et de ses parametres
    windows = Tk()
    windows.title("Commando Assaut")
    screen_height = windows.winfo_screenheight()
    screen_width = windows.winfo_screenwidth()
    windows.geometry("{}x{}+{}+{}".format(930, 660, 300, 75))
    # windows.attributes('-fullscreen', True)
    # windows.overrideredirect(1)
    windows.minsize(930, 660)
    windows.config(background="brown")
    windows.iconbitmap("Logo.ico")

    # Debut du jeu
    affichage = Menu(windows)

    windows.mainloop()
    pygame.quit()
