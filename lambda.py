import pychromecast
import speech_recognition as sr
from flux_led import WifiLedBulb

# Connexion à l'ampoule
bulb = WifiLedBulb('192.168.1.14')  # Remplacez par l'adresse IP de votre ampoule

# Dictionnaire des couleurs
colors = {
    "rouge": (255, 0, 0),
    "vert": (0, 255, 0),
    "bleu": (0, 0, 255),
    "jaune": (255, 255, 0),
    "magenta": (255, 0, 255),
    "cyan": (0, 255, 255),
    "blanc": (255, 255, 255),
    "noir": (0, 0, 0),
    "orange": (255, 165, 0),
    "violet": (128, 0, 128),
    "rose": (255, 192, 203),
    "marron": (165, 42, 42),
    "gris": (128, 128, 128),
    "turquoise": (64, 224, 208),
    "lavande": (230, 230, 250),
    "bordeaux": (128, 0, 0),
    "saumon": (250, 128, 114),
    "corail": (255, 127, 80),
    "menthe": (189, 252, 201),
    "olive": (128, 128, 0),
    "or": (255, 215, 0),
    "argent": (192, 192, 192),
    "bronze": (205, 127, 50),
    "ivoire": (255, 255, 240),
    "indigo": (75, 0, 130),
    "fuchsia": (255, 0, 255),
    "lilas": (200, 162, 200),
    "pêche": (255, 218, 185),
    "chocolat": (210, 105, 30),
    "beige": (245, 245, 220),
    "marine": (0, 0, 128),
    "sable": (244, 164, 96),
    "vert clair": (144, 238, 144),
    "vert foncé": (0, 100, 0),
    "bleu ciel": (135, 206, 235),
    "bleu nuit": (25, 25, 112),
    "pourpre": (160, 32, 240),
    "blanc cassé": (253, 245, 230),
    "rouille": (183, 65, 14),
    "saphir": (15, 82, 186),
    "émeraude": (80, 200, 120),
    "topaze": (255, 200, 124),
    "ambre": (255, 191, 0),
    "citron": (255, 247, 0),
    "grenat": (233, 0, 100),
    "prune": (142, 69, 133),
    "fumée": (96, 96, 96),
    "écarlate": (255, 36, 0),
    "cramoisi": (220, 20, 60),
    "amande": (239, 222, 205),
    "anis": (204, 255, 0),
    "aubergine": (113, 63, 144),
    "banane": (255, 255, 132),
    "bleu marine": (0, 0, 128),
    "bleuet": (100, 149, 237),
    "brique": (178, 34, 34),
    "café": (75, 54, 33),
    "cerise": (222, 49, 99),
    "chamois": (214, 196, 194),
    "châtaigne": (123, 63, 0),
    "citrouille": (255, 117, 24),
    "coquelicot": (245, 0, 0),
    "cuivre": (184, 115, 51),
    "curcuma": (255, 219, 88),
    "épinard": (61, 153, 112),
    "framboise": (227, 11, 93),
    "fraise": (252, 90, 141),
    "goudron": (21, 21, 21),
    "grenouille": (34, 139, 34),
    "héliotrope": (223, 115, 255),
    "hortensia": (193, 84, 193),
    "inca": (255, 225, 53),
    "jade": (0, 168, 107),
    "kaki": (240, 230, 140),
    "laque": (176, 23, 31),
    "melon": (253, 188, 180),
    "moutarde": (255, 219, 88),
    "mûre": (93, 57, 84),
    "myrtille": (63, 0, 102),
    "nacre": (245, 245, 220),
    "noisette": (197, 93, 57),
    "ocre": (204, 119, 34),
    "pastel": (204, 204, 255),
    "pistache": (190, 245, 116),
    "pourpre royale": (120, 81, 169),
    "poussière": (199, 191, 193),
    "prasin": (161, 214, 51),
    "rouge carmin": (150, 0, 24),
    "rouge rubis": (155, 17, 30),
    "rouge vermillon": (227, 66, 52),
    "safran": (244, 196, 48),
    "sang de bœuf": (123, 35, 0),
    "saphir foncé": (8, 37, 103),
    "sinople": (102, 141, 60),
    "tomate": (255, 99, 71),
    "vermeil": (255, 0, 51),
    "vert d'eau": (0, 221, 178),
    "zinnia": (227, 111, 26)
}
colors_str = ", ".join(colors.keys())


# Fonction pour changer la couleur de l'ampoule
def change_color(bulb, color_name):
    if color_name in colors:
        rgb = colors[color_name]
        bulb.setRgb(*rgb)
        print(f"L'ampoule a été changée en {color_name}.")
    else:
        print("Couleur non reconnue.")

# Fonction pour annoncer la couleur via Google Nest Mini
def announce_color(color_name):
    # Connexion à Chromecast via l'adresse IP du Nest Mini
    cast = pychromecast.Chromecast('192.168.1.10')

    # Annonce de la couleur via Google Nest Mini
    if cast:
        cast.wait()
        tts_url = f"http://translate.google.com/translate_tts?ie=UTF-8&q=La%20couleur%20est%20{color_name}&tl=fr&client=tw-ob"
        cast.media_controller.play_media(tts_url, 'audio/mp3')
        cast.media_controller.block_until_active()
        print(f"Annonce sur Nest Mini : La couleur est {color_name}")

# Fonction pour reconnaître la parole et contrôler la couleur de l'ampoule
def recognize_speech_and_control_bulb():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        # Joindre les noms des couleurs avec des virgules
        print("Dites une couleur parmi les suivantes :")
        print(colors_str)
        audio = recognizer.listen(source)

        try:
            # Utiliser Google Web Speech API pour la reconnaissance vocale
            color_name = recognizer.recognize_google(audio, language="fr-FR").lower()
            print(f"{color_name}")
            change_color(bulb, color_name)
            announce_color(color_name)
        except sr.UnknownValueError:
            print("Je n'ai pas compris la commande.")
        except sr.RequestError as e:
            print(f"Erreur de la reconnaissance vocale ; {e}")

# Exécution de la fonction de reconnaissance vocale en boucle
while True:
    recognize_speech_and_control_bulb()

