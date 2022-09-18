let consoleElement = document.querySelector("#console");
let clrConsoleBtn = document.querySelector("#clr-console");
function clrscr(){
    consoleElement.innerHTML = "";
    consoleElement.classList.remove("error");
}
clrConsoleBtn.addEventListener("click", function(){
    clrscr();
})