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
                updatePartyStats();
                updateHistoryTable();
            }
        });
});

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

function updateHistoryTable() {
    const partyId = document.querySelector('input[name="party_id"]').value;
    fetch(`/party/${partyId}/history`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('history-table-body');
            if (tbody && data.success) {
                tbody.innerHTML = data.consumption.map(
                    c => `<tr>
                        <td>${c[0]}</td>
                        <td>${c[1]}</td>
                        <td>${formatHour(c[2])}</td>
                        <td>${c[3]}</td>
                        <td>${c[4]}</td>
                    </tr>`
                ).join('');
            }
        });
}


function updatePartyStats() {
    const partyId = document.querySelector('input[name="party_id"]').value;
    const currentUserId = document.body.getAttribute('data-user-id');
    fetch(`/party/${partyId}/stats`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.querySelector('#cell-participants table tbody');
            if (tbody && data.stats) {
                tbody.innerHTML = data.stats.map(
                    stat => `<tr${stat.user_id == currentUserId ? ' class="current-user-row"' : ''}>
                        <td>${stat.user}</td>
                        <td>${stat.count}</td>
                        <td>${stat.alcoolemie ?? '-'}</td>
                    </tr>`
                ).join('');
            }
            const statsList = document.getElementById('party-stats');
            if (statsList) {
                statsList.innerHTML = data.stats.map(
                    stat => `<li>${stat.user} : ${stat.count} verres</li>`
                ).join('');
            }
        });
}

updatePartyStats();
updateHistoryTable();
setInterval(updatePartyStats, 5000);
setInterval(updateHistoryTable, 5000);

function formatHour(dateString) {
    const date = new Date(dateString);
    const hours = String(date.getUTCHours()).padStart(2, '0');
    const minutes = String(date.getUTCMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
}