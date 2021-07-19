// const hamburgerButton = document.getElementById('hamburger')
// const navList = document.getElementById('nav-list')

// function toggleButton() {
//     navList.classList.toggle('show')
// }

// hamburgerButton.addEventListener('click', toggleButton)

// borrowed code from https://tobiasahlin.com/moving-letters/#10 to animate letters
// Wrap every letter in a span
if (document.querySelector('.ml10 .letters')) {
   var textWrapper = document.querySelector('.ml10 .letters');
    textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: true})
  .add({
    targets: '.ml10 .letter',
    rotateY: [-90, 0],
    duration: 1300,
    delay: (el, i) => 45 * i
  }).add({
    targets: '.ml10',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000
  });


// // smooth scroll
// $('.navbar a').on('click', function (e) {
//     if (this.hash !== '') {
//       e.preventDefault();
  
//       const hash = this.hash;
  
//       $('html, body')
//         .animate({
//           scrollTop: $(hash).offset().top
//         },800);
//     }
//   });


  // let navbar = document.getElementById('navbar')
  // let scrollval = 0;
  // window.addEventListener('scroll', () => {
  //   if(scrollval > window.scrollY) {
  //       navbar.classList.remove('hide')
  //     console.log('Scroll up')
  //   } else {
  //     navbar.classList.add('hide')
  //     console.log('Scroll down')
  //   }
  //   scrollval = window.scrollY;
  // })}

  /* -- enable tooltips -- */
  $(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
  });


}

if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){

    $('body').addClass('noanimated'); // to remove transition}

}

/* Hide navbar on 404 and 500 pages */
document.addEventListener("DOMContentLoaded", function(event) {
  document.getElementById('navigation').style.display = 'none';
});