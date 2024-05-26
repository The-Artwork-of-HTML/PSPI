const api = "http://127.0.0.1:5000";

window.onload = () => {
    const searchButton = document.getElementById('search');
    if (searchButton) {
        searchButton.addEventListener('click', productFormOnSubmit);
    } else {
        console.error('Search button not found');
    }
}

const productFormOnSubmit = (event) => {
    event.preventDefault();
    const searchInput = document.getElementById('searchInput').value;
    searchProducts(searchInput);
}

const searchProducts = (productName) => {
    fetch(`${api}/search?name=${productName}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        displayProducts(data.products);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

const displayProducts = (products) => {
    const tbody = document.getElementById('productTableBody');
    tbody.innerHTML = '';
    products.forEach(product => {
        const row = tbody.insertRow();
        row.innerHTML = `
            <td>${product.ID}</td>
            <td>${product.Name}</td>
            <td>${product.Production_Year}</td>
            <td>${product.Price}</td>
            <td>${product.Color}</td>
            <td>${product.Size}</td>
        `;
    });
}
