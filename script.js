/* ==========================================================================
   1. STRUCTURE DE DONNÉES (JSON-like)
   Critère : "Les données ne sont pas codées en dur dans le HTML"
   ========================================================================== */
const portfolioData = {
    competences: [
        { nom: "Python (Automatisation)", type: "dev" },
        { nom: "HTML5 / CSS3 / JS", type: "dev" },
        { nom: "Git & GitHub", type: "dev" },
        { nom: "Analyse de fiabilité (FMDS)", type: "indus" },
        { nom: "Expertise Excel / VBA", type: "indus" },
        { nom: "Maintenance Prédictive", type: "indus" }
    ]
};

/* ==========================================================================
   2. AFFICHAGE DYNAMIQUE & FILTRAGE
   Critère : "Implémentation d’une fonctionnalité de filtrage"
   ========================================================================== */
function afficherCompetences(filtre = 'all') {
    const container = document.getElementById('skills-container');
    container.innerHTML = ''; // On vide le conteneur avant de remplir

    // Création des colonnes pour garder la mise en page
    let htmlContent = `
        <div class="skill-column">
            <h3>Liste filtrée : ${filtre.toUpperCase()}</h3>
            <ul>
    `;

    // Boucle sur les données
    portfolioData.competences.forEach(skill => {
        // Condition de filtrage : Si 'all' OU si le type correspond
        if (filtre === 'all' || skill.type === filtre) {
            htmlContent += `<li>✅ ${skill.nom}</li>`;
        }
    });

    htmlContent += `</ul></div>`;
    container.innerHTML = htmlContent;

    // Gestion de l'état "Actif" des boutons (Bonus UX)
    document.querySelectorAll('.btn-filter').forEach(btn => {
        btn.classList.remove('active');
        if(btn.getAttribute('onclick').includes(filtre)) {
            btn.classList.add('active');
        }
    });
}

// Fonction globale pour être appelée depuis le HTML
window.filtrerCompetences = afficherCompetences;

/* ==========================================================================
   3. GESTION DU FORMULAIRE DE CONTACT
   Critère : "Validation simple et messages de retour"
   ========================================================================== */
document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche le rechargement de la page

    // 1. Lecture des valeurs
    const nom = document.getElementById('nom').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    const feedback = document.getElementById('form-feedback');

    // 2. Validation simple
    if (!nom || !email || !message) {
        feedback.style.display = 'block';
        feedback.style.color = '#f85149'; // Rouge
        feedback.innerText = "❌ Erreur : Tous les champs sont obligatoires.";
        return;
    }

    if (!email.includes('@')) {
        feedback.style.display = 'block';
        feedback.style.color = '#f85149';
        feedback.innerText = "❌ Erreur : Format d'email invalide.";
        return;
    }

    // 3. Stockage temporaire (Simulation d'envoi)
    const nouveauMessage = {
        auteur: nom,
        contact: email,
        contenu: message,
        date: new Date().toLocaleDateString()
    };
    console.log("Message reçu :", nouveauMessage); // Visible dans la console (F12)

    // 4. Feedback Succès
    feedback.style.display = 'block';
    feedback.style.color = '#3fb950'; // Vert
    feedback.innerText = `✅ Merci ${nom} ! Votre message a bien été simulé.`;
    
    // Reset du formulaire
    document.getElementById('contact-form').reset();
});

/* ==========================================================================
   4. SIMULATEUR
   ========================================================================== */
let uptime = 100;

window.simulerPanne = function() {
    uptime -= (Math.random() * 5).toFixed(2);
    updateDisplay("EN PANNE", "#e74c3c");
}

window.maintenir = function() {
    uptime = 100;
    updateDisplay("OPÉRATIONNEL", "#3fb950");
}

function updateDisplay(statusText, color) {
    const dispoEl = document.getElementById('dispo-val');
    const statusEl = document.getElementById('sys-status');
    if (dispoEl && statusEl) {
        dispoEl.innerText = Math.max(0, uptime).toFixed(2);
        statusEl.innerText = statusText;
        statusEl.style.color = color;
    }
}

/* ==========================================================================
   INITIALISATION
   ========================================================================== */
// On lance l'affichage au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    afficherCompetences('all');
});