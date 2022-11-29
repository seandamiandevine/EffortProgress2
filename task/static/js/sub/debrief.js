var debriefchoice;
var debrief = {
    type:'external-html',
    url: "static/js/sub/debriefing.html",
    cont_btn: "submit",
    check_fn: function(elem){
      if (document.getElementById('affirmative').checked) {
        debriefchoice = 'agree';
        return true;
    } else if (document.getElementById('negative').checked) {
      debriefchoice = 'decline';
      return true
    } else {
        alert("Please choose one of the options");
        return false;
      }
      return false;
    },
   on_start: function() {

     document.body.style.background = "white";

   },
   on_finish: function(data) {
     jsPsych.data.addProperties({
       debrief: debriefchoice
     });
   }
  };
