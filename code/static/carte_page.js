document.addEventListener('DOMContentLoaded', () => {
    const cardsContainer = document.getElementById('cards-container');
    const editForm = document.getElementById('edit-form');
    const editCardForm = document.getElementById('edit-card-form');
    const editFieldsContainer = document.getElementById('edit-fields-container');
    const addFieldButton = document.getElementById('add-field-button');

    let allCards = [];

    function loadCards() {
        const cards = JSON.parse(localStorage.getItem('cards')) || [];
        allCards = cards;
        displayCards();
    }

    function displayCards() {
        cardsContainer.innerHTML = ''; // Réinitialise le conteneur des cartes

        allCards.forEach((card, index) => {
            const cardContainer = document.createElement('div');
            cardContainer.classList.add('card'); // Ajoute une classe CSS à la carte

            if (card.isNoisy) {
                cardContainer.classList.add('noisy'); // Applique la classe noisy si la carte est "bruyante"
            }

            const cardName = document.createElement('h5');
            cardName.classList.add('text-carte');
            cardName.textContent = card.name; // Définit le nom de la carte
            cardContainer.appendChild(cardName); // Ajoute le nom au conteneur de la carte

            // Création du conteneur des boutons
            const buttonContainer = document.createElement('div');
            buttonContainer.classList.add('button-container');

            // Bouton Bruyant
            const noisyButton = document.createElement('button');
            noisyButton.innerHTML = '<i class="bi bi-eye"></i>';
            noisyButton.classList.add('noisy-button');
            noisyButton.addEventListener('click', () => handleNoisyClick(index));
            buttonContainer.appendChild(noisyButton);

            // Bouton Annuler
            const cancelButton = document.createElement('button');
            cancelButton.textContent = 'Annuler';
            cancelButton.classList.add('cancel-button');
            cancelButton.addEventListener('click', () => handleCancelClick(index));
            buttonContainer.appendChild(cancelButton);

            // Bouton Valider
            const validateButton = document.createElement('button');
            validateButton.textContent = 'Valider';
            validateButton.classList.add('validate-button');
            validateButton.addEventListener('click', () => handleValidateClick(index));
            buttonContainer.appendChild(validateButton);

            // Bouton Modifier
            const editButton = document.createElement('button');
            editButton.innerHTML = '<i class="bi bi-pencil-square"></i>'; // Icône d'édition
            editButton.classList.add('edit-button');
            editButton.addEventListener('click', () => editCard(index));
            buttonContainer.appendChild(editButton);

            // Ajout du conteneur des boutons au conteneur de la carte
            cardContainer.appendChild(buttonContainer);

            // Ajout du conteneur de la carte au conteneur principal
            cardsContainer.appendChild(cardContainer);
        });
    }

    function handleNoisyClick(index) {
        const card = allCards[index];
        card.isNoisy = !card.isNoisy; // Bascule la valeur de isNoisy
        localStorage.setItem('cards', JSON.stringify(allCards));
        displayCards();
    }

    function handleCancelClick(index) {
        // Affiche une boîte de dialogue de confirmation
        const isConfirmed = confirm("Êtes-vous sûr de vouloir supprimer cette carte ?");

        // Si l'utilisateur clique sur "OK", continue avec la suppression
        if (isConfirmed) {
            allCards.splice(index, 1);
            localStorage.setItem('cards', JSON.stringify(allCards));
            displayCards();
        }
        // Sinon, ne fait rien
    }

    function handleValidateClick(index) {
        console.log('Bouton Valider cliqué pour la carte index', index);
        // Implémentez la logique de validation ici si nécessaire
    }

    function editCard(index) {
        const card = allCards[index];
        document.getElementById('edit-card-id').value = index;
        document.getElementById('edit-card-name').value = card.name;
        
        editFieldsContainer.innerHTML = '';
        card.fields.forEach(field => {
            const fieldGroup = document.createElement('div');
            fieldGroup.classList.add('form-group', 'field-group');
            fieldGroup.innerHTML = `
                <label for="field-name">Nom du Champ</label>
                <input type="text" class="field-name" value="${field.name}" required>
                <label for="field-type">Type du Champ</label>
                <select class="field-type" required>
                    <option value="" disabled>Choisissez le type de champ</option>
                    <option value="text" ${field.type === 'text' ? 'selected' : ''}>Texte</option>
                    <option value="number" ${field.type === 'number' ? 'selected' : ''}>Nombre</option>
                    <option value="email" ${field.type === 'email' ? 'selected' : ''}>Email</option>
                    <option value="address" ${field.type === 'address' ? 'selected' : ''}>Adresse</option>
                    <option value="date" ${field.type === 'date' ? 'selected' : ''}>Date</option>
                    <option value="table" ${field.type === 'table' ? 'selected' : ''}>Tableau</option>
                </select>
                <button type="button" class="remove-field-button">Supprimer</button>
            `;
            editFieldsContainer.appendChild(fieldGroup);
            
            // Ajouter un gestionnaire d'événement pour supprimer le champ
            fieldGroup.querySelector('.remove-field-button').addEventListener('click', () => {
                confirmDeletion(fieldGroup);
            });
        });

        editForm.style.display = 'block';
    }

    function addField() {
        const fieldGroup = document.createElement('div');
        fieldGroup.classList.add('form-group', 'field-group');
        fieldGroup.innerHTML = `
            <label for="field-name">Nom du Champ</label>
            <input type="text" class="field-name" placeholder="Nom du champ" required>
            <label for="field-type">Type du Champ</label>
            <select class="field-type" required>
                <option value="" disabled selected>Choisissez le type de champ</option>
                <option value="text">Texte</option>
                <option value="number">Nombre</option>
                <option value="email">Email</option>
                <option value="address">Adresse</option>
                <option value="date">Date</option>
                <option value="table">Tableau</option>
            </select>
            <button type="button" class="remove-field-button">Supprimer</button>
        `;
        editFieldsContainer.appendChild(fieldGroup);

        // Ajouter un gestionnaire d'événement pour supprimer le champ
        fieldGroup.querySelector('.remove-field-button').addEventListener('click', () => {
            confirmDeletion(fieldGroup);
        });
    }

    function confirmDeletion(fieldGroup) {
        const isConfirmed = confirm("Êtes-vous sûr de vouloir supprimer ce champ ?");
        
        if (isConfirmed) {
            fieldGroup.remove();
        }
    }

    addFieldButton.addEventListener('click', addField);

    editCardForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const index = document.getElementById('edit-card-id').value;
        const cardName = document.getElementById('edit-card-name').value;
        const fieldGroups = editFieldsContainer.querySelectorAll('.field-group');
        const fields = Array.from(fieldGroups).map(group => ({
            name: group.querySelector('.field-name').value,
            type: group.querySelector('.field-type').value
        }));
        
        allCards[index] = {
            name: cardName,
            fields: fields
        };
        
        localStorage.setItem('cards', JSON.stringify(allCards));
        displayCards();
        editForm.style.display = 'none';
    });

    loadCards();
});
