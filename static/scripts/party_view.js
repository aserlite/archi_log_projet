function ajouterLigneParticipant(id, pseudo) {
    const tbody = document.getElementById("participants-list");
    const ligne = document.createElement("tr");
    ligne.id = id;
    ligne.innerHTML = `
        <td>${pseudo}</td>
        <td>0</td>
        <td>0.00 ‰</td>
    `;
    tbody.appendChild(ligne);
}

function verifierNouveauxParticipants(partyId) {
    fetch(`/api/participants/${partyId}`)
        .then(response => response.json())
        .then(data => {
            if (data.participants && Array.isArray(data.participants)) {
                data.participants.forEach(p => {
                    if (!document.getElementById(p.id)) {
                        ajouterLigneParticipant(p.id, p.pseudo);
                    }
                });
            } else {
                console.error("Format inattendu :", data);
            }
        })
        .catch(err => console.error("Erreur récupération des participants :", err));
}

const partyId = Number(document.querySelector("input[name='party_id']").value);
verifierNouveauxParticipants(partyId); // Au chargement
setInterval(() => {
    verifierNouveauxParticipants(partyId);
}, 30000);




// Ajout d'une consommation
document.getElementById('add-conso-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const form = this;
    const data = new FormData(form);
    fetch(form.action, {
        method: 'POST',
        body: data,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                console.log(result)
                const tableau_participants = document.getElementById('participants-list')
                let existingRow = document.getElementById(result.id); 

                if (existingRow) {
                    existingRow.cells[1].textContent = result.new_count;
                } else {
                    const newRow = document.createElement('tr');
                    newRow.id = result.id;

                    const nameCell = document.createElement('td');
                    nameCell.textContent = result.pseudo;

                    const countCell = document.createElement('td');
                    countCell.textContent = result.new_count;

                    newRow.appendChild(nameCell);
                    newRow.appendChild(countCell);

                    tableau_participants.appendChild(newRow);
                }
            }
        })
});


// function mettreAJourMonTaux(userId) {
//     fetch('/party/write_taux')
//         .then(response => response.json())
//         .then(data => {
//             if (typeof data.taux !== "number") {
//                 console.warn("Taux non valide :", data);
//                 return;
//             }

//             const ligne = document.getElementById(String(userId));
//             if (ligne && ligne.cells.length >= 3) {
//                 ligne.cells[2].textContent = data.taux.toFixed(2) + " ‰";
//             } else {
//                 console.warn("Ligne introuvable pour userId :", userId);
//             }
//         })
//         .catch(error => console.error('Erreur lors de la mise à jour du taux perso :', error));
// }

// const userIdInput = document.querySelector("input[name='user_id']");
// const userId = userIdInput ? Number(userIdInput.value) : null;

// if (userId) {
//     mettreAJourMonTaux(userId);
//     setInterval(() => {
//         mettreAJourMonTaux(userId);
//     }, 30000);
// } else {
//     console.error("Champ caché user_id non trouvé ou invalide.");
// }




// Ajax pour chercher une boisson
document.getElementById('drink-search').addEventListener('input', function () {
    const query = this.value;
    const suggestionsDiv = document.getElementById('drink-suggestions');
    if (query.length < 1) {
        suggestionsDiv.innerHTML = '';
        return;
    }
    fetch('/drinks/search?q=' + encodeURIComponent(query))
        .then(response => response.json())
        .then(data => {
            let suggestions = data.drinks.map(drink =>
                `<a href="#" class="list-group-item list-group-item-action drink-suggestion" data-id="${drink.id}">${drink.nom}</a>`
            ).join('');
            if (data.drinks.length === 0) {
                suggestions += `<a href="/drinks/create" class="list-group-item list-group-item-action text-success">Ajouter "${query}"</a>`;
            }
            suggestionsDiv.innerHTML = suggestions;
        });
});

document.getElementById('drink-suggestions').addEventListener('click', function (e) {
    if (e.target && e.target.matches('a[data-id]')) {
        e.preventDefault();
        document.getElementById('drink-search').value = e.target.textContent;
        document.getElementById('selected-drink-id').value = e.target.getAttribute('data-id');
        this.innerHTML = '';
    }
});

function updatePartyStats() {
    const partyId = document.querySelector('input[name="party_id"]').value;
    fetch(`/party/${partyId}/stats`)
        .then(response => response.json())
        .then(data => {
            const statsList = document.getElementById('party-stats');
            if (statsList) {
                statsList.innerHTML = data.stats.map(
                    stat => `<li>${stat.user} : ${stat.count} verres</li>`
                ).join('');
            }
        });
}

updatePartyStats();
setInterval(updatePartyStats, 5000);