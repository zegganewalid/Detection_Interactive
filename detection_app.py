import cv2  # Bibliothèque OpenCV pour traitement d'images et vidéos
import mediapipe as mp  # Bibliothèque Google pour la détection des points clés du visage et des mains
import numpy as np  # Pour les opérations mathématiques sur les tableaux
import tkinter as tk  # Bibliothèque pour l'interface graphique
from tkinter import font as tkfont  # Pour gérer les polices d'affichage
from PIL import Image, ImageTk  # Pour la manipulation d'images (non utilisé dans ce code)

class DetectionApp:
    """
    Application de détection d'expressions faciales et de gestes de mains
    utilisant la webcam et les bibliothèques MediaPipe et OpenCV.
    """
    def __init__(self):
        # Initialiser les variables de base
        self.is_running = False  # État de l'application
        self.cap = None  # Capture vidéo (sera initialisée plus tard)
        self.detection_mode = None  # Mode de détection: 'face', 'hand', ou 'both'
        
        # Configuration de MediaPipe pour la détection du visage
        self.mp_face_mesh = mp.solutions.face_mesh  # Module pour le maillage facial
        self.face_mesh = None  # L'objet FaceMesh sera initialisé selon le mode choisi
        self.mp_drawing = mp.solutions.drawing_utils  # Utilitaires pour dessiner les points clés
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))  # Style de dessin
        
        # Configuration de MediaPipe pour la détection des mains
        self.mp_hands = mp.solutions.hands  # Module pour la détection des mains
        self.hands = None  # L'objet Hands sera initialisé selon le mode choisi
        
        # Créer l'écran d'accueil
        self.create_welcome_screen()
        
    def create_welcome_screen(self):
        """
        Crée l'écran d'accueil de l'application avec les boutons pour choisir
        le mode de détection.
        """
        # Créer la fenêtre principale Tkinter
        self.root = tk.Tk()
        self.root.title("Application de Détection")
        
        # Configuration de la fenêtre en plein écran
        screen_width = self.root.winfo_screenwidth()  # Largeur de l'écran
        screen_height = self.root.winfo_screenheight()  # Hauteur de l'écran
        self.root.geometry(f"{screen_width}x{screen_height}")  # Définir les dimensions
        self.root.attributes('-fullscreen', True)  # Mettre en plein écran
        
        # Configurer le fond en couleur sombre
        self.root.configure(bg="#121212")  # Fond noir/gris foncé
        
        # Créer le titre principal avec une grande police
        title_font = tkfont.Font(family="Helvetica", size=42, weight="bold")
        title = tk.Label(self.root, text="Application de Détection Interactive", 
                         font=title_font, bg="#121212", fg="#ffffff")
        title.pack(pady=(80, 40))  # Ajouter des marges verticales
        
        # Description du programme avec une police moyenne
        desc_font = tkfont.Font(family="Helvetica", size=18)
        description_text = """
        Bienvenue dans l'application de détection interactive !
        
        Cette application utilise la caméra de votre ordinateur pour détecter
        votre visage et/ou vos gestes de main en temps réel.
        
        Choisissez le mode que vous souhaitez utiliser ci-dessous :
        """
        description = tk.Label(self.root, text=description_text, font=desc_font,
                              bg="#121212", fg="#e0e0e0", justify="left")
        description.pack(pady=20)
        
        # Créer un conteneur pour les boutons (organisation en grille)
        button_frame = tk.Frame(self.root, bg="#121212")
        button_frame.pack(pady=30)
        
        # Configuration du style commun pour tous les boutons
        button_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        button_width = 20
        button_height = 3
        
        # Bouton pour le mode détection de visage (bleu)
        face_button = tk.Button(button_frame, text="Détection du Visage", 
                              font=button_font, bg="#4285F4", fg="white",
                              width=button_width, height=button_height,
                              command=lambda: self.start_detection('face'))
        face_button.grid(row=0, column=0, padx=20, pady=20)
        
        # Texte explicatif sous le bouton visage
        face_desc = tk.Label(button_frame, text="Détecte les expressions faciales:\nSourire, Surprise, Colère", 
                           font=desc_font, bg="#121212", fg="#e0e0e0", justify="center")
        face_desc.grid(row=1, column=0, padx=20)
        
        # Bouton pour le mode détection de main (vert)
        hand_button = tk.Button(button_frame, text="Détection des Mains", 
                              font=button_font, bg="#0F9D58", fg="white",
                              width=button_width, height=button_height,
                              command=lambda: self.start_detection('hand'))
        hand_button.grid(row=0, column=1, padx=20, pady=20)
        
        # Texte explicatif sous le bouton main
        hand_desc = tk.Label(button_frame, text="Détecte les gestes des mains:\nOK, Like, Coeur, I Love You", 
                           font=desc_font, bg="#121212", fg="#e0e0e0", justify="center")
        hand_desc.grid(row=1, column=1, padx=20)
        
        # Bouton pour le mode combiné (rouge)
        both_button = tk.Button(button_frame, text="Les Deux", 
                              font=button_font, bg="#DB4437", fg="white",
                              width=button_width, height=button_height,
                              command=lambda: self.start_detection('both'))
        both_button.grid(row=0, column=2, padx=20, pady=20)
        
        # Texte explicatif sous le bouton combiné
        both_desc = tk.Label(button_frame, text="Détecte simultanément\nles expressions et les gestes", 
                           font=desc_font, bg="#121212", fg="#e0e0e0", justify="center")
        both_desc.grid(row=1, column=2, padx=20)
        
        # Instructions pour quitter l'application
        quit_instructions = tk.Label(self.root, 
                                   text="Pour quitter l'application à tout moment, appuyez sur la touche 'Q'",
                                   font=desc_font, bg="#121212", fg="#e0e0e0")
        quit_instructions.pack(pady=40)
        
        # Bouton de sortie en bas de l'écran (rouge)
        exit_font = tkfont.Font(family="Helvetica", size=14)
        exit_button = tk.Button(self.root, text="Quitter", font=exit_font,
                               bg="#f44336", fg="white", padx=20, pady=10,
                               command=self.exit_application)
        exit_button.pack(pady=10)
        
        # Lancer la boucle principale de l'interface
        self.root.mainloop()
    
    def exit_application(self):
        """
        Ferme proprement l'application en libérant les ressources
        """
        # Libérer la capture vidéo si elle est active
        if self.cap is not None:
            self.cap.release()
        # Fermer toutes les fenêtres OpenCV ouvertes
        cv2.destroyAllWindows()
        # Fermer la fenêtre Tkinter
        self.root.destroy()
    
    def detect_facial_expression(self, face_landmarks, img_shape):
        """
        Analyse les points clés du visage pour détecter les expressions
        
        Args:
            face_landmarks: Points clés du visage détectés par MediaPipe
            img_shape: Dimensions de l'image (hauteur, largeur)
            
        Returns:
            String: L'expression détectée ou None si aucune n'est reconnue
        """
        # Obtenir les dimensions de l'image pour convertir les coordonnées relatives
        h, w = img_shape[:2]
        
        # Convertir les points de repère en coordonnées de pixels (x,y)
        landmarks = []
        for landmark in face_landmarks.landmark:
            x, y = int(landmark.x * w), int(landmark.y * h)
            landmarks.append((x, y))
        
        # Définir les points clés du visage (indices simplifiés du maillage facial MediaPipe)
        # Sourcils
        left_eyebrow = [landmarks[65], landmarks[66], landmarks[67]]  # Points du sourcil gauche
        right_eyebrow = [landmarks[295], landmarks[296], landmarks[297]]  # Points du sourcil droit
        
        # Points de la bouche
        top_lip = landmarks[13]  # Point supérieur de la lèvre
        bottom_lip = landmarks[14]  # Point inférieur de la lèvre
        mouth_width = landmarks[78][0] - landmarks[308][0]  # Largeur de la bouche
        mouth_height = bottom_lip[1] - top_lip[1]  # Hauteur de la bouche
        mouth_aspect_ratio = mouth_height / max(mouth_width, 1)  # Ratio hauteur/largeur (évite division par zéro)
        
        # Coins de la bouche
        left_mouth_corner = landmarks[61]  # Coin gauche
        right_mouth_corner = landmarks[291]  # Coin droit
        
        # Calculer les distances des sourcils par rapport à un point neutre
        eyebrow_neutral_y = (landmarks[8][1] + landmarks[168][1]) // 2  # Point entre les yeux
        left_eyebrow_dist = eyebrow_neutral_y - left_eyebrow[1][1]  # Distance sourcil gauche
        right_eyebrow_dist = eyebrow_neutral_y - right_eyebrow[1][1]  # Distance sourcil droit
        
        # Détecter un sourire (bouche large + coins relevés)
        smile_threshold = 0.2  # Seuil pour le ratio bouche
        mouth_corner_y_avg = (left_mouth_corner[1] + right_mouth_corner[1]) / 2  # Position moyenne des coins
        if mouth_aspect_ratio > smile_threshold and mouth_corner_y_avg < bottom_lip[1]:
            return "SOURIRE :)"
        
        # Détecter la surprise (sourcils levés + bouche ouverte)
        surprise_eyebrow_threshold = 25  # Seuil pour la hauteur des sourcils
        surprise_mouth_threshold = 0.5  # Seuil pour l'ouverture de la bouche
        if (left_eyebrow_dist > surprise_eyebrow_threshold and 
            right_eyebrow_dist > surprise_eyebrow_threshold and 
            mouth_aspect_ratio > surprise_mouth_threshold):
            return "SURPRISE :O"
        
        # Détecter le froncement de sourcils (colère)
        frown_threshold = -5  # Valeur négative car les sourcils descendent
        if left_eyebrow_dist < frown_threshold and right_eyebrow_dist < frown_threshold:
            return "FÂCHÉ >:("
        
        # Si aucune expression n'est détectée
        return None
    
    def detect_hand_gesture(self, hand_landmarks, hand_type):
        """
        Analyse les points clés de la main pour détecter un geste spécifique
        
        Args:
            hand_landmarks: Points clés de la main détectés par MediaPipe
            hand_type: "Left" ou "Right" selon la main détectée
            
        Returns:
            String: Le geste détecté ou None si aucun n'est reconnu
        """
        # Obtenir les coordonnées des points clés
        landmarks = hand_landmarks.landmark
        
        # Définir les points importants pour la détection des gestes
        # Points des bouts des doigts
        thumb_tip = landmarks[mp.solutions.hands.HandLandmark.THUMB_TIP]  # Bout du pouce
        index_tip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]  # Bout de l'index
        middle_tip = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]  # Bout du majeur
        ring_tip = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]  # Bout de l'annulaire
        pinky_tip = landmarks[mp.solutions.hands.HandLandmark.PINKY_TIP]  # Bout de l'auriculaire
        
        # Points intermédiaires des doigts
        thumb_ip = landmarks[mp.solutions.hands.HandLandmark.THUMB_IP]  # Articulation intermédiaire du pouce
        index_pip = landmarks[mp.solutions.hands.HandLandmark.INDEX_FINGER_PIP]  # Articulation médiane de l'index
        middle_pip = landmarks[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_PIP]  # Articulation médiane du majeur
        ring_pip = landmarks[mp.solutions.hands.HandLandmark.RING_FINGER_PIP]  # Articulation médiane de l'annulaire
        pinky_pip = landmarks[mp.solutions.hands.HandLandmark.PINKY_PIP]  # Articulation médiane de l'auriculaire
        
        # Point du poignet
        wrist = landmarks[mp.solutions.hands.HandLandmark.WRIST]
        
        # Calculer la distance entre le pouce et l'index en 3D
        thumb_index_distance = np.sqrt(
            (thumb_tip.x - index_tip.x)**2 + 
            (thumb_tip.y - index_tip.y)**2 + 
            (thumb_tip.z - index_tip.z)**2
        )
        
        # Détection du geste "OK" (pouce et index formant un cercle)
        if thumb_index_distance < 0.05:  # Seuil de proximité pour le cercle
            # Vérifier que les autres doigts sont tendus
            if middle_tip.y < middle_pip.y and ring_tip.y < ring_pip.y and pinky_tip.y < pinky_pip.y:
                return "OK 👌"
        
        # Détection du geste "Like" (pouce levé, autres doigts fermés)
        # Le traitement diffère selon qu'il s'agit de la main droite ou gauche
        if hand_type == "Right":
            # Pour la main droite, le pouce doit pointer vers la gauche (x plus petit que le poignet)
            thumb_direction = thumb_tip.x - wrist.x
            is_thumb_up = thumb_direction < 0 and thumb_tip.y < thumb_ip.y
        else:
            # Pour la main gauche, le pouce doit pointer vers la droite (x plus grand que le poignet)
            thumb_direction = thumb_tip.x - wrist.x
            is_thumb_up = thumb_direction > 0 and thumb_tip.y < thumb_ip.y
        
        # Vérifier si les autres doigts sont fermés (y plus grand = position plus basse)
        fingers_closed = (
            index_tip.y > index_pip.y and
            middle_tip.y > middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y
        )
        
        # Si pouce levé et autres doigts fermés = Like
        if is_thumb_up and fingers_closed:
            return "LIKE 👍"
        
        # Détection du geste "Coeur" (pouce et index formant un coeur)
        # Le pouce et l'index sont tendus, les autres doigts sont fermés
        if (thumb_tip.y < thumb_ip.y and  # Pouce levé
            index_tip.y < index_pip.y and  # Index tendu
            middle_tip.y > middle_pip.y and  # Majeur plié
            ring_tip.y > ring_pip.y and  # Annulaire plié
            pinky_tip.y > pinky_pip.y):  # Auriculaire plié
            
            # Vérifier la distance spécifique entre pouce et index pour le coeur
            if 0.1 < thumb_index_distance < 0.25:
                return "COEUR ❤️"
        
        # Détection du geste "I Love You" (pouce, index et auriculaire levés)
        if (thumb_tip.y < thumb_ip.y and  # Pouce levé
            index_tip.y < index_pip.y and  # Index tendu
            middle_tip.y > middle_pip.y and  # Majeur plié
            ring_tip.y > ring_pip.y and  # Annulaire plié
            pinky_tip.y < pinky_pip.y):  # Auriculaire tendu
            return "I LOVE YOU 🤟"
        
        # Si aucun geste n'est détecté
        return None
    
    def start_detection(self, mode):
        """
        Démarre la détection selon le mode choisi (visage, main ou les deux)
        
        Args:
            mode: 'face', 'hand', ou 'both' pour le type de détection à effectuer
        """
        # Enregistrer le mode de détection choisi
        self.detection_mode = mode
        
        # Fermer la fenêtre d'accueil Tkinter
        self.root.destroy()
        
        # Initialiser les détecteurs MediaPipe selon le mode choisi
        if mode == 'face' or mode == 'both':
            # Initialiser le détecteur de visage
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,  # Limiter à un seul visage
                min_detection_confidence=0.5,  # Seuil de confiance pour la détection
                min_tracking_confidence=0.5  # Seuil de confiance pour le suivi
            )
        
        if mode == 'hand' or mode == 'both':
            # Initialiser le détecteur de main
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=0.7,  # Seuil de confiance pour la détection
                min_tracking_confidence=0.5,  # Seuil de confiance pour le suivi
                max_num_hands=2  # Limiter à deux mains maximum
            )
        
        # Initialiser la capture vidéo depuis la webcam (0 = webcam par défaut)
        self.cap = cv2.VideoCapture(0)
        # Définir une résolution HD pour la capture
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Largeur
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Hauteur
        
        # Créer une fenêtre OpenCV pour afficher le flux vidéo
        window_name = "Détection Interactive"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        # Boucle principale de traitement des images
        while True:
            # Capturer une image depuis la webcam
            success, img = self.cap.read()
            if not success:
                print("Échec de la capture d'image")
                break
            
            # Inverser l'image horizontalement pour créer un effet miroir
            img = cv2.flip(img, 1)
            
            # Convertir l'image en RGB pour MediaPipe (qui n'accepte pas le BGR d'OpenCV)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Créer une image de fond noir pour dessiner les points de détection
            black_img = np.zeros_like(img)
            
            # Variables pour stocker les textes à afficher
            face_text = None  # Expression faciale détectée
            hand_text = None  # Geste de main détecté
            
            # Traitement selon le mode choisi
            if self.detection_mode in ['face', 'both']:
                # Détecter les visages avec MediaPipe
                face_results = self.face_mesh.process(img_rgb)
                
                # Si des visages sont détectés
                if face_results.multi_face_landmarks:
                    for face_landmarks in face_results.multi_face_landmarks:
                        # Dessiner le maillage facial sur l'image noire
                        self.mp_drawing.draw_landmarks(
                            image=black_img,
                            landmark_list=face_landmarks,
                            connections=self.mp_face_mesh.FACEMESH_TESSELATION,  # Tous les points reliés
                            landmark_drawing_spec=self.drawing_spec,
                            connection_drawing_spec=self.drawing_spec
                        )
                        
                        # Analyser l'expression faciale
                        expression = self.detect_facial_expression(face_landmarks, img.shape)
                        if expression:
                            face_text = expression
            
            if self.detection_mode in ['hand', 'both']:
                # Détecter les mains avec MediaPipe
                hand_results = self.hands.process(img_rgb)
                
                # Si des mains sont détectées
                if hand_results.multi_hand_landmarks:
                    for i, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                        # Dessiner les points clés et connexions de la main
                        self.mp_drawing.draw_landmarks(
                            black_img, 
                            hand_landmarks, 
                            self.mp_hands.HAND_CONNECTIONS
                        )
                        
                        # Obtenir le type de main (gauche ou droite)
                        if hand_results.multi_handedness:
                            hand_type = hand_results.multi_handedness[i].classification[0].label
                            
                            # Analyser le geste de la main
                            gesture = self.detect_hand_gesture(hand_landmarks, hand_type)
                            if gesture:
                                hand_text = gesture
            
            # Fusionner l'image originale avec l'image des points de repère (semi-transparente)
            combined_img = cv2.addWeighted(img, 0.7, black_img, 0.3, 0)
            
            # Afficher le titre du mode actif en haut de l'écran
            mode_title = ""
            if self.detection_mode == 'face':
                mode_title = "Mode: Détection d'Expressions Faciales"
            elif self.detection_mode == 'hand':
                mode_title = "Mode: Détection de Gestes des Mains"
            else:
                mode_title = "Mode: Détection Combinée (Visage et Mains)"
                
            # Ajouter le titre du mode sur l'image
            cv2.putText(combined_img, mode_title, (20, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Afficher les textes de détection en grand sur l'écran
            y_position = 100  # Position verticale initiale
            if face_text:
                # Afficher l'expression faciale détectée
                cv2.putText(combined_img, face_text, (50, y_position), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
                y_position += 80  # Décaler pour le prochain texte
                
            if hand_text:
                # Afficher le geste de main détecté
                cv2.putText(combined_img, hand_text, (50, y_position), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)
            
            # Afficher l'instruction pour quitter en bas de l'écran
            cv2.putText(combined_img, "Appuyez sur 'Q' pour quitter", 
                        (20, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, (255, 255, 255), 2)
            
            # Afficher l'image finale
            cv2.imshow(window_name, combined_img)
            
            # Quitter la boucle si la touche 'q' est pressée
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Nettoyer les ressources à la fin
        self.cap.release()  # Libérer la caméra
        cv2.destroyAllWindows()  # Fermer toutes les fenêtres OpenCV

# Point d'entrée du programme
if __name__ == "__main__":
    app = DetectionApp()  # Créer et lancer l'application