document.addEventListener('DOMContentLoaded', function() {
    const cart_product_consumer_modal = document.getElementById('cart_product_consumer_modal');
    
    cart_product_consumer_modal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id_cart_product');
        
        fetch(`/get_product_cart_product_consumer/${id}/`)
            .then(response => response.json())
            .then(data => {
                console.log(data.price);
                document.getElementById('image_cart_product_consumer').src = data.image; 
                document.getElementById('price_cart_product_consumer').innerText = `US$${data.price}`;
            });
    });

    const cart_product_consumer_form = document.getElementById('cart_product_consumer_form');
    const price_cart_product = document.getElementById('price_cart_product_consumer');
    const quantity_cart_product = document.getElementById('quantity_cart_product_consumer');

    cart_product_consumer_form.addEventListener('submit', function(event) {
        event.preventDefault();

        const cart_product = {
            price: parseInt(price_cart_product.innerText.replace('US$', '').trim()),
            quantity: parseInt(quantity_cart_product.value),
        };

        // Obtener el carrito del localStorage o crear uno nuevo
        let add_cart_product = JSON.parse(localStorage.getItem('add_cart_product')) || [];

        // Agregar el producto al carrito
        add_cart_product.push(cart_product);

        // Guardar el carrito en el localStorage
        localStorage.setItem('add_cart_product', JSON.stringify(add_cart_product));

        const cart_product_consumer_modal = bootstrap.Modal.getInstance(document.getElementById('cart_product_consumer_modal'));
        cart_product_consumer_modal.hide();
    });

    document.getElementById('go_shopping_cart_consumer').addEventListener('click', function() {
        window.location.href = "/shopping_cart";
    });

    document.getElementById('remove_from_cart').addEventListener('click', function() {
        quantity_cart_product.value = 0; // O algún otro comportamiento para eliminar el producto
    });
});
