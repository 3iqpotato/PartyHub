document.getElementById('filtersButton').addEventListener('click', function (event) {
    // Спираме стандартното поведение на бутона за филтри
    event.preventDefault(); // Това предотвратява изпращането на формата и рефреша на страницата

    const filtersDropdown = document.getElementById('filtersDropdown');
    filtersDropdown.style.display = filtersDropdown.style.display === 'block' ? 'none' : 'block';
});

// Скриване на филтрите при натискане извън тях
document.addEventListener('click', function (event) {
    if (!event.target.closest('.filters-container')) {
        document.getElementById('filtersDropdown').style.display = 'none';
    }
});

// Обработваме натискането на бутона за търсене
document.querySelector('.search-button').addEventListener('click', function (event) {
    // Няма нужда да спираме рефреша за търсенето, защото искаме да изпратим формата
    document.getElementById('searchForm').submit(); // Изпращаме формата ръчно
});


document.addEventListener('DOMContentLoaded', function () {
    const filtersCheckboxes = document.querySelectorAll('input[type="checkbox"][name="filter"]');

    filtersCheckboxes.forEach((checkbox) => {
        checkbox.addEventListener('change', function () {
            if (this.checked) {
                filtersCheckboxes.forEach((otherCheckbox) => {
                    if (otherCheckbox !== this) {
                        otherCheckbox.checked = false;
                    }
                });
            }
        });
    });
});
