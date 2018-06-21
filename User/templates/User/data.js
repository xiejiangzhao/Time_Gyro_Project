  function logotwo() {
            $.getJSON("/VoteAppraisal/VA/LoginCheak?User=" + $("#username").val() +
            "&&PassWord=" + $("#password").val(),
            function (data) {

                if (data != "") {
                    $("#yzuser").text(data);  //这个是[请登录]的标签 登录成功后显示用户名
                    alert("welcome!");

                    }
                else {
                    alert("false.");
                }
            });