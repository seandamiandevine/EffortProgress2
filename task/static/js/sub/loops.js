
var practice = {
  timeline: [prac_probe, prac_feedback, saveandUpdatePracData], 
  loop_function: function() {
    if(pracCount==nprac) {
      maxtime = adapt_time ? Quartile(rts, adapt_quant) : maxtime; 
      jsPsych.data.addProperties({deadline: maxtime});
      return false; 
    }
    return true; 
  }, 
  on_start: function() {
    // show progress bar
    document.querySelector('#jspsych-progressbar-container').style.display = 'none'; 
  }
};

var trials = {
  timeline: [probe, saveandUpdateData], 
  loop_function: function() {
    if(progCount==length_list[bCount]) return false; 
    return true; 
  }, 
  on_start: function() {
    if(prog_list[bCount]=='p') {
      // show progress bar
      document.querySelector('#jspsych-progressbar-container').style.display = 'inline-block'; 

      // add target at end of progress bar
      if(!document.getElementById('#targetHTML')) {
        targetHTML  = '<span id=#targetHTML style="color:green;font-size:30px;">\t<b>$'+reward_list[bCount].toFixed(2)+'</b></span>'; 
        document.querySelector('#jspsych-progressbar-container').insertAdjacentHTML('beforeEnd', targetHTML); 
     }
       // update progress bar per trial
      jsPsych.setProgressBar(progCount/length_list[bCount]);
    } else {
      document.querySelector('#jspsych-progressbar-container').style.display = 'none'; 
    }
  },
};


var flag; // fix weird bug with jsPsych so that blocks don't skip 
var countdown = {
  timeline:[show_countdown], 
  loop_function: function() {
    if(cdwn < 1) {
      cdwn = 3;
      flag = false; 
      return false
    }
    flag = true; 
    return true; 
  }
}; 

var blocks = {
  timeline: [countdown, trials, feedback_b],
  loop_function: function() {
    if(bCount==nblocks) return false; 

    return true; 
  },
  on_start: function() {
    //hide and reset progress bar
    document.querySelector('#jspsych-progressbar-container').style.display = 'none';
    
    // reset progress bar
    jsPsych.setProgressBar(0); 
    progCount=0; 

    // increment block and reset trial in block
    if(flag==false) {
      bCount++;
      tCount=0;
      flag = true; 
    }
  }
};
