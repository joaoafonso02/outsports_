// script.js

function smoothScroll(target) {
  document.querySelector(target).scrollIntoView({
    behavior: 'smooth'
  });
}
  
function submitForm() {
  var name = document.getElementById('name').value;
  var email = document.getElementById('email').value;
  var subject = document.getElementById('subject').value;
  var message = document.getElementsByName('message')[0].value;

  var mailtoLink = 'mailto:outsportsTeam@os.com?subject=' + encodeURIComponent(subject) +
    '&body=' + encodeURIComponent(message);

  window.location.href = mailtoLink;
}
