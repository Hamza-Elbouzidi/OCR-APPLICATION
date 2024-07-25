import ollama

def ask(card_data, text, csv):
    query = (f'Vous êtes un modèle linguistique extrêmement précis et méticuleux chargé d\'extraire des informations spécifiques à partir de texte extrait par OCR. '
             f'Le texte est fourni aux formats texte brut et CSV. Votre objectif est d\'extraire les données suivantes: \n{card_data}\n'
             f'seulment sans rien extraire de plus ou de moins et sans ajouter des détails ou informations supplémentaires non demandées depuis les fichiers suivants \n'
             f'CSV:\n{csv}\n'
             f'Text:\n{text}\n'
             f'Tu vas extraire les données qu\'on t\'a demandées et seulement ce qu\'on t\'a demandées de manière concise et précise sous format JSON en veillant à ce qu\'aucune donnée ou valeur ne soit modifiée. '
             f'Le résultat final doit être concis et ne contenir que l\'information demandée comme elle est précisée dans les textes donnés. Il ne faut pas raisonner, donne-moi les informations telles qu\'elles sont dans le fichier. '
             f'Si tu n\'arrives pas à trouver, dis que c\'est introuvable. Ne me dis rien à propos de tes connaissances linguistiques et n\'ajoute pas de contexte. '
             f'Réfléchis deux fois avant d\'extraire une donnée si elle est demandée ou pas.')
             
    response = ollama.chat(model='llama3', messages=[
        {'role': 'user', 'content': query},
    ])
    
    response = response['message']['content']
    print(f'Text: {text}')
    print(f'CSV: {csv}')

    return response
