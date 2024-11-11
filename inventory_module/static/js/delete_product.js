(function(){
    const btn_delete_product = document.querySelectorAll(".btn_delete_product");

    btn_delete_product.forEach(btn => {
        btn.addEventListener('click', (e) => {
            Swal.fire({
                title: 'Are you sure?',
                text: "Do you want to remove this product?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, confirm it!'
            }).then((result) => {
                if(!result.isConfirmed)
                    e.preventDefault();
            });
        });
    });

})();