document.addEventListener('DOMContentLoaded', function() {
    const edit_product_modal = document.getElementById('edit_product_modal');
    edit_product_modal.addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id');

        fetch(`/get_product/${id}/`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById('edit_name').value = data.name;
                document.getElementById('edit_category').value = data.category;
                document.getElementById('edit_sale_price').value = data.sale_price;
                document.getElementById('edit_description').value = data.description;
                document.getElementById('edit_image').src = data.image;
                document.getElementById('edit_id').value = id;

                document.getElementById('edit_product_form').action = `/edit_product/${id}/`;

                

            });
    });
});


// var edit_product_modal = document.getElementById('edit_product_modal');
// edit_product_modal.addEventListener('show.bs.modal', function (event) {
//     var button = event.relatedTarget;

    
// })