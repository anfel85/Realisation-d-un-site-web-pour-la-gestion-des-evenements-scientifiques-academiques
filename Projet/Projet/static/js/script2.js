var swiper = new Swiper(".slide-content", {
    slidesPerView: "auto",
    spaceBetween: 30,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },



    breakpoints:{
        0:{
            slidesPerView: 2,
        },
    
        662:{
            slidesPerView: 3,
        },
        950:{
            slidesPerView: 4,
        },
    }
  });