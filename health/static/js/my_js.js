var my_data = ""
function homePage(){
    $.ajax({
            type:'GET',
            url:'/home_captcha/',
            success:function(data){
                console.log(data)
                my_data = data
                tag = document.createElement("img");
                tag.src = "media/captcha.jpg"
                tag.classList.add("captchaImage");
                tag.setAttribute('id','captchaImage');
                document.getElementById('captcha_frame').prepend(tag);
            }
        })
}

function refreshCaptcha(){
    element = document.getElementById('captchaImage')
    element.remove()
    homePage()
}

function login(){
    let login = false
    let captcha = document.getElementById('captcha');
    inputs = document.getElementsByClassName("form-input")
    for (let i=0;i<inputs.length;i++){
        console.log(inputs[i].value)
        if(inputs[i].value!= 0){
            inputs[i].classList.add("valid")
            inputs[i].classList.remove("invalid")
            login = true
        }
        else{
            inputs[i].classList.remove("valid")
            inputs[i].classList.add("invalid")
            login =false
        }
    }
    if (login==true ){
        if (my_data.text == captcha.value ){
            document.getElementById("loginText").innerHTML = ""
            login =true
        }
        else {
            document.getElementById("loginText").innerHTML = " * Invalid Captcha"
            login =false
            }
        }
}

var timeLeft = 60;
var timerId;
function countdown() {
    if (timeLeft == -1) {
        clearTimeout(timerId);
        document.getElementById('resend-btn').hidden=false;
        document.getElementById('resend-text').hidden=true;
    } else {
        document.getElementById('resend-text').innerHTML = timeLeft + ' seconds remaining';
        timeLeft--;
    }
}

function otpGenerator(){
    if (document.getElementById('username').value.length == 0){
        document.getElementById('email-text').innerHTML = "enter the valid email";
    }
    else{
        document.getElementById('email-text').innerHTML = "";
        $.ajax({
        type:'POST',
        url:'/emailGeneration/',
        data:{
            email:document.getElementById('username').value,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
            },
        success:function(data){
            if(data == 'not valid'){
                document.getElementById('email-text').innerHTML = "enter the valid email";
                }
            else if (data == 'not unique'){
             document.getElementById('email-text').innerHTML = "entered email already exist";
            }
            else if(data == "send"){
                document.getElementById('otp').hidden=false;
                document.getElementById('otpGen').hidden=true;
                document.getElementById('buttons').hidden=false;
                document.getElementById('valid-btn').hidden=false;
                timerId = setInterval(countdown, 1000);
                document.getElementById('username').readOnly=true;
                emailVerified = 1;
               }
        }
    })
    }
}

function otpValidator(){
    $.ajax({
            type:'POST',
            url:'/emailValidation/',
            data:{
                otp:document.getElementById('my-otp').value,
                csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
                },
            success:function(data){
                if (data == 'valid'){
                    document.getElementById('email-text').innerHTML = "email is validated successfully"
                    document.getElementById('email-text').style.color = "green"
                    document.getElementById('otp').hidden=true;
                    document.getElementById('otpGen').hidden=true;
                    document.getElementById('buttons').hidden=true;
                    document.getElementById('password').hidden=false;
                    document.getElementById('confirm-password').hidden=false;
                    document.getElementById('submit-button').hidden=false;
                    document.getElementById('resend-btn').hidden=true;
                    document.getElementById('username').readOnly=true;
                }
                else{
                    document.getElementById('email-text').innerHTML = "wrong otp entered"
                }
            }
    })
}

function matchingOfPassword(){
    let password1 = document.getElementById('id_password').value;
    let password2 = document.getElementById('confirm_pass').value;
    if( password1 == password2){
        document.getElementById('password_text').innerHTML = "";
        passwordMatched = 1
//        document.getElementById('submit_button').disabled = false;
        }
    else
        {
//        document.getElementById('submit_button').disabled = true;
        passwordMatched=0
        document.getElementById('password_text').innerHTML = "passwords doesn't match";
        }
}