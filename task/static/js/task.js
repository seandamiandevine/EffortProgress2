// Miscelaneous preperation stuff
const filename = 'oddball_' + JSON.parse(tmp)[0]['ID'] + '_' + Date() + '.csv'; 

 jsPsych.data.addProperties({
   subject: JSON.parse(tmp)[0]['ID'],
   age: JSON.parse(tmp)[0]['AGE'], 
   sex: JSON.parse(tmp)[0]['SEX'],
   date: Date.now()
 });

var fs = {
	type: 'fullscreen', 
  fullscreen_mode: true,
  on_start: function(){
    // set up task appearence
    document.body.style.background = "black";
    document.body.style.color = 'white'   
    document.querySelector('#jspsych-progressbar-container').style.display    = 'none';
    document.querySelector('#jspsych-progressbar-container').style.background = 'black'; 
    document.querySelector('#jspsych-progressbar-container').style.border     = 'black'; 
    document.querySelector('#jspsych-progressbar-outer').style.height         = '25px'; 
  }, 
};

img_preload = ['static/images/oddball_up.png', 'static/images/oddball_down.png']; 
for(let i=1; i<19; i++) {
  img_preload.push('static/images/instructions/Slide'+i+'.png'); 
}

// Setup Timeline
if(debugmode) {
  timeline = [fs, blocks, task2Q, demographics, debrief_questions, DASS21, BISBAS, NFC, end];
} else {
  timeline = [fs, instructions1, practice, instructions2, inst_quiz, instructions3, blocks, task2Q, demographics, debrief_questions, DASS21, BISBAS, NFC, end];
}


// Run and preload images
jsPsych.init({
    timeline: timeline,
		show_preload_progress_bar: true,
    preload_images: img_preload,  
    show_progress_bar: true, 
    on_finish: function() {
      jsPsych.data.get().localSave('csv', filename); 
      window.close()
    }
  });
