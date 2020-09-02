/*---LEFT BAR ACCORDION----*/
$(function() {
  $('#nav-accordion').dcAccordion({
    eventType: 'click',
    autoClose: true,
    saveState: true,
    disableLink: true,
    speed: 'slow',
    showCount: false,
    autoExpand: true,
    cookie: 'dcjq-accordion-1',
    classExpand: 'dcjq-current-parent'
  });
});


var Script = function() {


  //    sidebar dropdown menu auto scrolling

  jQuery('#sidebar .sub-menu > a').click(function() {
    var o = ($(this).offset());
    diff = 250 - o.top;
    var hSize = $(window).height();
    
    setTimeout(function() { 
      var sidebar_hSize = 120 + $("#sidebar").height();
      if(hSize <= sidebar_hSize){ 
        $("#sidebar").css({'height':'100%'})
      } 
    
    }, 300)
    if (diff > 0){
      $("#sidebar").scrollTo("-=" + Math.abs(diff), 500);
    }else{
      $("#sidebar").scrollTo("+=" + Math.abs(diff), 500);
    }

    // if(){}



  });

  //    sidebar toggle

  $(function() {
    function responsiveView() {
      var wSize = $(window).width();
      if (wSize <= 768) {
        $('#container').addClass('sidebar-close');
        $('#sidebar').css({'height':'auto' });
        $('#sidebar > ul').hide();
      }

      if (wSize > 768) {
        $('#container').removeClass('sidebar-close');
        $('#sidebar').css({'height':'100%' });
        $('#sidebar > ul').show();
      }
    }
    $(window).on('load', responsiveView);
    $(window).on('resize', responsiveView);
  });

  $('.fa-bars').click(function() {
    if ($('#sidebar > ul').is(":visible") === true) {
      $('#main-content').css({
        'margin-right': '0px'
      });
      $('#sidebar').css({
        'margin-right': '0px',
        'width': '0px'
      });
      $('#sidebar > ul').fadeOut('3000');
      $("#sidebar").css({'height':'auto'})
      $("#container").addClass("sidebar-closed");
      
    } else {
      $('#main-content').css({
        'margin-right': '190px'
      });
      $('#sidebar > ul').fadeIn('3000');
      $('#sidebar').css({
        'margin-left': '0',
        'height':'100%',
        'width': '190px'
      });
      $("#container").removeClass("sidebar-closed");
    }
  });
  

  // custom scrollbar.getNiceScroll().resize();
  $("#sidebar").niceScroll({
    styler: "fb",
    cursorcolor: "rgb(252, 248, 227)",
    emulatetouch: false,
    cursorwidth: '3',
    cursorborderradius: '10px',
    background: ' rgb(167, 167, 168)',
    spacebarenabled: false,
    gesturezoom: true, 
    cursorborder: ''
  }).resize();

  
  //  $("html").niceScroll({styler:"fb",cursorcolor:"#4ECDC4", cursorwidth: '6', cursorborderradius: '10px', background: '#404040', spacebarenabled:false,  cursorborder: '', zindex: '1000'});

  // widget tools

  jQuery('.panel .tools .fa-chevron-down').click(function() {
    var el = jQuery(this).parents(".panel").children(".panel-body");
    if (jQuery(this).hasClass("fa-chevron-down")) {
      jQuery(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
      el.slideUp(200);
    } else {
      jQuery(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
      el.slideDown(200);
    }
  });

  jQuery('.panel .tools .fa-times').click(function() {
    jQuery(this).parents(".panel").parent().remove();
  });


  //    tool tips

  $('.tooltips').tooltip();

  //    popovers

  $('.popovers').popover();



  // custom bar chart

  if ($(".custom-bar-chart")) {
    $(".bar").each(function() {
      var i = $(this).find(".value").html();
      $(this).find(".value").html("");
      $(this).find(".value").animate({
        height: i
      }, 2000)
    })
  }

}();

jQuery(document).ready(function( $ ) {

  // Go to top
  $('.go-top').on('click', function(e) {
    e.preventDefault();
    $('html, body').animate({scrollTop : 0},500);
  });
});
