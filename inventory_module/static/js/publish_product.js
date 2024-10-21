document.addEventListener('DOMContentLoaded', function() {
    const type_select = document.getElementById('inputGroupSelect01');
    const price_input = document.getElementById('price_input');

    // Escuchar cuando cambie el tipo de producto
    type_select.addEventListener('change', function() {
        if (this.value === 'donation') {
            price_input.value = 0;
            price_input.disabled = true;
            price_input.style.backgroundColor = '#e9ecef'; 
        } else {

            price_input.disabled = false;
            price_input.style.backgroundColor = '';  
        }
    });
});