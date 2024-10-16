console.log("HOLAAA")
document.getElementById('chartForm').addEventListener('submit', function(event) {
    // Obtiene el valor seleccionado del select
    const chartType = document.getElementById('input_category').value;
    
    // Obtiene todas las checkboxes
    const checkboxes = document.querySelectorAll('.form-check-input');
    
    // Cuenta cuántas checkboxes están marcadas
    let checkedCount = 0;
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            checkedCount++;
        }
    });

    // Validación: Si el tipo de gráfico es "0" o menos de dos checkboxes marcadas, muestra alerta y detiene envío
    if (chartType === "0" || checkedCount < 2) {
        event.preventDefault(); // Evita que el formulario se envíe
        alert('Please select a chart type and at least two variables.');
    }
});