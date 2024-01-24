import os
import requests

def telecharger_video(url, destination):
    try:
        # Ajouter un en-tête User-Agent à la requête
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        # Envoyer une requête GET avec l'en-tête User-Agent
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        # Écrire le contenu de la réponse dans un fichier local
        with open(destination, 'wb') as fichier_video:
            for morceau in response.iter_content(chunk_size=8192):
                fichier_video.write(morceau)

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de {url} : {e}")

# Fonction principale pour lire les liens à partir du fichier et télécharger les vidéos
def telecharger_videos_a_partir_du_fichier(fichier_texte):
    try:
        # Obtenir le chemin du dossier actuel
        dossier_actuel = os.getcwd()

        # Concaténer le nom du fichier à télécharger avec le chemin du dossier actuel
        chemin_destination_base = os.path.join(dossier_actuel, "video_{}.mp4")

        # Lire les liens à partir du fichier texte
        with open(fichier_texte, 'r') as f:
            liens = f.read().splitlines()

        # Télécharger les vidéos en séquence
        for i, lien in enumerate(liens, start=1):
            print(f"Début du téléchargement de la vidéo {i}")
            
            # Utiliser le format pour générer un nom de fichier unique
            chemin_destination = chemin_destination_base.format(i)

            # Appeler la fonction de téléchargement de la vidéo
            telecharger_video(lien, chemin_destination)

            print(f"Fin du téléchargement de la vidéo {i}. Sauvegardée dans {chemin_destination}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Exemple d'utilisation
fichier_texte = input("Lien du fichier \n >>> ")
telecharger_videos_a_partir_du_fichier(fichier_texte)
