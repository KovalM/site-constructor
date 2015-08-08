// Generated by CoffeeScript 1.8.0
(function() {
  var currentPage, request, setAllPages, setHorizontalMenu, setVerticalMenu;

  $(function() {
    return $('input.view_menu[type=radio]').click(function() {
      var id;
      id = $('h2').attr("id_project");
      if ($(this).hasClass('horizontal')) {
        if (!$('div').is('.page_group_horizontal')) {
          setHorizontalMenu(id);
          return request(id, 'True');
        }
      } else {
        if (!$('div').is('.page_group_vertical')) {
          setVerticalMenu(id);
          return request(id, 'False');
        }
      }
    });
  });

  request = function(id, is_horizontal) {
    return $.ajax({
      url: "/menu/",
      type: "GET",
      data: {
        'proj_id': id,
        'is_horizontal': is_horizontal
      },
      success: function(data) {},
      error: function() {
        return alert('gyjudvasf');
      }
    });
  };

  currentPage = "";

  setHorizontalMenu = function(id) {
    currentPage = $('.curr_page').attr('id_page');
    $('.page_group_vertical').remove();
    $('.work_space').prepend('<div class="col-md-12 btn-group" role="group" ></div>');
    return setAllPages(id, '.page_group_horizontal', currentPage);
  };

  setVerticalMenu = function(id) {
    currentPage = $('.curr_page').attr('id_page');
    $('.page_group_horizontal').remove();
    $('.work_space').append('<div id="page_group" class="col-md-2 btn-group-vertical page_group_vertical" role="group"> </div>');
    return setAllPages(id, '.page_group_vertical', currentPage);
  };

  setAllPages = function(id, oriented, local_page) {
    return $.ajax({
      url: "/get_all_pages/",
      type: "GET",
      data: {
        'proj_id': id
      },
      success: function(data) {
        var page, _i, _len, _ref, _results;
        _ref = data.pages;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          page = _ref[_i];
          $(oriented).append('<button class="btn btn-primary page-select" id_page=""><span class="btn btn-xs glyphicon glyphicon-remove navbar-right"></span></button>');
          if (page.pageID.toString() === local_page.toString()) {
            $('[id_page = ""]').addClass('curr_page');
          }
          $('[id_page = ""]').append(page.pageName);
          _results.push($('[id_page = ""]').attr('id_page', page.pageID));
        }
        return _results;
      },
      error: function() {
        return alert('in change_menu');
      }
    });
  };

}).call(this);

//# sourceMappingURL=change_menu.js.map
