document.addEventListener('DOMContentLoaded', function () {
    const filtersButton = document.getElementById('filtersButton');
    const filtersDropdown = document.getElementById('filtersDropdown');

    filtersButton.addEventListener('click', function (e) {
        e.preventDefault();
        filtersDropdown.style.display =
            filtersDropdown.style.display === 'block' ? 'none' : 'block';
    });

    document.addEventListener('click', function (e) {
        if (!filtersButton.contains(e.target) && !filtersDropdown.contains(e.target)) {
            filtersDropdown.style.display = 'none';
        }
    });
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

function applyFiltersAndSearch(event) {
        event.preventDefault(); // Спираме стандартното поведение на формата

        // Вземаме всички избрани филтри
        let filters = [];
        document.querySelectorAll('.filters-dropdown input[type="checkbox"]:checked').forEach(function(checkbox) {
            filters.push(checkbox.value);
        });

        // Вземаме стойността на търсенето
        let searchQuery = document.querySelector('.search-input').value;

        // Създаваме URL с филтрите и търсенето
        let url = new URL(window.location.href);
        let params = new URLSearchParams(url.search);

        // Добавяме параметри за търсенето
        if (searchQuery) {
            params.set('q', searchQuery);
        }

        // Добавяме всички избрани филтри
        filters.forEach(function(filter) {
            params.append('filter', filter);
        });

        // Пренасочваме към новия URL
        window.location.href = url.pathname + '?' + params.toString();
    }

document.addEventListener("DOMContentLoaded", function() {
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.onsubmit = applyFiltersAndSearch;
    }
});
