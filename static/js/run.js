function _format(text_) {
    text_ = text_.slice(1, -1);
    text_ = text_.replaceAll(String.raw `\n`, "<br>");
    text_ = text_.replaceAll(String.raw `\t`, "&nbsp;&nbsp;");
    text_ = text_.replaceAll(String.raw `\r`, "");
    return text_;
  }

  submit_btn = document.getElementById('run-btn');
  submit_btn.addEventListener("click", function () {
    submit_btn.disabled = true;
    clrscr();
    consoleElement.innerHTML = "<div class='loader m-auto'></div>";
    var csrf = document.getElementsByName("csrfmiddlewaretoken")[0];
    csrf = csrf.value;
    data = new FormData();
    data.append('lang', document.getElementById('filechooser').value);
    data.append('stdin', document.getElementById('inputs').value);
    data.append('code', editor.getValue());
    // console.log(csrf);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/compile', true);
    xhr.setRequestHeader('X-CSRFToken', csrf);
    xhr.getResponseHeader('Content-type', 'application/json');
    xhr.onload = function () {
      if (this.status === 200) {
        //var text_ = _format(xhr.responseText);
        submit_btn.disabled = false;
        document.getElementById('console').classList.remove("error");
        document.getElementById('console').innerHTML = _format(xhr.responseText);
      } else if (this.status === 400) {
        console.warn(xhr.responseText);
        submit_btn.disabled = false;
        document.getElementById('console').classList.add("error");
        document.getElementById('console').innerHTML = _format(xhr.responseText);
      } else {
        console.log("Some error occured");
      }
    }
    xhr.send(data);
    return xhr.responseText;
  })