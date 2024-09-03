document.addEventListener('DOMContentLoaded', function() {
    const edit_product_modal_add_product = document.getElementById('edit_product_modal_add_product');
    edit_product_modal_add_product.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id_add_product');

        fetch(`/get_product_add_product/${id}/`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById('edit_name_add_product').value = data.name;
                document.getElementById('edit_quantity_add_product').value = data.quantity;
                document.getElementById('edit_id_add_product').value = id;

                document.getElementById('edit_product_form_add_product').action = `/edit_product_add_product/${id}/`;
                
                

            });
    });
});