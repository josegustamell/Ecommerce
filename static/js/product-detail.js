document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
})

num = 1;

function removeQuantity() {
num--;
setValue(num);
}

function addQuantity() {
num++;
setValue(num);
}

function setValue(value) {
document.getElementById('product-quantity').value = value;
}

setValue(num);