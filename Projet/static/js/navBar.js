let list = document.querySelectorAll(".navigation li");

function activatelink() {
    list.forEach((item) => {
        item.classList.remove("hovered");
    });
    this.classList.add("hovered");
}
list.forEach((item) => item.addEventListener("mouseover", activatelink));

let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");
let topbar = document.querySelector(".topbar"); 

const soumissionsMain = document.querySelector("#soumissionsContent .main");
const programmeMain = document.querySelector("#programmeContent .main");
const parametresMain = document.querySelector("#parametresContent .main");
const statistiquesMain = document.querySelector("#statistiquesContent .main");

toggle.onclick = function () {
    navigation.classList.toggle("active");
    main.classList.toggle("active");
    topbar.classList.toggle("active"); // Ajouter ou retirer la classe "active" du topbar en fonction de l'état de la navigation
    if (!navigation.classList.contains("active")) {
        topbar.classList.add("active");
        soumissionsMain.classList.add("active");
        programmeMain.classList.add("active");
        parametresMain.classList.add("active");
        statistiquesMain.classList.add("active");
    } else {
        topbar.classList.remove("active"); 
        soumissionsMain.classList.remove("active");
        programmeMain.classList.remove("active");
        parametresMain.classList.remove("active");
        statistiquesMain.classList.remove("active");
    }
};

// Ajouter un gestionnaire d'événements au toggle de la topbar
toggle.addEventListener("click", () => {
    topbar.classList.toggle("active");
    const soumissionsMain = document.querySelector("#soumissionsContent .main");
    const programmeMain = document.querySelector("#programmeContent .main");
    const parametresMain = document.querySelector("#parametresContent .main");
    const statistiquesMain = document.querySelector("#statistiquesContent .main");
    if (topbar.classList.contains("active")) {
        soumissionsMain.classList.add("active"); // Désactiver le main dans soumissionsContent lorsque la topbar est ouverte
        programmeMain.classList.add("active");
        parametresMain.classList.add("active"); 
        statistiquesMain.classList.add("active");

    }else{
        soumissionsMain.classList.remove("active");
        programmeMain.classList.remove("active");
        parametresMain.classList.remove("active");
        statistiquesMain.classList.remove("active");
    }
});

/********************************/
const cardEls = document.querySelectorAll(".card");
cardEls.forEach(cardEl =>{
    cardEl.addEventListener('click',() => {
        document.querySelector('.active')?.classList.remove('active');
        cardEl.classList.add('active');
    })
});

/************************************************************/
/*
function afficherContenu(page) {
    var contenuPrincipal = document.getElementById('contenuPrincipal');
    
    // Masquer tous les contenus de page
    document.querySelectorAll("#contenuPrincipal > div").forEach(div => {
      div.style.display = "none";
    });
  
    // Afficher le contenu de la page demandée
    var contenu = document.getElementById(page + "Content");
    if (contenu) {
      contenu.style.display = "block";
    } else {
      // Si la page demandée n'existe pas, afficher un message d'erreur
      contenuPrincipal.innerHTML = 'Page non trouvée';
    }
  }
  */

  function afficherContenu(page) {
    // Masquer tous les contenus de page
    document.querySelectorAll("#contenuPrincipal > div").forEach(div => {
        div.style.display = "none";
    });

    // Afficher le contenu de la page demandée
    var contenu = document.getElementById(page + "Content");
    if (contenu) {
        contenu.style.display = "block";
    } else {
        // Si la page demandée n'existe pas, afficher un message d'erreur
        console.log('Page non trouvée');
    }
}

// Ajoutez des gestionnaires d'événements pour les liens de navigation
document.querySelectorAll('.navigation a').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Empêche le comportement par défaut du lien
        var page = this.getAttribute('data-page'); // Récupère l'attribut data-page du lien
        afficherContenu(page); // Affiche le contenu de la page correspondante
    });
});

// Sélectionnez le lien pour ajouter un nouveau membre par son identifiant
const lienAjoutMembre = document.getElementById("lienAjoutMembre");

// Ajoutez un gestionnaire d'événements pour le clic sur le lien
lienAjoutMembre.addEventListener("click", function(event) {
    event.preventDefault(); // Empêcher le comportement par défaut du lien (rechargement de la page)
    
    // Ajoutez ici le code pour effectuer d'autres actions lorsque le lien est cliqué
    // Par exemple, ouvrir une modale, charger des données supplémentaires via AJAX, etc.
});

