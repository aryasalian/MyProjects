# Wordle-Solver Folder Content Descriptions:


## _What is WordleSolver?_
The WordleSolver is a simple Java application that assists you with the **NY Times' famous [Wordle](https://www.nytimes.com/games/wordle/index.html) puzzle**. Just input the first word
you guessed and the color of each of its letters and let WordleSolver suggest you the next word. _WordleSolver guarantees you to always get the answer_ and in most cases, **even 
performs better than another human!** So go ahead and bet that friend you lost to at Wordle last time...with WordleSolver, the tables will turn around this time :)

## Now onto each file...

### "Wordle-Solver.java"
This is the file you can run in your IDE to call your trusted buddy WordleSolver. This is where all the code is.

### "Wordle-SolverAPI.java"
This is the back-end API that connects the web server to the main code and logic: Wordle-Solver.java.

### "main.js"
This is the Javascript and jQuery code that helps the website get functionality by accepting user inputs and displaying corresponding answers.

### "main.css"
This is the stylesheet used for designing the website; as of now very rudimentary.

### "index.html"
This is the skeleton of the website made with HTML where the Javascript elements are added in.

### "solutions.csv"
A necessary file that WordleSolver needs to give you the right solution. It contains the `La` words dictionary which is basically a dictionary/word list of all words that appear as 
solutions in the puzzle. This is **2,315 words long!** But you don't need to worry about that, WordleSolver cuts that to nothing in no time ;)

### "allwords.csv"
ANOTHER necessary file which WordleSolver needs to give you the right solution (yes, WordleSolver needs lotta assistance too). This one contains all the `La` words AND a new dictionary
called `Ta`: a dictionary/word list of all words that the puzzle considers as acceptable guesses but never chooses as solutions. That means _"allwords.csv"_ contains all those words that
Wordle accepts as valid 5-letter words of the English dictionary. This is **10,657 words long!**

### "/.vscode folder"
WordleSolver was originally developed in VSCode and hence has this birthmark: a .JSON file storing the configurations of how the VSCode terminal needs to show the output.
_This can be ignored._

