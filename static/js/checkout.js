// Set delivery form to display if delivery button is checked  
let delivery = document.querySelector('#flexSwitchCheckDefault')
delivery.addEventListener('change', function() {
    if (delivery.checked) {
    document.querySelector('.delivery-info').classList.remove('d-none')
    }
    else {
        document.querySelector('.delivery-info').classList.add('d-none')
    }
})

let form = document.querySelector('.form')
form.addEventListener('submit', function(e) {
    //Prevent form from being submited, so more form processing can be done 
    e.preventDefault()
    console.log('Form submited..')

    document.querySelector('.submit-form').classList.add('d-none')
    document.querySelector('.payment-options').classList.remove('d-none')

    document.querySelector('.make-payment').addEventListener('click', function() {
        submitFormData()
    })
})

function submitFormData() {
    let userFormData = {
        'fname':null,
        'lname':null,
        'email':null,
        'phone':null,
    }

    let deliveryFormData = {
        'city':null,
        'address':null,
        'restaurant':null,
        'delivery':null,
        'delivery_time':null
    }

    deliveryFormData.delivery = form.delivery.checked
    deliveryFormData.restaurant = form.restaurant.value
    deliveryFormData.delivery_time = form.delivery_time.value


    if (delivery.checked) {
        deliveryFormData.city = form.city.value
        deliveryFormData.address = form.address.value
    }

    if (user == 'AnonymousUser') {
        userFormData.fname = form.fname.value
        userFormData.lname = form.lname.value
        userFormData.email = form.email.value
        userFormData.phone = form.phone.value
    }

    //Where the data will be sent 
    let url = '/process_order/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-type': 'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'userFormData': userFormData, 'deliveryFormData':deliveryFormData})
    })

    .then((response) => response.json())
    .then((data) => {
        console.log('Success: ', data)
        alert('Transaction complete')
        window.location.href = "/"
    })
}



