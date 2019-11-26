$(document).ready(function() {

	blogEditor.document.designMode = 'On';
	blogEditor.document.execCommand("fontName",false,'"Helvetica Neue", Helvetica, Arial, sans-serif');

	$("#bold-button").click(function() {
		$(this).toggleClass('btn-warning');
		execCmd("bold");	
	});

	$("#italic-button").click(function() {		
		execCmd("italic");
	});

	$("#underline-button").click(function() {		
		execCmd("underline");
	})

	$("#align-left").click(function() {		
		execCmd("justifyLeft");		
	});

	$("#align-right").click(function() {
		execCmd("justifyRight");		
	});

	$("#align-center").click(function() {
		execCmd("justifyCenter");	
	});

	$("#align-justify").click(function() {
		execCmd("justifyFull");
	});

	$("#indent").click(function() {
		execCmd("indent");
	});

	$("#outdent").click(function() {
		execCmd("outdent");
	})

	$("#ordered-list").click(function() {
		execCmd("insertOrderedList");
	})
	$("#unordered-list").click(function() {		
		execCmd("insertUnorderedList");
	});


	function execCmd(cmd) {
		blogEditor.document.execCommand(cmd,false,null);
		blogEditor.focus();	
	}
});

