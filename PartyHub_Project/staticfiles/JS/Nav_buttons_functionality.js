    document.querySelector('.dropbtn').addEventListener('click', function(event) {
        var dropdownContent = document.querySelector('.dropdown-content');

        // Превключваме показването на падащото меню
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';

        // Спираме нормалното поведение на линка, за да не се презарежда страницата
        event.preventDefault();
    });