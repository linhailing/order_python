;
var account_set_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".do-account .save").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var nickname = $(".do-account input[name=nickname]")
            var mobile = $(".do-account input[name=mobile]")
            var email = $(".do-account input[name=email]")
            var login_name = $(".do-account input[name=login_name]")
            var login_pwd = $(".do-account input[name=login_pwd]")
            var id = $(".do-account input[name=id]")

            if( nickname.val() == undefined || nickname.val().length < 1){
                common_ops.tip( "请输入正确的用户名~~", nickname);
                return;
            }
            if( mobile.val() == undefined || mobile.val().length < 10){
                common_ops.tip( "请输入正确的手机号码~~", nickname);
                return;
            }
            if( email.val() == undefined || email.val().length < 1){
                common_ops.tip( "请输入正确的邮箱~~", email);
                return;
            }

            if( login_name.val() == undefined || login_name.val().length < 1){
                common_ops.tip( "请输入正确的登录用户名~~", login_name);
                return;
            }
            if( login_pwd.val() == undefined || login_pwd.val().length < 1){
                common_ops.tip( "请输入正确的登录密码~~", login_pwd);
                return;
            }

            btn_target.addClass("disabled");
            $.ajax({
                url:common_ops.buildUrl("/account/set"),
                type:'POST',
                data:{ 'nickname':nickname.val(),'mobile':mobile.val(),'email':email.val(),'login_name':login_name.val(),'login_pwd':login_pwd.val(),'id':id.val() },
                dataType:'json',
                success:function(res){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/account/set");
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });
        } );
    }
};

$(document).ready( function(){
    account_set_ops.init();
} );