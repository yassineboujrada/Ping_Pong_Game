document.getElementById('score1').innerHTML = user.score1
document.getElementById('score2').innerHTML = user.score2
document.getElementById('playernamedata1').innerHTML = user.player1
document.getElementById('playernamedata2').innerHTML = user.player2
let pause = false
let degx = 1
let degy = 1
let x = 398
let y = 260
let hell = document.getElementById("hell")
let rightborder = document.getElementById("rightborder1")
let leftborder = document.getElementById("leftborder1")
let a = document.getElementById("texthey")
let Line1 = document.getElementById("Line1")
let Line2 = document.getElementById("Line2")
let score1 = 0
let score2 = 0
let move
score1 = user.score2
score2 = user.score1

function collidesWith(element1, element2) {
    var Element1 = {};
    var Element2 = {};

    Element1.top = $(element1).offset().top;
    Element1.left = $(element1).offset().left;
    Element1.right = Number($(element1).offset().left) + Number($(element1).width());
    Element1.bottom = Number($(element1).offset().top) + Number($(element1).height());

    Element2.top = $(element2).offset().top;
    Element2.left = $(element2).offset().left;
    Element2.right = Number($(element2).offset().left) + Number($(element2).width());
    Element2.bottom = Number($(element2).offset().top) + Number($(element2).height());

    if (Element1.right > Element2.left && Element1.left < Element2.right && Element1.top < Element2.bottom && Element1.bottom > Element2.top) {
        return true
    } else {
        return false
    }
}

function moving() {
    a.setAttribute('cx', x);
    a.setAttribute('cy', y);
    if (collidesWith(a, rightborder) || collidesWith(a, leftborder)) {
        degx = -degx
    }
    if (!collidesWith(a, hell)) {
        degy = -degy
    }
    x += 1 * degx
    y += 1 * degy
    if (collidesWith(a, Line1)) {
        score1++
        document.getElementById('score2').innerHTML = score1
        x = 398
        y = 260
        degx = -degx
        degy = -degy
    }
    if (collidesWith(a, Line2)) {
        score2++
        document.getElementById('score1').innerHTML = score2
        x = 398
        y = 260
        degx = -degx
    }
    move = setTimeout('moving()', 1)
    if (pause == true) {
        return 0;
    }
}
//Button to start the game//
document.addEventListener('click', function(R) {
    if (R.target.id == 'Button') {
        moving()
        document.getElementById('Button').style.display = 'none'
    }
});
let left_br = document.getElementById("leftborder")
let right_br = document.getElementById("rightborder")
let last_b_pss = left_br.style.top
let last_r_pss = right_br.style.top
last_b_pss = last_r_pss = 250
let left_br_1 = document.getElementById("leftborder1")
let right_br_1 = document.getElementById("rightborder1")
let last_b_pss_1 = left_br.style.top
let last_r_pss_1 = right_br.style.top
last_b_pss_1 = last_r_pss_1 = 250
let keysPressed = {};
document.addEventListener('keydown', (event) => {
    keysPressed[event.key] = true;
    console.log(event.key)

    if (event.key == 's') {
        if (last_b_pss == 420) { Number(last_b_pss) = 420 }
        last_b_pss = Number(last_b_pss) + 30
        left_br.style.top = `${last_b_pss}px`

        if (last_b_pss_1 == 420) { Number(last_b_pss_1) = 420 }
        last_b_pss_1 = Number(last_b_pss_1) + 30
        left_br_1.style.top = `${last_b_pss_1}px`
    } else if (event.key == 'w') {
        if (last_b_pss == 0) { Number(last_b_pss) = 0 }
        last_b_pss = Number(last_b_pss) - 30
        left_br.style.top = `${last_b_pss}px`

        if (last_b_pss_1 == 0) { Number(last_b_pss_1) = 0 }
        last_b_pss_1 = Number(last_b_pss_1) - 30
        left_br_1.style.top = `${last_b_pss_1}px`
    } else if (event.key == 'l') {
        if (last_r_pss == 420) { Number(last_r_pss) = 420 }
        last_r_pss = Number(last_r_pss) + 30
        right_br.style.top = `${last_r_pss}px`

        if (last_r_pss_1 == 420) { Number(last_r_pss_1) = 420 }
        last_r_pss_1 = Number(last_r_pss_1) + 30
        right_br_1.style.top = `${last_r_pss_1}px`
    } else if (event.key == 'o') {
        console.log(right_br_1.style.top )
        if (last_r_pss_1 == 0) { Number(last_r_pss) = 0 }
        last_r_pss_1 = Number(last_r_pss_1) - 30
        right_br_1.style.top = `${last_r_pss_1}px`

        if (last_r_pss == 0) { Number(last_r_pss_1) = 0 }
        last_r_pss = Number(last_r_pss) - 30
        right_br.style.top = `${last_r_pss}px`
    }
});

function out() {
    let user_score = {
        'player1': score1,
        'player2': score2
    }
    const request = new XMLHttpRequest()
    request.open('POST', `/${JSON.stringify(user_score)}`)
    request.onload = () => {
        const data = request.responseText
        console.log(data)
    }
    request.send()
    clearTimeout(move)
    document.getElementById('Button').style.display = 'block'
}