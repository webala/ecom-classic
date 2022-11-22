//Fetch number of cart items and set the value
const cartItems = document.querySelector('.cart_items')
const cartTotal = document.querySelector('.cart_total')
const cartItemsEndpoint = '/shop/cart_items'

const getCartItems = () => {
    fetch(cartItemsEndpoint)
    .then((res) => res.json())
    .then((data) => {
        const items = data.cart_items
        const total = data.cart_total
        cartItems.innerHTML = items.toString()
        if (cartTotal) {
            cartTotal.innerHTML = total.toString()
        }
    })
    .catch((error) => console.log(error))
}

getCartItems()

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

//This function deletes the cart cookies
function deleteCartCookies() {
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
    console.log('cart: ', cart)
}

//define and initialize cart from cookies. Create cart cookie if it does not exist
let cart = JSON.parse(getCookie('cart'))

if (cart == undefined) {
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
}

console.log('cart: ', cart)

const removeElement = (elementId) => {
    let element = document.getElementById(elementId)
    if (element) {
        element.remove()
    } else {
        return
    }
}

const modifyCartQuantity = (productId, quantity) => {
    const id = `product-quantity-${productId}`
    let element = document.getElementById(id)
    if (element) {
        element.innerHTML = quantity
    } else {
        return
    }
}

//modify cart function
const modifyCartCookie = (action, productId) => {
    // Modifies the cart cookie and updates the value of cart in document.cookie

    if (action === 'add') {
        console.log('action: ', action)
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] +=1
        }
        modifyCartQuantity(productId, cart[productId]['quantity'])
    }
    else if (action === 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId]
            removeElement(productId)
        }

        modifyCartQuantity(productId, cart[productId]['quantity'])
    }
    else if (action === 'delete') {
        delete cart[productId]
        removeElement(productId)
    }

    
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
    
    getCartItems()
}

//get update cart buttons
const updateCartBtns = Array.from(document.getElementsByClassName('update-cart'))

//add click event listener to modify cart on click
updateCartBtns.forEach((btn) => {
    
    btn.addEventListener('click', () => {
        
        const productId = btn.dataset.productid
        const action = btn.dataset.action
        modifyCartCookie(action, productId)
    })

})


//Button with .back class used for going back
const backBtn = document.querySelector('.back')
if (backBtn) {
    backBtn.addEventListener('click', () => history.back())
}


//SOME ANIMATIONS

    const products = document.querySelector('.products')
    const quote = document.querySelector('.quote')
    const navIcon = document.getElementById('nav-icon')
    const navItems = document.querySelector('.nav-items')
    const logo = document.querySelector('.logo')
    const cartItemsList = document.querySelector('.cart-items')
    const footer = document.querySelector('.footer')
    

    

    window.onload = () => {
        if (cartItemsList) {
            cartItemsList.classList.add('loaded')
        }
        if (logo) {
            logo.classList.add('loaded')
        }
        if (navItems) {
            navItems.classList.add('loaded')
        }
        if (quote) {
            quote.classList.add('loaded')
        }
        if (footer) {
            footer.classList.add('loaded')
        }
    }

    window.addEventListener('scroll', () => {
        if (products) {
            products.classList.toggle('loaded', window.scrollY > 0)
        }
        // cartItems.classList.toggle('loaded', window.scrollY > 0)
    })

    const individualNavItems = Array.from(document.getElementsByClassName('nav-item'))

    //Navigation toggle


    navIcon.addEventListener('click', () => {

        const navToggleClasses = [
            'absolute',
            'toggle',
            'right-0',
            'px-10',
            'py-5',
            'hidden',
            'flex',
            'flex-col', 
            'bg-backgroundSecondary'
        ]

        navToggleClasses.forEach(className => {
            navItems.classList.toggle(className)
        })

        individualNavItems.forEach(item => {
            item.classList.toggle('my-2')
        })
    })