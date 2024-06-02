function afficherContenuCarte(carte) {
    // Masquer tous les contenus d'information
    document.querySelectorAll(".information").forEach(info => {
        info.style.display = "none";
    });
    document.querySelectorAll(".container_form").forEach(contenu => {
        contenu.style.display = "none";
    });

    // Afficher le contenu spécifique à la carte demandée
    var contenu = document.getElementById(carte + "Content");
    if (contenu) {
        contenu.style.display = "block";
    } else {
        // Si le contenu spécifique à la carte demandée n'existe pas, afficher un message d'erreur
        console.log('Contenu de la carte non trouvé');
    }
}

/***********************************popup piste*****************/
document.querySelector("#show-piste").addEventListener("click",function(){
    document.querySelector(".popupPiste").classList.add("active");


});

document.querySelector(".popupPiste .close-btn").addEventListener("click",function(){
    document.querySelector(".popupPiste").classList.remove("active");
    document.getElementById('trackForm').reset();
});

document.querySelector(".elementPiste button").addEventListener("click",function(){
    document.querySelector(".popupPiste").classList.remove("active");
});

/********************************tableau pistes********************************/
// Tableau pour stocker les pistes
let pistes = [];

// Références aux éléments du formulaire
const formPiste = document.querySelector('.formPiste');
const closeBtn = document.querySelector('.close-btn');
const validerBtn = document.getElementById('submitPiste'); // Modifié l'ID du bouton de validation
const titreInput = document.getElementById('titrePiste'); // Modifié l'ID du champ de titre
const domaineInput = document.getElementById('domainePiste'); // Modifié l'ID du champ de domaine
const sousDomaineInput = document.getElementById('sous-domainePiste'); // Modifié l'ID du champ de sous-domaine
const emailInput = document.getElementById('EmailPiste'); // Modifié l'ID du champ d'email
const enTeteTableau = document.querySelector('#tableauPistes thead');

// Gestionnaire d'événement pour la soumission du formulaire
validerBtn.addEventListener('click', function(event) {
    event.preventDefault(); // Empêche le rechargement de la page

    // Récupère les valeurs saisies par l'utilisateur
    const titre = titreInput.value;
    const domaine = domaineInput.value;
    const sousDomaine = sousDomaineInput.value;
    const email = emailInput.value;

    // Ajoute les informations sur la nouvelle piste au tableau
    pistes.push({
        titre: titre,
        domaine: domaine,
        sousDomaine: sousDomaine,
        email: email
    });

    // Met à jour l'affichage pour refléter les changements
    afficherPistes();

    // Réinitialise les champs du formulaire
    titreInput.value = '';
    domaineInput.value = '';
    sousDomaineInput.value = '';
    emailInput.value = '';
});

// Gestionnaire d'événement pour le bouton de fermeture du formulaire
closeBtn.addEventListener('click', function() {
    // Cache le formulaire
    formPiste.style.display = 'none';
});

// Fonction pour afficher les pistes dans un tableau
function afficherPistes() {
    // Référence à l'élément où afficher les pistes
    const tableauPistes = document.querySelector('#tableauPistes tbody');

    // Vide le contenu actuel du tableau
    tableauPistes.innerHTML = '';

    // Parcourt toutes les pistes dans le tableau et les ajoute au tableau HTML
    pistes.forEach(function(piste) {
        const ligne = document.createElement('tr');
        ligne.innerHTML = `
            <td>${piste.titre}</td>
            <td>${piste.domaine}</td>
            <td>${piste.sousDomaine}</td>
            <td>${piste.email}</td>
        `;
        tableauPistes.appendChild(ligne);
    });

    // Mettre à jour la visibilité de l'en-tête de la table
    if (pistes.length > 0) {
        enTeteTableau.classList.remove('hidden'); // Affiche la rangée de l'en-tête
    } else {
        enTeteTableau.classList.add('hidden'); // Masque la rangée de l'en-tête
    }
}


