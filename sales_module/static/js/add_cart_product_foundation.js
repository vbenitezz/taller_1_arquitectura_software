document.addEventListener('DOMContentLoaded', function() {
    const cart_product_consumer_modal = document.getElementById('cart_product_consumer_modal');
    
    cart_product_consumer_modal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id_cart_product');
        document.getElementById('id_product_cart').value = id;
        
        fetch(`/get_product_cart_product_consumer/${id}/`)
            .then(response => response.json())
            .then(data => {
                
                document.getElementById('name_cart_product_consumer').value = data.name;
                document.getElementById('image_cart_product_consumer').src = data.image; 
                document.getElementById('price_cart_product_consumer').innerText = `US$${data.price}`;
                document.getElementById('publish_quantity_cart_product_consumer').value = data.publish_quantity;
            });
    });

    const cart_product_consumer_form = document.getElementById('cart_product_consumer_form');
    const id_product_cart = document.getElementById('id_product_cart');
    const price_cart_product = document.getElementById('price_cart_product_consumer');
    const quantity_cart_product = document.getElementById('quantity_cart_product_consumer');
    const subtotal_cart_product_consumer = document.getElementById('subtotal_cart_product_consumer');
    const name_cart_product = document.getElementById('name_cart_product_consumer');
    const image_cart_product = document.getElementById('image_cart_product_consumer');
    const type_cart_product = document.getElementById('type_cart_product');

    const publish_quantity_cart_product = document.getElementById('publish_quantity_cart_product_consumer');

    cart_product_consumer_form.addEventListener('submit', function(event) {
        quantity = parseInt(quantity_cart_product.value);
        publish_quantity = parseInt(publish_quantity_cart_product.value);
        id = parseInt(id_product_cart.value);
        
        if (quantity > publish_quantity) {
            event.preventDefault();
            alert(`The amount is not valid`);
        }else{
            event.preventDefault();
            new_quantity = publish_quantity-quantity;
            update_published_quantity(id, new_quantity);
            const cart_product = {
                price: parseInt(price_cart_product.innerText.replace('US$', '').trim()),
                quantity: parseInt(quantity_cart_product.value),
                name: name_cart_product.value,
                image: image_cart_product.src,
                type: type_cart_product.value
            };
            let add_cart_product = JSON.parse(localStorage.getItem('add_cart_product')) || [];

            // Buscar el índice del producto en el carrito
            const index = add_cart_product.findIndex(product => product.name === cart_product.name && product.type === cart_product.type);

            if (index !== -1) {
                // Si el producto ya existe, actualizar la cantidad
                add_cart_product[index].quantity += cart_product.quantity;
            } else {
                // Si el producto no existe, agregar uno nuevo
                add_cart_product.push(cart_product);
            }

            // Guardar el carrito actualizado en el localStorage
            localStorage.setItem('add_cart_product', JSON.stringify(add_cart_product));

            update_subtotal_cart_product_consumer();

            const cart_product_consumer_modal = bootstrap.Modal.getInstance(document.getElementById('cart_product_consumer_modal'));
            cart_product_consumer_modal.hide();
        }
        
    });

    document.getElementById('go_shopping_cart_foundation').addEventListener('click', function() {
        window.location.href = "/shopping_cart_foundation";
    });
});

function update_published_quantity(id,new_quantity){

    const csrftoken = getCookie('csrftoken');  // Obtiene el token CSRF
    fetch('/update_product_quantity/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'X-CSRFToken': csrftoken,
            product_id: id,
            quantity: new_quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Product added to cart successfully');
            location.reload();

        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

