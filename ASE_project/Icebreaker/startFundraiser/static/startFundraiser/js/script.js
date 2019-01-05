
 // $('h1').slideUp(1000).slideDown(1000);
 // $('#main').css({
 //    color: 'red',
 //    fontSize: 25
 // });


// $('p').click(function() {
//     $(this).hide();
// })

 // Preloader
 $(window).on('load', function() {
     $('#status').fadeOut();
     $('#preloader').delay(350).fadeOut('slow');
 }); //anonymous function

 $(window).on('scroll', function() {
                if($(window).scrollTop()){
                    $('nav').addClass('black');
                }
                else{
                    $('nav').removeClass('black');
                }
            });


 $(document).ready(function() {
     $(function() {
         $( "#dialogbox" ).dialog({
             modal: true,
             closeOnEscape: false,
             dialogClass: "no-close",
             resizable: false,
             draggable: false,
             width: 600,
             buttons: [
                 {
                     text: "Confirm",
                     click: function() {
                         $( this ).dialog( "close" );
                     }
                 }
                    ]
         });
     });
 });


 $(function () {
     $('campaigns').owlCarousel({
         items:2,
         autoplay:true,
         smartSpeed: 700,
         loop:true,
         autoplayHoverPause: true,
         nav: true,
         dots: false,
         navText: ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>']
     });

 });
