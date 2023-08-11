import static spark.Spark.*;
import com.google.gson.Gson;

import java.io.Console;
import java.util.*;

public class WordleSolverAPI {
    
    private Wordle_Solver wordleSolver;

    private static class GuessRequest {
        String guessedWord;
        String[] letterColors;
    }

    private static class GuessResponse {
        ArrayList<String> all_valid_words;
        String valid_word;
        boolean word_found;
    }
    
    public static void main(String[] args) {

        port(8080); // Use the desired port number
        enableCORS("http://127.0.0.1:3000", "*", "*");
        WordleSolverAPI api = new WordleSolverAPI();
        api.setupRoutes();
        awaitInitialization();
    }

    // Helper method to enable CORS
    private static void enableCORS(final String origin, final String methods, final String headers) {
        options("/*", (request, response) -> {

            String accessControlRequestOrigins = request.headers("Access-Control-Request-Origin");
            if (accessControlRequestOrigins != null){
                response.header("Access-Control-Allow-Origin", accessControlRequestOrigins);
            }

            String accessControlRequestHeaders = request.headers("Access-Control-Request-Headers");
            if (accessControlRequestHeaders != null) {
                response.header("Access-Control-Allow-Headers", accessControlRequestHeaders);
            }

            String accessControlRequestMethod = request.headers("Access-Control-Request-Method");
            if (accessControlRequestMethod != null) {
                response.header("Access-Control-Allow-Methods", accessControlRequestMethod);
            }

            return "OK";
        });

        before((request, response) -> {
            response.header("Access-Control-Allow-Origin", origin);
            response.header("Access-Control-Allow-Credentials", "true");
            response.header("Access-Control-Allow-Headers", headers);
            response.header("Access-Control-Allow-Methods", methods);
        });
    }

    private void setupRoutes() {

        // Test for Website to Backend Server connectivity
        /*
        get("/hello/world", (req, res) -> {
            String name = req.queryParams("name");
            res.body("Hello "+name+"!");
            return res.body();
        });
        */

        get("/wordle/initialize_WordleSolver", (req, res) -> {
            wordleSolver = new Wordle_Solver();
            wordleSolver.extract_words();
            res.type("text/plain");
            return "WordleSolver initialized!";
        });

        get("/wordle/get_valid_guesses", (req, res) -> {
            Gson gson = new Gson();
            String valid_guesses = gson.toJson(wordleSolver.accepted_guess_words);
            res.type("application/json");
            return valid_guesses;
        });

        post("/wordle/solve", (req, res) -> {

            // Deserializing the JSON request body into a custom-defined GuessRequest Object
            Gson gson = new Gson();
            GuessRequest guessRequest = gson.fromJson(req.body(), GuessRequest.class);

            // Initializing input variables to inputs received from the request body
            String guessedWord = guessRequest.guessedWord;
            String[] letterColors = guessRequest.letterColors;

            // Call update_CharLists() for each letter of the word
            for (int index = 0; index < 5; index++) {
                char letter = guessedWord.charAt(index);
                char letterColor = letterColors[index].charAt(0);
                wordleSolver.update_CharLists(letter, letterColor, index);
            }

            // Populate GuessResponse object with output values calculated by WordleSolver
            GuessResponse guessResponse = new GuessResponse();
            guessResponse.all_valid_words = wordleSolver.suggest_all_valid_words();
            if (guessResponse.all_valid_words.size() > 1) {
                guessResponse.word_found = false;
                guessResponse.valid_word = wordleSolver.suggest_valid_word();
            } else if (guessResponse.all_valid_words.size() == 1) {
                guessResponse.word_found = true;
                guessResponse.valid_word = guessResponse.all_valid_words.get(0);
            } else {
                guessResponse.word_found = false;
                guessResponse.valid_word = "ERROR: NO SUCH WORD"; // Error message should be: "Something went wrong...Could we try again?"
            }

            // Converting the response to JSON
            String jsonResponse = gson.toJson(guessResponse, GuessResponse.class);

            // Defining HTTP response resource's type
            res.type("application/json");
            return jsonResponse;
        });
    }
}
