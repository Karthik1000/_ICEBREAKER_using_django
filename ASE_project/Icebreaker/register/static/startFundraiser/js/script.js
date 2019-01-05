
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

 $()