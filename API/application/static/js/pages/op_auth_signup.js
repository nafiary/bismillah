/*
 *  Document   : op_auth_signup.js
 *  Author     : pixelcave
 *  Description: Custom JS code used in Sign Up Page
 */

var OpAuthSignUp = function() {
    // Init Sign Up Form Validation, for more examples you can check out https://github.com/jzaefferer/jquery-validation
    var initValidationSignUp = function(){
        jQuery('.js-validation-signup').validate({
            errorClass: 'invalid-feedback animated fadeInDown',
            errorElement: 'div',
            errorPlacement: function(error, e) {
                jQuery(e).parents('.form-group > div').append(error);
            },
            highlight: function(e) {
                jQuery(e).closest('.form-group').removeClass('is-invalid').addClass('is-invalid');
            },
            success: function(e) {
                jQuery(e).closest('.form-group').removeClass('is-invalid');
                jQuery(e).remove();
            },
            rules: {
                'signup-username': {
                    required: true,
                    minlength: 3
                },
                'signup-pesan': {
                    required: true,
                    minlength: 10
                },
                'signup-nama': {
                    required: true,
                    minlength: 1
                },
                'signup-email': {
                    required: true,
                    email: true
                },
                'signup-password': {
                    required: true,
                    minlength: 5
                },
                'signup-password-confirm': {
                    required: true,
                    equalTo: '#signup-password'
                },
                'signup-terms': {
                    required: true
                }
            },
            messages: {
                'signup-username': {
                    required: 'Masukkan Username',
                    minlength: 'Username minimal 3 karakter'
                },
                'signup-pesan': {
                    required: 'Masukkan Pesan',
                    minlength: 'Pesan terlalu singkat'
                },
                'signup-nama': {
                    required: 'Masukkan Nama Anda',
                    minlength: 'Nama terlalu singkat'
                },
                'signup-email': 'Masukkan alamat email yang valid',
                'signup-password': {
                    required: 'Masukkan Password Dengan Benar',
                    minlength: 'Password minimal 5 karakter'
                },
                'signup-password-confirm': {
                    required: 'Masukkan Password Dengan Benar',
                    minlength: 'Password minimal 5 karakter',
                    equalTo: 'Password tidak sesuai'
                },
                'signup-terms': 'You must agree to the service terms!'
            }
        });
    };

    return {
        init: function () {
            // Init SignUp Form Validation
            initValidationSignUp();
        }
    };
}();

// Initialize when page loads
jQuery(function(){ OpAuthSignUp.init(); });