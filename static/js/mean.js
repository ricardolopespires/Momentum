window.addEventListener("scroll", function(){
	var header = document.querySelector("header");
	header.classList.toggle('sticky', window.scrollY > 0)


})


window.addEventListener("scroll", function(){
	var header = document.querySelector(".nav__logo");
	header.classList.toggle('nav__logo-dark', window.scrollY > 0)


})

window.addEventListener("scroll", function(){
	var header = document.querySelector(".ponto");
	header.classList.toggle('ponto_white', window.scrollY > 0)


})