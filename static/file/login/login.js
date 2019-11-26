$(document).ready(function() {

var studentIcon = "static/photos/student.png",
	adminIcon = "static/photos/admin.png";

var studentIDregex = new RegExp(/^(.*[a-z])+(.*[A-Z])+(.*[@!#$%^&])+(.*\d)+$/i);  //student id regex
var password = new RegExp(/^[a-zA-Z0-9!@#$%^& ]{8,16}$/);

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
		var studentPasswd = document.forms['studentForm']['passwd'].value;

		if(password.test(studentPasswd) == true || password.test(studentPasswd) == false) {		// && studendIDregex.test(studentID) == true
			document.forms['studentForm'].submit();
		} else {
			alert("Password and registration number must be valid");
		}
	});

	$("#adminSubmitBtn").click(function(e) {
		e.preventDefault();
		var adminPasswd = document.forms['adminForm']['passwd'].value;

		if(/admin/.test(adminPasswd)) {
			document.forms['adminForm'].submit();
		} else {
			alert("Password is not valid");	
		}

	});

	// in case of login failure by admin

	var failLogin = window.location.href;

	if(failLogin.indexOf("a=1") != -1) {
		$("#adminForm").css("display","block");
		$("#studentForm").css("display","none");
		$("#loggerImage").attr("src",adminIcon);

		$("#adminBtn").addClass("btn-info active");
		$("#studentBtn").removeClass("btn-info active").addClass("btn-default");
	}
});