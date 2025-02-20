//弹出框，包括信息text，以及一个确认按钮
function alertDiv(text){
    //生成一个随机id
    var time=new Date().getMilliseconds()
    var num=Math.ceil(Math.random()*10000)
    var id=time+""+num
    //设置完全屏蔽的div
    width=window.screen.width+"px"
    height=window.screen.height+"px"
    //alert(width+"-"+height)
    var div_html="<div id='cover"+id+"' style='position: absolute;top: 0px;left: 0px;width:"+width+";height:"+height+";'></div>"
    $("body").append(div_html)
    //设置弹出框
    width2=window.screen.width*0.2+"px"
    height2=window.screen.height*0.2+"px"
    left2=window.screen.width*0.22+"px"
    top2=window.screen.height*0.1+"px"
    top2_begin=window.screen.height*0.3+"px"
    var div2_html="<div id='alert"+id+"' class='shadow alert' style='top:"+top2_begin+";left:"+left2+";width:"+width2+";height:"+height2+";'></div>"
    $("body").append(div2_html)
    //设置弹出框显示内容
    height3=window.screen.height*0.2*0.6+"px"
    var content_html="<div style='background-color: white;height:"+height3+"'>"+text+"</div>"
    $("#alert"+id).append(content_html)
    //设置弹出框的确定按钮
    width3=window.screen.width*0.2*0.5+"px"
    var button_html="<button onclick=\"delCover('"+id+"')\" style='margin-top:15px;width:"+width3+"'>确定</button>"
    $("#alert"+id).append(button_html);
    //从下渐出
    $("#alert"+id).animate({
        top:top2,
        opacity:'1'
    })
}
//关闭刚才的弹出框
function delCover(id){
    $("#alert"+id).animate({
        top:'200px',
        opacity:'0'
    })
    $('#cover'+id).remove()
    setTimeout(function(){
        $('#alert'+id).remove()
    },300)

}
//弹出框，包括一个iFrame，路径为参数
function alertFrame(path,bu1_name,bu2_name,fun_name){
    // alert(window.scrollY)
    //生成一个随机id
    var time=new Date().getMilliseconds();
    var num=Math.ceil(Math.random()*10000);
    var id=time+""+num;
    //设置完全屏蔽的div
    width=window.screen.width;
    height=window.screen.height;
    //alert(width+"-"+height)
    var div_html="<div id='cover"+id+"' style='position: absolute;top: 0px;left: 0px;width:"+width+"px;height:"+height+"px;'></div>";
    $("body").append(div_html);
    //设置弹出框
    width2=window.screen.width*0.4;
    height2=window.screen.height*0.6;
    left2=window.screen.width*0.11;
    top2=window.screen.height*0.1 + window.scrollY;
    top2_begin=window.screen.height*0.3 + window.scrollY;
    if (window.top != window.self){
        top2 = top2 + window.parent.scrollY;
        top2_begin = top2_begin + window.parent.scrollY;
    }

    var div2_html="<div id='alert"+id+"' class='shadow alert' style='position: absolute;top:"+top2_begin+"px;left:"+left2+"px;width:"+width2+"px;height:"+height2+"px;'></div>"
    $("body").append(div2_html)

    //设置弹出框显示内容
    height3=height2*0.90
    width3=width2
    var content_html="<iframe src='"+path+"' id='alertFrame' width='"+width3+"px' style='background-color: white;height:"+height3+"px;'>"+path+"</iframe>"
    $("#alert"+id).append(content_html)
    //设置弹出框的确定按钮
    width4=window.screen.width*0.2*0.5
    var button_html = ""
    if (bu2_name) {
        margeleft4 = (width3 - width4 * 2) / 3
        button_html +="<button onclick=\"delCover('"+id+"')\" style='margin-top:15px;margin-left:" + margeleft4 +"px;width:"+width4+"px'>"+bu1_name+"</button>"
        button_html += "<button onclick=\"" + fun_name + "('" + id + "')\" style='margin-top:15px;margin-left:" + margeleft4 +"px;width:" + width4 + "px;'>" + bu2_name + "</button>"
    }else{
        margeleft4 = (width3 - width4) / 2
        button_html +="<button onclick=\"delCover('"+id+"')\" style='margin-top:15px;margin-left:" + margeleft4 +"px;width:"+width4+"px'>"+bu1_name+"</button>"
    }

    $("#alert"+id).append(button_html)
    //从下渐出
    $("#alert"+id).animate({
        top:top2,
        opacity:'1'
    })
}