var bCount      = 0;
var tCount      = 0; 
var totalTrial  = 0; 
var progCount   = 0; 
var totalTokens = 0; 
var cdwn        = 3; 
var common      = null;
var odd         = null; 
var oddIdx      = null; 
var sequence    = null; 
var ans         = null; 
var timedout    = null; 
var key_press   = null; 
var rt          = null; 
var pcorrect    = null; 

var probe = {
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
    
    // (4. If no progress bar, show reward)
    if(prog_list[bCount]=='np') {
      html += '<div style="color:green; font-size:75px;"><b>$'+reward_list[bCount].toFixed(2)+'</b></div>'; 
    }

    // Show probes
    html += '<br><br><br><br>';
    html += '<table><tr>'; 

    for(let i=0; i<3; i++) {
      html += '<td><img src='+sequence[i]+'></td>'; 
    };
    html += '</tr></table>';

    return html;
  },
  choices: keys,
  trial_duration: maxtime,
  post_trial_gap: isi,
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
  }
};

var feedback_t = {
  type: 'html-keyboard-response',
  stimulus: function() {
    if(timedout)    return '<div style="font-size:75px;color:red">TOO SLOW!</div>'; 
    if(accuracy==0) return'<div style="font-size:75px;color:red">INCORRECT!</div>'; 
    if(accuracy==1) return ''; 

  },
  choices: ['space'],
  trial_duration: function(){
    if(timedout||accuracy==0) return errtime; 
    return 0; 
  }
};

var feedback_b = {
  type: 'html-keyboard-response',
  stimulus: function() {
    if(pcorrect >= acc_crit) {
      html = '<div style="font-size:75px;">You won $'+reward_list[bCount].toFixed(2)+'</div>'; 
    } else {
      html = '<div style="font-size:40px;">You made too many mistakes! No money this round.</div>'; 
    }
    html += '<br><br>'; 
    html += "<div style='font-size:25px;'>When you're ready, press SPACE to continue.</div>"; 
    return html;
  },
  choices: ['space'],
  //trial_duration: rewtime,
  post_trial_gap: rewiti, 
  on_finish: function() {
    if(pcorrect >= acc_crit) totalTokens += reward_list[bCount-1]; 
  }
};

var saveandUpdateData = {
  type: 'html-keyboard-response',
  stimulus: '',
  trial_duration: 0,
  on_finish: function(data) {
    data.isDataTrial   = true; // helpful for parsing
    data.block         = bCount;
    data.showprog      = prog_list[bCount]=='p' ? true:false;  
    data.blocklen      = length_list[bCount];
    data.trialinblock  = tCount;
    data.trial         = totalTrial;
    data.progress      = progCount/data.blocklen;
    data.reward        = reward_list[bCount];
    data.common        = common; 
    data.odd           = odd;  
    data.oddidx        = oddIdx;
    data.correct_ans   = ans; 
    data.key_press     = key_press; 
    data.rt            = rt; 
    data.accuracy      = accuracy; 
    data.timedout      = timedout; 
    data.totalTokens   = totalTokens; 
    data.timestamp     = Date.now(); 

    timedout = false; 
    tCount++;
    totalTrial++;

    // only increment progress bar if answer is correct 
    if(accuracy==1) progCount++; 
    pcorrect = progCount/tCount; 
  }
};

var show_countdown = {
  type: 'html-keyboard-response',
  stimulus: function() {
    html = '<div style="font-size:75px;">'+cdwn+'</div>'; 
    return html;
  },
  choices: jsPsych.NO_KEYS,
  trial_duration: 1000,
  on_finish: function() {
    cdwn -= 1; 
  }
};

var end = {
    type: 'html-keyboard-response',
    stimulus: function() {
        html  = "<p>You are done the experiment!</p>";
        html += '<p>You earned a <b>bonus</b> $'+maxPayout+'. Congratulations!</p>';
        html += "<p>Press SPACE to finish and receive your payment. Thank you so much!</p>";
        return html;
    },
    choices: ['space']
};
