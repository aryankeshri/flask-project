$(document).ready(function() {

	$(".progress-bar").css("width","50%");
	$("#sidebar").css("display","block");
	
	setTimeout(glow,4000);

	$("#step1").addClass("active");
	$("#submit-text").css("color","#00ff00");

	function glow() {
		$("#upload-text").css("color","#00ff00");
		$("#step2").addClass("active");
		$("#step2").addClass("glowing");
	}

	var image_path = '', signature_path = '', marksheet_path = '';
	var form = document.forms['upload_images'];

	$("#photo_img").click(function() {
		$("input[name='image']").click();

		$("input[name='image']").change(function(event) {
			image_path = URL.createObjectURL(event.target.files[0]);
			$("#photo_img").attr('src',image_path);
		});
	});

	$("#signature_img").click(function() {
		$("input[name='signature']").click();

		$("input[name='signature']").change(function(event) {
			signature_path = URL.createObjectURL(event.target.files[0]);
			$("#signature_img").attr('src',signature_path);
		});
	});

	$("#marksheet_img").click(function() {
		$("input[name='marksheet']").click();

		$("input[name='marksheet']").change(function(event) {
			marksheet_path = URL.createObjectURL(event.target.files[0]);
			$("#marksheet_img").attr('src',marksheet_path);
		});
	});

	$("#next").click(function(e) {

		e.preventDefault();

		var Errors = '';

		if(image_path == '')
			Errors = "Image cannot be empty"+'\n';
		if(signature_path == '')
			Errors += "Signature cannot be empty"+'\n';
		if(marksheet_path == '')
			Errors += "Marksheet cannot be empty";

		// if(Errors)
		// 	alert(Errors);
		// else
			form.submit();
	});

});