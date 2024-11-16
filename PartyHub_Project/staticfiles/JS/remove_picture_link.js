
    // This is how i remove the link to the profile picture becouse i dont think the user should see it!!!
    // Изберете параграфа, съдържащ линка и полето за избор на файл
    const profileContainer = document.getElementById('picture-form-id');
    {/*// Премахнете линка и текста "Currently:"*/}
    const link = profileContainer.querySelector('a');
    const currentText = profileContainer.querySelector('br');
    const p_tag = profileContainer.querySelector('p');
    const input_form = p_tag.querySelector('input');
    p_tag.textContent = 'Change: '
    p_tag.appendChild(input_form)
    if (link) {
        link.remove();  // Премахва линка
    }

    if (currentText) {
        currentText.remove();  // Премахва <br> елемента
    }
