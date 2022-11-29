var task2Q = {
    type: 'html-keyboard-response',
    stimulus: function() {
        html =  '<p>You are finished the main part of the study!</p>';
        html += '<p>We just have a few questions for you to answer and then you will be done for today. Please answer these questions honestly.</p>';
        html += '<p>Press SPACE to continue.</p>';
        return html
    },
    choices: ['space'], 
    on_finish: function() {
      document.body.style.background = "white";
      document.body.style.color = 'black'   
    }
};

var demographics = {
  type: 'survey-text',
  questions: [
    {prompt: "For statistical purposes, how old are you? (please type out in years)", name:'age', required: true},
    {prompt: "For statistical purposes, What is your gender? (please type out your answer below)", name:'gender', required: true}
      ],
  preamble: 'Please answer these questions.',
  on_finish: function(data) {
    jsPsych.data.addProperties({
      age:    JSON.parse(data.responses)['age'],
      gender: JSON.parse(data.responses)['gender']
    });

  }
};

var debrief_questions = {
  type: 'survey-text',
  questions: [
    {prompt: "Did you have any explicit strategy while completing the task?", name:'strategy', required: true},
    {prompt: "Do you have any other comments you would like to share?", name:'comments', required: true},
      ],
  preamble: 'Please answer these questions.',
  on_finish: function(data) {
    jsPsych.data.addProperties({
      strategy: JSON.parse(data.responses)['strategy'],
      comments: JSON.parse(data.responses)['comments']
    });
  }
};


var DASS21 = {
  type: 'survey-likert',
  questions: [
    {prompt: "I found it hard to wind down", name:'DASS1', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I was aware of dryness of my mouth", name:'DASS2', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I couldn’t seem to experience any positive feeling at all", name:'DASS3', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I experienced breathing difficulty (e.g. excessively rapid breathing, breathlessness in the absence of physical exertion)", name:'DASS4', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I found it difficult to work up the initiative to do things", name:'DASS5', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I tended to over-react to situations", name:'DASS6', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I experienced trembling (e.g. in the hands)", name:'DASS7', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I felt that I was using a lot of nervous energy", name:'DASS8', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I was worried about situations in which I might panic and make a fool of myself", name:'DASS9', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I felt that I had nothing to look forward to I found myself getting agitated", name:'DASS10', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I found myself getting agitated", name:'DASS11', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I found it difficult to relax", name:'DASS12', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I felt down-hearted and blue", name:'DASS13', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I was intolerant of anything that kept me from getting on with what I was doing", name:'DASS14', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I felt I was close to panic", name:'DASS15', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I was unable to become enthusiastic about anything'", name:'DASS16', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I felt I wasn’t worth much as a person", name:'DASS17', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I felt that I was rather touchy", name:'DASS18', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I was aware of the action of my heart in the absence of physical exertion (e.g. sense of heart rate increase, heart missing a beat)", name:'DASS19', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I felt scared without any good reason.", name:'DASS20', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']},
    {prompt: "I felt that life was meaningless", name:'DASS21', required: true, labels:['Did not apply to me much or very often','1','2','Applied to me very much or most of the time']}

      ],
  preamble: 'Please answer these questions. The rating scale is as follows: 0 =Did not apply to me at all, 1 = Applied to me to some degree, or some of the time, 2 =Applied to me to a considerable degree or a good part of time, 3 =Applied to me very much or most of the time',
  scale_width: 500, 
  on_finish: function(data) {
    jsPsych.data.addProperties({
      DASS1_s:     JSON.parse(data.responses)['DASS1'],
      DASS2_a:     JSON.parse(data.responses)['DASS2'],
      DASS3_d:     JSON.parse(data.responses)['DASS3'],
      DASS4_a:     JSON.parse(data.responses)['DASS4'],
      DASS5_d:     JSON.parse(data.responses)['DASS5'],
      DASS6_s:     JSON.parse(data.responses)['DASS6'],
      DASS7_a:     JSON.parse(data.responses)['DASS7'],
      DASS8_s:     JSON.parse(data.responses)['DASS8'],
      DASS9_a:     JSON.parse(data.responses)['DASS9'],
      DASS10_d:    JSON.parse(data.responses)['DASS10'],
      DASS11_s:    JSON.parse(data.responses)['DASS11'],
      DASS12_s:    JSON.parse(data.responses)['DASS12'],
      DASS13_d:    JSON.parse(data.responses)['DASS13'],
      DASS14_s:    JSON.parse(data.responses)['DASS14'],
      DASS15_a:    JSON.parse(data.responses)['DASS15'],
      DASS16_d:    JSON.parse(data.responses)['DASS16'],
      DASS17_d:    JSON.parse(data.responses)['DASS17'],
      DASS18_s:    JSON.parse(data.responses)['DASS18'], 
      DASS19_a:    JSON.parse(data.responses)['DASS19'],
      DASS20_a:    JSON.parse(data.responses)['DASS20'],
      DASS21_d:    JSON.parse(data.responses)['DASS21']
    });
  }
};

