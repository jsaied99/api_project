// var submit = true;

// function inputValidation() {
//   var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;

//   var email = $("#username").val();
//   return regex.test(email);
// }

// function checkEmail(email)
// {
//   var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
//   if (regex.test(email))
//   {
//     $("#email").css("color", "green");
//     submit= true;
//   }
//   else{
//     $("#email").css("color", "red");
//     submit= false;
//   }

// }

// $(function () {
//   $("#submitB").click(function () {

//     if ($("#password").val() != '' && submit)
//     {
//       var params = {
//         email: $("#email").val(),
//         password: $("#password").val(),
//       };

//     $.post("php/login.php", params, function (response) {
//       if (response == "success") {
//         window.location.replace("html/Jas8dzHomePage.php");
//       } else if (response == "failed") {
//         alert("Incorrect Username or Password");
//       }
//     });

//   }
//   });

//   document
//     .getElementById("myForm")
//     .addEventListener("submit", function (event) {
//       event.preventDefault();
//     });
// });

function seeBooks ()
{
  window.location.replace("/api/books/all");
}