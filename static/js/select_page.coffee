window.onload = ->
  if $('.page-select').length
    $('.page-select:first').addClass('curr_page')
    load_page()
$ ->
  $('.page-select').click ->
    id_curr_page = $('.curr_page').attr("id_page")
    content = ""
    $.each $('.for-padding').children(), (index, val) ->
      content += val.outerHTML
    $.ajax
      url: "/editor/"+$('h2').attr("id_project")+'/'
      type: "GET"
      data: {'id_page':id_curr_page,'content': content}
      async:false
      success:->
      error: ->
        alert 'gyjudvasf'
    $('.page-select').removeClass('curr_page')
    $('.for-padding').children().remove()
    $(this).addClass('curr_page')
    load_page()

  $('#droppable').on('mousemove', ->
    )

load_page = ->
  id = $('.curr_page').attr("id_page")
  $.ajax
    url:"/editor/"+$('h2').attr("id_project")+'/'
    type:"GET"
    data:{'id_return_page':id}
    async:false
    success:(data)->
      $('.for-padding').append(data.page)
