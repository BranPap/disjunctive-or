//The following code initializes the JS Psych 

const jsPsych = initJsPsych({
    show_progress_bar: true,
    auto_update_progress_bar: false,
    on_finish: function(data) {
        proliferate.submit({"trials": data.values()}); // This onfinish function calls the proliferate pipeline to collect data
        // jsPsych.data.displayData('csv'); // Uncomment to see the sumbitted csv at the end of the experiment
    }
});

let timeline = [];
// push experiment logic the timeline here...
// ......

// IRB FORM //

const irb = {
    // Which plugin to use
    type: jsPsychHtmlButtonResponse,
    // What should be displayed on the screen
    stimulus: '<p><font size="3">We invite you to participate in a research study on language production and comprehension. Your experimenter will ask you to do a linguistic task such as reading sentences or words, naming pictures or describing scenes, making up sentences of your own, or participating in a simple language game. <br><br>There are no risks or benefits of any kind involved in this study. <br><br>You will be paid for your participation at the posted rate.<br><br>If you have read this form and have decided to participate in this experiment, please understand your participation is voluntary and you have the right to withdraw your consent or discontinue participation at anytime without penalty or loss of benefits to which you are otherwise entitled. You have the right to refuse to do particular tasks. Your individual privacy will be maintained in all published and written data resulting from the study. You may print this form for your records.<br><br>CONTACT INFORMATION: If you have any questions, concerns or complaints about this research study, its procedures, risks and benefits, you should contact the Protocol Director Meghan Sumner at (650)-725-9336. If you are not satisfied with how this study is being conducted, or if you have any concerns, complaints, or general questions about the research or your rights as a participant, please contact the Stanford Institutional Review Board (IRB) to speak to someone independent of the research team at (650)-723-2480 or toll free at 1-866-680-2906. You can also write to the Stanford IRB, Stanford University, 3000 El Camino Real, Five Palo Alto Square, 4th Floor, Palo Alto, CA 94306 USA.<br><br>If you agree to participate, please proceed to the study tasks.</font></p>',
    // What should the button(s) say
    choices: ['Continue'],
    on_finish: function(data) {
        data.category = "irb" // Setting a custom category allows for easy filtering in the data analysis stage
    }
};

timeline.push(irb) // This adds the previous constant (irb) to the experimental timeline. =

// INSTRUCTIONS //

const instructions = {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: "In this experiment, you will read a series of sentences and will be asked to indicate the word which best completes each one.<br><br><strong>Please type the word 'is', 'are', or 'am' in the blank, then press ENTER when you're ready to move on to the next sentence.</strong> <br><br>If you're unsure about your choice, follow your first instinct.<br><br>When you're ready to begin, press the space bar.",
    choices: [" "],
    on_finish: function(data) {
        data.category = "instructions"
    }
};

timeline.push(instructions);


let tv_array = create_tv_array(trial_objects) // Import our stimuli, defined in a separate js file as "trial_objects", and convert them into object types that jsPsych can use
shuffleArray(tv_array) // Shuffle the array for randomization

// TRIALS //

const trials = {
    timeline: [ 
        {
            type: jsPsychCloze,
            button_text: "Submit",
            data: jsPsych.timelineVariable('data'), // make sure that the data from the stimuli object is imported
            text: jsPsych.timelineVariable('text'), // same with the text, which will define what is shown in the html
            allow_blanks: false, // Disallow participants to proceed without entering something
            check_answers: true, // Will display an error, defined in "mistake_fn", if the participant does not provide an allowed answer
            prompt: "Press enter to continue",
            mistake_fn: function (){ alert("Please ensure your answer is either 'is', 'are', or 'am'.") }, // define the error returned when participants do not provide an accepted answer
            on_finish: function(data) {
                jsPsych.setProgressBar((data.trial_index - 1) / (timeline.length + tv_array.length)); // Defines how far along the progress bar should be advanced at the end of the trial
                console.log("data.cond: "+data.cond)
            }
        }
    ],
    timeline_variables: tv_array, // Import the list of stimuli defined in 'let tv_array' above
    randomize_order: true // Randomize stimuli order. This is redundant in this because we already shuffled the array, but it's nice to have just in case.
}

timeline.push(trials)

const questionnaire = {
    type: jsPsychSurvey,
    pages: [ // each page will generate a unique question, defined by the 'type' parameter
        [
            {
                type: 'html', // Basic text to display at the top of the page
                prompt: "Please answer the following questions. All questions are optional. Scroll all the way to the bottom for the 'finish' button."
            },
            {
                type: 'multi-choice',
                prompt: 'Did you read the instructions and do you think you did the task correctly?', 
                name: 'correct', 
                options: ['Yes', 'No', 'I was confused']
            },
            {
                type: 'drop-down',
                prompt: 'Gender:',
                name: 'gender',
                options: ['Female', 'Male', 'Non-binary/Non-conforming', 'Other']
            },
            {
                type: 'text',
                prompt: 'Age:',
                name: 'age',
                textbox_columns: 10
            },
            {
                type: 'drop-down',
                prompt: 'Level of education:',
                name: 'education',
                options: ['Some high school', 'Graduated high school', 'Some college', 'Graduated college', 'Hold a higher degree']
            },
            {
                type: 'drop-down',
                prompt: 'In what US state did you spend the longest period of time during your childhood?',
                name: 'state',
                options: ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Washington DC', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'I was raised primarily outside of the United States']
            },
            {
                type: 'text',
                prompt: 'What city(ies) did you spend the longest period of time during your childhood? These cities should be located in the state you indicated on the previous question.',
                name: 'city',
                textbox_columns: 30,
                textbox_rows: 5
            },
            {
                type: 'multi-choice',
                prompt: "Is English your first language (i.e. did you start speaking English before age 5)?",
                name: 'language',
                options: ['Yes','No']
            },
            {
                type: 'text',
                prompt: "If you speak another language(s) fluently, please indicate the language(s) below.",
                name: 'other-language',
                textbox_columns: 20
            },
            {
                type: 'drop-down',
                prompt: 'Do you think the payment was fair?',
                name: 'payment',
                options: ['The payment was too low', 'The payment was fair']
            },
            {
                type: 'drop-down',
                prompt: 'Did you enjoy the experiment?',
                name: 'enjoy',
                options: ['Worse than the average experiment', 'An average experiment', 'Better than the average experiment']
            },
            {
                type: 'text',
                prompt: "Do you have any other comments about this experiment?",
                name: 'comments',
                textbox_columns: 30,
                textbox_rows: 4
            }
        ]
    ],
    on_finish: function(data) {
        data.category = "demographics"
    }
};
timeline.push(questionnaire)

// THANKS //

const thanks = {
    type: jsPsychHtmlButtonResponse,
    choices: ['Continue'],
    stimulus: "Thank you for your time! Please click 'Continue' and then wait a moment until you're directed back to Prolific.<br><br>",
    on_finish: function(data) {
        data.category = "thanks"
    }
}
timeline.push(thanks)

// FINAL FUNCTION CALL //

jsPsych.run(timeline)
