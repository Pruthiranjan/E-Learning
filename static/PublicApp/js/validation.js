$(document).ready(function() {
    $("#SignUpForm").validate({
        rules: {
            first_name: {
                required: true,
                minlength: 3,
                nowhitespace: true,
                lettersonly: true,
            },
            last_name: {
                required: true,
                nowhitespace: true,
                lettersonly: true,
            },
            email: {
                required: true,
                email: true,
                nowhitespace: true,
            },
            password: {
                required: true,
                minlength: 6,
                nowhitespace: true,
            },
            password2: {
                required: true,
                equalTo: "#pw"
            },
        },
        highlight: function(element) {
            $(element).addClass("c1")
        },
        unhighlight: function(element) {
            $(element).removeClass("c1")
        },
        messages: {
            first_name: {
                required: "First Name is Mandatory",
                minlength: "3 Character must",
                nowhitespace: "White Space Not Allowed",
                lettersonly: "Enter Only Character"
            },
            last_name: {
                required: "Last Name is Mandatory",
                nowhitespace: "White Space Not Allowed",
                lettersonly: "Enter Only Character"
            },
            email: {
                required: "Email is Madatory",
                email: "Input Email in Propper Format",
                nowhitespace: "White Space Not Allowed",
            },
            password: {
                required: "Password is Madatory",
                minlength: "6 Digit must",
                nowhitespace: true,
            },
            password2: {
                required: "Confirm Password is Madatory",
                nowhitespace: true,
                equalTo: "Both Password are not Identical"
            },
        }
    });
});
$(document).ready(function() {
    $("#loginform").validate({
        rules: {
            username: {
                required: true,
                email: true,
                nowhitespace: true,
            },
            password: {
                required: true,
                nowhitespace: true,
            },
        },
        highlight: function(element) {
            $(element).addClass("c1")
        },
        unhighlight: function(element) {
            $(element).removeClass("c1")
        },
        messages: {
            username: {
                required: "Email is Madatory",
                email: "Input Email in Propper Format",
                nowhitespace: "White Space Not Allowed",
            },
            password: {
                required: "Password is Madatory",
                nowhitespace: true,
            }
        }
    });
});