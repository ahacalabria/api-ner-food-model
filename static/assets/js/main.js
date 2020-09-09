  $(document).ready(function(){
    $('a#calculate').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
      }, function(data) {
        $("#result").text(data.result);
      });
      return false;
    });
    
    
    $("body").on("click", ".tabs ul li a", function(ev){
      ev.preventDefault()
      if(!$(this).parent().hasClass("active")){
        $(".tabs ul li").each(function(){
          $(this).removeClass("is-active")
        })
        $(this).parent().addClass("is-active")
        $(".tabs-container .tab-content").each(function(){
          $(this).removeClass("active")
        })
        let target = $(this).data('target')
        $(target).addClass("active")
      }
    })

    var current_file = "", current_img = ""

    loading = () => {
      $("#menu, #ocr, #img").html(`<div class="lds-ring text-center"><div></div><div></div><div></div><div></div></div>`)
    }

    $("body").on("click", ".genocr", function(ev){
      ev.preventDefault()
      loading()
      let url = $(this).attr("href")
      let ocr = $(this).data("file")
      let img = $(this).data("img")

      current_file = ocr
      current_img = img
      $("#menu").load(url)      

      return false;
    })
    $("body").on("click", ".getocr", function(ev){
      ev.preventDefault()
      loading()
      let url = $(this).attr("href")
      let ocr = $(this).data("file")
      let img = $(this).data("img")

      current_file = ocr
      current_img = img
      $("#menu").load(url)      

      return false;
    })
    

    $("body").on("click", ".viewocr", function(ev){
      ev.preventDefault()
      if(current_file != "")
        $("#ocr").load(current_file)
    })
    $("body").on("click", ".viewimg", function(ev){
      ev.preventDefault()
      if(current_img != "")
        $("#img").html(`<img src="${current_img}" width="100%" height="auto"/>`)
    })
  })