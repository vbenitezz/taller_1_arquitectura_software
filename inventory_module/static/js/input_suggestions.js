
document.addEventListener('DOMContentLoaded', function() {
    const input_name = document.getElementById('input_name');
    const suggestions_list = document.getElementById('suggestions_list');
    input_name.addEventListener('input', function() {
            const query = input_name.value;
            if (query.length < 2) {
                suggestions_list.style.display = 'none';
                return;
            }

            fetch(`http://35.222.205.184/search_products_suggestions/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestions_list.innerHTML = '';
                    if (data.length > 0) {
                        suggestions_list.style.display = 'block';
                        data.forEach(product => {
                            const li = document.createElement('li');
                            li.classList.add('list-group-item')
                            li.classList.add('suggestion_li')
                            li.textContent = product.name;
                            li.addEventListener('click', () => {
                                input_name.value = product.name;
                                suggestions_list.style.display = 'none';
                            });
                            suggestions_list.appendChild(li);
                        });
                    } else {
                        suggestions_list.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        });

        // Ocultar la lista de sugerencias cuando se hace clic fuera del input
        document.addEventListener('click', function(event) {
            if (!input_name.contains(event.target) && !suggestions_list.contains(event.target)) {
                suggestions_list.style.display = 'none';
            }
        });
    });

