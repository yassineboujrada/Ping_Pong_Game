function show_password() {
    var x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }
function password_confirm(){
  a = document.getElementById('password')
  b = document.getElementById('confirm_password')
  if(b.value && b.value.length>a.value.length){
    if (a.value===b.value) {
      b.style.border='0px'
        console.log('worn')
    } else {
        b.style.border='1px solid red'
        console.log('go on')
    }
  }
  else {
      b.style.border='0px'
    }
  
setTimeout('password_confirm()', 100)
}
if (document.getElementById('password')){
password_confirm()
}


