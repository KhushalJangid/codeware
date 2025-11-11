function readFile(input) {
    let file = input.files[0];
    let filename = file.name;
    var filetype = filename.split(".").at(-1);
    const select = document.getElementById("filechooser");
    const nameElement = document.getElementById("filename");
    console.log(filetype);
    nameElement.innerText = filename;
    select.value = filetype;
    

    let reader = new FileReader();

    reader.readAsText(file);

    reader.onload = function () {
      editor.setValue(reader.result);
    };

    reader.onerror = function () {
      console.log(reader.error);
    };
  }