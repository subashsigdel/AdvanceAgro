$(document).ready(function() {
    $(".notification-drop .item").on('click',function() {
      $(this).find('ul').toggle();
    });
  });