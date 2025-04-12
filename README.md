# Application de Détection Interactive

Cette application utilise la caméra de votre ordinateur pour détecter en temps réel les expressions faciales et les gestes des mains. Elle permet trois modes de fonctionnement : détection du visage, détection des mains, ou les deux simultanément.

## Fonctionnalités

- **Détection des expressions faciales** : Reconnaît automatiquement le sourire, la surprise et la colère
- **Détection des gestes de mains** : Identifie les gestes "OK", "Like", "Cœur" et "I Love You"
- **Interface graphique intuitive** : Interface simple et claire pour choisir le mode de détection
- **Visualisation en temps réel** : Affiche les points de repère et indique les expressions/gestes détectés

## Prérequis

Pour exécuter l'application depuis le code source, vous aurez besoin de :

- Python 3.7 ou supérieur
- OpenCV
- MediaPipe
- NumPy
- Tkinter (généralement inclus avec Python)
- PIL (Pillow)

## Installation

### Méthode 1 : Utiliser l'exécutable (recommandé pour les débutants)

1. Téléchargez le fichier `DetectionApp.exe` depuis la section "Releases"
2. Double-cliquez sur l'exécutable pour lancer l'application

### Méthode 2 : Exécuter depuis le code source

1. Clonez ce dépôt ou téléchargez les fichiers source
2. Installez les dépendances requises :
   ```bash
   pip install opencv-python mediapipe numpy pillow
   ```
3. Exécutez le programme :
   ```bash
   python detection_app.py
   ```

## Utilisation

1. **Lancement de l'application** :
   - Double-cliquez sur `DetectionApp.exe` ou exécutez `python detection_app.py`
   - Une interface graphique s'ouvrira en plein écran

2. **Choix du mode** :
   - Cliquez sur "Détection du Visage" pour reconnaître les expressions faciales
   - Cliquez sur "Détection des Mains" pour reconnaître les gestes manuels
   - Cliquez sur "Les Deux" pour activer les deux modes simultanément

3. **Pendant l'utilisation** :
   - Positionnez-vous face à la caméra à une distance confortable (50-100 cm)
   - Les expressions et gestes détectés s'afficheront en grand sur l'écran
   - Un maillage vert semi-transparent s'affichera sur votre visage ou vos mains

4. **Quitter** :
   - Appuyez sur la touche 'Q' à tout moment pour quitter le mode détection
   - Cliquez sur le bouton "Quitter" sur l'écran d'accueil pour fermer l'application

## Expressions et gestes reconnus

### Expressions faciales :
- **Sourire** : Souriez normalement
- **Surprise** : Ouvrez grand les yeux et la bouche comme si vous étiez surpris
- **Colère** : Froncez les sourcils

### Gestes de mains :
- **OK** : Formez un cercle avec le pouce et l'index, autres doigts tendus
- **Like** : Pouce levé, autres doigts repliés
- **Cœur** : Pouce et index tendus et rapprochés, autres doigts repliés
- **I Love You** : Pouce, index et auriculaire tendus, majeur et annulaire repliés

## Résolution des problèmes courants

### La caméra ne s'active pas
- Vérifiez que votre webcam est correctement connectée et fonctionne
- Assurez-vous qu'aucune autre application n'utilise déjà la caméra
- Redémarrez l'application

### La détection ne fonctionne pas bien
- Assurez-vous d'être dans un environnement bien éclairé
- Évitez les arrière-plans trop chargés ou en mouvement
- Positionnez-vous à une distance appropriée de la caméra (50-100 cm)

### L'application est lente
- Fermez les applications inutiles en arrière-plan
- Réduisez la résolution de la webcam si possible
- Sur des ordinateurs moins puissants, privilégiez un seul mode de détection à la fois

## Création de votre propre exécutable

Si vous souhaitez créer vous-même l'exécutable à partir du code source :

1. Installez PyInstaller :
   ```bash
   pip install pyinstaller
   ```

2. Créez l'exécutable :
   ```bash
   python -m PyInstaller --onefile --windowed --name DetectionApp detection_app.py
   ```

3. L'exécutable sera généré dans le dossier `dist`

## Vie privée et sécurité

- Cette application utilise uniquement la caméra locale de votre ordinateur
- Aucune donnée n'est transmise via Internet
- Les images capturées par la caméra ne sont pas enregistrées sur le disque

## Licence

[Précisez ici la licence de votre choix]

## Contact

Pour toute question ou suggestion, veuillez contacter : [Votre email ou autre contact]
