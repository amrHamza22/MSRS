const defaultBtn = document.getElementById("default-btn");
const uploadBtn = document.getElementById("Upload");
const searchBtn = document.getElementById("Search");
const uploadedImage = document.querySelector("#img");
const uploadedVideo = document.querySelector("#video");
const message = document.getElementById("message")
const outputList = document.querySelector(".output");
const selectList = document.getElementById("algorithms");

let algorithmValue = 0;
let selectedImage = '';
let selectedVideo = '';
let uploadType = '';

selectList.addEventListener("change", e => {
  e.preventDefault();
  algorithmValue = e.target.value;
});

uploadBtn.addEventListener('click', () => {
  defaultBtn.click();
});

defaultBtn.addEventListener('change', (e) => {
  e.preventDefault();
  uploadType = e.target.files[0].type.split("/")[0]
  if (uploadType == "image"){
    var reader = new FileReader();
    reader.onload = (event) => {
      $('#img')
      .attr('src', event.target.result)
      .width(400)
      .height(300)
    };
    selectedImage = e.target.files[0]
    reader.readAsDataURL(selectedImage);
    uploadedImage.style.display = "block";
    uploadedVideo.style.display = "none";
  }
  else if (uploadType == "video"){
    var reader = new FileReader();
    reader.onload = (event) => {
      $('#video')
      .attr('src', event.target.result)
      .width(400)
      .height(300)
    };
    selectedVideo = e.target.files[0]
    reader.readAsDataURL(selectedVideo);
    uploadedVideo.style.display = "block";
    uploadedImage.style.display = "none";
  }
});

searchBtn.addEventListener('click', () => {
  if (uploadType === '') return;

  if (uploadType === 'image') {
    const formData = new FormData();
    formData.append("image", selectedImage);
    const imageConfig = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };
    axios.post(`http://127.0.0.1:5000/searchimage/${algorithmValue}`, formData, imageConfig)
    .then((res) => {
                  removeAllChildNodes(outputList);
                  const results = res.data;
                  results.forEach(item => {
                    createImage(outputList, item)
                  })
              })
              .catch((err) => {
                message.innerText="the image wasn't uploaded successfully";
                message.style.display= "block";
                message.classList.remove("success");
                message.classList.add("fail");
              });
  } else if (uploadType === 'video') {
    const formData = new FormData();
    formData.append("video", selectedVideo);
    axios.post("http://127.0.0.1:5000/searchvideo/", formData)
            .then((res) => {
              removeAllChildNodes(outputList);
              const results = res.data;
                results.forEach(item => {
                  createVideo(outputList, item)
                })
            })
            .catch((err) =>{ 
              message.innerText="the video wasn't uploaded successfully";
              message.style.display= "block";
              message.classList.remove("success");
              message.classList.add("fail");
            });
  }
})

const createImage = (list, src) => {
  const listItem = document.createElement("LI");    
  const image = document.createElement("IMG");
  image.setAttribute('src', src);
  listItem.appendChild(image);
  list.appendChild(listItem);
}

const createVideo = (list, src) => {
  const listItem = document.createElement("LI");    
  const video = document.createElement("VIDEO");
  video.setAttribute('src', src);
  video.setAttribute('controls', true);
  listItem.appendChild(video);
  list.appendChild(listItem);
}

const removeAllChildNodes = (parent) => {
  while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
  }
}



