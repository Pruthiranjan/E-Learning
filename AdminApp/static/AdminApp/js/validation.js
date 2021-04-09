$(document).ready(function() {
    $("#changepassword").validate({
        rules: {
            oldpass: {
                required: true,
            },
            password: {
                required: true,
                minlength: 6,
                nowhitespace: true,
            },
            password1: {
                required: true,
                equalTo: "#pw"
            },
        },
        highlight: function(element) {
            $(element).addClass("border border-danger")
        },
        unhighlight: function(element) {
            $(element).removeClass("border border-danger")
        },
        messages: {
            oldpass: {
                required: "Old Password is Madatory",
            },
            password: {
                required: "Password is Madatory",
                minlength: "6 Digit must",
                nowhitespace: true,
            },
            password1: {
                required: "Confirm Password is Madatory",
                nowhitespace: true,
                equalTo: "Both Password are not Identical"
            },
        }
    });
});
$(document).ready(function() {
    $("#userdetail").validate({
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
            password: {
                required: true,
                minlength: 6,
                nowhitespace: true,
            },
            password1: {
                required: true,
                equalTo: "#pw"
            },
            contact: {
                required: true,
                number: true,
                minlength: 10,
                maxlength: 10,
            },
            address: {
                required: true,
            }
        },
        highlight: function(element) {
            $(element).addClass("border border-danger")
        },
        unhighlight: function(element) {
            $(element).removeClass("border border-danger")
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
            password: {
                required: "Password is Madatory",
                minlength: "6 Digit must",
                nowhitespace: true,
            },
            password1: {
                required: "Confirm Password is Madatory",
                nowhitespace: true,
                equalTo: "Both Password are not Identical"
            },
            contact: {
                required: "Contact is Mandatory",
                number: "Enter Only Numbers",
                minlength: "Enter 10 digit Number",
                maxlength: "Enter 10 digit Number",
            },
            address: {
                required: "Address is Mandatory",
            }

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
            $(element).addClass("border border-danger")
        },
        unhighlight: function(element) {
            $(element).removeClass("border border-danger")
        },
        messages: {
            username: {
                required: "Email is Madatory",
                email: "Input Email in Propper Format",
                nowhitespace: "White Space Not Allowed",
            },
            password: {
                required: "Password is Madatory",
                nowhitespace: "No Whitespace Allowed",
            }
        }
    });
});
$(document).ready(function() {
    $("#signupform").validate({
        rules: {
            first_name: {
                required: true,
                minlength: 3,
                nowhitespace: true,
                lettersonly: true,
            },
            last_name: {
                nowhitespace: true,
                lettersonly: true,
            },
            contact: {
                required: true,
                number: true,
                minlength: 10,
                maxlength: 10,
            },
            dob: {
                required: true,
            },
            email: {
                required: true,
                email: true,
                nowhitespace: true,
            },
            password: {
                required: true,
                minlength: 8,
                nowhitespace: true,
            },
            password2: {
                required: true,
                equalTo: "#pw"
            },

        },
        highlight: function(element) {
            $(element).addClass("border border-danger")
        },
        unhighlight: function(element) {
            $(element).removeClass("border border-danger")
        },
        messages: {
            first_name: {
                required: "Name is Mandatory",
                minlength: "3 Character must",
                nowhitespace: "White Space Not Allowed",
                lettersonly: "Enter Only Character"
            },
            last_name: {
                nowhitespace: "White Space Not Allowed",
                lettersonly: "Enter Only Character"
            },
            contact: {
                required: "Contact is Mandatory",
                number: "Enter Only Numbers",
                minlength: "Enter 10 digit Number",
                maxlength: "Enter 10 digit Number",
            },
            dob: {
                required: "DOB is Madatory",
            },
            email: {
                required: "Email is Madatory",
                email: "Input Email in Propper Format",
                nowhitespace: "White Space Not Allowed",
            },
            password: {
                required: "Password is Madatory",
                minlength: "8 Digit must",
                nowhitespace: "White Space Not Allowed",
            },
            password2: {
                required: "Confirm Password is Madatory",
                nowhitespace: "White Space Not Allowed",
                equalTo: "Both Password are not Identical"
            },
        }
    });
});
$(document).ready(function() {
    $("#profile").validate({
        rules: {
            profilepic: {
                required: true,
            }
        },
        messages: {
            profilepic: {
                required: "Select Your Picture First",
            }
        }
    });
});