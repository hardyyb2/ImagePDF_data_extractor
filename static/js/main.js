document.addEventListener("DOMContentLoaded", function () {
  console.log("loaded");
  let fileupload = document.querySelector(".file-upload-field");
  let wrapper = document.querySelector(".file-upload-wrapper");

  fileupload.addEventListener("change", function () {
    const fileName = this.files[0].name;

    wrapper.setAttribute("data-text", fileName || "file");
  });
});
