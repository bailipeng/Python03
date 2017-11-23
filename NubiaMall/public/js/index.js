//手机   下拉菜单控制
$('.list1 li a:eq(1)').mouseover(function(){
	$('.list0').slideDown().siblings().slideUp()
})

$('.list0').mouseover(function(){
	$('.list0').show()
})

$('.list0').mouseout(function(){
	$('.list0').slideUp()
})

//配件   下拉菜单控制
$('.list1 li a:eq(2)').mouseover(function(){
	$('.list-p').slideDown().siblings().slideUp()
})

$('.list-p').mouseover(function(){
	$('.list-p').show()
})

$('.list-p').mouseout(function(){
	$('.list-p').slideUp()
})


//摄影   下拉菜单控制
$('.list1 li a:eq(3)').mouseover(function(){
	$('.list-s').slideDown().siblings().slideUp()
})

$('.list-s').mouseover(function(){
	$('.list-s').show()
})

$('.list-s').mouseout(function(){
	$('.list-s').slideUp()
})


//nubia   下拉菜单控制
$('.list1 li a:eq(7)').mouseover(function(){
	$('.list-n').slideDown().siblings().slideUp()
})

$('.list-n').mouseover(function(){
	$('.list-n').show()
})

$('.list-n').mouseout(function(){
	$('.list-n').slideUp()
})




//商品列表页左侧菜单js
$('.leftlist .seri-info').mouseover(function(){
	var i = $(this).attr("id");
	$('.Allmenu .menu-hide').eq(i-1).show();
})


$('.leftlist .seri-info').mouseout(function(){
	var i = $(this).attr("id");
	$('.Allmenu .menu-hide').eq(i-1).hide();
})



//商品列表鼠标移入特效

$('.hot-goods').mouseover(function(){
	$(this).find('p').show()
	// $('.price').hide()
	$(this).css('padding-top','40px')
})

$('.hot-goods').mouseout(function(){
	$(this).find('p').hide()
	// $('.price').show()
	$(this).css('padding-top','54px')
})



//商品详情页
$('.top-list li').eq(0).css('border-bottom', '2px solid red')

$('.top-list li').mouseover(function(){
	$(this).css('border-bottom', '2px solid red')
})

$('.top-list li').mouseout(function(){
	$(this).css('border-bottom', '0')
})



//滚动一定距离 显示商品详情和规格参数按钮

$(window).scroll(function(){
	var DT =$(window).scrollTop();
	var $ul=$('<ul class="detailtab"><li>商品详情</li><li  class="tab-2">规格参数</li></ul>')
	
	if(DT>=1650){
		$('.fixed-btn-div').prepend($ul);
		$('.fixed-btn-div').on("click",".detailtab",function(){
			// $('.detailtab li').eq(0).css('color','red')
			$('.detailtab li').eq(0).click(function(){
				$('.row-1').show();
				$('.row-2').hide();
				$(this).css('color','red')
				$(this).next().css('color','black')

			})

			$('.detailtab li').eq(1).click(function(){
				$('.row-2').show();
				$('.row-1').hide();
				$(this).css('color','red');
				$('.detailtab li').eq(0).css('color','black');
				
			})
		})
		
		$(window).unbind();
	}

})

// 商品详情按钮 和 规格参数按钮
$('.detailtab li').eq(0).css('color','red')
$('.detailtab li').eq(0).click(function(){
	$('.row-1').show();
	$('.row-2').hide();
	$(this).css('color','red')
	$(this).next().css('color','black')

})

$('.detailtab li').eq(1).click(function(){
	$('.row-2').show();
	$('.row-1').hide();
	$(this).css('color','red');
	$('.detailtab li').eq(0).css('color','black');
	
})







// 放大镜

//绑定鼠标移入移出
$('.small').mouseover(function(){
	$('.big').show();
	$('.move').show();

	//计算move的宽高
	var blx = $('.big').width()/$('.bimg').width();
	var bly = $('.big').height()/$('.bimg').height();

	var newW=$('.small').width()*blx;
	var newH=$('.small').height()*bly;
	//给move设置合适的大小
	$('.move').css({width:newW+'px',height:newH+'px'})
}).mouseout(function(){
	$('.big').hide();
	$('.move').hide();
})
//鼠标移动跟随
$('.small').mousemove(function(e){
	//鼠标的位置
	var mx = e.pageX;
	var my = e.pageY;

	//move位置
	var x = mx-$(this).offset().left-$('.move').width()/2;
	var y = my-$(this).offset().top-$('.move').height()/2;


	//获取最大的top和left
	var MaxTop = $('.small').height() - $('.move').height();
	var MaxLeft = $('.small').width() - $('.move').width();
	if(x<=0){x=0}
		if(y<=0){y=0}

			if(y>=MaxTop){y=MaxTop}
				if(x>=MaxLeft){x=MaxLeft}
	//设置
	$('.move').css({top:y+'px',left:x+'px'})

	//设置大图移动

	//计算 移动比例
	var xp = x/$('.small').width();
	var yp = y/$('.small').height();

	//计算大图的移动距离
	var Nx = xp*$('.bimg').width();
	var Ny = yp*$('.bimg').height();

	//设置大图移动
	$('.bimg').css({top:-Ny+'px',left:-Nx+'px'});


})

