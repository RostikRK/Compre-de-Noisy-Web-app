
function ekUpload(){
  function Init() {

    console.log("Upload Initialised");

    var fileSelect    = document.getElementById('file-upload'),
        fileDrag      = document.getElementById('file-drag'),
        submitButton  = document.getElementById('submit-button');

    fileSelect.addEventListener('change', fileSelectHandler, false);

    var xhr = new XMLHttpRequest();
    if (xhr.upload) {
      // File Drop
      fileDrag.addEventListener('dragover', fileDragHover, false);
      fileDrag.addEventListener('dragleave', fileDragHover, false);
      fileDrag.addEventListener('drop', fileSelectHandler, false);
    }
  }

  function fileDragHover(e) {
    var fileDrag = document.getElementById('file-drag');

    e.stopPropagation();
    e.preventDefault();

    fileDrag.className = (e.type === 'dragover' ? 'hover' : 'modal-body file-upload');
  }

function fileSelectHandler(e) {
  var files = e.target.files || e.dataTransfer.files;

  fileDragHover(e);

  for (var i = 0, f; f = files[i]; i++) {
    parseFile(f);
  }

  uploadFiles(files);
}

  function output(msg) {
    var m = document.getElementById('messages');
    m.innerHTML = msg;
  }

  function parseFile(file) {

    console.log(file.name);
    output(
      '<strong>' + encodeURI(file.name) + '</strong>'
    );

    var imageName = file.name;

    var isGood = (/\.(?=gif|jpg|png|jpeg)/gi).test(imageName);
    if (isGood) {
      document.getElementById('start').classList.add("hidden");
      document.getElementById('response').classList.remove("hidden");
      document.getElementById('notimage').classList.add("hidden");
      document.getElementById('file-image').classList.remove("hidden");
      document.getElementById('file-image').src = URL.createObjectURL(file);
    }
    else {
      document.getElementById('file-image').classList.add("hidden");
      document.getElementById('notimage').classList.remove("hidden");
      document.getElementById('start').classList.remove("hidden");
      document.getElementById('response').classList.add("hidden");
      document.getElementById("file-upload-form").reset();
    }
  }

  function setProgressMaxValue(e) {
    var pBar = document.getElementById('file-progress');

    if (e.lengthComputable) {
      pBar.max = e.total;
    }
  }

  function updateFileProgress(e) {
    var pBar = document.getElementById('file-progress');

    if (e.lengthComputable) {
      pBar.value = e.loaded;
    }
  }

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function uploadFiles(files) {
  var xhr = new XMLHttpRequest(),
    pBar = document.getElementById('file-progress'),
    fileSizeLimit = 1024; // In MB

  if (xhr.upload) {
    var totalFileSize = Array.from(files).reduce((total, file) => total + file.size, 0);
    if (totalFileSize <= fileSizeLimit * 1024 * 1024) {
      pBar.style.display = 'inline';

      xhr.upload.addEventListener('loadstart', setProgressMaxValue, false);
      xhr.upload.addEventListener('progress', updateFileProgress, false);

      xhr.onreadystatechange = function(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
          var response = JSON.parse(xhr.responseText);

          if (response.redirect_url) {
            window.location.href = response.redirect_url;
          }
        }
      };

      xhr.open('POST', document.getElementById('file-upload-form').action, true);

      var formData = new FormData();
      Array.from(files).forEach((file, index) => {
        formData.append('image', file);
      });

      var csrftoken = getCookie('csrftoken');

      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      xhr.send(formData);
    } else {
      output('Please upload smaller files (< ' + fileSizeLimit + ' MB in total).');
    }
  }
}





  if (window.File && window.FileList && window.FileReader) {
    Init();
  } else {
    document.getElementById('file-drag').style.display = 'none';
  }
}
ekUpload();