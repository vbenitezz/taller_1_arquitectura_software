var show_details_modal = document.getElementById('show_details_modal');
show_details_modal.addEventListener("show.bs.modal", function (event) {
    var button = event.relatedTarget;

    // var id = button.getAttribute('data-id');
    var name = button.getAttribute('data-name');
    var category = button.getAttribute('data-category');
    var sale_price = button.getAttribute('data-sale_price');
    var description = button.getAttribute('data-description');
    var image = button.getAttribute('data-image');
        
    var card_title = show_details_modal.querySelector('.card-title');
    var card_subtitle = show_details_modal.querySelector('.card-subtitle');
    var card_description = show_details_modal.querySelector('.card_description');
    var card_sale_price = show_details_modal.querySelector('.card_sale_price');
    var card_image = show_details_modal.querySelector('.card_image');

    card_title.textContent = name;
    card_subtitle.textContent = category;
    card_description.textContent = description;
    card_sale_price.textContent = `$ ${sale_price}`;
    card_image.setAttribute('src', image);
})