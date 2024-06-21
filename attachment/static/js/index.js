$(document).ready(function () {
  // Supervisor auto suggest
  // const inputField = document.getElementById("supervisor-input");
  // const itemList = document.getElementById("item-list");

  // const lec = document.getElementById("lec-selector")
  // const lecBtn = document.getElementById("#lec-submit")
  // lec.addEventListener('input', function(){
  //   let inputValue = this.value.trim();
  //   lecBtn.disabled = inputValue === ''
  // })


  
  const inputFields = Array.from(
    document.getElementsByClassName("supervisor-input")
  );
  const itemList = Array.from(document.getElementsByClassName("item-list"));

  inputFields.forEach((element) => {
    element.addEventListener("input", function () {
      const search = element.value;
      fetch(`/attachment/?query=${search}`)
        .then((response) => response.json())
        .then((data) => {
          itemList.forEach((selector) => {
            selector.innerHTML = "";
            data.forEach((item) => {
              const li = document.createElement("li");
              li.textContent = item;
              selector.appendChild(li);
            });
          });
        });
    });
  });

  itemList.forEach((element) => {
    element.addEventListener("click", (event) => {
      if (event.target.tagName === "LI") {
        inputFields.forEach((input) => {
          input.value = event.target.textContent;
          element.innerHTML = "";
        });
      }
    });
  });
  // inputField.addEventListener("input", function () {
  //   const search = inputField.value;
  //   fetch(`/attachment/admin/?query=${search}`)
  //     .then((response) => response.json())
  //     .then((data) => {
  //       itemList.innerHTML = "";
  //       data.forEach((item) => {
  //         const li = document.createElement("li");
  //         li.textContent = item;
  //         itemList.appendChild(li);
  //       });
  //     });
  // });

  // itemList.addEventListener("click", (event) => {
  //   if (event.target.tagName === "LI") {
  //     inputField.value = event.target.textContent;
  //     itemList.innerHTML = "";
  //   }
  // });

  // Getting the cookie Data

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
  }
  const csrfToken = getCookie("csrftoken");

  //sending log book data to the backend
  $("#logForm").submit(function (e) {
    e.preventDefault();
    let formData = $(this).serialize();
    $.ajax({
      type: "POST",
      url: "/attachment/logbook/",
      data: formData,
      success: function (response) {
        if (response.is_valid) {
          // window.location.href('http://127.0.0.1:8000/attachment/summary/')
          alert("Succesffully updated");
        } 
        else {
          alert("LogBook date must come after your attachment start date");
        }
      },
      error: function (xhr, textStatus, errorThrown) { },
    });
    this.reset();
  });

  // file upload handler
  const form = document.querySelector("#file-upload");
  fileInput = form.querySelector(".file-input");
  progressArea = document.querySelector(".progress-area");
  uploadedArea = document.querySelector(".uploaded-area");

  form.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.onchange = ({ target }) => {
    let file = target.files[0];
    if (file) {
      let fileName = file.name;
      if (fileName.length >= 12) {
        let splitName = fileName.split(".");
        fileName = splitName[0].substring(0, 12) + ".... ." + splitName[1];
      }
      uploadFile(fileName);
    }
  };

  function uploadFile(name) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8000/attachment/uploads/");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.upload.addEventListener("progress", ({ loaded, total }) => {
      let fileLoaded = Math.floor((loaded / total) * 100);
      let fileTotal = Math.floor(total / 1000);
      let fileSize;
      fileTotal < 1024
        ? (fileSize = fileTotal + " KB")
        : (fileSize = loaded / (1024 * 1024)).toFixed(2) + " MB";
      let progressHTML = ` <li class="row">
                              <i class="fa-solid fa-file-pdf"></i>
                              <div class="content">
                                <div class="details">
                                  <span class="name">${name} . Uploading</span>
                                  <span class="percent">${fileLoaded}%</span>
                                </div>
                                <div class="progress-bar">
                                  <div class="progress" style="width: ${fileLoaded}%"></div>
                                </div>
                              </div>
                              </li>`;
      uploadedArea.innerHTML = "";
      progressArea.innerHTML = progressHTML;
      if (loaded == total) {
        progressArea.innerHTML = "";
        let uploadedHTML = ` <li class="row">
                               <div class="content">
                                 <i class="fa-solid fa-file-pdf"></i>
                                 <div class="details">
                                   <span class="name">${name} . Uploaded</span>
                                   <span class="size">${fileSize} KB</span>
                                 </div>
                               </div>
                               <i class="fas fa-check"></i>
                                </li>`;
        uploadedArea.innerHTML = uploadedHTML;
      }
    });
    let formData = new FormData(form);
    xhr.send(formData);
  }
});
