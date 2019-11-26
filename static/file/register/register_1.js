$(document).ready(function() {

	$("#step1").addClass("active");
	$("#submit-text").css("color","#00ff00");
	$("#step1").addClass("glowing");
	
// document.addEventListener("scroll", function() {
// 	var per = document.getElementById("personal");
// 	var exam = document.getElementById("exam");
// 	var res = document.getElementById("residence");
// 	//scrollMax
// 	//scrollMax-30
// 	window.scroll({top: 0,behavior : 'smooth'});
// });

	function Validator() {

		this.passwd_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)+(?=.*[!@#$%^&])[a-zA-Z\d!@#$%^&]{8,16}$/,
		this.name_regex = /^[a-z ]+$/i,
		this.phone_regex = /^\d{10,20}$/,

		this.check = {
			phone_ok: false,
			passwd_len_ok: false,
			passwd_eq_ok: false,
			passwd_valid_ok: false,
			name_ok: false,
			father_name_ok: false,
			mother_name_ok: false,
		},

		this.error = {
			phone: "Phone number must contain at least 10 digits",
			passwd_len: "Password length must be 8 characters long",
			passwd_eq: "Password and Confirm Password fields do not match",
			passwd_valid: "Password must contain one uppercase, one lowercase, one digit and one of !@#$%^&",
			name: "Entered name does not seem to be valid",
			father_name: "Entered father name does not seem to be valid",
			mother_name: "Entered mother name does not seem to be valid",

		}


		this.check_password_len = function(passwd) {
			return passwd.length >= 8;

		},

		this.check_password_eq = function(passwd, confirm_passwd) {
			return passwd == confirm_passwd;
		},

		this.check_password_valid = function(passwd) {
			return this.passwd_regex.test(passwd);
		},

		this.check_name = function(name) {
			return this.name_regex.test(name);
		},

		this.check_father_name = function(father_name) {
			return this.name_regex.test(father_name)
		},

		this.check_mother_name = function(mother_name) {
			return this.name_regex.test(mother_name);
		},

		this.check_phone = function(phone) {
			return this.phone_regex.test(phone);
		},

		this.valid = function(data) {
			this.check['phone_ok'] = this.check_phone(data['phone']);
			this.check['passwd_len_ok'] = this.check_password_len(data['passwd']);
			this.check['passwd_eq_ok'] = this.check_password_eq(data['passwd'],data['confirm_passwd']);
			this.check['passwd_valid_ok'] = this.check_password_valid(data['passwd']);
			this.check['name_ok'] = this.check_name(data['name']);
			this.check['father_name_ok'] = this.check_father_name(data['father_name']);
			this.check['mother_name_ok'] = this.check_mother_name(data['mother_name']);

			return this.check;
		}
	}


	var states = [
					"Andhra Pradesh", "Arunachal Pradesh", "Assam",
					"Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
					"Himachal Pradesh", "Jammu and Kashmir", "Jharkhand",	
					"Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",
					"Manipur", "Meghalaya", "Mizoram", "Nagaland",
					"Odissa", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
					"Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
				];

	var form = document.forms['application_form'];
	var st_of_elig = form['state_of_eligibility'];
	var option, data = Object();

	for(var i = 0; i < states.length; ++i) {

		option = document.createElement('option');
		option.setAttribute('value',states[i]);
		option.innerHTML = states[i];
		st_of_elig.appendChild(option);
	}

	var date = form['date'];

	for(var i = 1; i < 32; ++i) {
		option = document.createElement('option');
		option.setAttribute('value',i);
		option.innerHTML = i;
		date.appendChild(option);
	}

	var month = form['month'];

	for(var i = 1; i < 13; ++i) {

		option = document.createElement('option');
		option.setAttribute('value',i);
		option.innerHTML = i;
		month.appendChild(option);
	}

	var year = form['year'];

	for(var i = 1997; i <= 2006; ++i) {
		option = document.createElement('option');
		option.setAttribute('value',i);
		option.innerHTML = i;
		year.appendChild(option);
	}

	$("#next").click(function(e) {

		e.preventDefault();

		data['name'] = form['name'].value.toUpperCase().trim();
		data['father_name'] = form['father_name'].value.toUpperCase().trim();
		data['mother_name'] = form['mother_name'].value.toUpperCase().trim();
		data['gender'] = form['gender'].options[form['gender'].selectedIndex].value.toUpperCase();
		data['state_of_eligibility'] = form['state_of_eligibility'].options[form['state_of_eligibility'].selectedIndex].value.toUpperCase();
		data['date'] = form['date'].options[form['date'].selectedIndex].value.toUpperCase();
		data['month'] = form['month'].options[form['month'].selectedIndex].value.toUpperCase();
		data['year'] = form['year'].options[form['year'].selectedIndex].value.toUpperCase();
		data['category'] = form['category'].options[form['category'].selectedIndex].value.toUpperCase();
		data['pwd'] = form['pwd'].options[form['pwd'].selectedIndex].value.toUpperCase();
		data['applying_for'] = form['applying_for'].options[form['applying_for'].selectedIndex].value;
		data['mode_of_exam'] = form['mode_of_exam'].options[form['mode_of_exam'].selectedIndex].value.toUpperCase();
		data['paper_medium'] = form['paper_medium'].options[form['paper_medium'].selectedIndex].value.toUpperCase();
		data['address'] = form['address'].value.toUpperCase().trim();
		data['email'] = form['email'].value.trim();
		data['phone'] = form['phone'].value.toUpperCase().trim();
		data['passwd'] = form['passwd'].value;
		data['confirm_passwd'] = form['confirm_passwd'].value;

		var v = new Validator();
		var result = v.valid(data);
		var Errors = '';

		if(!result['phone_ok'])
			Errors += v.error['phone']+"\n";
		if(!result['passwd_len_ok'])
			Errors += v.error['passwd_len']+"\n";
		if(!result['passwd_eq_ok'])
			Errors += v.error['passwd_eq']+"\n";
		if(!result['passwd_valid_ok'])
			Errors += v.error['passwd_valid']+"\n";
		if(!result['name_ok'])
			Errors += v.error['name']+"\n";
		if(!result['father_name_ok'])
			Errors += v.error['father_name']+"\n";
		if(!result['mother_name_ok'])
			Errors += v.error['mother_name']+"\n";

		if(Errors)
			alert(Errors);
		else
			form.submit();

	});
});