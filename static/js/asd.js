var swiper = new Swiper('.swiper-container', {
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    slidesPerView: 1,  //초기값 설정 모바일값이 먼저!!
    spaceBetween: 10,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    breakpoints: {
    
      768: {
        slidesPerView: 2,  //브라우저가 768보다 클 때
        spaceBetween: 20,
      },
      1024: {
        slidesPerView: 3,  //브라우저가 1024보다 클 때
        spaceBetween: 30,
      },
      3000: {
        slidesPerView: 4,  
        spaceBetween: 0,
      }
    },
    autoplay:{
        delay: 10000,
    }
  });

  $(function () {
    $(document).scroll(function () {
      var $nav = $(".fixed-top");
      $nav.toggleClass('scrolled', $(this).scrollTop() > $nav.height());
    });
  });

  $( document ).ready(function () {
    $(".moreBox").slice(0, 3).show();
      if ($(".blogBox:hidden").length != 0) {
        $("#loadMore").show();
      }   
      $("#loadMore").on('click', function (e) {
        e.preventDefault();
        $(".moreBox:hidden").slice(0, 6).slideDown();
        if ($(".moreBox:hidden").length == 0) {
          $("#loadMore").fadeOut('slow');
        }
      });
    });