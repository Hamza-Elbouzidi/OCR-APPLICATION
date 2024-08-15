// Sélectionner tous les boutons d'action dans les cartes
document.addEventListener('DOMContentLoaded', () => {
    // Bouton de modification
    document.querySelectorAll('.card .edit-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const card = e.target.closest('.card');
            // Implémentez ici la logique de modification (ex. ouvrir un formulaire de modification)
            alert(`Modifier la carte : ${card.dataset.cardTitle}`);
        });
    });

    // Bouton de suppression
    document.querySelectorAll('.card .delete-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const card = e.target.closest('.card');
            // Afficher la boîte de confirmation de suppression
            document.getElementById('confirm-delete-dialog').style.display = 'block';

            // Confirmer la suppression
            document.getElementById('delete-yes').addEventListener('click', () => {
                // Implémentez ici la logique de suppression
                card.remove();
                document.getElementById('confirm-delete-dialog').style.display = 'none';
            });

            // Annuler la suppression
            document.getElementById('delete-no').addEventListener('click', () => {
                document.getElementById('confirm-delete-dialog').style.display = 'none';
            });
        });
    });

    // Bouton de changement de couleur
    document.querySelectorAll('.card .color-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const card = e.target.closest('.card');
            // Implémentez ici la logique de changement de couleur (ex. ouvrir une palette de couleurs)
            const newColor = prompt('Entrez la nouvelle couleur en hex (ex. #FF5733) :');
            if (newColor) {
                card.style.backgroundColor = newColor;
            }
        });
    });
});

// Fonction pour sélectionner une carte
function selectCard(cardElement) {
    // Implémentez ici la logique pour sélectionner une carte (ex. affichage des détails)
    alert(`Carte sélectionnée : ${cardElement.dataset.cardTitle}`);
}
