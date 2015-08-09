// Generated by CoffeeScript 1.8.0
(function() {
  var load_page, request;

  window.onload = function() {
    if ($('.page-select').length) {
      $('.page-select:first').addClass('curr_page');
      return load_page();
    }
  };

  $('.btn').mousedown(function() {
    return request();
  });

  $('body').on('click', '.page-select', function() {
    request();
    $('.page-select').removeClass('curr_page');
    $('.for-padding').children().remove();
    $(this).addClass('curr_page');
    return load_page();
  });

  request = function() {
    var conten, id_curr_pag;
    id_curr_pag = $('.curr_page').attr("id_page");
    conten = "";
    $.each($('.for-padding').children(), function(index, val) {
      return conten += val.outerHTML;
    });
    return $.ajax({
      url: "/editor/" + $('h2').attr("id_project") + '/',
      type: "POST",
      data: {
        'id_page': id_curr_pag,
        'content': conten,
        'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val()
      },
      async: false,
      success: function() {},
      error: function() {
        return alert('gyjudvasf');
      }
    });
  };

  load_page = function() {
    var id;
    id = $('.curr_page').attr("id_page");
    return $.ajax({
      url: "/editor/" + $('h2').attr("id_project") + '/',
      type: "POST",
      data: {
        'id_return_page': id,
        'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val()
      },
      async: false,
      success: function(data) {
        $('.for-padding').append(data.page);
        return sortab();
      }
    });
  };

}).call(this);

//# sourceMappingURL=select_page.js.map
