$(document).foundation();

$(document).foundation('reflow');

$(document).on('opened.fndtn.reveal', '[data-reveal]', function () {
  $(document).foundation('reflow');
});

