// JavaScript Document

$(document).ready(function () {
	var height=$(document).height();
	$('.main').css('height',height);
})
$(function(){
    $(".tipTimer").trigger("click");
})

$(function (){
   $('.captcha').click(function (){
	   // console.log('click');
	   $.getJSON("/captcha/refresh/",function (result){
		   $('.captcha').attr('src',result['image_url']);
		   $('#id_captcha_0').val(result['key'])
	   })
   });
});

var countdown = 60; //总倒计时时间
var timer; //计时器
function startCountdown() {
    var btn = document.getElementById("btn");
    btn.disabled = true; // 按钮不可用
    timer = setInterval(function () {
        countdown--; // 倒计时减1秒
        if (countdown <= 0) { // 倒计时结束
            clearInterval(timer); // 清除计时器
            btn.disabled = false; // 恢复按钮状态
            btn.textContent = "获取邮箱验证码"; // 恢复默认按钮文字
            countdown = 60; // 重置倒计时时间
        } else {
            btn.textContent = countdown + "s后可重新发送"; // 更新倒计时显示
        }
    }, 1000); // 每隔1秒更新一次倒计时
    }
 function sendVerificationCode(emails) {
            // 获取输入的手机号
            const formData = new FormData()
            formData.append('email', emails)

            fetch("/users/send-code/" + emails + '/', {
                method: "POST",
                body: formData,
            })
                .then(response => {
                    if (response.success) {
                        console.log("验证码发送成功！");
                        // 启动倒计时计时器
                        startCountdown();
                    } else {
                        console.log("验证码发送失败，请重试！");
                    }
                });
        }

         ;


