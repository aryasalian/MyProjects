$(document).ready(function () {
    let letterColors = []; // Array to store the letter colors

    $('#GuessedWordForm').on('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        const guessedWord = document.getElementById('guessedWord').value.trim();
        const LetterColorsForm = document.getElementById('LetterColorsForm');
        for (let i = 0; i < guessedWord.length; i++){
            letterColors[i] = "";           // initialize each value to an empty string so that "no options chosen" error is caught
        }

        // Show the letterColorsForm
        LetterColorsForm.style.display = "flex";

        // Clear any existing form elements
        LetterColorsForm.innerHTML = '';

        // Traverse over each letter of the guessed word
        for (let i = 0; i < guessedWord.length; i++) {
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
    });

    function createRadioButtonGroup(index) {
        const radioButtonGroup = document.createElement('div');
        radioButtonGroup.className = 'btn-group btn-group-toggle';
        radioButtonGroup.setAttribute('data-toggle', 'buttons');

        const colors = ['Green', 'Yellow', 'Grey'];
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
            label.textContent = color;

            const radioButton = document.createElement('input');
            radioButton.type = 'radio';
            radioButton.name = `options${index}`;
            radioButton.autocomplete = 'off';
            radioButton.value = color;

            // Add event listener to the radio button
            radioButton.addEventListener('click', function () {
                if (this.checked) {
                    letterColors[index] = this.value; // Update the LetterColors array
                    console.log(letterColors);
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
        if (letterColors.some(color => color !== 'Green' && color !== 'Yellow' && color !== 'Grey')) {
            // Alert if any button is not selected
            alert('Please select color for all letters.');
        } else {
            // Create an object with the guessed word and letter colors
            const guessedWord = document.getElementById('guessedWord').value.trim();
            const data = {
                guessedWord: guessedWord,
                letterColors: letterColors
            };
            console.log(data); // You can use this data object for further processing or sending to the backend API

            // Reset the form and LetterColors array
            $('#GuessedWordForm')[0].reset();
            letterColors = [];

            // Hide the letterColorsForm after submission
            LetterColorsForm.style.display = "none";
        }
    });
});




/*
$(document).ready(function() {
    
    let letterColors = []; // Array to store the letter colors

    $('#GuessedWordForm').on('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        const guessedWord = document.getElementById('guessedWord').value.trim();
        const LetterColorsForm = document.getElementById('LetterColorsForm');
        

        // Show the letterColorsForm
        $(LetterColorsForm).addClass('active1');

        // Clear any existing form elements
        LetterColorsForm.innerHTML = '';

        // Traverse over each letter of the guessed word
        for (let i = 0; i < guessedWord.length; i++) {
            const letter = guessedWord[i];

            // Create a label for the letter and color input
            const label = document.createElement('label');
            label.textContent = `Enter color for letter '${letter}': `;
            label.style.padding = '5px';

            // Create the green button
            const greenButton = document.createElement('button');
            greenButton.type = 'button';
            greenButton.className = 'btn btn-outline-success btn-sm'; // Use Bootstrap classes to style the button
            greenButton.textContent = 'Green'; // Set the text of the button to the letter

            // Add click event listener to the green button
            $(greenButton).on('click', function () {
                // Toggle the selected state of the button when clicked
                $(this).toggleClass('active'); // Use Bootstrap class to style the active button
                const letterIndex = $(this).parent().index(); // Get the index of the button's parent (div) element
                letterColors[letterIndex] = $(this).hasClass('active') ? 'Green' : ''; // Update the LetterColors array
            });

            // Append the label and green button to the form
            const quesContainer = document.createElement('div');
            quesContainer.append(label);
            quesContainer.append(greenButton);
            $('#LetterColorsForm').append(quesContainer);
        }

        // Create a button to submit the letter colors
        const submitButton = document.createElement('button');
        submitButton.type = 'submit';
        submitButton.textContent = 'Submit Letter Colors';
        $('#LetterColorsForm').append(submitButton);
    });

    $('#LetterColorsForm').on('submit', function (event) {
        event.preventDefault(); // Prevent Form Submission

        // Check if all green buttons are selected
        if (letterColors.some(color => color !== 'Green' && color !== 'Yellow' && color !== 'Grey')) {
            // Alert if any button is not selected
            alert('Please select color for all letters.');
        } else {
            // Create an object with the guessed word and letter colors
            const guessedWord = document.getElementById('guessedWord').value.trim();
            const data = {
                guessedWord: guessedWord,
                letterColors: letterColors
            };
            console.log(data); // You can use this data object for further processing or sending to the backend API

            // Reset the form and LetterColors array
            $('#GuessedWordForm')[0].reset();
            letterColors = [];

            // Hide the letterColorsForm after submission
            $('#LetterColorsForm').removeClass('active1');
        }
    });
    */

    /* THIS IS BOOTSTRAP FOR A RADIO BUTTON GROUP(WILL BE USED TO TAKE COLOR INPUTS!!)
    <div class="btn-group btn-group-toggle" data-toggle="buttons">
  <label class="btn btn-secondary active">
    <input type="radio" name="options" id="option1" autocomplete="off" checked> Green
  </label>
  <label class="btn btn-secondary">
    <input type="radio" name="options" id="option2" autocomplete="off"> Yellow
  </label>
  <label class="btn btn-secondary">
    <input type="radio" name="options" id="option3" autocomplete="off"> Grey
  </label>
</div>
*/


    /*
        // Send the data as JSON to the backend API
        fetch('/wordle/solve', {
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
    */

    