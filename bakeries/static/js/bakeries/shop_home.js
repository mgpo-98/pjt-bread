// 현재 클릭한 탭 버튼에 따라 tap-btns/tap-infos 태그 활성화
const tapBtns = document.querySelectorAll('.tap-btns a')
const tapInfos = document.querySelectorAll('.tap-infos article')

for (let tapBtn of tapBtns) {
  tapBtn.addEventListener('click', function (event) {
    event.preventDefault()
    // 전체 탭 버튼(a 태그)의 클래스에서 active 삭제
    for (let tapBtn of tapBtns) {
      tapBtn.classList.remove('active')
    }
    // 현재 클릭한 탭 버튼의 클래스에만 active 추가
    event.target.classList.add('active')

    // 전체 tap-infos 태그의 클래스에서 active 삭제
    for (let tapInfo of tapInfos) {
      tapInfo.classList.remove('active')
    }
    // 현재 클릭한 탭 버튼에 해당하는 tap-infos 태그에만 active 추가
    let idx = parseInt(event.target.dataset.order)
    tapInfos[idx].classList.add('active')
  })
}



// home 탭의 가게 편의 시설 정보에서 가장 마지막의 '/'는 빼기
const facilityDetails = document.querySelectorAll('.facility_details span')

facilityDetails[facilityDetails.length - 1].textContent = ''



// 빵집 이미지 carousel
// 첫번째 button과 첫번째 carousel-item의 클래스에 active 추가 
const shopImageCarouselButtons = document.querySelectorAll('.carousel-indicators > button')
const shopImageCarouselItems = document.querySelectorAll('.carousel-item')

shopImageCarouselButtons[0].classList.add('active')
shopImageCarouselItems[0].classList.add('active')
