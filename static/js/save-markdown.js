// Generated by CoffeeScript 1.8.0
(function() {
  $(function() {
    $('textarea').autoGrow();
    return $('#droppable').on('keyup', '.markdown-field', function() {
      $(this).text($(this).val());
      return $('textarea').autoGrow();
    });
  });

}).call(this);

//# sourceMappingURL=save-markdown.js.map