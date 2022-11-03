// 빵집 이미지 carousel
// 첫번째 button과 첫번째 carousel-item의 클래스에 active 추가 
const shopImageCarouselButtons = document.querySelectorAll('.carousel-indicators > button')
const shopImageCarouselItems = document.querySelectorAll('.carousel-item')

shopImageCarouselButtons[0].classList.add('active')
shopImageCarouselItems[0].classList.add('active')
