const searchIcon = document.querySelector('.navbar .search i');
const searchForm = document.querySelector('.navbar .search');
const cartIcon = document.querySelector('.navbar .cart');
const cartItems = document.querySelector('.navbar .cart-items');
const menuBarIcon = document.querySelector('.navbar .menu-bar i');
const menuBarList = document.querySelector('.navbar .menu-bar-list');

searchIcon.onclick = () => {
  searchForm.classList.toggle('active');
  cartItems.classList.remove('active');
  menuBarList.classList.remove('active');
}

cartIcon.onclick = () => {
  cartItems.classList.toggle('active');
  searchForm.classList.remove ('active');
  menuBarList.classList.remove('active');
}

menuBarIcon.onclick = () => {
  menuBarList.classList.toggle('active');
  searchForm.classList.remove('active');
  cartItems.classList.remove('active');
}

window.onscroll = () => {  
  cartItems.classList.remove('active');
  searchForm.classList.remove('active');
  menuBarList.classList.remove('active');
}