//Let's JS access the user 
let user = '{{ request.user }}';

//Auto close bootstrap messages
alertWindow = document.querySelectorAll('#msg');

if (alertWindow.length > 0) {
  setTimeout(function () {
    let messages = document.querySelector('#msg');
    let alert = new bootstrap.Alert(messages);
    alert.close();
  }, 3000);
}

function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    let cookieArr = document.cookie.split(";");
  
    // Loop through the array elements
    for (let i = 0; i < cookieArr.length; i++) {
      let cookiePair = cookieArr[i].split("=");
  
      /* Removing whitespace at the beginning of the cookie name
      and compare it with the given string */
      if (name == cookiePair[0].trim()) {
        // Decode the cookie value and return
        return decodeURIComponent(cookiePair[1]);
      }
    }
  
    // Return null if not found
    return null; 
  }
  
  let cart = JSON.parse(getCookie('cart'));
  
  //If there is no cart, set it to an empty object
  if (cart == undefined){
    cart = {};
    console.log('Cart Created!', cart);
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
  }
  console.log('Cart:', cart);

