$(document).ready(function() {
	$(".brand-slider.owl-carousel").owlCarousel({
	  	items: 7,
	  	margin: 30,
	  	loop: true,
	  	nav: false,
	  	dots: false,
	  	autoplay: true,
	  	autoplayTimeout: 5000,
  	});
  	$('.popup-video').magnificPopup({
		disableOn: 700,
		type: 'iframe',
		mainClass: 'mfp-fade',
		removalDelay: 160,
		preloader: false,

		fixedContentPos: false
	});

});
$( document ).ready(function() {
    new WOW().init();
});
