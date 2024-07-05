"use strict";

// Class Definition
var KTLogin = function () {
    var _login;

    var _showForm = function (form) {
        var cls = 'login-' + form + '-on';
        var form = 'kt_login_' + form + '_form';

        _login.removeClass('login-forgot-on');
        _login.removeClass('login-signin-on');
        _login.removeClass('login-signup-on');

        _login.addClass(cls);

        KTUtil.animateClass(KTUtil.getById(form), 'animate__animated animate__backInUp');
    }

    var _handleSignInForm = function () {
        var validation;

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            KTUtil.getById('kt_login_signin_form'),
            {
                fields: {
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'Email address is required'
                            },
                            emailAddress: {
                                message: 'The value is not a valid email address'
                            }
                        }
                    },
                    password: {
                        validators: {
                            notEmpty: {
                                message: 'Password is required'
                            },
                            stringLength: {
                                min: 1,
                                max: 50,
                                message: 'Please enter a menu within text length range 1 and 50'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    submitButton: new FormValidation.plugins.SubmitButton(),
                    //defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
                    // Uncomment this line to enable normal button submit after form validation
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        $('#kt_login_signin_submit').on('click', function (e) {
            e.preventDefault();

            validation.validate().then(function (status) {
                if (status == 'Valid') {
                    swal.fire({
                        text: "All is cool! Now we submitted Your info to the Server",
                        icon: "success",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, Do it!",
                        customClass: {
                            confirmButton: "btn font-weight-bold btn-light-primary"
                        }
                    }).then(function () {
                        jQuery.ajax('/signIn', {
                            type: "POST",
                            data: $("#kt_login_signin_form").serialize(),
                            success: (data) => {
                                window.location.replace('/')
                            },
                            error: function (data) {
                                $('[data-switch=true]').bootstrapSwitch();
                                let content = {};
                                content.message = data.responseJSON.error;
                                $.notify(content, {
                                    type: 'danger',
                                    placement: {
                                        from: 'top',
                                        align: 'left'
                                    },
                                    offset: {
                                        x: 30,
                                        y: 30
                                    },
                                });
                            }
                        });
                    });
                } else {
                    swal.fire({
                        text: "Sorry, looks like there are some errors detected, please try again.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn font-weight-bold btn-light-primary"
                        }
                    }).then(function () {
                        KTUtil.scrollTop();
                    });
                }
            });
        });

        // Handle forgot button
        $('#kt_login_forgot').on('click', function (e) {
            e.preventDefault();
            _showForm('forgot');
        });

        // Handle signup
        $('#kt_login_signup').on('click', function (e) {
            e.preventDefault();
            _showForm('signup');
        });
    }

    var _handleSignUpForm = function (e) {
        var validation;
        var form = KTUtil.getById('kt_login_signup_form');

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            form,
            {
                fields: {
                    username: {
                        validators: {
                            notEmpty: {
                                message: 'Username is required'
                            },
                            callback: {
                                message: 'Username cannot be only spaces',
                                callback: function(input) {
                                    console.log(input.value);
                                    if(input.value.trim() !== ''){
                                        return true;
                                    }else{
                                        return false;
                                    }
                                }
                            },
                            stringLength: {
                                min: 1,
                                max: 50,
                                message: 'Please enter a menu within text length range 1 and 50'
                            }
                        }
                    },
                    first_name: {
                        validators: {
                            notEmpty: {
                                message: 'Firstname is required'
                            },
                            callback: {
                                message: 'Firstname cannot be only spaces',
                                callback: function(input) {
                                    console.log(input.value);
                                    if(input.value.trim() !== ''){
                                        return true;
                                    }else{
                                        return false;
                                    }
                                }
                            },
                            stringLength: {
                                min: 1,
                                max: 50,
                                message: 'Please enter a menu within text length range 1 and 50'
                            }
                        }
                    },
                    last_name: {
                        validators: {
                            notEmpty: {
                                message: 'Lastname is required'
                            },
                            callback: {
                                message: 'Lastname cannot be only spaces',
                                callback: function(input) {
                                    console.log(input.value);
                                    if(input.value.trim() !== ''){
                                        return true;
                                    }else{
                                        return false;
                                    }
                                }
                            },
                            stringLength: {
                                min: 1,
                                max: 50,
                                message: 'Please enter a menu within text length range 1 and 50'
                            }
                        }
                    },
                    company: {
                        validators: {
                            notEmpty: {
                                message: 'Company is required'
                            },
                            callback: {
                                message: 'Company cannot be only spaces',
                                callback: function(input) {
                                    console.log(input.value);
                                    if(input.value.trim() !== ''){
                                        return true;
                                    }else{
                                        return false;
                                    }
                                }
                            },
                            stringLength: {
                                min: 1,
                                max: 50,
                                message: 'Please enter a menu within text length range 1 and 50'
                            }

                        }
                    },
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'Email address is required'
                            },
                            emailAddress: {
                                message: 'The value is not a valid email address'
                            }
                        }
                    },
                    password: {
                        validators: {
                            notEmpty: {
                                message: 'The password is required'
                            },
                            stringLength: {
                                min: 1,
                                max: 50,
                                message: 'Please enter a menu within text length range 1 and 50'
                            }
                        }
                    },
                    cpassword: {
                        validators: {
                            notEmpty: {
                                message: 'The password confirmation is required'
                            },
                            identical: {
                                compare: function () {
                                    return form.querySelector('[name="password"]').value;
                                },
                                message: 'The password and its confirm are not the same'
                            },
                            stringLength: {
                                min: 1,
                                max: 50,
                                message: 'Please enter a menu within text length range 1 and 50'
                            }
                        }
                    },
                    agree: {
                        validators: {
                            notEmpty: {
                                message: 'You must accept the terms and conditions'
                            }
                        }
                    },
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        $('#kt_login_signup_submit').on('click', function (e) {
            e.preventDefault();

            validation.validate().then(function (status) {
                if (status == 'Valid') {
                    $('#kt_login_signup_submit').prop('disabled', true);
                    swal.fire({
                        text: "All is cool! Now you submit this form",
                        icon: "success",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn font-weight-bold btn-light-primary"
                        }
                    }).then(function () {
                          function showLoader() {
                            $('#loader-overlay').show();
                          }

                          function hideLoader() {
                            $('#loader-overlay').hide();
                          }

                          $('#loader-overlay').on('click', function(event) {
                            event.preventDefault();
                            event.stopPropagation();
                          });

                          showLoader();
                        jQuery.ajax('/signUp', {
                            type: "POST",
                            data: $("#kt_login_signup_form").serialize(),
                            success: (data) => {
                                hideLoader();
                                $('[data-switch=true]').bootstrapSwitch();
                                let content = {};
                                content.message = data.success;
                                $.notify(content, {
                                    type: 'success',
                                    placement: {
                                        from: 'top',
                                        align: 'left'
                                    },
                                    offset: {
                                        x: 30,
                                        y: 30
                                    },
                                });
                                setTimeout(() => {
                                    window.location.replace('/');
                                }, 3000);
                            },
                            error: function (data) {
                                hideLoader();
                                $('#kt_login_signup_submit').prop('disabled', false);
                                $('[data-switch=true]').bootstrapSwitch();
                                let content = {};
                                content.message = data.responseJSON.error;
                                $.notify(content, {
                                    type: 'danger',
                                    placement: {
                                        from: 'top',
                                        align: 'left'
                                    },
                                    offset: {
                                        x: 30,
                                        y: 30
                                    },
                                });
                            }
                        });
                    });
                } else {
                    swal.fire({
                        text: "Sorry, looks like there are some errors detected, please try again.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn font-weight-bold btn-light-primary"
                        }
                    }).then(function () {
                        KTUtil.scrollTop();
                    });
                }
            });
        });

        // Handle cancel button
        $('#kt_login_signup_cancel').on('click', function (e) {
            e.preventDefault();
            window.location.reload();
            _showForm('signin');
        });
    }

    var _handleForgotForm = function (e) {
        var validation;

        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validation = FormValidation.formValidation(
            KTUtil.getById('kt_login_forgot_form'),
            {
                fields: {
                    email: {
                        validators: {
                            notEmpty: {
                                message: 'Email address is required'
                            },
                            emailAddress: {
                                message: 'The value is not a valid email address'
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap()
                }
            }
        );

        // Handle submit button
        $('#kt_login_forgot_submit').on('click', function (e) {
            e.preventDefault();

            validation.validate().then(function (status) {
                if (status == 'Valid') {
                    $('#kt_login_forgot_submit').prop('disabled', true);
                    swal.fire({
                        text: "All is cool! Now you submit this form",
                        icon: "success",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn font-weight-bold btn-light-primary"
                        }
                    }).then(function () {
                          function showLoader() {
                            $('#loader-overlay').show();
                          }

                          function hideLoader() {
                            $('#loader-overlay').hide();
                          }

                          $('#loader-overlay').on('click', function(event) {
                            event.preventDefault();
                            event.stopPropagation();
                          });

                          showLoader();
                        jQuery.ajax('/forgot_password/', {
                            type: "POST",
                            data: $("#kt_login_forgot_form").serialize(),
                            success: (data) => {
                                hideLoader();
                                $('[data-switch=true]').bootstrapSwitch();
                                let content = {};
                                content.message = data.success;
                                $.notify(content, {
                                    type: 'success',
                                    placement: {
                                        from: 'top',
                                        align: 'left'
                                    },
                                    offset: {
                                        x: 30,
                                        y: 30
                                    },
                                });
                                setTimeout(() => {
                                    window.location.replace('/');
                                }, 3000);
                            },
                            error: function (data) {
                                hideLoader();
                                $('#kt_login_forgot_submit').prop('disabled', false);
                                $('[data-switch=true]').bootstrapSwitch();
                                let content = {};
                                content.message = data.responseJSON.error;
                                $.notify(content, {
                                    type: 'danger',
                                    placement: {
                                        from: 'top',
                                        align: 'left'
                                    },
                                    offset: {
                                        x: 30,
                                        y: 30
                                    },
                                });
                            }
                        });
                    });
                } else {
                    swal.fire({
                        text: "Sorry, looks like there are some errors detected, please try again.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn font-weight-bold btn-light-primary"
                        }
                    }).then(function () {
                        KTUtil.scrollTop();
                    });
                }
            });
        });

        // Handle cancel button
        $('#kt_login_forgot_cancel').on('click', function (e) {
            e.preventDefault();
            window.location.reload();
            _showForm('signin');
        });
    }

    // Public Functions
    return {
        // public functions
        init: function () {
            _login = $('#kt_login');

            _handleSignInForm();
            _handleSignUpForm();
            _handleForgotForm();
        }
    };
}();

// Class Initialization
jQuery(document).ready(function () {
    KTLogin.init();
});

function togglePasswordVisibility() {
    var passwordField = document.getElementById("in-password");
    var eyeIcon = document.getElementById("eyeIcon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        eyeIcon.className = "fa fa-eye";
    } else {
        passwordField.type = "password";
        eyeIcon.className = "fa fa-eye-slash";
    }
}
document.addEventListener("DOMContentLoaded", function() {
    var passwordField = document.getElementById("in-password");
    var togglePasswordButton = document.getElementById("eyeIcon");

    togglePasswordButton.style.display = "none";

    passwordField.addEventListener("input", function() {
        if (passwordField.value.length > 0) {
            togglePasswordButton.style.display = "block";
        } else {
            togglePasswordButton.style.display = "none";
        }
    });
});
document.getElementById('in-password').addEventListener('input', function() {
  console.log("====================");
  var inputWidth = 90; // Adjust based on padding and font size
  this.style.width = inputWidth + '%';
});