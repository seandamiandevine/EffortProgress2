var DEBUG = JSON.parse(tmp)[0]['DEBUG']; 

const debugmode   = DEBUG=='true'? true:false;                       // whether to skip instructions + practice (for debugging) 
const maxPayout   = 2.00;                                            // maximum dollar amount subjects can earn
const tpb         = debugmode ? [10,10]:[60];                        // correct responses needed per block to finish
const rewards     = [0.02,0.20];                                     // possible rewards
const adapt_time  = false                                            // adaptive deadlines or not
const adapt_quant = 0.70                                             // if adapative deadlines, what quantile of baseline RTs to use
const progcond    = ['p','np'];                                      // progress conditions
const reps        = debugmode? 1:4;                                  // number of repetitions
const maxn        = tpb.length*rewards.length*progcond.length*reps   // max number of blocks 
const nblocks     = debugmode ? 4:maxn;                              // total number of blocks
const nprac       = adapt_time ? 30:20;                              // total number of practice trials
const stimdir     = 'static/images/'                                 // stimulus directory
const stim        = ['up','down'];                                   // direction of oddball 
const fontsize    = '100px';                                         // font size
const keys        = ['q','w','e'];                                   // keys to press
const acc_crit    = 0.75                                             // P(correct) needed to get points 
//const rewtime     = 2500;                                          // time that rewards stay on screen
const rewiti      = 1000;                                            // time from rewards back to task
const errtime     = 1500;                                            // error or timeout message duration (in ms.)
var   maxtime     = 750;                                             // max response deadline (if !adapt_time)
var   isi         = 100;                                             // short isi to avoid "glitch" feel

var prog_list     = [];
var reward_list   = []; 
var length_list   = []; 

for(let rep = 0; rep < reps; rep++) {
  for(let p = 0; p < 2; p++) {
    for(let l = 0; l < tpb.length; l++) {
      for(let r = 0; r < rewards.length; r++){
        prog_list.push(progcond[p]); 
        length_list.push(tpb[l]); 
        reward_list.push(rewards[r]);
      } 
    }
  }
}; 


// shuffle
randIdx     = _.shuffle([...Array(nblocks).keys()]);
prog_list   = randIdx.map(i => prog_list[i]);
length_list = randIdx.map(i => length_list[i]);
reward_list = randIdx.map(i => reward_list[i]);

// check to be sure counterbalancing worked
// x = {'p':{0.02:[], 0.20:[]}, 'np':{0.02:[], 0.20:[]} }; 
// for (let [i,t] of prog_list.entries()) {
//     x[t][reward_list[i]].push(length_list[i]); 
// }

function Quartile(data, q) {
  data=Array_Sort_Numbers(data);
  var pos = ((data.length) - 1) * q;
  var base = Math.floor(pos);
  var rest = pos - base;
  if( (data[base+1]!==undefined) ) {
    return data[base] + rest * (data[base+1] - data[base]);
  } else {
    return data[base];
  }
}

function Array_Sort_Numbers(inputarray){
  return inputarray.sort(function(a, b) {
    return a - b;
  });
}