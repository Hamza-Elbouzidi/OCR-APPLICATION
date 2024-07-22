import ollama

def ask(requests, text, csv):
    query = f'Vous êtes un modèle linguistique extrêmement précis et méticuleux chargé d\'extraire des informations spécifiques à partir de texte extrait par OCR. Le texte est fourni aux formats texte brut et CSV. Votre objectif est d\'extraire les tout les donnes suivants: \n{requests}\nseulement sans rien extraire de plus ou de moins et sans ajouter des details ou informations supplementaires non demandes depuis les fichiers suivants \ncsv:\n{csv}\ntext:\n{text}\ntu vas extraire les donnes q\'on t\'as demande et seulement ce qu\'on t\'as demande de manière concise et précise sous format JSON en veillant à ce qu\'aucune donnée ou valeur ne soit modifiée. Le resultat final doit etre concis et ne contenir que l information demandee comme elle est precisee dans les texts donnes. il ne faut pas resonner, donne moi les informations tels qu\'elles sont dans le fichier, si tu n\'arrive pas a trouver dit que c\'est introuvable, ne me dit rien a propos de tes connaissances linguistiques et n\'ajoute pas de contexte \nreflechit 2 fois avant d\'extraire un donnee si elle est demandee ou pas)'
    response = ollama.chat(model='llama3', messages=[
    {
        'role': 'user',
        'content': query,
    },
    ])
    response = response['message']['content']
    print(f'Text: {text}')
    print(f'CSV: {csv}')


    return response

