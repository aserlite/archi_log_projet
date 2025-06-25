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
                document.getElementById('quantity').value = 1;
                document.getElementById('comment').value = '';
                document.getElementById('drink-count').textContent = result.new_count;
                updateHistoryTable();
            }
        })
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
                    </tr>`
                ).join('');
            }
        });
}


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
updateHistoryTable();
setInterval(updatePartyStats, 5000);
setInterval(updateHistoryTable, 5000);

function formatHour(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
}