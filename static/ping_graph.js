const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const button = document.getElementById('button')
const form = document.getElementById('inputForm');

dropArea.addEventListener('dragenter', (e) => {
    e.preventDefault();
    dropArea.style.border = '2px dashed #3677f9';
});
// // check on mous movment if the cursonr is in drop area or in an element inside it
// dropArea.addEventListener('mousemove', (e) => {
//     e.preventDefault();
//     if (e.target === dropArea || e.target === button) {
//         dropArea.style.border = '2px dashed #3677f9';
//     } else {
//         dropArea.style.border = '2px dashed #ccc';
//     }
// });


dropArea.addEventListener('dragleave', () => {
    dropArea.style.border = '2px dashed #ccc';
});

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.style.border = '2px dashed #ccc';
    fileInput.files = e.dataTransfer.files;
    console.log(fileInput.files[0].name);
    form.submit();
});

fileInput.addEventListener('change', () => {
    const files = fileInput.files;
    console.log(files[0].name);
    form.submit();
});

// json file upload
button.addEventListener('click', () => {
    fileInput.click();
});