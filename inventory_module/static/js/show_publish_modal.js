var publish_modal = document.getElementById('publish_modal');
publish_modal.addEventListener("show.bs.modal",function(event){
    var button = event.relatedTarget;
    var product_name=button.getAttribute('data-name');
    var product_total_quantity=button.getAttribute('data-quantity');
    var product_id=button.getAttribute('data-id');
    var product_total_sale_price=button.getAttribute('data-price');

    var modal_title = publish_modal.querySelector('.modal-title');
    var modal_attribute_quantity = publish_modal.querySelector("#quantity");
    var modal_product_id = publish_modal.querySelector("#product_id");

    modal_title.textContent= "ID: " + product_id + "      " + product_name;
    modal_attribute_quantity.setAttribute("max",product_total_quantity);
    modal_product_id.value = product_id;
})