document.addEventListener("DOMContentLoaded",function(){
    const d = new Date();
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    function displayDate(){
        let month = months[d.getMonth()];
        let  year = d.getFullYear();
        let display = `${month} ${year}`
        document.getElementById("datetime").innerHTML = display;
    }
    setInterval(() => {
        displayDate();
    }, 60*60*1000);

    displayDate();
});