// JavaScript Document
var countdown=60; 
function settime(val) { 
	if (countdown == 0) { 
		val.removeAttribute("disabled"); 
		val.text="获取到短信验证码"; 
		countdown =60;

	} else { 
		val.setAttribute("disabled", true); 
		val.text=countdown+"秒后可重新发送"; 
		countdown--; 
		setTimeout(function() { 
			settime(val) 
		},1000) 
	} 

} 
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

