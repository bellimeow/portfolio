$(document).ready(function() {
  // This code will be run when the document is ready.

  $('.dropdown-menu a').on('click', function(e) {
    var a = $(e.currentTarget)
    var input = a.find('input')
    if (input) {
      // Toggle the 'checked' property.
      input.prop('checked', !input.prop('checked'));
    }

    // Unfocus element.
    a.blur();

    // Return false to prevent dropdown menu from closing.
    return false;
  });
});
