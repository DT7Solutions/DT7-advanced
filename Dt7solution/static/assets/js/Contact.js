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

















