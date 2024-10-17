document.addEventListener('DOMContentLoaded', function() {
    const shopping_cart_container = document.getElementById('shopping_cart_container');
    const modalBody = document.querySelector('.modal_body'); // Aquí añadiremos las tarjetas de cada producto

    let shopping_cart = JSON.parse(localStorage.getItem('add_cart_product')) || [];

    function renderCart() {
        // Limpiar cualquier contenido previo dentro del modal
        modalBody.innerHTML = ''; 

        if (shopping_cart.length === 0) {
            shopping_cart_container.innerHTML = '<p>Your cart is empty</p>';
        } else {
            shopping_cart.forEach((product, index) => {
                if (product.type === "sale") {
                    // Crear una tarjeta para cada producto
                    const div_product = document.createElement('div');
                    div_product.classList.add('card', 'mb-3');
                    div_product.style.maxWidth = '450px';
                    
                    div_product.innerHTML = `
                        <div class="row g-0" style="height: 100px;">
                            <div class="col-md-4" style="padding: 0; height: 100%;">
                                <img src="${product.image}" class="img-fluid rounded-start" alt="${product.name}" style="width: 100%; height: 100%; object-fit: cover; display: block;">
                            </div>
                            <div class="col-md-8" style="height: 100%; position: relative;">
                                <div class="card-body p-2 d-flex flex-column justify-content-center" style="height: 100%;">
                                    <h5 class="card-title" style="font-size: 1rem;">${product.name}</h5>
                                    <p class="card-text" style="font-size: 0.875rem;">US$${product.price}</p>
                                    <p class="card-text"><small class="text-body-secondary">${product.quantity} unit(s)</small></p>
                                </div>
                                <!-- Ícono de basura -->
                                <button class="btn btn-danger position-absolute" style="top: 10px; right: 10px;" id="delete_product_${index}">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </div>
                        </div>
                    `;
                    
                    // Agregar cada tarjeta al cuerpo del modal
                    modalBody.appendChild(div_product);

                    // Agregar evento de eliminar
                    const deleteButton = document.getElementById(`delete_product_${index}`);
                    deleteButton.addEventListener('click', function() {
                        const delete_product = shopping_cart.splice(index, 1)[0];
                        update_publish_quantity(delete_product);

                        localStorage.setItem('add_cart_product', JSON.stringify(shopping_cart));
                        renderCart();
                    });

                    // Función para actualizar la publish_quantity del producto correspondiente
                    function update_publish_quantity(delete_product){
                        const id_product = delete_product.id;
                        // Selecciona el producto en el DOM por su data-id_cart_product
                        const productElement = document.querySelector(`[data-id_cart_product="${id_product}"]`);
    
                        if(productElement){
                            // Busca el elemento con id="new_quantity_<id_product>" y actualiza su contenido
                            const quantityElement = productElement.closest('.card').querySelector(`#new_quantity_${id_product} strong`);
                            const current_quantity = parseInt(quantityElement.nextSibling.nodeValue.trim());
                            const new_quantity = current_quantity + delete_product.quantity;

                            // Actualiza la cantidad en el HTML
                            quantityElement.nextSibling.nodeValue = ` ${new_quantity}`;
                        }
                    }
                }
            });
        }
    }

    // Renderizar el carrito al cargar la página
    renderCart();
});
