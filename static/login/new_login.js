$(document).ready(function() {

    var studentIcon = "static/photos/student.png",
	adminIcon = "static/photos/admin.png";

	$("#studentBtn").click(function() {
		$("#studentForm").css("display","block");
		$("#adminForm").css("display","none");
		$("#loggerImage").attr("src",studentIcon);

		$("#studentBtn").addClass("btn-info active");
		$("#adminBtn").removeClass("btn-info active").addClass("btn-default");
	});

	$("#adminBtn").click(function() {
		$("#adminForm").css("display","block");
		$("#studentForm").css("display","none");
		$("#loggerImage").attr("src",adminIcon);

		$("#adminBtn").addClass("btn-info active");
		$("#studentBtn").removeClass("btn-info active").addClass("btn-default");
	});
});