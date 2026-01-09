/* ==========================================================================
   1. DONNÉES (DATA) - STRUCTURE OBJET/TABLEAU
   Critère : "Les données ne sont pas codées en dur dans le HTML"
   ========================================================================== */
const portfolioData = {
    competences: [
        { nom: "Python (Automatisation)", type: "dev" },
        { nom: "HTML5 / CSS3 / JS", type: "dev" },
        { nom: "Unity / C#", type: "dev" },
        { nom: "Git & GitHub", type: "dev" },
        { nom: "Analyse de fiabilité (FMDS)", type: "indus" },
        { nom: "Expertise Excel / VBA", type: "indus" },
        { nom: "SIG (QGIS / GFI)", type: "indus" }
    ],
    experiences: [
        { 
            annee: 2023, titre: "Technicien Bureau d'Étude", entreprise: "Eiffage", 
            desc: "<strong>Gestion de Données :</strong> Bases techniques (APCOM).<br>• <strong>SIG :</strong> Analyse réseaux QGIS.", categorie: "indus" 
        },
        { 
            annee: 2018, titre: "Technicien de Maintenance", entreprise: "Envie Var", 
            desc: "<strong>Diagnostic :</strong> Détection de pannes.<br>• <strong>Maintenance :</strong> Réparation complexe.", categorie: "indus" 
        },
        { 
            annee: 2013, titre: "Ingénieur Fiabilité (SDF)", entreprise: "Studec", 
            desc: "<strong>Analyse :</strong> Calculs de disponibilité Excel.", categorie: "indus" 
        },
        { 
            annee: 2011, titre: "Ingénieur Apprenti RAMS", entreprise: "Alstom", 
            desc: "<strong>Modélisation :</strong> Fiabilité prédictive.", categorie: "indus" 
        }
    ],
    projets: [
        { titre: "Snake Game Python", desc: "Jeu en POO avec Pygame.", tech: "Python" },
        { titre: "Portfolio Dynamique", desc: "Interface web JS/CSS.", tech: "HTML / JS" },
        { titre: "Prototype Unity 6", desc: "Physique 3D & C#.", tech: "C# / Unity" }
    ]
};

/* ==========================================================================
   2. FONCTIONS D'AFFICHAGE & TRI
   Critère : "Affichage dynamique" + "Fonctionnalité de filtrage/tri"
   ========================================================================== */

function afficherParcours(tri = 'date') {
    const container = document.getElementById('timeline-container');
    if (!container) return;
    container.innerHTML = '';
    
    // Copie pour ne pas modifier l'original
    let data = [...portfolioData.experiences];

    // Logique de tri
    if (tri === 'entreprise') data.sort((a, b) => a.entreprise.localeCompare(b.entreprise));
    else if (tri === 'poste') data.sort((a, b) => a.titre.localeCompare(b.titre));
    else data.sort((a, b) => b.annee - a.annee);

    // Injection dans le DOM
    data.forEach(exp => {
        const div = document.createElement('div');
        div.className = 'exp-card-vertical';
        div.innerHTML = `
            <div class="exp-date-box">${exp.annee}</div>
            <div class="exp-info">
                <h4>${exp.titre} <span class="ent-label">@ ${exp.entreprise}</span></h4>
                <p>${exp.desc}</p>
            </div>
        `;
        container.appendChild(div);
    });

    // Critère : "Gestion d'un état simple" (bouton actif)
    document.querySelectorAll('.btn-sort').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('onclick').includes(tri));
    });
}

function afficherProjets() {
    const container = document.getElementById('projets-container');
    if (!container) return;
    container.innerHTML = portfolioData.projets.map(p => `
        <div class="project-item">
            <h4 style="color:var(--accent-blue)">${p.titre}</h4>
            <p>${p.desc}</p>
            <span class="tag-tech">${p.tech}</span>
        </div>
    `).join('');
}

function filtrerCompetences(filtre = 'all') {
    const container = document.getElementById('skills-container');
    if (!container) return;
    container.innerHTML = '';
    
    portfolioData.competences.forEach(s => {
        if (filtre === 'all' || s.type === filtre) {
            container.innerHTML += `<div class="skill-item">✅ ${s.nom}</div>`;
        }
    });

    // Gestion de l'état actif des boutons
    document.querySelectorAll('.btn-filter').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('onclick').includes(filtre));
    });
}

/* ==========================================================================
   3. GESTION DU FORMULAIRE
   Critère : "Lecture, Stockage, Validation, Messages"
   ========================================================================== */
document.addEventListener('DOMContentLoaded', () => {
    // Initialisation des données
    afficherParcours();
    afficherProjets();
    filtrerCompetences('all');

    const form = document.getElementById('contact-form');
    if(form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault(); // Empêche le rechargement
            
            // 1. Lecture des valeurs
            const nom = document.getElementById('nom').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            const feedback = document.getElementById('form-feedback');

            // 2. Validation simple
            if(nom.length < 2 || !email.includes('@')) {
                feedback.style.display = 'block';
                feedback.style.color = 'var(--accent-red)';
                feedback.innerText = "❌ Erreur : Veuillez vérifier votre nom ou email.";
                return;
            }

            // 3. Stockage temporaire (Simulation d'envoi)
            const messageData = {
                auteur: nom,
                contact: email,
                contenu: message,
                date: new Date().toISOString()
            };
            console.log("📨 Message stocké temporairement :", messageData);

            // 4. Message de retour utilisateur
            feedback.style.display = 'block';
            feedback.style.color = 'var(--accent-green)';
            feedback.innerText = `✅ Merci ${nom}, votre message a été simulé avec succès !`;
            
            form.reset();
            
            // Masquer le message après 3 secondes
            setTimeout(() => { feedback.style.display = 'none'; }, 3000);
        });
    }
});

/* ==========================================================================
   4. EXPORT FONCTIONS POUR HTML (Global Scope)
   ========================================================================== */
window.trierParcours = afficherParcours;
window.filtrerCompetences = filtrerCompetences;

// Simulateur de disponibilité
let uptime = 100;
window.simulerPanne = () => {
    uptime -= (Math.random() * 5);
    document.getElementById('dispo-val').innerText = Math.max(0, uptime).toFixed(2);
    const status = document.getElementById('sys-status');
    status.innerText = "ALERTE SYSTÈME";
    status.style.color = "var(--accent-red)";
};
window.maintenir = () => {
    uptime = 100;
    document.getElementById('dispo-val').innerText = "100.00";
    const status = document.getElementById('sys-status');
    status.innerText = "SYSTÈME OPÉRATIONNEL";
    status.style.color = "var(--accent-green)";
};