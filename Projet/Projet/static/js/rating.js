const allStars = document.querySelectorAll('.star');
console.log(allStars);
allStars.forEach( (star,i) =>{
    star.onclick = function(){
        event.preventDefault();
        let current_star_level = i + 1;
        allStars.forEach((star, j) =>{
            if(current_star_level >= j +1){
                star.innerHTML = '&#9733';
            }else{
                star.innerHTML = '&#9734';
            }
    })
    }
});

const allStars2 = document.querySelectorAll('.star2');
console.log(allStars2);
allStars2.forEach( (star2,k) =>{
    star2.onclick = function(){
        event.preventDefault();
        let current_star_level = k + 1;
        allStars2.forEach((star2, r) =>{
            if(current_star_level >= r +1){
                star2.innerHTML = '&#9733';
            }else{
                star2.innerHTML = '&#9734';
            }
    })
    }
});