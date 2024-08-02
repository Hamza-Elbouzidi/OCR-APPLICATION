document.addEventListener('DOMContentLoaded', () => {
    const createCategoryForm = document.getElementById('create-category-form');
    const saveCardButton = document.getElementById('save-card-button');
    const addFieldButton = document.getElementById('add-field-button');
    const fieldsContainer = document.getElementById('fields-container');
    const fieldTypeSelect = document.getElementById('field-type');

    // Ajouter un champ au formulaire
    addFieldButton.addEventListener('click', () => {
        const fieldType = fieldTypeSelect.value;
        const fieldName = document.querySelector('.field-name').value.trim();
        
        if (!fieldType) {
            alert('Veuillez choisir un type de champ.');
            return;
        }

        const fieldGroup = document.createElement('div');
        fieldGroup.classList.add('form-row', 'field-group');
        let fieldHTML;

        switch (fieldType) {
            case 'text':
            case 'number':
            case 'date':
            case 'email':
                fieldHTML = `
                    <div class="input-data">
                        <input type="${fieldType}" class="field-name" required>
                        <label>Nom du Champ</label>
                        <div class="underline"></div>
                    </div>
                `;
                break;
            case 'dropdown':
                fieldHTML = `
                    <div class="input-data">
                        <select class="field-dropdown" required>
                            <option value="" disabled selected>Choisissez une option</option>
                            <option value="option1">Option 1</option>
                            <option value="option2">Option 2</option>
                            
                        </select>
                        <label>Nom du Champ</label>
                        <div class="underline"></div>
                    </div>
                `;
                break;
        }
        fieldGroup.innerHTML = fieldHTML;
        fieldsContainer.appendChild(fieldGroup);
    });

    // Enregistrer la carte
    saveCardButton.addEventListener('click', (e) => {
        e.preventDefault(); // Empêcher la soumission par défaut
        
        const cardName = document.getElementById('category-name').value.trim();
        const fieldGroups = document.querySelectorAll('.field-group');
        const fields = Array.from(fieldGroups).map(group => ({
            name: group.querySelector('.field-name') ? group.querySelector('.field-name').value.trim() : null,
            type: group.querySelector('select') ? 'dropdown' : group.querySelector('input').type
        }));

        if (cardName && fields.every(field => field.name || field.type === 'dropdown')) {
            const card = {
                name: cardName,
                fields: fields
            };

            saveCard(card);

            // Réinitialiser le formulaire
            createCategoryForm.reset();
            fieldsContainer.innerHTML = '';
        } else {
            alert('Veuillez remplir tous les champs');
        }
    });

    function saveCard(card) {
        let cards = JSON.parse(localStorage.getItem('cards')) || [];
        cards.push(card);
        localStorage.setItem('cards', JSON.stringify(cards));
    }

    // Load existing cards on page load
    function loadCards() {
        const cards = JSON.parse(localStorage.getItem('cards')) || [];
        cards.forEach(card => {
            
        });
    }

    loadCards();
});

document.addEventListener('DOMContentLoaded', () => {
    const viewAllCardsButton = document.getElementById('view-all-cards-button');

    viewAllCardsButton.addEventListener('click', () => {
        window.location.href = 'carte_page.html'; // Redirect to the wallets page
    });

    // Handle button clicks for the style
    $("button").on("touchstart mousedown", function () {
        $(this).addClass("clicked");
    });

    $("button").on("touchend mouseup", function () {
        $(this).removeClass("clicked");
    });
});