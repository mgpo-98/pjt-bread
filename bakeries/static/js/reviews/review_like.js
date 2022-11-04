// (1) 좋아요 버튼
const likeBtn = document.querySelector('#like-btn')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

console.log(likeBtn)
// (2) 좋아요 버튼을 클릭하면, 함수 실행
likeBtn.addEventListener('click', function (event) {
    // 서버로 비동기 요청(axios)을 하고 싶음
    event.preventDefault()
    console.log(event.currentTarget.dataset.reviewId)
    axios({
    method: 'post',
    url: `/reviews/${event.currentTarget.dataset.reviewId}/like/`,
    headers: { 'X-CSRFToken': csrftoken },
    })
    .then(response => {
    console.log(response)
    console.log(response.data)
    const likeReview = document.querySelector('#like-btn > button > i')
    likeReview.classList.toggle('bi-heart')
    likeReview.classList.toggle('bi-heart-fill')
    // 다음 주석 처리한 내용과 동일
    // if (response.data.isLiked === true) {
    //     event.target.classList.add('bi-heart-fill')
    //     event.target.classList.remove('bi-heart')
    // } else {
    //     event.target.classList.add('bi-heart')
    //     event.target.classList.remove('bi-heart-fill')
    // }
    const likeCount = document.querySelector('#review-like-user-cnt')
    likeCount.innerText = response.data.likeCount   
    })
})