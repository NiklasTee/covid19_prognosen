document.getElementById("openArrow").addEventListener("click", function() {
    const item = document.getElementById("opened");
    const itemDisplay = getComputedStyle(item).display;
    const openArrow = document.getElementById("openArrow")
    if (itemDisplay === "none") {
        item.style.display = "flex";
        openArrow.style.display = "none";
      } else {
        item.style.display = "none";
      }
    });

document.getElementById("closeArrow").addEventListener("click", function() {
    const item = document.getElementById("opened");
    const openArrow = document.getElementById("openArrow")
    if (item.style.display === "none") {
        item.style.display = "flex";
    } else {
        item.style.display = "none";
        openArrow.style.display = "block";
    }
});