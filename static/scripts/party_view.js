// Ajout d'une consommation (protégé si le formulaire existe)
const addConsoForm = document.getElementById('add-conso-form');
const drink_search = document.getElementById('drink-search');
if (addConsoForm) {
    if(drink_search != ""){}
    addConsoForm.addEventListener('submit', function (e) {
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
                    form.reset();
                    document.getElementById('add_button').textContent = 'Verre ajouté !';
                    setTimeout(() => {
                        document.getElementById('add_button').textContent = 'Ajouter un verre';

                    }, 2000);
                    updatePartyStats();
                    updateHistoryTable();
                }
            });
    });
}

// Ajax pour chercher une boisson (protégé si le champ existe)
const drinkSearch = document.getElementById('drink-search');
if (drinkSearch) {
    drinkSearch.addEventListener('input', function () {
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
                    `<br><a href="#" class="list-group-item list-group-item-action drink-suggestion" data-id="${drink.id}">${drink.nom}</a> <br>`
                ).join('');
                if (data.drinks.length === 0) {
                    suggestions += `<a href="/drinks/create" class="list-group-item list-group-item-action text-success">Ajouter "${query}"</a>`;
                }
                suggestionsDiv.innerHTML = suggestions;
            });
    });
}

const drinkSuggestions = document.getElementById('drink-suggestions');
if (drinkSuggestions) {
    drinkSuggestions.addEventListener('click', function (e) {
        if (e.target && e.target.matches('a[data-id]')) {
            e.preventDefault();
            document.getElementById('drink-search').value = e.target.textContent;
            document.getElementById('selected-drink-id').value = e.target.getAttribute('data-id');
            this.innerHTML = '';
        }
    });
}

function updateHistoryTable() {
    const partyIdInput = document.querySelector('input[name="party_id"]');
    const userIdInput = document.querySelector('input[name="user_id"]');
    if (!partyIdInput) return;
    const partyId = partyIdInput.value;
    const userID = userIdInput.value;
    const isFinished = window.partyStatus === "finished";
    fetch(`/party/${partyId}/history`)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('history-table-body');
            if (tbody && data.success) {
                tbody.innerHTML = data.consumption.map(c => {
                    const isUser = userID == c[0];
                    return `
                        <tr>
                            <td>${c[1]}</td>
                            <td>${c[2]}</td>
                            <td>${formatHour(c[3])}</td>
                            <td>${c[4]}</td>
                            <td>${c[5]}</td>
                            ${(!isFinished && isUser) ? `
                                <td>
                                    <form action="/party/delete_conso" method="post">
                                        <input type="hidden" name="id_user" value="${c[0]}">
                                        <input type="hidden" name="id_soiree" value="${c[6]}">
                                        <input type="hidden" name="id_boisson" value="${c[7]}">
                                        <input type="hidden" name="timestamp" value="${formatToSQLDateTimeParis(c[3])}">
                                        <button type="submit" class="btn btn-sm btn-danger">Supprimer</button>
                                    </form>
                                </td>` : ''
                        }
                        </tr>
                    `;
                }).join('');
            }
        });

    const table = document.querySelector('#cell-historique table');
    if (table) {
        const ths = table.querySelectorAll('th');
        if (ths.length > 5) {
            ths[5].style.display = isFinished ? 'none' : '';
        }
        const trs = table.querySelectorAll('tbody tr');
        trs.forEach(tr => {
            const tds = tr.querySelectorAll('td');
            if (tds.length > 5) {
                tds[5].style.display = isFinished ? 'none' : '';
            }
        });
    }
}

function formatToSQLDateTimeParis(dateString) {
    const date = new Date(dateString);

    const formatter = new Intl.DateTimeFormat('fr-FR', {
        timeZone: 'Europe/Paris',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });

    const parts = formatter.formatToParts(date);
    const get = type => parts.find(p => p.type === type).value;

    return `${get('year')}-${get('month')}-${get('day')} ${get('hour') - 2}:${get('minute')}:${get('second')}`;
}


function updatePartyStats() {
    const partyIdInput = document.querySelector('input[name="party_id"]');
    if (!partyIdInput) return;
    const partyId = partyIdInput.value;
    const currentUserId = document.body.getAttribute('data-user-id');
    const tbody = document.querySelector('#cell-participants table tbody');
    fetch(`/party/${partyId}/stats`)
        .then(response => response.json())
        .then(data => {
            if (tbody && data.stats) {
                tbody.innerHTML = data.stats.map(
                    stat => `<tr${stat.user_id == currentUserId ? ' class="current-user-row"' : ''}>
                        <td>${stat.user}</td>
                        <td>${stat.count}</td>
                        <td>${stat.alcoolemie.taux ?? '-'}</td>
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

document.addEventListener('DOMContentLoaded', function () {
    const randomBtn = document.getElementById('random-drink-btn');
    if (randomBtn) {
        randomBtn.addEventListener('click', function () {
            fetch('/drinks/search?q=')
                .then(response => response.json())
                .then(data => {
                    if (data.drinks && data.drinks.length > 0) {
                        const random = data.drinks[Math.floor(Math.random() * data.drinks.length)];
                        document.getElementById('drink-search').value = random.nom;
                        document.getElementById('selected-drink-id').value = random.id;
                        document.getElementById('drink-suggestions').innerHTML = '';
                    }
                });
        });
    }
});

// Copier le code d'invitation dans le presse-papier
const copyButton = document.getElementById('logo_copier');
const code = document.getElementById('party-invitation-code');
const pathPrimary = document.getElementById('primary');

copyButton.addEventListener('click', function () {
    if (navigator.clipboard && code) {
        navigator.clipboard.writeText(code.textContent.trim())
            .then(() => {
                if (pathPrimary) {
                    pathPrimary.removeAttribute('stroke');
                    pathPrimary.setAttribute('fill', '#fff');
                }
            })
            // revient à la normal au bout de 5 secondes
            .then(() => {
                setTimeout(() => {
                    if (pathPrimary) {
                        pathPrimary.setAttribute('stroke', '#fff');
                        pathPrimary.setAttribute('fill', 'none');
                    }
                }, 2000);
            })
            .catch(err => {
                console.error('Erreur de copie :', err);
            });
    }
});
