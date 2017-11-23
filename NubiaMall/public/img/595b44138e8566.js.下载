/**
 * Created by nubia on 17/7/4.
 */
jQuery(function($) {

    $(window).scroll(function () {
        if($(window).scrollTop()>66){$(".sub-nav .btn-buy").css({
            "width":"120px",
            "height":"60px",
            "line-height":"60px",
            "margin-top":"0px",
            "font-size":"14px"
        })}else{
            $(".sub-nav .btn-buy").css({
                "width":"85px",
                "height":"25px",
                "line-height":"25px",
                "margin-top":"17px",
                "font-size":"12px"
            })
        }
    })
    
    $("#leftmenu").on("mouseenter",".nb-ml-side ul li",function () {
        var $this=$(this).children(".nb-mlside-menu");
        var _len=$this.children("a").length;

        if(_len>6){
            $this.css("width","400px")
        if(_len>12){$this.css("width","600px")}
        }else{$this.css("width","240px")}

        for(var i=0;i<6;i++){
            $this.children("a:eq("+(i+6)+")").css({
                "position":"absolute",
                "left":"200px",
                "top":89*i
            });
            $this.children("a:eq("+(i+12)+")").css({
                "position":"absolute",
                "left":"400px",
                "top":89*i
            })
        }

    });
});
