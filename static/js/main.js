function getBotResponse() {
    var rawText = $("#textInput").val();
    var userHtml = '<p class="userText"><span>' + rawText + '</span></p>';
    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
    $.get("/get", { msg: rawText }).done(function(data) {
      var botHtml = '<p class="botText"><span>' + data + '</span></p>';
      $("#chatbox").append(botHtml);
      document.getElementById('userInput').scrollIntoView({block: 'start', behavior: 'smooth'});
    });
}
$("#textInput").keypress(function(e) {
    if(e.which == 13) {
        getBotResponse();
    }
});
$("#buttonInput").click(function() {
  getBotResponse();
})

const body = document.querySelector("body")
const modeSwitch = document.querySelector(".dark__mode")
const modeText = document.querySelector(".mode__text")
const sunMode = document.querySelector(".sun__mode")
const moonMode = document.querySelector(".moon__mode")

modeSwitch.addEventListener("click", () => {
  body.classList.toggle("dark")

  if(body.classList.contains("dark")){
      sunMode.style.display = 'inline-block'
      moonMode.style.display = 'none'
      modeText.innerText = "Light Mode"
  }
  else{
      sunMode.style.display = 'none'
      moonMode.style.display = 'inline-block'
      modeText.innerText = "Dark Mode"
  }
})