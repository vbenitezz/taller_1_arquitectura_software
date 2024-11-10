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
                            <div class="row g-0" style="height: 100px;">
                            <div class="col-md-4" style="padding: 0; height: 100%;">
                                <img src="${product.image}" class="img-fluid rounded-start" alt="${product.name}" style="width: 100%; height: 100%; object-fit: cover; display: block;">
                            </div>
                            <div class="col-md-8 d-flex flex-column justify-content-center" style="height: 100%; position: relative; padding: 0 6px;">
                                <div class="card-body p-2" style="height: 100%;">
                                    <h5 class="card-title" style="font-size: 1rem; margin-bottom: 0.1rem;">${product.name}</h5>
                                    <p class="card-text" style="font-size: 0.8rem; margin-bottom: 0.1rem;">US$${product.price}</p>
                                    <p class="card-text" style="font-size: 0.8rem; margin-bottom: 0.1rem;"><small class="text-body-secondary">${product.address}</small></p>
                                    <p class="card-text" style="font-size: 0.8rem;"><small class="text-body-secondary">${product.quantity} unit(s)</small></p>
                                </div>
                            </div>
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