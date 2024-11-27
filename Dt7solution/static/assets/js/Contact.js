$(document).ready(function(){
    $('#submitBtn').click(function(event){
        event.preventDefault();

        let firstName = $('#firstName').val();
        let lastName = $('#lastName').val();
        let email = $('#email').val();
        let message = $('#message').val();
        let csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
        
        // Get services interested in
        let servicesInterestedIn = [];
        $('input[name="servicesInterestedIn"]:checked').each(function() {
            servicesInterestedIn.push($(this).val());
        });

        let data = new FormData();
        data.append('firstName', firstName);
        data.append('lastName', lastName);
        data.append('email', email);
        data.append('message', message);
        data.append('csrfmiddlewaretoken', csrfmiddlewaretoken);

        // Append servicesInterestedIn array to FormData
        servicesInterestedIn.forEach((service) => {
            data.append('servicesInterestedIn', service);
        });
        

        $.ajax({
            type: 'POST',
            url: '/contact/',  // Replace with your form submission URL
            processData: false,
            contentType: false,
            cache: false,
            data: data,
            success: function(data, status, xhr){
                $('#myForm')[0].reset();
                if(data.success === true){
                    console.log(data)
                
                  alert("Form Submission Successful");
                } else{
                    alert("Invalid Form Submission");
                }   
            },
            error: function(data){
                alert("Form Submission Failed");
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
