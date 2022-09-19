# UnderDaC

## Introduction
UnderDaC is a small restaurant chain focusing on seafood with each restaurant focusing on a particular major ocean. On the website you are able to reserve tables and place ordersfor pickup or delivery, the user is also able to create an account for faster booking and checkout. All information that is saved to the database will be readable, editable, updateable and deletable by the creator and/or the admin accounts. 

## Showcase
Picture of website on different devices

### Live Website
A deployed link to the website can be found [here](https://underdac.herokuapp.com/)

# Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Credits](#credits)


## Design

### Wireframes

 <details>
  <summary>Click here to view all wireframes for desktop:</summary>

  ![](docs/home.png)
  ![](docs/menu.png)
  ![](docs/contact.png)
  ![](docs/reservation.png)
  ![](docs/checkout.png)
  ![](docs/registration.png)
  ![](docs/login.png)

  </details>

### Database

I made multiple tables for the website; Customer, Restaurant, MenuItem, Booking, Order, OrderItem, DeliveryInfo and Contact. 

The Customer table is used for storing additional customer information upon user registration.

The Restaurant table stores information about the restaurants; name, phone, address, image, open-hours, and a map number for getting the correct map on the home page

The MenuItem table stores information about menuitems; category, name, description, price, image, and as well a function to calculate half price

The Booking table stores information about table reservations customers are making; customer as a ForeignKey with a relationship to User, first name, last name, phone, email, restaurant as a ForeignKey with a relationship to the Restaurant table, guest count, date and time

The Order table stores information about an order made by a customer; customer as a ForeignKey with a relationship to User, restaurant as a ForeignKey with a relationship to the Restaurant table, delivery time, created on, wheather the order is completed, and wheather the order should be delivered. It also has a function for getting cart count and a function for calculating cart total.

The OrderItem table is used for relating an item to an order; item as a ForeignKey with a relationship to MenuItem, order as a ForeignKey with a relationship to the Order table, quantity. It also has a function for calculating the item price by the quantity.

The DeliveryInfo table is used for storing an order delivery information; customer as a ForeignKey with a relationship to the User table, order as a ForeignKey with a relationship to the Order table, first name, last name, address, city and created on.

The Contact table stores messages regarding whatever the customer wants to tell or ask the company; customer as a ForeignKey with a relationship to User, email, subject, message


<details>
  <summary>Click here to view the ERD:</summary>

  ![](docs/erd.png)

</details>


# Features
## Existing Features

### Navbar
The main navbar contains a logo, a top navbar and a bottom navbar. If the user is logged in, then the top navbar contains a logout button, a profile button, and if the user has an active booking it also displays a notification to remind the user of the upcoming reservation. If the useris not logged in it will display a login and a sign up button. And wheather or not the user is logged in it will always display the language selction and a cart. The bottom navbar contains links to all the main pages of the site; Home, Menu, Booking Table and Contact Us.

### Footer 
The footer contains copyright information and links to social media

### Home Page
The home page displays a two sections; one for offers and specials and the other for restaurant info. The first section has two banners. The first banner has two links, the first link says "Today's special" and goes to the menu page, and the second link says "Book a table" and takes the user to the table booking page. The second banner displays an offer that says that "Kids eat for half price". The restaurant section that shows each restaurant's details and also has a dropdown that shows the restaurants locations on a map.

### Menu Page 
The menu page displays all menu items seperated by the categories Menu, Vegan menu and kids menu. The admin can add as many items as they want and the page will accomadate for it. Each menu item has an "add to order" button.

### Book Table Page
The book table page has at the top a row of buttons that each take the user to the respective restaurant booking page. The page displays a large image of the restaurant and benath it all the current reservations the user has for this particular restaurant  and beneath that a form for reserving a table. Next to the form there is a phone number so that the customer can reserve a table by phone. Beneath that there is information about the restaurants address and its open hours.

### Contact Us Page
This page has a form for anyone to message the company's about questions or complaints

### Cart Page
This page shows a summary of everything the customer has added to their order, and a checkout button that takes the user to the checkout page. The user has the ability to add or subtract from the menu items they've added.

### Checkout Page
The checkout page displays a summary of the order before the customer finally makes the purchase. The customer can choose restaurant and pickup/delivery time, they can also choose to get the order delivered or if they rather want to pick it up at the restaurant, if they want it delivered they need to fill out their city and address as well. When everything is filled out the can click the conrinue button that will then display payment options.

### My Bookings
This page is reached through the profile button in the navbar. The page will display all bookings that the customer has across all the restaurants. Here the user can edit or delete their reservations

### My Details
Here the user can edit their information or delete their account 






## Media
- Home page specials picture from https://www.iheart.com/content/2022-02-08-this-san-dimas-restaurant-has-the-best-seafood-in-southern-california/
- Home page kids offer picture from https://www.renfrewshire24.co.uk/2021/04/23/kids-give-their-opinion-on-new-redhurst-hotel-junior-menu/
- Home page restaurant 1 picture from https://www.tippleandbrine.com/easy-steps-choose-great-seafood-restaurant/
- Home page restaurant 2 picture from https://quark-studio.com/portfolio/seafood-restaurant/
- Home page restaurant 3 picture from 
- Menu-item-1 and Menu-item-2 from https://www.istockphoto.com/se/search/2/image?phrase=fish+fry+india
- Menu-item-3 from https://restaurantclicks.com/most-popular-seafood-dishes/
- Menu-item-4 from https://hipfoodiemom.com/2019/05/22/seafood-recipes-for-summer-a-video/
- KidsMenu-item-1 from https://www.delish.com/cooking/recipe-ideas/recipes/a53296/easy-fish-taco-recipe/
- KidsMenu-item-2 from https://dizzybusyandhungry.com/crab-cake-on-a-bun/
- KidsMenu-item-3 from https://ishavet.nu/receptbank/recept/fish-n-chips/
- Veganmenu-item-1 from https://www.pinterest.se/pin-builder/?url=https%3A%2F%2Favegtastefromatoz.com%2Fvegan-simple-seafood-pasta%2F&media=https%3A%2F%2Favegtastefromatoz.com%2Fwp-content%2Fuploads%2F2019%2F06%2FSeafood-Pasta-Close-Up.jpg&description=Vegan+Simple+Seafood+Pasta+-+a+Veg+Taste+from+A+to+Z&method=button
- Veganmenu-item-2 from https://www.pinterest.se/pin-builder/?url=https%3A%2F%2Favegtastefromatoz.com%2Fbest-vegan-salmon%2F&media=https%3A%2F%2Fi0.wp.com%2Favegtastefromatoz.com%2Fwp-content%2Fuploads%2F2021%2F03%2Fcarrot-lox-side.jpg%3Fresize%3D1170%252C1755%26ssl%3D1&description=best+vegan+salmon+%2F+carrot+lox+close+up+on+a+wooden+tray+with+lemon+wedges%2C+capers+and+dill&method=button
- Veganmenu-item-3 from https://nutriciously.com/vegan-fish-seafood-recipes/


## Credit
- Tech with tim
- Dennis Ivy 
- Pretty printed 
- Caleb Curry 
- The net ninja

- getCookie function in base.js taken from https://www.w3schools.com/js/js_cookies.asp


## Bugs 
- Getting all cookies from a request 
- Closing the pop up message from before it the time out is over causes an exception because now there is nothing to close
- Maps don't resize on home page

## Fixed Bugs
- Static files doesn't get uploaded with heroku
- Could not deploy to heroku because the main folder "underdac" was called "UnderDaC" in the Procfile and the settings 