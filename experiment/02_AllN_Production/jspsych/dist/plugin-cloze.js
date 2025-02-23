// NOTE: THIS VERSION OF JSPSYCH CLOZE HAS BEEN MODIFIED BY BRANDON PAPINEAU TO ACCEPT MULTIPLE CLOZE ANSWERS AND TO DISABLE PASTING. 

// Features of this version include:

// - An optional "prompt parameter"
// - Multiple possible answers with custom getAnswers function
// - Does not allow for multiple cloze blanks within a task
// - This version auto-focuses the text box for entry, so participants don't have to click on it each time
// - Similarly, the "continue" button has been replaced with an event listener for the enter key when the text entry box is in focus


var jsPsychCloze = (function (jspsych) {
  'use strict';

  const info = {
      name: "cloze",
      parameters: {
          /** The cloze text to be displayed. Blanks are indicated by %% signs and automatically replaced by input fields. If there is a correct answer you want the system to check against, it must be typed between the two percentage signs (i.e. %solution%). */
          text: {
              type: jspsych.ParameterType.HTML_STRING,
              pretty_name: "Cloze text",
              default: undefined,
          },
          /** Text of the button participants have to press for finishing the cloze test. */
          button_text: {
              type: jspsych.ParameterType.STRING,
              pretty_name: "Button text",
              default: "OK",
          },
          /** Boolean value indicating if the answers given by participants should be compared against a correct solution given in the text (between % signs) after the button was clicked. */
          check_answers: {
              type: jspsych.ParameterType.BOOL,
              pretty_name: "Check answers",
              default: false,
          },
          /** Boolean value indicating if the participant may leave answers blank. */
          allow_blanks: {
              type: jspsych.ParameterType.BOOL,
              pretty_name: "Allow blanks",
              default: true,
          },
          /** Function called if either the check_answers is set to TRUE or the allow_blanks is set to FALSE and there is a discrepancy between the set answers and the answers provide or if all input fields aren't filled out, respectively. */
          mistake_fn: {
              type: jspsych.ParameterType.FUNCTION,
              pretty_name: "Mistake function",
              default: () => { },
          },
          /** This parameter adds the option for a prompt, to be displayed beneath the cloze task */
          prompt: {
            type: jspsych.ParameterType.HTML_STRING,
            pretty_name: "Prompt",
            default: null,
          }
      },
  };
  /**
   * **cloze**
   *
   * jsPsych plugin for displaying a cloze test and checking participants answers against a correct solution
   *
   * @author Philipp Sprengholz
   * @see {@link https://www.jspsych.org/plugins/jspsych-cloze/ cloze plugin documentation on jspsych.org}
   */
  class ClozePlugin {
      constructor(jsPsych) {
          this.jsPsych = jsPsych;
      }
      trial(display_element, trial) {
          var html = '<div class="cloze">';
          // odd elements are text, even elements are the blanks
          var elements = trial.text.split("%");
          const solutions = this.getSolutions(trial.text);
          let solution_counter = 0;
          for (var i = 0; i < elements.length; i++) {
              if (i % 2 === 0) {
                  html += elements[i];
              }
              else {
                  html += `<input class = "inputBox" onpaste="return false" type="text" id="input${solution_counter}" value="">`;
                  solution_counter++;
              }
          }
          html += "</div>";
          if (trial.prompt !== "null") { // Adds the prompt functionality
            html += '<br><br><div id="jspsych-html-button-response-prompt" style="font-size:90%"> <strong>' + trial.prompt + "</strong></div>"
        };
          display_element.innerHTML = html;
          const check = () => {
              var answers = [];
              var answers_correct = true;
              var answers_filled = true;
              var field = document.getElementById("input"+0);
              var user_response = field.value.trim();
              answers.push(user_response);
            //   console.log("Solutions: "+solutions);
            //   console.log("User Response:"+user_response);
              if (trial.check_answers) {
                if (!solutions.includes(user_response)) {
                    field.style.color = "red";
                    answers_correct = false;
                }
                else {
                    field.style.color = "black";
                }
            }
            if (!trial.allow_blanks) {
                if (answers[i] === "") {
                    answers_filled = false;
                }
            }
            if ((trial.check_answers && !answers_correct) || (!trial.allow_blanks && !answers_filled)) {
                  trial.mistake_fn();
            }
            else {
                  var trial_data = {
                      response: answers,
                  };
                  display_element.innerHTML = "";
                  this.jsPsych.finishTrial(trial_data);
            }
          };
          // Function for enter key being used to progress the trial, and added EventListener below
          function enterPress(p) { 
              if (p.key == "Enter") {
                  p.preventDefault();
                  check();
              }
          };
          display_element.querySelector(".inputBox").addEventListener("keypress", enterPress); 
          display_element.querySelector(".inputBox").focus() // Auto focuses the text box
      }
      // custom getSolutions method for multiple answers, which are contained in the format "%answer1,answer2,answer3%"
      getSolutions(text) {
        const solutions = [];
        const elements = text.split("%");
        for (let i = 0; i < elements.length; i++) {
            if (i % 2 == 1) {
                // Split each element further based on ","
                const words = elements[i].split(",");
                words.forEach(word => {
                    // Push each word (trimmed) as a separate solution
                    solutions.push(word.trim());
                });
            }
        }
        return solutions;
    }    
      simulate(trial, simulation_mode, simulation_options, load_callback) {
          if (simulation_mode == "data-only") {
              load_callback();
              this.simulate_data_only(trial, simulation_options);
          }
          if (simulation_mode == "visual") {
              this.simulate_visual(trial, simulation_options, load_callback);
          }
      }
      create_simulation_data(trial, simulation_options) {
          const solutions = this.getSolutions(trial.text);
          const responses = [];
          for (const word of solutions) {
              if (word == "") {
                  responses.push(this.jsPsych.randomization.randomWords({ exactly: 1 }));
              }
              else {
                  responses.push(word);
              }
          }
          const default_data = {
              response: responses,
          };
          const data = this.jsPsych.pluginAPI.mergeSimulationData(default_data, simulation_options);
          //this.jsPsych.pluginAPI.ensureSimulationDataConsistency(trial, data);
          return data;
      }
      simulate_data_only(trial, simulation_options) {
          const data = this.create_simulation_data(trial, simulation_options);
          this.jsPsych.finishTrial(data);
      }
      simulate_visual(trial, simulation_options, load_callback) {
          const data = this.create_simulation_data(trial, simulation_options);
          const display_element = this.jsPsych.getDisplayElement();
          this.trial(display_element, trial);
          load_callback();
          const inputs = display_element.querySelectorAll('input[type="text"]');
          let rt = this.jsPsych.randomization.sampleExGaussian(750, 200, 0.01, true);
          for (let i = 0; i < data.response.length; i++) {
              this.jsPsych.pluginAPI.fillTextInput(inputs[i], data.response[i], rt);
              rt += this.jsPsych.randomization.sampleExGaussian(750, 200, 0.01, true);
          }
          this.jsPsych.pluginAPI.clickTarget(display_element.querySelector("#finish_cloze_button"), rt);
      }
  }
  ClozePlugin.info = info;

  return ClozePlugin;

})(jsPsychModule);
