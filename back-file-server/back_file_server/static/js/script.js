// Обработчик контекстного меню
document.addEventListener("DOMContentLoaded", function() {
    // Находим элемент, на котором будем ловить правый клик
    const Elements = document.querySelectorAll(".has-context-menu");

    // Обработчик правого клика
    Elements.forEach(element => { element.addEventListener("contextmenu", function(event) {
        event.preventDefault();  // Отменяем стандартное контекстное меню
        const fileId = element.getAttribute('data-file-id');
        const folderId = element.getAttribute('data-folder-id');
        var address = ''
        // Например, вы можете создать кастомное контекстное меню:
        const contextMenu = document.createElement('div');
        contextMenu.style.position = 'absolute';
        contextMenu.style.left = event.pageX + 'px';
        contextMenu.style.top = event.pageY + 'px';
        contextMenu.style.background = '#fff';
        contextMenu.style.border = '1px solid #ccc';
        contextMenu.style.boxShadow = '0px 2px 5px rgba(0,0,0,0.15)';
        contextMenu.style.zIndex = '1000';

                // Добавляем опции меню
        const deleteOption = document.createElement('div');
        deleteOption.textContent = 'Удалить';
        deleteOption.style.padding = '8px';
        deleteOption.style.cursor = 'pointer';
        deleteOption.addEventListener('click', function() {
            element.remove();
            if (fileId !== null) {address = `/files/delete_file/${fileId}/`}
            else if (folderId !== null) {address = `/files/delete_folder/${folderId}/`};
            fetch(address, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                            }
                        })
            .then(response => {
                    if (!response.ok) {
                        throw new Error('Ошибка при удалении элемента');
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                });
            contextMenu.remove();  // Закрыть меню после выбора
        });

        const option2 = document.createElement('div');
        option2.textContent = 'Опция 2';
        option2.style.padding = '8px';
        option2.style.cursor = 'pointer';
        option2.addEventListener('click', function() {
            alert('Вы выбрали Опцию 2');
            contextMenu.remove();  // Закрыть меню после выбора
        });

        contextMenu.appendChild(deleteOption);
        contextMenu.appendChild(option2);

        document.body.appendChild(contextMenu);

        // Закрыть меню, если кликнуть в любое другое место
        document.addEventListener('click', function() {
            contextMenu.remove();
        });
        });
    });
});

// Обработчик для попапов
document.addEventListener('DOMContentLoaded', function() {
    const openPopupBtn = document.getElementById('openPopupBtn');
    const closePopupBtn = document.getElementById('closePopupBtn');
    const popup = document.getElementById('popup');
    const openPopupFileFormBtn = document.getElementById('openPopupFileFormBtn');
    const popupFileForm = document.getElementById('popupFileForm');

    // Открыть попап
    openPopupBtn.addEventListener('click', function() {
        popup.style.display = 'block';
    });

    openPopupFileFormBtn.addEventListener('click', function() {
        popupFileForm.style.display = 'block';
    });

    // Закрыть попап
//    closePopupBtn.addEventListener('click', function() {
//        popup.style.display = 'none';
//    });

    // Закрыть попап, если кликнули вне его
    window.addEventListener('click', function(event) {
        if (event.target === popup) {
            popup.style.display = 'none';
        }
        else if (event.target === popupFileForm) {
            popupFileForm.style.display = 'none';
        }
    });



});


//Обработчик для удаления файлов
document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function() {
            const fileId = this.getAttribute('data-file-id');

            fetch(`/files/delete_file/${fileId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Файл удален!');
                    this.parentElement.remove();  // Удаляем элемент из DOM
                } else {
                    alert('Ошибка удаления');
                }
            });
        });
    });

//Обработчик для удаления папок
document.querySelectorAll('.delete-folder-button').forEach(button => {
        button.addEventListener('click', function() {
            const folderId = this.getAttribute('data-folder-id');

            fetch(`/files/delete_folder/${folderId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Папка удалена!');
                    this.parentElement.remove();  // Удаляем элемент из DOM
                } else {
                    alert('Ошибка удаления');
                }
            });
        });
    });

//Обработчик для формы создания папки
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form_create_folder");
    const responseDiv = document.getElementById("response");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Отключить стандартную отправку формы

        const formData = new FormData(form);
        console.log(formData)

        // Получение CSRF-токена
        const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;

        // AJAX-запрос с Fetch API
        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                responseDiv.innerHTML = `<p>${data.message}</p>`;
            } else {
                let errors = "";
                for (const [key, value] of Object.entries(data.errors)) {
                    errors += `<p>${key}: ${value}</p>`;
                }
                responseDiv.innerHTML = errors;
            }
        })
        .catch(() => {
            responseDiv.innerHTML = "<p>Произошла ошибка при отправке формы.</p>";
        });
    });
});

//Обработчик для формы загрузки файлов
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form_upload_file");
    const responseDiv = document.getElementById("response");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Отключить стандартную отправку формы

        const formData = new FormData(form);
        console.log(formData)

        // Получение CSRF-токена
        const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;

        // AJAX-запрос с Fetch API
        fetch(form.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                responseDiv.innerHTML = `<p>${data.message}</p>`;
            } else {
                let errors = "";
                for (const [key, value] of Object.entries(data.errors)) {
                    errors += `<p>${key}: ${value}</p>`;
                }
                responseDiv.innerHTML = errors;
            }
        })
        .catch(() => {
            responseDiv.innerHTML = "<p>Произошла ошибка при отправке формы.</p>";
        });
    });
});