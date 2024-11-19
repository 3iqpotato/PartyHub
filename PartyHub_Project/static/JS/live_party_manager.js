
document.addEventListener('DOMContentLoaded', () => {
        const csrfToken = '{{ csrf_token }}';

        async function handleButtonClick(event) {
            event.preventDefault();

            const button = event.target;
            const form = button.closest('.attendance-form');
            const ticketId = form.dataset.ticketId;
            const actionUrl = form.dataset.action;

            try {
                const response = await fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ ticket_id: ticketId }),
                });

                if (response.ok) {
                    const data = await response.json();
                    moveTicket(data.ticket, button);
                } else {
                    console.error('Error:', response.statusText);
                }
            } catch (error) {
                console.error('Request failed:', error);
            }
        }

        function moveTicket(ticket, button) {
            const currentList = button.closest('ul');
            const otherList = currentList.closest('.attendance-list').nextElementSibling?.querySelector('ul')
                || currentList.closest('.attendance-list').previousElementSibling?.querySelector('ul');
            if (!otherList) return;

            // Премахваме текущия елемент
            const listItem = button.closest('li');
            currentList.removeChild(listItem);

            // Променяме атрибутите на формата и бутона
            const form = listItem.querySelector('.attendance-form');
            form.dataset.action = ticket.new_action_url;

            const newButton = form.querySelector('button');
            newButton.textContent = ticket.new_button_text;

            // Проверка на класовете
            const oldButton = listItem.querySelector('button');

            if (oldButton.classList.contains('status-button')) {
                newButton.classList.add('status-button1');
                newButton.classList.remove('status-button');
            } else {
                newButton.classList.add('status-button');
                newButton.classList.remove('status-button1');
            }

            // Добавяме елемента към другия списък
            otherList.appendChild(listItem);
        }

        function attachButtonListeners() {
            const buttons = document.querySelectorAll('.attendance-form button');
            buttons.forEach(button => {
                button.removeEventListener('click', handleButtonClick); // Премахваме стари слушатели
                button.addEventListener('click', handleButtonClick);   // Добавяме нови слушатели
            });
        }

        // Присвояваме слушатели при първоначално зареждане
        attachButtonListeners();
    });
