(function(){
    const btn_delete_product = document.querySelectorAll(".btn_delete_product");

    btn_delete_product.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const conf = confirm('Do you want to remove this product?');
            if(!conf){
                e.preventDefault();
            }
        });
    });

})();