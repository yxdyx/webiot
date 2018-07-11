layui.config({
	base : "js/"
}).use(['form','layer','jquery','layedit','laydate'],function(){
	var form = layui.form(),
		layer = parent.layer === undefined ? layui.layer : parent.layer,
		laypage = layui.laypage,
		layedit = layui.layedit,
		laydate = layui.laydate,
		$ = layui.jquery;

	//创建一个编辑器
 	var editIndex = layedit.build('news_content');
 	var addNewsArray = [],addNews;
 	form.on("submit(addNews)",function(data){
 		//是否添加过信息
	 	if(window.sessionStorage.getItem("addNews")){
	 		addNewsArray = JSON.parse(window.sessionStorage.getItem("addNews"));
	 	}
	 	//显示、审核状态
 		var isShow = data.field.show=="on" ? "checked" : "",
 			newsStatus = data.field.shenhe=="on" ? "在线" : "离线";

 		addNews = '{"newsName":"'+$(".newsName").val()+'",';  //设备名称
 		addNews += '"newsId":"'+new Date().getTime()+'",';	 //设备id
        addNews += '"newsPwd":"'+$(".newsPwd").val()+'",'; //设备密码
 		addNews += '"newsAuthor":"'+$(".newsAuthor").val()+'",'; //设备用户
 		addNews += '"newsStatus":"'+ newsStatus +'"}'; //设备状态
 		addNewsArray.unshift(JSON.parse(addNews));
 		window.sessionStorage.setItem("addNews",JSON.stringify(addNewsArray));
 		//弹出loading
 		var index = top.layer.msg('数据提交中，请稍候',{icon: 16,time:false,shade:0.8});
        setTimeout(function(){
            top.layer.close(index);
			top.layer.msg("设备添加成功！");
 			layer.closeAll("iframe");
	 		//刷新父页面
	 		parent.location.reload();
        },2000);
 		return false;
 	})
	
})
