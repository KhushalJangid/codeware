let hamburger = document.querySelector("#hamburger");
let sidebar = document.querySelector("#sidebar");
let state = 0;

hamburger.addEventListener('click', function(){
    console.log("aslkdjflasdkfj");
    toggleHamburger();
});

function toggleSidebar(){
    if(state){
        sidebar.classList.remove("collapsed");
    }else{
        sidebar.classList.add("collapsed");
    }
}

function toggleHamburger(){
    if(state){
        hamburger.classList.remove("is-active");
        state = 0;
        console.log("collapsed");
    }else{
        hamburger.classList.add("is-active");
        state = 1;
    }
    toggleSidebar();
}