var consent = {
  type:'external-html',
  url: "static/js/sub/consent.html",
  cont_btn: 'agree',
  on_start: function() {
    document.body.style.background = "white";
    document.querySelector('#jspsych-progressbar-container').style.display = 'none';
  }
};
