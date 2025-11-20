
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('applyJobModal');

    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const jobTitle = button.getAttribute('data-jobtitle');

        document.getElementById('applyJobModalTitle').innerText =
            `Apply for ${jobTitle}`;
    });
});



function jobapplication(jobtitle){
    debugger;
    let name  = document.getElementById("full_name").value;
    let email  = document.getElementById("email").value;
    let message  = document.getElementById("message").value;
    let resume = document.getElementById("resume_file").files[0];

    let formData = new FormData();
    formData.append("full_name", name);
    formData.append("email", email);
    formData.append("message", message);
    formData.append("job_title", jobtitle);
    formData.append("resume", resume);;

    fetch("/apply-job/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            alert("Application submitted successfully!");
            location.reload();
        } else {
            alert("Error: " + data.message);
        }
    })
    .catch(err => {
        console.error(err);
        alert("Something went wrong!");
    });
}
// phone validation in jobform 
document.getElementById("phone").addEventListener("input", function () {
    this.value = this.value.replace(/[^0-9]/g, "");
});


