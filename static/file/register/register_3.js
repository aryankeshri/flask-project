$(document).ready(function() {
	//animation on page load
	$(".progress-bar").css("width","100%");
	$("#sidebar").css("display","block");
	
	setTimeout(glow,4000);

	$("#step1").addClass("active");
	$("#submit-text").css("color","#00ff00");

	$("#step2").addClass("active");
	$("#upload-text").css("color","#00ff00");

	function glow() {
		$("#payment-text").css("color","#00ff00");
		$("#step3").addClass("active");
		$("#step3").addClass("glowing");
	}



	var form = document.forms['payment'];

	for(var i = 1; i < 13; ++i) {
		var option = document.createElement('option');
		option.setAttribute('value',i);
		option.innerHTML = i;
		form['expiry_month'].appendChild(option);
	}

	for(var i = 2019; i < 2051; ++i) {
		var option = document.createElement('option');
		option.setAttribute('value',i);
		option.innerHTML = i;
		form['expiry_year'].appendChild(option);
	}
	$("#pay").click(function(e) {

		e.preventDefault();

		var card_number_regex = /^\d{16}$/;
		var name_regex = /^[a-z ]+$/i;
		var cvv_code_regex = /^\d{3}$/;

		var data = Object(), Errors = '';

		data['card_number'] = form['card_number'].value.trim();
		data['name'] = form['name'].value.trim();
		data['expiry_month'] = form['expiry_month'].options[form['expiry_month'].selectedIndex].value;
		data['expiry_year'] = form['expiry_year'].options[form['expiry_year'].selectedIndex].value;
		data['cvv_code'] = form['cvv_code'].value;

		if(!card_number_regex.test(data['card_number']))
			Errors += 'Card number is invalid'+'\n';

		if(!name_regex.test(data['name']))
			Errors += 'Name is invalid'+'\n';

		if(!cvv_code_regex.test(data['cvv_code']))
			Errors += 'CVV Code is invalid';

		if(Errors)
			alert(Errors);
		else
			form.submit();
	});
});