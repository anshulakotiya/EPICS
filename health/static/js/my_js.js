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
                document.getElementById('id_username').readOnly=true;
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
                    document.getElementById('id_username').readOnly=true;
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