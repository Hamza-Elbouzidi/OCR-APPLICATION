document.addEventListener('DOMContentLoaded', () => {
    const confirmDeleteDialog = document.getElementById('confirm-delete-dialog');
    const deleteYesButton = document.getElementById('delete-yes');
    const deleteNoButton = document.getElementById('delete-no');
    const editCardModal = document.getElementById('edit-card-modal');
    const editCardForm = document.getElementById('edit-card-form');
    const closeEditModalButton = document.getElementById('close-edit-modal');
    const createCardModal = document.getElementById('create-card-modal');
    const createCardForm = document.getElementById('create-card-form');
    const closeCreateModalButton = document.getElementById('close-create-modal');
    const createCardButton = document.getElementById('btn1');  // Bouton de création de carte
    const cardsWrapper = document.querySelector('.cards-wrapper');
    const cardContainer = document.getElementById('card-container');
    const searchInput = document.getElementById('search-input');


    let selectedCard = null;

    // Fonction pour nettoyer les données JSON
    // function cleanJsonData(jsonData) {
    //     return jsonData
    //         .replace(/[{}]/g, '')   // Supprimer les accolades
    //         .replace(/\\/g, '')     // Supprimer les barres obliques inverses
    //         .replace(/"/g, '');     // Supprimer les guillemets doubles
    //  }




    // function cleanJsonData(jsonData) {
    //     // Nettoyer la chaîne JSON en supprimant les accolades, barres obliques inverses, et guillemets doubles
    //     let cleanedData = jsonData
    //         .replace(/[{}]/g, '')   // Supprimer les accolades
    //         .replace(/\\/g, '')     // Supprimer les barres obliques inverses
    //         .replace(/"/g, '');     // Supprimer les guillemets doubles
    
    //     // Diviser la chaîne en parties
    //     let parts = cleanedData.split(',');  // Diviser par les virgules pour obtenir chaque paire clé-valeur
    //     let keys = [];
    
    //     // Extraire les clés
    //     parts.forEach(part => {
    //         let [key] = part.split(':');  // Diviser chaque partie par les deux-points
    //         if (key) {
    //             keys.push(key.trim());   // Ajouter la clé après avoir supprimé les espaces
    //         }
    //     });
    
    //     // Retourner uniquement les clés sous forme de chaîne, séparées par des virgules
    //     return keys.join(', ');
    // }


    function cleanJsonData(jsonData) {
        // Nettoyer la chaîne JSON en supprimant les accolades, barres obliques inverses, et guillemets doubles
        let cleanedData = jsonData
            .replace(/[{}]/g, '')   // Supprimer les accolades
            .replace(/\\/g, '')     // Supprimer les barres obliques inverses
            .replace(/"/g, '');     // Supprimer les guillemets doubles
    
        // Diviser la chaîne en parties
        let parts = cleanedData.split(',');  // Diviser par les virgules pour obtenir chaque paire clé-valeur
        let keys = [];
    
        // Extraire les clés
        parts.forEach(part => {
            let [key] = part.split(':');  // Diviser chaque partie par les deux-points
            if (key) {
                keys.push(key.trim());   // Ajouter la clé après avoir supprimé les espaces
            }
        });
    
        // Retourner uniquement les clés sous forme de chaîne, séparées par des retours à la ligne
        return keys.join('\n');
    }
    



    
    // Fonction pour afficher une carte
    function displayCard(cardData) {
        const cardElement = document.createElement('div');
        cardElement.className = 'card';
        cardElement.dataset.cardTitle = cardData.title;
        cardElement.dataset.cardDescription = cardData.description;
        cardElement.dataset.cardJsonStructure = JSON.stringify(cardData.jsonStructure);

        cardElement.innerHTML = `
            <h3>${cardData.title}</h3>
            <div class="card-details">
                <p>${cardData.description}</p>
                <pre>${JSON.stringify(cardData.jsonStructure, null, 2)}</pre>
            </div>
            <div class="button-container">
                <button class="edit-button"><i class="bi bi-pencil-square"></i></button>
                <button class="noisy-button"><i class="bi bi-eye"></i></button>
                <button class="cancel-button" style="width:100px;">Supprimer</button>
                <button class="validate-button">Valider</button>
            </div>
        `;

        cardContainer.appendChild(cardElement);

        // Ajouter l'événement de clic pour le bouton d'édition
        cardElement.querySelector('.edit-button').addEventListener('click', (e) => {
            e.stopPropagation();
            selectedCard = cardElement;

            // Récupérer les données JSON de la carte et les nettoyer
            let rawJsonStructure = selectedCard.dataset.cardJsonStructure;
            let cleanedKeys = cleanJsonData(rawJsonStructure);

            // Remplir le formulaire de modification
            document.getElementById('card-title').value = selectedCard.dataset.cardTitle;
            document.getElementById('card-description').value = selectedCard.dataset.cardDescription;
          document.getElementById('card-json-structure').value = cleanedKeys;

            // Afficher la boîte modale
            editCardModal.style.display = 'block';
        });

        // Ajouter les événements pour les boutons de suppression
        cardElement.querySelector('.cancel-button').addEventListener('click', (e) => {
            e.stopPropagation();
            selectedCard = cardElement;
            confirmDeleteDialog.style.display = 'block';
        });

        // Ajouter les événements pour les boutons de changement de couleur
        cardElement.querySelector('.color-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            const newColor = prompt('Entrez la nouvelle couleur en hex (ex. #FF5733) :');
            if (newColor) {
                cardElement.style.backgroundColor = newColor;
            }
        });
    }

    // Fonction pour gérer les clics sur les boutons des cartes
    function setupCardButtons() {
        // Gérer les boutons de suppression
        document.querySelectorAll('.card .cancel-button').forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                selectedCard = e.target.closest('.card');
                confirmDeleteDialog.style.display = 'block';
            });
        });

        // Gérer les boutons d'édition
        document.querySelectorAll('.card .edit-button').forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                selectedCard = e.target.closest('.card');
                if (selectedCard) {
                    // Remplir le formulaire avec les données de la carte
                    document.getElementById('card-title').value = selectedCard.dataset.cardTitle;
                    document.getElementById('card-description').value = selectedCard.dataset.cardDescription;
                    document.getElementById('card-json-structure').value = cleanJsonData(selectedCard.dataset.cardJsonStructure);
                    // Afficher la boîte modale
                    editCardModal.style.display = 'block';
                    document.getElementById('modal-backdrop').style.display = 'block'
                } else {
                    console.log('Aucune carte sélectionnée');
                }
            });
        });

      // Gérer les boutons de changement de couleur
      document.querySelectorAll('.card .noisy-button').forEach(button => {
        button.addEventListener('click', () => {
          if (confirm("Voulez-vous vraiment rendre la carte invisible par le user ?")) {
            const cardElement = button.closest('.card');
            cardElement.classList.add('transparent');
            console.log(cardElement.classList); // Log the classList
      
            // Changement de l'icône
            const iconElement = button.querySelector('i');
            iconElement.classList.toggle('bi-eye');
            iconElement.classList.toggle('bi-eye-slash');
          }
        });
      });
        
        
    }

    setupCardButtons();

    // Gérer la confirmation de suppression
    deleteYesButton.addEventListener('click', () => {
        if (selectedCard) {
            selectedCard.remove();
            confirmDeleteDialog.style.display = 'none';
            selectedCard = null;
        }
    });

    deleteNoButton.addEventListener('click', () => {
        confirmDeleteDialog.style.display = 'none';
        selectedCard = null;
    });

    // Gérer la fermeture du formulaire modale
    closeEditModalButton.addEventListener('click', () => {
        editCardModal.style.display = 'none';     
       document.getElementById('modal-backdrop').style.display = 'none';

    });

    // Gérer la soumission du formulaire d'édition
    editCardForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (selectedCard) {
            // Mettre à jour les données de la carte avec les nouvelles valeurs
            selectedCard.dataset.cardTitle = document.getElementById('card-title').value;
            selectedCard.dataset.cardDescription = document.getElementById('card-description').value;
            selectedCard.dataset.cardJsonStructure = document.getElementById('card-json-structure').value;

            // Mettre à jour le contenu de la carte affiché
            selectedCard.querySelector('h3').textContent = document.getElementById('card-title').value;
            selectedCard.querySelector('.card-details p').textContent = document.getElementById('card-description').value;
            selectedCard.querySelector('.card-details pre').textContent = document.getElementById('card-json-structure').value;

            // Fermer la boîte modale
            editCardModal.style.display = 'none';
            document.getElementById('modal-backdrop').style.display = 'none';
        } else {
            console.log('Aucune carte sélectionnée pour la mise à jour');
        }
    });

    // Ouvrir la boîte modale de création de carte
    createCardButton.addEventListener('click', () => {
        createCardModal.style.display = 'block';
        document.getElementById('modal-backdrop-create').style.display = 'block';
    });

    // Fermer la boîte modale de création de carte
    closeCreateModalButton.addEventListener('click', () => {
        createCardModal.style.display = 'none';
        document.getElementById('modal-backdrop-create').style.display = 'none';

    });

    // Soumettre le formulaire de création de carte
    createCardForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Récupérer les valeurs du formulaire
        const newCardTitle = document.getElementById('new-card-title').value;
        const newCardDescription = document.getElementById('new-card-description').value;
        const newCardJsonStructure = JSON.parse(document.getElementById('new-card-json-structure').value);

        // Créer une nouvelle carte
        const newCard = document.createElement('div');
        newCard.classList.add('card');
        newCard.dataset.cardTitle = newCardTitle;
        newCard.dataset.cardDescription = newCardDescription;
        newCard.dataset.cardJsonStructure = JSON.stringify(newCardJsonStructure);
        newCard.innerHTML = `
            <h3>${newCardTitle}</h3>
            <div class="card-details">
                <p>${newCardDescription}</p>
                <pre>${JSON.stringify(newCardJsonStructure, null, 2)}</pre>
            </div>
            <div class="button-container">
                <button class="edit-button"><i class="bi bi-pencil-square"></i></button>
                <button class="noisy-button"><i class="bi bi-eye"></i></button>
                <button class="cancel-button" style="width:100px;">Supprimer</button>
                <button class="validate-button">Valider</button>
            </div>
        `;

        // Ajouter la nouvelle carte au conteneur
        cardsWrapper.appendChild(newCard);

        // Réinitialiser le formulaire et fermer la boîte modale
        createCardForm.reset();
        createCardModal.style.display = 'none';

        // Réinitialiser les événements des boutons de la nouvelle carte
        setupCardButtons();
    });

    // Fonction de recherche
    searchInput.addEventListener('input', () => {
        const searchValue = searchInput.value.toLowerCase();
        document.querySelectorAll('.card').forEach(card => {
            const title = card.dataset.cardTitle.toLowerCase();
            const description = card.dataset.cardDescription.toLowerCase();
            if (title.includes(searchValue) || description.includes(searchValue)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});