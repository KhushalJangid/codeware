var editor = CodeMirror.fromTextArea(document.getElementById("editor-0"), {
    mode: "python",
    theme: "dracula",
    lineNumbers: true,
    autoCloseTags: true,
    autoCloseBrackets: true,
  });

var tabBar = document.getElementById('tab-bar');

document.getElementById('add-file').addEventListener('click',(element)=>{
    var tabs = tabBar.querySelectorAll('div');
    let tab = document.createElement('div');
    tab.id = `tab-${tabs.length}`;
    tab.classList.add('tab');
    tab.innerHTML = `Untitled.py
    <button type="button"><i class="fa fa-times"></i></button>`;
    tabBar.insertBefore(tab,tabBar.lastElementChild);

})