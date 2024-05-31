// create_tv_array is a function used to read in the js formatted stimuli and convert them into object dictionaries that can be used by jspsych

function create_tv_array(json_object) {
    let tv_array = [];
    for (let i = 0; i < json_object.length; i++) {
        obj = {};
        obj.text = json_object[i].text;
        obj.data = {}; // everything defined in obj.data will be available to jsPsych when "jsPsych.timelinevariable('data)" is called
        obj.data.id = json_object[i].id;
        obj.data.conj1 = json_object[i].conj1;
        obj.data.conj2 = json_object[i].conj2;
        obj.data.text = json_object[i].text;
        obj.data.dataType = json_object[i].dataType;
        obj.data.cond = json_object[i].cond;
        obj.data.conj1_agr = json_object[i].conj1_agr
        obj.data.conj2_agr = json_object[i].conj2_agr
        tv_array.push(obj)
    }
    return tv_array;
}

// Preliminary Functions //

// Define Function Using the Fisher-Yates (Knuth) Shuffle Algorithm to randomize stimulus selection //
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  }
