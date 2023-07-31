import spark.Spark;
import com.google.gson.Gson;
import java.util.*;

class WordleSolverAPI {
    
    private Wordle_Solver wordleSolver;

    public WordleSolverAPI() {
        wordleSolver = new Wordle_Solver();
        wordleSolver.extract_words();
    }

    private static class GuessRequest {
        String guessedWord;
        String letterColors;
    }

    private static class GuessResponse {
        ArrayList<String> validWords;
        // Add any other fields you want to include in the response
    }
    
    public static void main(String[] args) {
        WordleSolverAPI api = new WordleSolverAPI();
        api.setupRoutes();
    }

    private void setupRoutes() {
        Spark.port(8080); // Use the desired port number

        Spark.post("/wordle/solve", (req, res) -> {
            Gson gson = new Gson();
            GuessRequest guessRequest = gson.fromJson(req.body(), GuessRequest.class);

            String guessedWord = guessRequest.guessedWord;
            String letterColors = guessRequest.letterColors;

            // Process the inputs and call the Wordle Solver methods
            // You need to parse the input strings and pass them to the solver methods

            // Assuming your Wordle_Solver methods return the result as a list of valid words
            ArrayList<String> validWords = wordleSolver.suggest_all_valid_words();

            // Create the response object
            GuessResponse response = new GuessResponse();
            response.validWords = validWords;

            // Convert the response to JSON and send it as the response
            String jsonResponse = gson.toJson(response);
            res.type("application/json");
            return jsonResponse;
        });
    }
}