var BISBAS = {
  // see https://local.psy.miami.edu/people/faculty/ccarver/availbale-self-report-instruments/bisbas-scales/
  type: 'survey-likert',
  questions: [
    {prompt: "A person's family is the most important thing in life.", name:'BB1', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "Even if something bad is about to happen to me, I rarely experience fear or nervousness.", name:'BB2', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I go out of my way to get things I want.", name:'BB3', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "When I'm doing well at something I love to keep at it.", name:'BB4', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I'm always willing to try something new if I think it will be fun.", name:'BB5', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "How I dress is important to me.", name:'BB6', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "When I get something I want, I feel excited and energized.", name:'BB7', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "Criticism or scolding hurts me quite a bit.", name:'BB8', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "When I want something I usually go all-out to get it.", name:'BB9', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I will often do things for no other reason than that they might be fun.", name:'BB10', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "It's hard for me to find the time to do things such as get a haircut.", name:'BB11', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "If I see a chance to get something I want I move on it right away.", name:'BB12', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I feel pretty worried or upset when I think or know somebody is angry at me.", name:'BB13', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "When I see an opportunity for something I like I get excited right away.", name:'BB14', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I often act on the spur of the moment.", name:'BB15', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "If I think something unpleasant is going to happen I usually get pretty worked up.", name:'BB16', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I often wonder why people act the way they do.", name:'BB17', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "When good things happen to me, it affects me strongly.", name:'BB18', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I feel worried when I think I have done poorly at something important.", name:'BB19', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I crave excitement and new sensations.", name:'BB20', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "When I go after something I use a no holds barred approach.", name:'BB21', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I have very few fears compared to my friends.", name:'BB22', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "It would excite me to win a contest.", name:'BB23', required: true, labels:['Very true for me','2','3','Very false for me']},
    {prompt: "I worry about making mistakes.", name:'BB24', required: true, labels:['Very true for me','2','3','Very false for me']}
      ],
  preamble: 'Please answer these questions. The rating scale is as follows:\n1 = Very true for me, 2 = Somewhat true for me, 3 = Somewhat false for me, 4 = Very false for me.',
  scale_width: 500, 
  on_finish: function(data) {
    jsPsych.data.addProperties({
      BB1:     JSON.parse(data.responses)['BB1'],
      BB2:     JSON.parse(data.responses)['BB2'],
      BB3:     JSON.parse(data.responses)['BB3'],
      BB4:     JSON.parse(data.responses)['BB4'],
      BB5:     JSON.parse(data.responses)['BB5'],
      BB6:     JSON.parse(data.responses)['BB6'],
      BB7:     JSON.parse(data.responses)['BB7'],
      BB8:     JSON.parse(data.responses)['BB8'],
      BB9:     JSON.parse(data.responses)['BB9'],
      BB10:    JSON.parse(data.responses)['BB10'],
      BB11:    JSON.parse(data.responses)['BB11'],
      BB12:    JSON.parse(data.responses)['BB12'],
      BB13:    JSON.parse(data.responses)['BB13'],
      BB14:    JSON.parse(data.responses)['BB14'],
      BB15:    JSON.parse(data.responses)['BB15'],
      BB16:    JSON.parse(data.responses)['BB16'],
      BB17:    JSON.parse(data.responses)['BB17'],
      BB18:    JSON.parse(data.responses)['BB18'], 
      BB19:    JSON.parse(data.responses)['BB19'],
      BB20:    JSON.parse(data.responses)['BB20'],
      BB21:    JSON.parse(data.responses)['BB21'],
      BB22:    JSON.parse(data.responses)['BB22'],
      BB23:    JSON.parse(data.responses)['BB23'],
      BB24:    JSON.parse(data.responses)['BB24']
    });
  }
};

