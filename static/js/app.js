$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').focus()
});

function getCookie(name) {
	var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return r ? r[1] : undefined;
}

$(".btn-agree").click(function() {
	data = {
	  'agree': $(this).data("agree"), 
	  'application': $("#application").data("appid"),
	  '_xsrf':getCookie("_xsrf")
	};

	$.ajax({
	  url: "/application/agree", 
	  data: data, 
	  dataType: "JSON", 
	  type: "POST",
	  success: function(response) {
	    if(response.success) {
	        console.log(response);
	        $(".application-approved .text-content").html(
	        $("<h1></h1>").text("Solicitud aceptada: " + response.agree_state)
	      );
	      $("#agree_state").text(response.agree_state);
	    }
	    else {
	      alert('La solicitud no existe');  
	    }
	  }
	});
});