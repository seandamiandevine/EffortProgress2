var pracCount   = 0; 
var common      = null;
var odd         = null; 
var oddIdx      = null; 
var sequence    = null; 
var ans         = null; 
var key_press   = null; 
var rt          = null; 
var rts         = []; 

var prac_probe = {
  type: 'html-keyboard-response',
  stimulus: function() {

    html = ''; 

    // 1. Sample sequence
    oddIdx = _.sample([0,1,2]); 
    common = _.sample(stim); 
    odd    = stim.filter(s => s!=common)[0]; 


    // 2. Create stim
    sequence = Array(3).fill(stimdir+'oddball_'+common+'.png'); 
    sequence[oddIdx] = stimdir+'oddball_'+odd+'.png'; 
    
    // 3. Determine correct answer and display stim in HTML format
    ans  = keys[oddIdx]; 

    // Show probe
    html += '<br><br><br><br>';
    html += '<table><tr>'; 

    for(let i=0; i<3; i++) {
      html += '<td><img src='+sequence[i]+'></td>'; 
    };
    html += '</tr></table>';

    return html;
  },
  choices: keys,
  //trial_duration: maxtime,
  on_finish: function(data){
    if(data.key_press==null) {
      timedout     = true;
      key_press    = null;
      rt           = null;
      accuracy     = 0; 
    } else {
      key_press  = jsPsych.pluginAPI.convertKeyCodeToKeyCharacter(data.key_press);
      rt         = data.rt;
      accuracy   = key_press==ans ? 1:0; 
    }
    rts.push(rt); 
  }
};

var prac_feedback = {
  type: 'html-keyboard-response',
  stimulus: function() {
    if(accuracy==0) {
      html = '<div style="font-size:75px;"><b>Incorrect</b></div>'; 
      html += '<br><br>'; 
      html += '<div font-size:50px;">The '+['left','middle','right'][oddIdx]+' shape was the odd one out, so you needed to press '+ans.toUpperCase()+'!</div>'; 
    } else {
      html = '<div style="font-size:75px;"><b>Correct</b></div>'; 
    }
    return html;
  },
  choices: jsPsych.NO_KEYS,
  trial_duration: 2500,
  post_trial_gap: rewiti, 
};

var saveandUpdatePracData = {
  type: 'html-keyboard-response',
  stimulus: '',
  trial_duration: 0,
  on_finish: function(data) {
    data.isDataTrial   = true; // helpful for parsing
    data.block         = 'practice';
    data.trialinblock  = pracCount;
    data.common        = common; 
    data.odd           = odd;  
    data.oddidx        = oddIdx;
    data.correct_ans   = ans; 
    data.key_press     = key_press; 
    data.rt            = rt; 
    data.accuracy      = accuracy; 
    data.totalTokens   = 0; 
    data.timestamp     = Date.now(); 

    pracCount++; 

  }
};