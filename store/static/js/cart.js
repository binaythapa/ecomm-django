/* ---------Cart Item-------*/
var updateBtns= document.getElementsByClassName("update-cart");
        for(var i=0; i<updateBtns.length; i++){
                updateBtns[i].addEventListener('click', function(){
                var productId= this.dataset.product
                var action= this.dataset.action


if ( user == 'AnonymousUser'){
addCookieItem(productId, action)
}

else
{
updateUserOrder(productId, action)
} }) }


function updateUserOrder(productId, action){
var url= '/update_item/'

fetch(url,{
    method: 'POST',
    headers:{
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
         },
    body:JSON.stringify({'productId': productId, 'action': action })
       })
       .then((response) => {
         return response.json()
       })
       .then((data) => {
         console.log('data:',data)
         location.reload()
       })
}


function addCookieItem(productId, action){
if (action == 'add'){
    if(cart[productId] == undefined){
        cart[productId]= {'quantity':1}
    }
    else{
        cart[productId]['quantity'] += 1
     }
}

else if(action =='remove'){
     cart[productId]['quantity'] -= 1

    if(cart[productId]['quantity'] <= 0){

       }}

document.cookie= 'cart=' + JSON.stringify(cart)+ ";domain=;path=/";


}
  /* console.log("User is not logged in but still can make order") */

/*--------Wishlist---------*/

var updateBtns= document.getElementsByClassName("wishlist");
        for(var i=0; i<updateBtns.length; i++){
                updateBtns[i].addEventListener('click', function(){
                var productId= this.dataset.product
                console.log("wishlist product id is", productId)



if ( user == 'AnonymousUser'){
console.log("Please login first")
}

else
{
updatewishlist(productId)
} }) }


function updatewishlist(productId){
var url= '/update_wishlist/'

fetch(url,{
    method: 'POST',
    headers:{
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
         },
    body:JSON.stringify({'productId': productId})
       })
       .then((response) => {
         return response.json()
       })
       .then((data) => {
         console.log('data:',data)
         location.reload()
       })
}

/*--------Like---------*/

var updateBtns= document.getElementsByClassName("like");
        for(var i=0; i<updateBtns.length; i++){
                updateBtns[i].addEventListener('click', function(){
                var productId= this.dataset.product
                console.log("Like product id is", productId)



if ( user == 'AnonymousUser'){
console.log("Please login first")
}

else
{
updatelike(productId)
} }) }


function updatelike(productId){
var url= '/update_like/'

fetch(url,{
    method: 'POST',
    headers:{
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
         },
    body:JSON.stringify({'productId': productId})
       })
       .then((response) => {
         return response.json()
       })
       .then((data) => {
         console.log('data:',data)
         location.reload()
       })
}