//给缩略图绑定单机事件
$('.uimg li').eq(0).css('border-color','#EB502D').siblings().css('border-color','#CCC')
$('.uimg li').click(function(){
	//获取src属性
	$(this).css('border-color','#EB502D').siblings().css('border-color','#CCC')
	var add = $(this).find('img').attr('src')

	$('.simg').attr('src',add)
	$('.bimg').attr('src',add)
})



//详情选择点击事件

$('.select_btn').click(function(){
	$(this).css('border-color','#EB502D').siblings().css('border-color','#CCC')
})



//滚动   产品图片静止  部分事件

$(window).scroll(function(){
	//获取文档滚动距离
	 var t=$(window).scrollTop();
	 if(t<120){
	 	$('.goods-info').css({position:'static'})
	 	$('.goods-img').css({position:'static'})	 	

	 }

	 if(t>=120){
	 	$('.goods-info').css({position:'relative',left:'585px'})
	 	$('.goods-img').css({
	 		position:'fixed',
	 		top:'0px'
	 	})	 	
	 }
	 if(t>1100){
	 	$('.goods-img').css({
	 		position:'relative',
	 		top:'950px'
	 	})
	 	$('.goods-info').css({position:'relative',left:'0px'})	 	
	 }
})



// 购物车

// 购物车加法
$('.btn-cnts button').eq(1).click(function(){
	var num=$('.btn-cnts input').val();
	var a = eval(Number(num)+1);
	$('.btn-cnts input').attr('value',a);

	var sum = a*2799;
	$('.sum p').html('¥'+eval(Math.floor(sum/1000))+','+eval((sum%1000))+'.00');


})


// 购物车减法
$('.btn-cnts button').eq(0).click(function(){

		var num=$('.btn-cnts input').val();
	if(num>=2){
		var a = eval(Number(num)-1);
		var sum = a*2799;
		$('.sum p').html('¥'+eval(Math.floor(sum/1000))+','+eval((sum%1000))+'.00');

		$('.btn-cnts input').attr('value',a)
	}
})

// 直接输入数量
$('.btn-cnts input').blur(function(){
	var num=$('.btn-cnts input').val();
	var sum = Number(num)*2799;
	$('.sum p').html('¥'+eval(Math.floor(sum/1000))+','+eval((sum%1000))+'.00');
})

//购物车清空

$('.close').click(function(){
	console.log(1)
	$('.shopping-car').hide()
	$('.jindu').hide()
	$('.empty').show()
})



// 登录页面方式按钮

$('.loadType li').eq(0).css('color','red')
$('.loadType li').eq(0).click(function(){
	$(this).css('color','red')
	$(this).next().css('color','black')
})

$('.loadType li').eq(1).click(function(){
	$(this).css('color','red');
	$('.loadType li').eq(0).css('color','black');
})


// 用户名 正则表达验证

//全局变量
var UserOk = false;
var PassOk = false;
// var EmailOk = false;

//绑定表单的提交事件
$('form').submit(function(){
	//触发所有的丧失焦点事件
	$('input').trigger('blur');

	//判断字段是否正确
	if(UserOk && PassOk){
		//都正确就可以提交
		return true;
	}else{
		//有一个错误都不能提交
		return false;
	}
})



//当丧失焦点时进行验证
$('input[type=username]').blur(function(){
	//获取用户输入的信息.进行验证
	var v = $(this).val();
	//进行正则验证
	var reg = /^\w{6,18}$/;
	if(reg.test(v)){
			UserOk = true;
	}else{
		$(this).css('border','1px solid red');
		$(this).next('span').html('用户名不符合要求').css('color','red');
		UserOk = false;
	}

	if(v==""){
		$(this).next('span').html('请填写信息').css('color','red');


	}
})

//给密码框绑定丧失焦点事件
$('input[type=password]').blur(function(){
	//获取用户输入的信息.进行验证
	var v = $(this).val();
	//进行正则验证
	var reg = /(?!^[0-9]+$)(?!^[A-z]+$)(?!^[^A-z0-9]+$)^.{6,16}$/;
	if(reg.test(v)){
		PassOk = true;
	}else{
		$(this).css('border','1px solid red');
		$(this).next('span').html('密码格式错误').css('color','red');
		PassOk = false;
	}
})

