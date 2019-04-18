;
var user_edit_ops = {
    init:function(){
        this.eventBind();
    },
    eventBind:function(){
        $(".do-edit .save").click( function(){
            var btn_target = $(this);
            if( btn_target.hasClass("disabled") ){
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var name = $(".do-edit input[name=nickname]")
            var email = $(".do-edit input[name=email]")

            if( name.val() == undefined || name.val().length < 1){
                common_ops.tip( "请输入正确的登录用户名~~", name);
                return;
            }
            if( email.val() == undefined || email.val().length < 1){
                common_ops.tip( "请输入正确的邮箱~~", email);
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url:common_ops.buildUrl("/user/edit"),
                type:'POST',
                data:{ 'name':name.val(),'email':email.val() },
                dataType:'json',
                success:function(res){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if( res.code == 200 ){
                        callback = function(){
                            window.location.href = common_ops.buildUrl("/user/edit");
                        }
                    }
                    common_ops.alert( res.msg,callback );
                }
            });
        } );
    }
};

$(document).ready( function(){
    user_edit_ops.init();
} );