document.addEventListener("DOMContentLoaded", function() {
    // Избор на всички div с клас 'form-group'
    var formGroups = document.querySelectorAll('.form-group');

    // Проверка дали имаме поне 5 елемента
    if (formGroups.length >= 5) {
        var targetDiv = formGroups[4]; // Избира 5-тия div (индекс 4)

        // Премахване на съдържанието на 5-тия div
        targetDiv.innerHTML = '';

        // Вмъкване само на нужния label и input
        var changeLabel = document.createElement('label');
        changeLabel.setAttribute('for', 'id_picture');
        changeLabel.textContent = 'Change:';

        var changeInput = document.createElement('input');
        changeInput.setAttribute('type', 'file');
        changeInput.setAttribute('name', 'picture');
        changeInput.setAttribute('class', 'form-control-file');
        changeInput.setAttribute('aria-describedby', 'id_picture_helptext');
        changeInput.setAttribute('id', 'id_picture');

        targetDiv.appendChild(changeLabel);
        targetDiv.appendChild(changeInput);
    }
});

