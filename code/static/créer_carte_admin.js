
document.addEventListener('DOMContentLoaded', () => {
    const createCategoryForm = document.getElementById('create-category-form');
    const saveCardButton = document.getElementById('save-card-button');
    const addFieldButton = document.getElementById('add-field-button');
    const fieldsContainer = document.getElementById('fields-container');

    // Ajouter un champ au formulaire
    addFieldButton.addEventListener('click', () => {
        const fieldGroup = document.createElement('div');
        fieldGroup.classList.add('form-row', 'field-group');
        fieldGroup.innerHTML = `
            <div class="form-row">
                <div class="input-data">
                    <input type="text" class="field-name" required>
                    <label>Nom de Champ</label>
                    <div class="underline"></div>
                </div>
                <div class="input-data">
                    <select class="field-type" required>
                        <option value="" disabled selected>Choisissez le type de champ</option>
                        <option value="text">Texte</option>
                        <option value="number">Nombre</option>
                        <option value="email">Email</option>
                        <option value="address">Adresse</option>
                        <option value="date">Date</option>
                        <option value="table">Tableau</option>
                    </select>
                    <div class="underline"></div>
                </div>
            </div>
            <button type="button" class="remove-field" onclick="removeField(this)">Supprimer</button>
        `;
        fieldsContainer.appendChild(fieldGroup);
    
    });


// Fonction pour supprimer un champ avec confirmation
window.removeField = function(button) {
const fieldGroup = button.parentElement;
if (confirm('Êtes-vous sûr de vouloir supprimer ce champ ?')) {
    if (fieldGroup) {
        fieldGroup.remove();
    }
}
};

// Enregistrer la carte
saveCardButton.addEventListener('click', (e) => {
e.preventDefault(); // Empêcher la soumission par défaut

const cardName = document.getElementById('category-name').value.trim();

// Inclure les champs initiaux et dynamiquement ajoutés
const fieldGroups = document.querySelectorAll('.field-group');
const fields = Array.from(fieldGroups).map(group => ({
name: group.querySelector('.field-name').value.trim(),
type: group.querySelector('.field-type').value
}));

if (cardName && fields.every(field => field.name && field.type)) {
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
    // Ici, ajoutez le code pour afficher les cartes existantes si nécessaire
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