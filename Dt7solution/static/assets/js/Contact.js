// $(document).ready(function () {
//     $('#submitBtn').click(function (event) {
//         event.preventDefault();
//         debugger
        
        
//         let firstName = $('#firstNamecontact').val();
//         let lastName = $('#lastNamecontact').val();
//         let email = $('#emailcontact').val();
//         let message = $('#messagecontact').val();
//         let csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

//         let servicesInterestedIn = [];
//         $('input[name="servicesInterestedIncontact"]:checked').each(function () {
//             servicesInterestedIn.push($(this).val());
//         });

   
//         if (!firstName || !lastName || !email || !message) {
//             alert('Please fill out all required fields.');
//             return;
//         }

//         if (servicesInterestedIn.length === 0) {
//             alert('Please select at least one service.');
//             return;
//         }

       
//         let data = new FormData();
//         data.append('firstName', firstName);
//         data.append('lastName', lastName);
//         data.append('email', email);
//         data.append('message', message);
//         data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

//         servicesInterestedIn.forEach((service) => {
//             data.append('servicesInterestedIn', service);
//         });

    
//         for (let pair of data.entries()) {
//             console.log(pair[0] + ': ' + pair[1]);
//         }

       
//         $.ajax({
//             type: 'POST',
//             url: '/contact/',
//             processData: false,
//             contentType: false,
//             cache: false,
//             data: data,
//             success: function (response) {
//                 if (response.success) {
//                     jQuery('#myForm')[0].reset();
//                     jQuery('.sent-message').show().text("Your message has been sent successfully!");
//                 } else {
//                     jQuery('.error-message').show().text("Form submission failed. Please try again.");
//                 }
//             },
//             error: function () {
//                 jQuery('.loading').hide();
//                 jQuery('.error-message').show().text("An error occurred. Please try again later.");
//             }
           
//         });
//     });
// });

jQuery(document).ready(function () {
    jQuery('#submitBtn').click(function (event) {
        event.preventDefault(); 
        debugger
        // Collect form data
        let firstName = jQuery('#FirstName').val();
        let lastName = jQuery('#LastName').val();
        let email = jQuery('#Email').val();
        let message = jQuery('#Message').val();
        let csrfmiddlewaretoken = jQuery('input[name=csrfmiddlewaretoken]').val();
        // let recaptchaResponse = grecaptcha.getResponse();

        // Validate form fields
        if (!firstName || !lastName  || !email  || !message) {
            jQuery('.error-message').show().text("All fields are required.");
            return;
        }

        jQuery('.error-message').hide(); // Hide any previous error messages

        // Prepare the data for submission
        let data = new FormData();
        data.append('FirstName', firstName);
        data.append('LastName', lastName);
        data.append('Email', email);
        data.append('Message', message);
        data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);
        // data.append('g-recaptcha-response', recaptchaResponse);

        // Display loading indicator
        jQuery('.loading').show();

        // AJAX request to submit the form
        jQuery.ajax({
            url: '/contact/', 
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            success: function (response) {
                jQuery('.loading').hide();
                if (response.success) {
                    jQuery('#myForm')[0].reset();
                    jQuery('.sent-message').show().text("Your message has been sent successfully!");
                } else {
                    jQuery('.error-message').show().text("Form submission failed. Please try again.");
                }
            },
            error: function () {
                jQuery('.loading').hide();
                jQuery('.error-message').show().text("An error occurred. Please try again later.");
            }
        });
    });
});


// $(document).ready(function(){
//     debugger
//     $('#popupBtn').click(function(event){
//         event.preventDefault();

//         let name = $('#exampleInputName').val();
//         let phone = $('#exampleInputPhone').val();
//         let email = $('#exampleInputEmail').val();
//         let message = $('#exampleInputMessageinfo').val();
//         let csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

//         // Get services interested in
//         let servicesInterestedIn = [];
//         $('input[name="servicesInterestedIn"]:checked').each(function() {
//             servicesInterestedIn.push($(this).val());
//         });

//         let data = new FormData();
//         data.append('name', name);
//         data.append('phone', phone);
//         data.append('email', email);
//         data.append('message', message);
//         data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

       
//         servicesInterestedIn.forEach((service) => {
//             data.append('servicesInterestedIn', service);
//         });

//         $.ajax({
//             type: 'POST',
//             url: '/', 
//             processData: false,
//             contentType: false,
//             cache: false,
//             data: data,
//             success: function(data, status, xhr){
//                 $('popForm')[0].reset();
//                 if(data.success === true){
//                   alert("Form Submission Successful");
//                 } else{
//                     alert("Invalid Form Submission");
//                 }   
//             },
//             error: function(data){
//                 alert("Form Submission Failed");
//             }
//         });
//     });
// });
