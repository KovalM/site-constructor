$ ->
  $('.glyphicon').click ->
    id = $(this).parent().children('.proj_id').val()
    parent = $(this).parent()
    $.ajax
      url: "/my_projects/"
      type: "GET"
      data: {'proj_id': id}
      success:(data) ->
        parent.remove()
      error: ->
        alert 'gyjudvasf'