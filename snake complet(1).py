"""
Jeu : Snake
@author : TUX
Le célébre jeu Snake légendaire que tout le monde connait
"""
import pygame, sys, time, random, clock

# Vérification s'il existe une erreur ou pas
verif_erreurs = pygame.init()


# pygame.init() exemple sortie -> (6, 0)
# le 2ème nombre dans le tuple donne un nombre d'erreurs  second number in tuple gives number of errors
if verif_erreurs[1] > 0:
    print(f'[!] a {verif_erreurs[1]} de erreurs au démarrage du jeu ...')
    sys.exit(-1)
else:
    print(' Le jeu a démarré correctement !!')

# fps --> Frame per second, pour le nombre d'images par seconde
fps_controller = pygame.time.Clock()

# Taille de la fenêtre
largeur = 900
longueur = 700
"""Choisissez le niveau de difficulté :
    Facile      -> 15
    Moyen       -> 25
    Difficile   -> 40
    Expert      -> 60
    CAUCHEMAR   -> 120
    GOD         -> 200  
"""
fps = 60
#Commandes initiales et basiques
pygame.display.set_caption('Snake') # Le titre de la fenêtre
game_window = pygame.display.set_mode((largeur, longueur)) # Créer la fenêtre pour le jeu avec les données saisis

# Les couleurs
noir = pygame.Color(0, 0, 0)
blanc = pygame.Color(255, 255, 255)
rouge = pygame.Color(255, 0, 0)
vert = pygame.Color(0, 255, 0)
bleu = pygame.Color(0, 0, 255)


# Variations du jeu 
snake_pos = [100, 50] 
snake_corps = [[100, 50], [100-10, 50], [100-(2*10), 50]]

appat_pos = [random.randrange(1, (largeur//10)) * 10, random.randrange(1, (longueur//10)) * 10]
appat_spawn = True

direction = 'RIGHT'
changer_pour = direction

score = 0

# Game Over
def game_over():
    """
    Fonction préparant les conditions si le joueur a perdu contenant toute police d'écriture et ses coordonnées , fond d'écrans etc ...
    :return: (string) retourne le score .
    """
    fond = pygame.font.SysFont('Times new roman', 90) # Type de police d'écriture stocké avec sa taille
    game_over_surface = fond.render('Game over', True, rouge) # Simple display que vous avez perdu le jeu en rouge
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (largeur/2, longueur/4)
    game_window.fill(noir)                         # Fond d'écran noir
    game_window.blit(game_over_surface, game_over_rect)
    
    afficher_score(0, rouge, 'times', 40)   # Afficher le score que vous avez obtenu à la fin de jeu
    pygame.display.flip()
    
    time.sleep(2) #attendre 3 secondes pour fermer le code
    pygame.quit() #Quitter 
    sys.exit()
    
def afficher_score(choice, color, font, size):
    """
    Fonction qui sert à afficher le score tout en haut de la fenêtre contenant 3 variables la couleur, le font et la taille.
    :return: None
    """
    global score
    score_font = pygame.font.SysFont(font, size)
    
    score_surface = score_font.render("Score: "+ str(score), True, color)
    score_rect = score_surface.get_rect() # rafraishir le score
    
    if choice == 1:
        score_rect.midtop = (largeur/10, 15)
    else:
        score_rect.midtop = (largeur/2, longueur/1.25)
    game_window.blit(score_surface, score_rect)
    pygame.display.flip()
    
# Partie de programmation evenementielle 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Si jamais une touche est pressée :
        elif event.type == pygame.KEYDOWN:
           # Partie de la programmation événementielle 
            if event.key == pygame.K_UP: # Si la touche appuyée est up 
                changer_pour = 'UP'
            if event.key == pygame.K_DOWN : # Si la touche appuyée est down 
                changer_pour = 'DOWN'
            if event.key == pygame.K_LEFT :# Même chose pour les autres fonctions
                changer_pour = 'LEFT'
            if event.key == pygame.K_RIGHT:
                changer_pour = 'RIGHT'
            # Esc -> Créer un évenement pour quitter le jeu
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            
    # Bouger le serpent 
    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10
        
    
    # Pour vérifier que le serpent ne peut pas changer de direction en opposition instantanément
    
    if changer_pour == 'UP' and direction != 'DOWN': # Bien sur on peut pas changer de direction opposément directement
        direction = 'UP'
    if changer_pour == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if changer_pour == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if changer_pour == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Méchanisme pour le serpent s'augmente de plus en plus
    snake_corps.insert(0, list(snake_pos))
    if snake_pos[0] == appat_pos[0] and snake_pos[1] == appat_pos[1]:
        score +=1
        appat_spawn = False # dès qu'il augmente un nouveaut appat disparrait
    else:
        snake_corps.pop()



# Apparission immédiate de l'appat aléatoire dans l'écran 
    if not appat_spawn:
        appat_pos = [random.randrange(1, (largeur//10)) * 10, random.randrange(1, (longueur//10)) * 10]
    appat_spawn = True

    # interface graphique de bords
    game_window.fill(noir)
    for pos in snake_corps:
        # Corps du snake :
        # Coordonnées de X et y -> avec la fonction .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, vert, pygame.Rect(pos[0], pos[1], 10, 10))

    # spawn de l'appat du snake 
    pygame.draw.rect(game_window, blanc, pygame.Rect(appat_pos[0], appat_pos[1], 10, 10))

    # Conditions de l'arrêt du jeu
    
    if snake_pos[0] < 0 or snake_pos[0] > largeur-10: # Si le serpent atteint une extremité 
        game_over()                                   # 
                                                      #Si le serpent atteint une extremité 
    if snake_pos[1] < 0 or snake_pos[1] > longueur-10:#
        game_over()
    
    # Le cas ou le serpent mange son corps le jeu s'arrête
    for block in snake_corps[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    afficher_score(1, blanc, 'consolas', 20)
    # Rafraishir l'écran (taux de rafraishissement)
    pygame.display.update()
    # taux de rafraishissements :
    fps_controller.tick(fps)