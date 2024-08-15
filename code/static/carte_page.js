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

    let selectedCard = null;

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
                    // Afficher la boîte modale
                    editCardModal.style.display = 'block';
                } else {
                    console.log('Aucune carte sélectionnée');
                }
            });
        });

        // Gérer les boutons de changement de couleur
        document.querySelectorAll('.card .color-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                const card = e.target.closest('.card');
                const newColor = prompt('Entrez la nouvelle couleur en hex (ex. #FF5733) :');
                if (newColor) {
                    card.style.backgroundColor = newColor;
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
    });

    // Gérer la soumission du formulaire d'édition
    editCardForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (selectedCard) {
            // Mettre à jour les données de la carte avec les nouvelles valeurs
            selectedCard.dataset.cardTitle = document.getElementById('card-title').value;
            selectedCard.dataset.cardDescription = document.getElementById('card-description').value;
            // Mettre à jour le contenu de la carte affiché
            selectedCard.querySelector('h3').textContent = document.getElementById('card-title').value;
            selectedCard.querySelector('p').textContent = document.getElementById('card-description').value;
            // Fermer la boîte modale
            editCardModal.style.display = 'none';
        } else {
            console.log('Aucune carte sélectionnée pour la mise à jour');
        }
    });

    // Ouvrir la boîte modale de création de carte
    createCardButton.addEventListener('click', () => {
        createCardModal.style.display = 'block';
    });

    // Fermer la boîte modale de création de carte
    closeCreateModalButton.addEventListener('click', () => {
        createCardModal.style.display = 'none';
    });

    // Soumettre le formulaire de création de carte
    createCardForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Récupérer les valeurs du formulaire
        const newCardTitle = document.getElementById('new-card-title').value;
        const newCardDescription = document.getElementById('new-card-description').value;

        // Créer une nouvelle carte
        const newCard = document.createElement('div');
        newCard.classList.add('card');
        newCard.dataset.cardTitle = newCardTitle;
        newCard.dataset.cardDescription = newCardDescription;
        newCard.innerHTML = `
            <h3>${newCardTitle}</h3>
            <p>${newCardDescription}</p>
            <div class="button-container">
                <button class="edit-button"><i class="bi bi-pencil-square"></i></button>
                <button class="noisy-button"><i class="bi bi-eye"></i></button>
                <button class="cancel-button" style="width:100px ;">Supprimer</button>
                <button class="validate-button">Valider</button>
            </div>
        `;
        

        // Ajouter la carte au conteneur des cartes
        cardsWrapper.appendChild(newCard);

        // Réinitialiser le formulaire et fermer la modale
        createCardForm.reset();
        createCardModal.style.display = 'none';

        // Reconfigurer les boutons des nouvelles cartes
        setupCardButtons();
    });
});

const searchInput = document.getElementById('search-input');
    const cards = document.querySelectorAll('.card');

    searchInput.addEventListener('input', function() {
        const searchValue = searchInput.value.toLowerCase();

        cards.forEach(card => {
            const title = card.getAttribute('data-card-title').toLowerCase();
            const description = card.getAttribute('data-card-description').toLowerCase();

            if (title.includes(searchValue) || description.includes(searchValue)) {
                card.style.display = ''; // Affiche la carte
            } else {
                card.style.display = 'none'; // Cache la carte
            }
        });
    });