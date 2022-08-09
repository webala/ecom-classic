//function to get cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//define and initialize cart from cookies. Create cart cookie if it does not exist
let cart = getCookie('cart')

if (cart == null) {
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
}

console.log('cart: ', cart)

//modify cart function
const modifyCartCookie = (action, productId) => {
    // Modifies the cart cookie and updates the value of document.cookie
    if (action === 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }
    else if (action === 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId]
        }
    }
    else if (action === 'delete') {
        delete cart[productId]
    }

    console.log('modified cart: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
    location.reload()
}