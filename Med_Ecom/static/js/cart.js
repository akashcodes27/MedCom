
    // Get all buttons with class "add_to_btn"
    const addToCartButtons = document.querySelectorAll('.add_to_btn');

    // Add event listeners to each button
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            addToCart(productId);
        });
    });

    // Add the following code to your existing JavaScript code

// Function to update the cart total quantity displayed in the navbar
function updateCartTotalQuantity(totalQuantity) {
    const cartTotalElement = document.getElementById('cart-total');
    cartTotalElement.textContent = totalQuantity;
}



// Updated addToCart function
function addToCart(productId) {
    fetch(`/add_to_cart/${productId}/`)
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Display a success message or handle the response accordingly
            location.reload()
            if (data.success) {
                // If the request was successful, update the cart total quantity
                updateCartTotalQuantity(data.cart_total_quantity);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
// We made a post request using fetch API to add items to cart(and hence to the database as well)
// ---------------------------------------------------------------------------------------------------------------------------
// This entire code snippet is for increasing the number of items in cart

const arrowUpDivs = document.querySelectorAll('.arrow_up_div');

arrowUpDivs.forEach(arrowUpDiv => {
    arrowUpDiv.addEventListener('click', () => {
        const productId = arrowUpDiv.getAttribute('arrow-product-id');
        updateArrowQty(productId);
    });
});

function updateArrowQty(productId){
    // alert('function is calledddd')

    fetch(`/update_arrow_qty/${productId}/`)
        .then(response => response.json())
        .then(data => {
            alert(data.message); 
            // location.reload()
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// ----------------------------------------------------------------------------------------------------------------------------

// This entire code snippet is for decreasing the number of items in cart

const arrowDownDivs = document.querySelectorAll('.arrow_down_div');

arrowDownDivs.forEach(arrowDownDiv => {
    arrowDownDiv.addEventListener('click', () => {
        const productId = arrowDownDiv.getAttribute('arrow-product-id');
        downdateArrowQty(productId);
    });
});

function downdateArrowQty(productId){
    // alert('function is calledddd')

    fetch(`/downdate_arrow_qty/${productId}/`)
        .then(response => response.json())
        .then(data => {
            alert(data.message); 
            // location.reload()
        })
        .catch(error => {
            console.error('Error:', error);
        });
}