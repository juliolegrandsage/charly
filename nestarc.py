import sounddevice as sd
import numpy as np
import vosk
import wave
import json
import webbrowser
import subprocess

# Fonction pour enregistrer de l'audio
def enregistrer_audio(duree, nom_fichier):
    print("Enregistrement...")
    audio = sd.rec(int(duree * 44100), samplerate=44100, channels=1, dtype='int16')
    sd.wait()  # Attendre la fin de l'enregistrement
    print("Enregistrement terminé.")

    # Sauvegarder l'audio dans un fichier WAV
    with wave.open(nom_fichier, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16 bits
        wf.setframerate(44100)
        wf.writeframes(audio.tobytes())
    print(f"Fichier audio sauvegardé sous: {nom_fichier}")

# Fonction pour charger les commandes à partir d'un fichier
def charger_commandes(nom_fichier):
    commandes = {}
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne:
                commande, action = ligne.split(':')
                commandes[commande.lower()] = action.strip()
    return commandes

# Fonction pour ouvrir un navigateur
def ouvrir_navigateur():
    print("Ouverture du navigateur par défaut...")
    webbrowser.open("http://www.google.com")

def ouvrir_disney():
    print("Ouverture de Disney...")
    webbrowser.open("https://www.disneyplus.com/fr-fr")

def ouvrir_youtube():
    print("Ouverture de YouTube")
    webbrowser.open("https://youtube.com/")

# Fonction pour ouvrir Dolphin (l'explorateur de fichiers)
def ouvrir_dolphin():
    print("Ouverture de Dolphin...")
    subprocess.run(["dolphin"])

# Fonction pour ouvrir Firefox
def ouvrir_firefox():
    print("Ouverture de Firefox...")
    subprocess.run(["firefox"])
def ouvrir_steam():
    print("ouverture de steam")
    subprocess.run(["steam"])

# Chemin vers le modèle Vosk
model_path = "vosk-model-small-fr-pguyot-0.3"  # Chemin vers le modèle
model = vosk.Model(model_path)

# Nom du fichier audio
audio_file_path = "enregistrement.wav"

# Charger les commandes depuis le fichier
commandes = charger_commandes("commandes.txt")

# Fonction pour détecter la phrase d'activation
def detecter_phrase_activation():
    print("En attente de la phrase d'activation 'Charly !'...")
    while True:
        enregistrer_audio(5, audio_file_path)  # Enregistrer 5 secondes d'audio
        wf = wave.open(audio_file_path, "rb")
        rec = vosk.KaldiRecognizer(model, wf.getframerate())

        while True:
            data = wf.readframes(4000)
            if not data:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "text" in result:
                    command = result["text"].lower()
                    if "charly" in command:
                        print("Phrase d'activation détectée !")
                        return  # Retourne à l'appelant après avoir détecté la phrase d'activation
            else:
                print(rec.PartialResult())

# Appeler la fonction pour détecter la phrase d'activation
detecter_phrase_activation()

# Boucle principale pour écouter les commandes après la phrase d'activation
while True:
    enregistrer_audio(5, audio_file_path)  # Enregistrer 5 secondes d'audio
    wf = wave.open(audio_file_path, "rb")
    rec = vosk.KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if not data:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            if "text" in result:
                command = result["text"].lower()
                if command in commandes:
                    action = commandes[command]
                    if action == "navigateur":
                        ouvrir_navigateur()
                    elif action == "dolphin":
                        ouvrir_dolphin()
                    elif action == "firefox":
                        ouvrir_firefox()
                    elif action == "disney":
                        ouvrir_disney()
                    elif action == "youtube":
                        ouvrir_youtube()
                    elif action == "jeux":
                        ouvrir_steam()
                    else:
                        print(f"Aucune action définie pour la commande: {command}")
                else:
                    print(f"Commande non reconnue: {command}")
        else:
            print(rec.PartialResult())

    final_result = json.loads(rec.FinalResult())
    print("Résultat final:", final_result)

    if "text" in final_result:
        command = final_result["text"].lower()
        if command in commandes:
            action = commandes[command]
            if action == "navigateur":
                ouvrir_navigateur()
            elif action == "dolphin":
                ouvrir_dolphin()
            elif action == "firefox":
                ouvrir_firefox()
            elif action == "disney":
                ouvrir_disney()
            elif action == "youtube":
                ouvrir_youtube()
            else:
                print(f"Aucune action définie pour la commande: {command}")
        else:
            print(f"Commande non reconnue: {command}")
