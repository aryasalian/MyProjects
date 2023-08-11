$(document).ready(function () {
    let letterColors = []; // Array to store the letter colors\
    var valid_guesses = []; // Array to store all valid guesses the user can make
    const apiDomainAndPort = "http://localhost:8080"; // Backend server general URL(route not included)

    // Initialize WordleSolver class in WordleSolverAPI to ensure new WordleSolver object for each session
    fetch (apiDomainAndPort+"/wordle/initialize_WordleSolver", {
        method: 'GET'
    })
    .then(response => response.text())
    .then(response => {
        console.log(response);
        // Get list of words that are accepted as valid guesses by Wordle after WordleSolver is initialized
        return fetch (apiDomainAndPort+"/wordle/get_valid_guesses", {method: 'GET'}); 
    })
    .then(response => response.json())
    .then(guesses => {
        valid_guesses = guesses;
    })
    .catch(error => {
        console.error("Error:", error);
    })

    // User submits word guessed in this turn
    $('#GuessedWordForm').on('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        if (!(valid_guesses.includes(document.getElementById('guessedWord').value.trim()))) {
            alert('Please enter a valid 5-letter word that you\'ve guessed in the official Wordle website!');
        }
        else {
            const guessedWord = document.getElementById('guessedWord').value.trim();
            const LetterColorsForm = document.getElementById('LetterColorsForm');
            for (let i = 0; i < guessedWord.length; i++){
                letterColors[i] = "";           // initialize each value to an empty string so that "no options chosen" error is caught
            }
    
            // Create element of LetterColorsForm only if it wasn't visible before clicking submit
            //if (LetterColorsForm.style.display == "none") {
                // Show the letterColorsForm
                LetterColorsForm.style.display = "flex";

                // Clear any existing form elements
                LetterColorsForm.innerHTML = '';

                // Traverse over each letter of the guessed word
                for (let i = 0; i < 5; i++) {
                    const letter = guessedWord[i];

                    // Create a label for the letter and color input
                    const label = document.createElement('label');
                    label.textContent = `Enter color for letter '${letter}': `;
                    label.style.padding = '5px';

                    // Create the radio button group
                    const radioButtonGroup = createRadioButtonGroup(i);

                    // Append the label and radio button group to the form
                    const quesContainer = document.createElement('div');
                    quesContainer.append(label);
                    quesContainer.append(radioButtonGroup);
                    $('#LetterColorsForm').append(quesContainer);
                }

                // Create a button to submit the letter colors
                const submitButton = document.createElement('button');
                submitButton.type = 'submit';
                submitButton.textContent = 'Submit Letter Colors';
                $('#LetterColorsForm').append(submitButton);

                // Create a button to start afresh
                const restartButton = document.createElement('button');
                restartButton.type = 'reset';
                restartButton.textContent = 'Wanna start afresh?';
                $('#LetterColorsForm').append(restartButton);

                restartButton.addEventListener('click', function () {
                    $('body').load(window.location.href);
                });
            //}
        }
    });

    function createRadioButtonGroup(index) {
        const radioButtonGroup = document.createElement('div');
        radioButtonGroup.className = 'btn-group btn-group-toggle';
        radioButtonGroup.setAttribute('data-toggle', 'buttons');

        const colors = ['Green', 'Yellow', 'Black'];
        colors.forEach((color, i) => {
            const label = document.createElement('label');
            if(i==0){
                label.className = 'btn btn-outline-success';
            }
            else if(i==1){
                label.className = 'btn btn-outline-warning';
            }
            else{
                label.className = 'btn btn-outline-secondary';
            }

            if(color === 'Black'){
                label.textContent = 'Gray';
            }
            else{
                label.textContent = color;
            }

            const radioButton = document.createElement('input');
            radioButton.type = 'radio';
            radioButton.name = `options${index}`;
            radioButton.autocomplete = 'off';
            radioButton.value = color;

            // Add event listener to the radio button
            radioButton.addEventListener('click', function () {
                if (this.checked) {
                    letterColors[index] = this.value; // Update the LetterColors array
                    //console.log(letterColors);
                }
            });

            label.appendChild(radioButton);
            radioButtonGroup.appendChild(label);
        });

        return radioButtonGroup;
    }

    $('#LetterColorsForm').on('submit', function (event) {
        event.preventDefault(); // Prevent Form Submission

        // Check if all green buttons are selected
        if (letterColors.some(color => color !== 'Green' && color !== 'Yellow' && color !== 'Black')) {
            // Alert if any button is not selected
            alert('Please select color for all letters!');
        } else {
            // Creating an object with the guessed word and letter colors
            const guessedWord = document.getElementById('guessedWord').value.trim();
            const data = {
                guessedWord: guessedWord,
                letterColors: letterColors
            };

            // Resetting the form and LetterColors array
            $('#GuessedWordForm')[0].reset();
            letterColors = [];
            
            // Testing if input value successfully accepted
            //console.log(data);

            // Hiding the letterColorsForm after submission
            LetterColorsForm.style.display = "none";

            // Send the data as JSON to the backend API
            fetch(apiDomainAndPort+"/wordle/solve", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                // Handle the API response here (e.g., display the suggestions on the page)
                console.log(result);
            })
            .catch(error => {
                // Handle errors if the API request fails
                console.error('Error:', error);
            });
        }
    });
});
