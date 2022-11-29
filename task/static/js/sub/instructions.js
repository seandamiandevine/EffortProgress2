var inst_ratio  = 1.77;
var inst_height = window.innerHeight;
var inst_width  = inst_ratio*inst_height;
var instIdx = 1; 
var inst_screen = {
    type: 'image-keyboard-response',
    stimulus: function() {
      return 'static/images/instructions/Slide'+instIdx+'.png'
    },
    choices: ['leftarrow', 'rightarrow'],
    stimulus_height: inst_height,
    stimulus_width: inst_width, 
    on_finish: function(data) {
        key_press = jsPsych.pluginAPI.convertKeyCodeToKeyCharacter(data.key_press);
        if(key_press=='rightarrow') { 
            instIdx++; 
        } else {
            instIdx = Math.max(1,instIdx-1); 
        }
    }
};

var instructions1 = {
  timeline: [inst_screen], 
  loop_function: function() {
    if(instIdx>7) return false; 
    return true; 
  }
}; 

var instructions2 = {
  timeline: [inst_screen], 
  loop_function: function() {
    if(instIdx>17) return false; 
    return true; 
  }
}; 

var instructions3 = {
  timeline: [inst_screen], 
  loop_function: function() {
    if(instIdx>18) return false; 
    return true; 
  }
}; 

var instQAns = null; 
var inst_quiz = {
    type: 'survey-multi-choice',
    questions: [
      {
        prompt: 'What key do you need to press if the shape on the LEFT is the odd one out?',
        options: [keys[0], keys[1], 'spacebar', 'It depends what the shape is'],
        name: 'q1',
        required: true
      },
      {
        prompt: 'What key do you need to press if the shape in the MIDDLE is the SAME as the shape on the RIGHT?',
        options: [keys[0], keys[1], 'spacebar', 'F'],
        name: 'q2',
        required: true
      },
      {
        prompt: 'Will the progress bar fill up every time you answer?', 
        options: ['Yes', 'Only if I get the answer right', 'Only if I get the answer wrong'],
        name: 'q3',
        required: true
      },
      {
        prompt: 'What happens after you finish judging a series of shapes?',
        options: ['You win money', 'You lose money', 'Nothing'],
        name: 'q4',
        required: true
      },
      {
        prompt: 'How much time do you have to judge each shape?',
        options: ['As much time as I need', 'A fixed time limit', 'It depends on the word'],
        name: 'q5',
        required: true
      },
    ],
    randomize_question_order: true,
    on_finish:function(data){
      instQAns   = JSON.parse(data.responses);
      instQ1Cor  = instQAns.q1 == keys[0] ? 1:0;
      instQ2Cor  = instQAns.q2 == keys[0] ? 1:0;
      instQ3Cor  = instQAns.q3 == 'Only if I get the answer right' ? 1:0;
      instQ4Cor  = instQAns.q4 == 'You win money' ? 1:0;
      instQ5Cor  = instQAns.q5 == 'A fixed time limit' ? 1:0;
      totalInstQ = instQ1Cor+instQ2Cor+instQ3Cor+instQ4Cor+instQ5Cor;

      jsPsych.data.addProperties({
          instQ1     : instQAns.q1, 
          instQ2     : instQAns.q2, 
          instQ3     : instQAns.q3, 
          instQ4     : instQAns.q4, 
          instQ5     : instQAns.q5,
          totalInstQ : totalInstQ
        });
    }
};
