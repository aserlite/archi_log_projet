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
            }
        })
});

// Ajax pour chercher une boisson
document.getElementById('drink-search').addEventListener('input', function () {
    const query = this.value;
    if (query.length < 1) {
        document.getElementById('drink-suggestions').innerHTML = '';
        return;
    }
    fetch('/drinks/search?q=' + encodeURIComponent(query))
        .then(response => response.json())
        .then(data => {
            const suggestions = data.drinks.map(drink =>
                `<a href="#" class="list-group-item list-group-item-action drink-suggestion" data-id="${drink.id}">${drink.nom}</a>`
            ).join('');
            document.getElementById('drink-suggestions').innerHTML = suggestions;
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