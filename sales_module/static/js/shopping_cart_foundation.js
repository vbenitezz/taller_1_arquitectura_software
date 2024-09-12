document.addEventListener('DOMContentLoaded', function() {
    const shopping_cart_container = document.getElementById('shopping_cart_container');
    
    let shopping_cart = JSON.parse(localStorage.getItem('add_cart_product')) || [];
    if(shopping_cart.length === 0){
        shopping_cart_container.innerHTML = '<p>Your cart is empty</p>';
    } else{
        shopping_cart.forEach((product, index) => {
            if(product.type==="donation"){
                const div_product = document.createElement('div');
                div_product.classList.add('card', 'mb-3');
                div_product.style.maxWidth = '300px';
                div_product.innerHTML = `
                    <div class="row g-0" style="height: 100px;">
                        <div class="col-md-4" style="padding: 0; height: 100%;">
                            <img src="${product.image}" class="img-fluid rounded-start" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block;">
                        </div>
                        <div class="col-md-8" style="height: 100%;">
                            <div class="card-body p-2 d-flex flex-column justify-content-center" style="height: 100%;">
                                <h5 class="card-title" style="font-size: 1rem;">${product.name}</h5>
                                <p class="card-text" style="font-size: 0.875rem;">US$${product.price}</p>
                                <p class="card-text"><small class="text-body-secondary">${product.quantity} unit</small></p>
                            </div>
                        </div>
                    </div>
                `;
                shopping_cart_container.appendChild(div_product)
            }
        });
    }
});


