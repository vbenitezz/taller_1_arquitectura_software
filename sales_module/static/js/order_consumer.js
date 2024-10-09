
// For generating order
const generate_order = document.getElementById('generate_order');
generate_order.addEventListener('click', function() {    
    products =  JSON.parse(localStorage.getItem('add_cart_product'));
    order_container = document.getElementById('order_container');
    total_price_container = document.getElementById('total_order');
    let total_price=0;
    let product_total_price
    console.log(products);
    order_container.innerHTML="";
    if (products) {
        products.forEach(product => {
            product_total_price=product.quantity*product.price
            total_price += product_total_price;

            const product_order_HTML = `
            <div class="d-flex justify-content-between align-items-center border p-2 mb-2 product_container">
                <div class="d-flex align-items-center">
                    <div class="img_container bg-secondary d-flex justify-content-center align-items-center">
                        <img src="${product.image}" alt="${product.name}" class="img-fluid product_image" width="50" height="50">
                    </div>
                    <div class="product_info ms-2">
                        <h6 class="m-0">${product.name}</h6>
                        <small class="text-muted">$${product.price} per unit</small>
                    </div>
                </div>
                <p class="m-0 me-4 fw_bold">x${product.quantity}</p>
            </div>
            `;

            order_container.innerHTML += product_order_HTML;
        });
        total_price_container.innerText = `US$ ${total_price}`;
        total_price_container.value=total_price;
        
    } else {
        order_container.innerHTML = `<div class="alert alert-warning" role="alert">There are no products in the shopping cart</div>`
        total_price_container.innerText = `US$ ${total_price}`;
        total_price_container.value=total_price;


    }

});

// When the customer buy the order
const buy_order = document.getElementById('buy_order');
buy_order.addEventListener('click', function() {
    let products = JSON.parse(localStorage.getItem('add_cart_product'));

    if (!products || products.length === 0) {
        alert("There are no products in the shopping cart");
        return; 
    } else {
        let confirmation = window.confirm("Are you sure you want to confirm your purchase?");

        if (confirmation){
            let total_price = products.reduce((sum, product) => sum + product.price * product.quantity, 0);
            let order_data = {
                products: JSON.stringify(products) , 
                total_price: total_price
            };
            fetch('/buy_order_consumer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',  
                },
                body: JSON.stringify(order_data)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                alert('Successful purchase');
                localStorage.removeItem('add_cart_product');
                const modal = document.getElementById('order_modal');
                const modal_instance = bootstrap.Modal.getInstance(modal);
                modal_instance.hide();
                window.location.reload();
            })
            .catch(error => {
                console.error('Error sending the order', error);
            });
        }
    }
});
