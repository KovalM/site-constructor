// Generated by CoffeeScript 1.9.3
(function() {
  $(function() {
    $('body').on('click', 'select', function() {
      return $('#select_lang_form').submit();
    });
    return $('body').on('click', 'option', function() {
      $('option').removeAttr('selected');
      return $(this).attr('selected', 'selected');
    });
  });

}).call(this);

//# sourceMappingURL=change_language.js.map