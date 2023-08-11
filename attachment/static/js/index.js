$(document).ready(function () {
  // Change the date input string to a date object
  document.getElementById("date").valueAsDate = new Date();

  //sending data to the backend
  $("#logForm").submit(function (e) {
    e.preventDefault();
    let formData = $(this).serialize();
    console.log(data)
    $.ajax({
      type: "POST",
      url: "{% url 'update_logbook'%}",
      data: formData,
      success: function (response) {
        alert("Successfully Update");
      },
      error: function (xhr, textStatus, errorThrown) {},
    });
  });
});
