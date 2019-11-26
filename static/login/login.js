$(document).ready(function() {

var studentIcon = "static/photos/student.png",
	adminIcon = "static/photos/admin.png";

var studentIDRegex = /^\d{1,4}[a-z]{1,6}\d{1,4}$/i,
	passwordRegex = /^[a-zA-Z0-9 ]+$/;

	//button click to change form from student to admin and vice-versa
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

	$("#studentSubmitBtn").click(function(e) {
		e.preventDefault();
		var studentID = document.forms['studentForm']['id'].value.trim();
		var studentPasswd = document.forms['studentForm']['passwd'].value.trim();

		if(studentIDRegex.test(studentID) == true && passwordRegex.test(studentPasswd) == true) {
			document.forms['studentForm'].submit();
		} else {
			alert("Password and registration number must be valid");
		}
	});

	$("#adminSubmitBtn").click(function(e) {
		e.preventDefault();
		var adminPasswd = document.forms['adminForm']['passwd'].value.trim();

		if(passwordRegex.test(adminPasswd)) {
			document.forms['adminForm'].submit();
		} else {
			alert("Password must not contain special characters");
		}

	});

	// in case of login failure by admin

	var failLogin = window.location.href;

	console.log(failLogin.indexOf("a=1"));

	if(failLogin.indexOf("a=1") != -1) {
		$("#adminForm").css("display","block");
		$("#studentForm").css("display","none");
		$("#loggerImage").attr("src",adminIcon);

		$("#adminBtn").addClass("btn-info active");
		$("#studentBtn").removeClass("btn-info active").addClass("btn-default");
	}
});