var NFC = {
  // see https://centerofinquiry.org/uncategorized/need-for-cognition-scale-wabash-national-study/
  type: 'survey-likert',
  questions: [
    {prompt: "I would prefer complex to simple problems.", name:'NFC1', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I like to have the responsibility of handling a situation that requires a lot of thinking.", name:'NFC2', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "Thinking is not my idea of fun.", name:'NFC3', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I would rather do something that requires little thought than something that is sure to challenge my thinking abilities.", name:'NFC4', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I try to anticipate and avoid situations where there is likely a chance I will have to think in depth about something.", name:'NFC5', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I find satisfaction in deliberating hard and for long hours.", name:'NFC6', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I would prefer complex to simple problems.", name:'NFC1', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I only think as hard as I have to.", name:'NFC7', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I prefer to think about small, daily projects to long-term ones.", name:'NFC8', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I like tasks that require little thought once I’ve learned them.", name:'NFC9', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "The idea of relying on thought to make my way to the top appeals to me.", name:'NFC10', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I really enjoy a task that involves coming up with new solutions to problems.", name:'NFC11', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "Learning new ways to think doesn’t excite me very much.", name:'NFC12', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I prefer my life to be filled with puzzles that I must solve.", name:'NFC13', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "The notion of thinking abstractly is appealing to me.", name:'NFC14', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I would prefer a task that is intellectual, difficult, and important to one that is somewhat important but does not require much thought.", name:'NFC15', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I feel relief rather than satisfaction after completing a task that required a lot of mental effort.", name:'NFC16', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "It’s enough for me that something gets the job done; I don’t care how or why it works.", name:'NFC17', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']},
    {prompt: "I usually end up deliberating about issues even when they do not affect me personally.", name:'NFC18', required: true, labels:['Extremely uncharacteristic','2','3','4','Extremely characteristic']}
      ],
  preamble: 'For each of the statements below, please indicate to what extent the statement is characteristic of you. The rating scale is as follows: 1 = extremely uncharacteristic, 2 = somewhat uncharacteristic, 3 = uncertain, 4 = somewhat characteristc, 5 = extremely characteristic',
  scale_width: 500, 
  on_finish: function(data) {
    jsPsych.data.addProperties({
      NFC1:     JSON.parse(data.responses)['NFC1'],
      NFC2:     JSON.parse(data.responses)['NFC2'],
      NFC3:     JSON.parse(data.responses)['NFC3'],
      NFC4:     JSON.parse(data.responses)['NFC4'],
      NFC5:     JSON.parse(data.responses)['NFC5'],
      NFC6:     JSON.parse(data.responses)['NFC6'],
      NFC7:     JSON.parse(data.responses)['NFC7'],
      NFC8:     JSON.parse(data.responses)['NFC8'],
      NFC9:     JSON.parse(data.responses)['NFC9'],
      NFC10:    JSON.parse(data.responses)['NFC10'],
      NFC11:    JSON.parse(data.responses)['NFC11'],
      NFC12:    JSON.parse(data.responses)['NFC12'],
      NFC13:    JSON.parse(data.responses)['NFC13'],
      NFC14:    JSON.parse(data.responses)['NFC14'],
      NFC15:    JSON.parse(data.responses)['NFC15'],
      NFC16:    JSON.parse(data.responses)['NFC16'],
      NFC17:    JSON.parse(data.responses)['NFC17'],
      NFC18:    JSON.parse(data.responses)['NFC18']
    });
  }
};

