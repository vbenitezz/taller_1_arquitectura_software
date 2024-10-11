document.addEventListener('DOMContentLoaded', function() {
    const cart_product_consumer_modal = document.getElementById('cart_product_consumer_modal');
    
    cart_product_consumer_modal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id_cart_product');
        
        fetch(`/get_product_cart_product_consumer/${id}/`)
            .then(response => response.json())
            .then(data => {
                
                document.getElementById('name_cart_product_consumer').value = data.name;
                document.getElementById('image_cart_product_consumer').src = data.image; 
                document.getElementById('price_cart_product_consumer').innerText = `US$${data.price}`;
                document.getElementById('publish_quantity_cart_product_consumer').value = data.publish_quantity;
                update_subtotal_cart_product_consumer();
            });
    });

    const cart_product_consumer_form = document.getElementById('cart_product_consumer_form');
    const price_cart_product = document.getElementById('price_cart_product_consumer');
    const quantity_cart_product = document.getElementById('quantity_cart_product_consumer');
    const subtotal_cart_product_consumer = document.getElementById('subtotal_cart_product_consumer');
    const name_cart_product = document.getElementById('name_cart_product_consumer');
    const image_cart_product = document.getElementById('image_cart_product_consumer');
    const publish_quantity_cart_product = document.getElementById('publish_quantity_cart_product_consumer');

    cart_product_consumer_form.addEventListener('submit', function(event) {
        quantity = parseInt(quantity_cart_product.value);
        publish_quantity = parseInt(publish_quantity_cart_product.value);
        
        if (quantity > publish_quantity) {
            event.preventDefault();
            alert(`The amount is not valid`);
        }else{
            event.preventDefault();
            const cart_product = {
                price: parseInt(price_cart_product.innerText.replace('US$', '').trim()),
                quantity: parseInt(quantity_cart_product.value),
                name: name_cart_product.value,
                image: image_cart_product.src
            };
            let add_cart_product = JSON.parse(localStorage.getItem('add_cart_product')) || [];
            add_cart_product.push(cart_product);
            localStorage.setItem('add_cart_product', JSON.stringify(add_cart_product));

            update_subtotal_cart_product_consumer();

            const cart_product_consumer_modal = bootstrap.Modal.getInstance(document.getElementById('cart_product_consumer_modal'));
            cart_product_consumer_modal.hide();
        }
        
    });

    document.getElementById('go_shopping_cart_consumer').addEventListener('click', function() {
        window.location.href = "/shopping_cart";
    });


    function update_subtotal_cart_product_consumer() {
        let add_cart_product = JSON.parse(localStorage.getItem('add_cart_product')) || [];
        
        // Calcular el subtotal sumando el precio de cada producto multiplicado por su cantidad
        let subtotal = add_cart_product.reduce((total, product) => {
            return total + (product.price * product.quantity);
        }, 0);

        // Actualizar el elemento subtotal
        subtotal_cart_product_consumer.innerText = `US$${subtotal}`;
        

    }
});
