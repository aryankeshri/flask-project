$(document).ready(function() {
	$("#maths").click(function() {
		$("#claim-subject").text("Enter your Mathematics Claim");
		$("input[name='subject']").attr('value',"maths");
	});

	$("#physics").click(function() {
		$("#claim-subject").text("Enter your Physics Claim");
		$("input[name='subject']").attr('value',"physics");
	});

	$("#chemistry").click(function() {
		$("#claim-subject").text("Enter your Chemistry Claim");
		$("input[name='subject']").attr('value',"chemistry");
	});

	$("button[type='submit'").click(function() {
		document.forms['claim'].submit();
	})
});