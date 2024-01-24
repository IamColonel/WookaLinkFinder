import requests
import re

def chercher_variable(url, variable):
    try:
        # Obtenir le code source de la page
        response = requests.get(url)
        response.raise_for_status()
        code_source = response.text

        # Rechercher la variable dans la partie JavaScript du code source
        pattern = r'\b' + re.escape(variable) + r'\b'
        match = re.search(pattern, code_source)

        if match:
            start_index = match.start()
            end_index = match.end()

            # Rechercher "https" à gauche de la variable
            start_http_index = code_source.rfind('https', 0, start_index)
            if start_http_index == -1:
                start_http_index = 0

            # Rechercher ".mp4" à droite de la variable (y compris)
            end_mp4_index = code_source.find('.mp4', end_index)
            if end_mp4_index == -1:
                end_mp4_index = len(code_source)

            found_part = code_source[start_http_index:end_mp4_index + 4]  # Ajout de 4 caractères pour inclure ".mp4"

            # Supprimer les barres obliques inverses
            found_part = found_part.replace('\\', '')

            print(f"La variable '{variable}' a été trouvée dans le code source JavaScript :")
            print(found_part)

        else:
            print(f"La variable '{variable}' n'a pas été trouvée dans le code source JavaScript.")

    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la récupération de la page : {e}")

# Remplacez l'URL et la variable selon votre besoin
url = input("Veuillez indiquer l'url Wooka du film à télécharger : \n>>> ")
variable_a_chercher = "iptvfrenchforyou"

chercher_variable(url, variable_a_chercher)
