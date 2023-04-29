//*
// 登录表单验证
// /
function nameForm() {
    var name = document.forms["login_form"]["username"].value;

    if (name == null || name == "") {
        alert("用户名不能为空！！！");
        return false;
    }
    if (document.login_form.username.value.length > 12) {
        alert("用户名不能超过12个字符！");
        document.login_form.username.focus();
        return false;
    } else {
        var reg = /^[0-9a-zA-Z]*$/;

        if (reg.test(name) === false) {
            alert("用户名只能是字母或数字！！！");
            return false;
        }

    }
}

function passwordForm() {
    var pwd = document.forms["login_form"]["password"].value;

    if (pwd == null || pwd == "") {
        alert("密码不能为空！！！");
        return false;
    }
    if (document.login_form.password.value.length < 6) {
        alert("密码必须大于6字符！");
        document.login_form.password.focus();
        return false;
    } else {
        var reg = /^[0-9a-zA-Z]*$/;

        if (reg.test(pwd) === false) {
            alert("密码只能是字母或数字！！！");
            return false;
        }

    }
}

function validateForm() {
    var flag =  nameForm() || passwordForm();
    return flag;
}

