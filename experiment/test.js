// getSolutions(text) {
//     const solutions = [];
//     const elements = text.split("%");
//     for (let i = 0; i < elements.length; i++) {
//         if (i % 2 == 1) {
//             solutions.push(elements[i].trim());
//         }
//     }
//     return solutions;
// }


let text = "This is a %stupid,fucking% test";

const solutions = [];
const elements = text.split("%");
for (let i = 0; i < elements.length; i++) {
    if (i % 2 == 1) {
        const words = elements[i].split(",");
        words.forEach(word => {
            solutions.push(word.trim());
        });
    }
}

console.log(solutions);
