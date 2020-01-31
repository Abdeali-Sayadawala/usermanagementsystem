function val(){
    let errs = 0;
    //Name Validation
    if(document.getElementById('name').value === ''){
        document.querySelector('#error.name').innerHTML = 'please enter your name';
        errs = errs + 1;
    }
    //E-mail validation
    if(document.getElementById('mail').value === ''){
        document.querySelector('#error.mail').innerHTML = 'please enter E-mail';
        errs = errs + 1;
    }else{
        let mail = document.getElementById('mail').value;
        let atpos = mail.indexOf('@');
        let dotpos = mail.lastIndexOf('.');
        if(atpos === -1){
            document.querySelector('#error.mail').innerHTML = 'E-mail invalid';
            errs = errs + 1;
        }
        if (atpos > dotpos+2 && dotpos+2 > mail.length){
            document.querySelector('#error.mail').innerHTML = 'E-mail invalid';
            errs = errs + 1;
        }
    }
    //password validation
    if(document.getElementById('pass').value === ''){
        document.querySelector('#error.pass').innerHTML = 'please enter Password';
        errs = errs + 1;
    }else if(document.getElementById('pass').value.length < 8){
        document.querySelector('#error.pass').innerHTML = 'please enter Password with length 8+';
        errs = errs + 1;
    }
    //confirmpassword validation 
    if(document.getElementById('cpass').value === ''){
        document.querySelector('#error.cpass').innerHTML = 'please enter Confirm-Password';
        errs = errs + 1;
    }else if(document.getElementById('pass').value !== document.getElementById('cpass').value){
        document.querySelector('#error.cpass').innerHTML = "Passwords don't match";
        errs = errs + 1;
    }
    //mobile validation
    if(document.getElementById('mobile').value === ''){
        document.querySelector('#error.num').innerHTML = 'please enter Mobile';
        errs = errs + 1;
    }else if(document.getElementById('mobile').value.length != 10){
        document.querySelector('#error.num').innerHTML = 'Enter Valid Mobile Number';
        errs = errs + 1;
    }
    // console.log(errs);
    if(errs !== 0){
        console.log(errs);
        return false;
    }
}