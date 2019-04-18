;
var user_reset_pwd_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".do-reset .save").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var old_password = $("#old_password")
            var new_password = $("#new_password")

            if( old_password.val() == undefined || old_password.val().length < 1){
                common_ops.tip( "请输入正确的旧密码~~", old_password);
                return;
            }
            if( new_password.val() == undefined || new_password.val().length < 6){
                common_ops.tip( "请输入正确的新密码~~", new_password);
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url:common_ops.buildUrl("/user/reset-pwd"),
                type:'POST',
                data:{ 'old_password':old_password.val(),'new_password':new_password.val() },
                dataType:'json',
                success:function(res){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/user/reset-pwd");
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });
        } );
    }
};

$(document).ready( function(){
    user_reset_pwd_ops.init();
} );