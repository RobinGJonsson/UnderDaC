
//Add eventlistener to all update cart buttons
let updateCartBtns = document.querySelectorAll('.update-cart');
let addToCartBtns = document.querySelectorAll('.add-to-cart');


for (let btn of updateCartBtns) {
    btn.addEventListener('click', function() {
        let itemID = this.dataset.item;
        let action = this.dataset.action;
        console.log(itemID, action);
        console.log(user);

        if (user === 'AnonymousUser') {
            addCookieItem(itemID, action);
        }
        else {
            updateUserOrder(itemID, action);
        }
    }); 
}


function addCookieItem(itemID, action) {
    console.log('Not logged in..');

    // Add 1 or create a cart with a quantity of 1
    if (action == 'add'){
        if (cart[itemID] == undefined){
            cart[itemID] = {'quantity':1};
        } 
        else {
            cart[itemID].quantity += 1;
        }

    if (action == 'subtract'){
        cart[itemID].quantity -= 1;
    }   if (cart[itemID].quantity <= 0){
            delete cart[itemID];
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/';
    location.reload();
}

function updateUserOrder(itemID, action) {
    console.log('User is logged in, sending data');

    let url = '/update_cart/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': csrftoken,
        },
        body:JSON.stringify({'itemID': itemID, 'action': action})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        console.log('data: ', data);
        location.reload();
    });
}
