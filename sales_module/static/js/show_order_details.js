const modal = document.getElementById('show_details_modal');

modal.addEventListener('show.bs.modal', function(event) {

    const details = event.relatedTarget;
    const order_id = details.getAttribute('data-id');
    const details_container = document.getElementById('details_container');
    details_container.innerHTML="";
    fetch('/show_details/',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') 
            },
        body: JSON.stringify({order_id:order_id})
            })
            .then(response => response.json())
            .then(data => {
                if (data.products) { 
                    const products = data.products;
                    products.forEach(product => {
                        const product_HTML = `
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
                                <p class="m-0 me-4 fw-bold">x${product.quantity}</p>
                            </div>
                        `;
                        details_container.innerHTML += product_HTML;  
                    });
                } else {

                    details_container.innerHTML = `<p>No products found for this order.</p>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);  // Manejo de errores
                details_container.innerHTML = `<p>Error loading order details. Please try again later.</p>`;
            });
})
            
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}