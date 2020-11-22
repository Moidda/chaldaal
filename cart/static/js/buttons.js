document.getElementById("buttonAdd").addEventListener("click", function(){
    var pid = this.getAttribute("data-pid");
    window.location.href = "increase_item/" + pid + "/";
});

document.getElementById("buttonMinus").addEventListener("click", function(){
    var pid = this.getAttribute("data-pid");
    window.location.href = "decrease_item/" + pid + "/";
});

document.getElementById("buttonErase").addEventListener("click", function(){
    var pid = this.getAttribute("data-pid");
    window.location.href = "erase_item/" + pid + "/";
});