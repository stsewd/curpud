var container = $('#main-content > div');
var navb = $('#main-content > div > .navbar');

container.removeClass('container');
navb.remove();

// Translations
$('tbody > tr > td[colspan="999"] > div').text('No se encontraron elementos.');
