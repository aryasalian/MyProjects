document.getElementById('wordleForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
  
    const guessedWord = document.getElementById('guessedWord').value;
    const letterColors = document.getElementById('letterColors').value;
  
    // Create an object with the guessed word and letter colors
    const data = {
      guessedWord: guessedWord,
      letterColors: letterColors
    };
  
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
  });