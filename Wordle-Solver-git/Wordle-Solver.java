import java.io.*;
import java.util.*;

class Wordle_Solver{

    ArrayList<String> accepted_guess_words = new ArrayList<String>();       //a list of all the words which Wordle accepts as valid word for guessing
    ArrayList<String> target_words = new ArrayList<String>();       //a list of words which Wordle chooses as its solution word
    ArrayList<String> valid_words = new ArrayList<String>();        //a list that keeps updating itself with all words that are valid according to the recent search criteria
    String UnusedCharList=  "abcdefghijklmnopqrstuvwxyz";       //String which stores the list of characters that havent been used yet/should be included in the search criteria
    HashMap<Character, boolean[]> YellowCharList = new HashMap<Character, boolean[]>(); //key:value pair stores letter and corresponding indices where it shouldn't be
    HashMap<Character, boolean[]> GreenCharList = new HashMap<Character, boolean[]>(); //key:value pair stores letter and corresponding indices where it should be

    /**
     * extracts all the target/solution words from the .csv file and stores it in a global ArrayList<String> object
     */
    private void extract_words(){

        try{
        File target_word_file = new File("/Users/testing/MyProjects-github/Wordle-Solver-git/solutions.csv");
        BufferedReader br = new BufferedReader(new FileReader(target_word_file));
        String line = "";

        while((line = br.readLine())!=null){
            String[] words = line.split("[,]");
            for(String word : words){
                word = word.trim();
                word = word.substring(1, word.length()-1);
                target_words.add(word);
            }
        }
        valid_words = (ArrayList<String>)target_words.clone();
        br.close();

        File accepted_guess_words_file = new File("/Users/testing/MyProjects-github/Wordle-Solver-git/allwords.csv");
        BufferedReader br1 = new BufferedReader(new FileReader(accepted_guess_words_file));
        line = "";  //repurposing old String variable made in this function

        while((line = br1.readLine())!=null){
            String[] words = line.split("[,]");
            for(String word : words){
                word = word.trim();
                word = word.substring(1, word.length()-1);
                accepted_guess_words.add(word);
            }
        }
        br1.close();

        } catch (FileNotFoundException e) {
            System.out.println("Please ensure both .csv files are in the same directory and folder as this .java file\n"+e);
        } catch (Exception e) {
            System.out.println(e);
        }

    }

    private void update_CharLists(char letter, char letterColor, int index){
        
        if(letterColor=='B'||letterColor=='b'){       //Letters which aren't in the target/solution word
            if(YellowCharList.containsKey(letter)){
                boolean[] temp = YellowCharList.get(letter);
                temp[index] = true;
                YellowCharList.put(letter, temp);
            }
            else{
                UnusedCharList = UnusedCharList.replace(letter, '\u0000');
            }
        }
        else if(letterColor=='Y'||letterColor=='y'){      //Letters which are in the target/solution word but not at that position


            if(!(YellowCharList.containsKey(letter))){
                boolean[] temp = new boolean[5];
                temp[index] = true;                         //true if it should not be at that position
                YellowCharList.put(letter, temp);
            }
            else{
                boolean[] temp = YellowCharList.get(letter);
                temp[index] = true;
                YellowCharList.put(letter, temp);
            }
            
        }
        else if(letterColor=='G'||letterColor=='g'){      //Letters which are in the target/solution word and at that position

            for(char key : YellowCharList.keySet()){
                if(key!=letter){
                    boolean[] temp  = YellowCharList.get(key);
                    temp[index] = true;                         //since this position will be reserved for this green letter and no other letter can come here(narrows down search)
                    YellowCharList.put(key, temp);
                }
            }

            if(!(GreenCharList.containsKey(letter))){
                boolean[] temp = new boolean[5];
                temp[index] = true;                         //true if it is supposed to be at that posiiton            
                GreenCharList.put(letter, temp);     
            }
            else{
                boolean[] temp = GreenCharList.get(letter);
                temp[index] = true;
                GreenCharList.put(letter, temp);
            }

        }

    }
    
    private boolean black_criteria(String word){
        
        int index = -1;
        for(char c : word.toCharArray()){
            index++;
            if(!(UnusedCharList.contains(c+""))){       //if a letter of the word is not present in UnusedCharList, returns false. I do not want it to return false if it is a green letter and is at its correct index
                if(GreenCharList.containsKey(c) && GreenCharList.get(c)[index]==true){      //when letter is green and black, let this letter slide but only if its at the right position
                    continue;
                }
                return false;       //word does not meet criteria
            }
        }
        return true;        //word meets criteria

    }

    private boolean yellow_criteria(String word){

         for(char key : YellowCharList.keySet()){
            if(!(word.contains(key+""))){
                return false;       //all yellow letters should exist in the word
            }
            else{
                for(int i = 0; i < 5; i++){
                    if(YellowCharList.get(key)[i] == true && word.charAt(i) == key){
                        return false;       //all yellow letters should not exist at certain indices and should be present elsewhere
                    }
                }
            }
        }
        return true;        //word meets criteria

    }

    private boolean green_criteria(String word){

        for(char key : GreenCharList.keySet()){
            if(!(word.contains(key+""))){
                return false;       //all green letters should exist in the word
            }
            else{
                for(int i = 0; i < 5; i++){
                    if(GreenCharList.get(key)[i] == true && word.charAt(i) != key){
                        return false;       //all green letters should exist at certain indices and can be present elsewhere too
                    }
                }
            }
        }
        return true;        //word meets criteria

    }

    private boolean all_criterias(String word){

        return black_criteria(word) && yellow_criteria(word) && green_criteria(word);  //word should meet all criterias

    }

    private ArrayList<String> suggest_all_valid_words(){     //suggests all valid words as an ArrayList

        ArrayList<String> temp = (ArrayList<String>)valid_words.clone();
        valid_words.clear();
        for(String word : temp){
            if(all_criterias(word)==true){
                valid_words.add(word);
            }
        }
        return valid_words;

    }

    private String suggest_valid_word(){          //suggests one random valid word

        Random rand = new Random();
        return valid_words.get(rand.nextInt(valid_words.size()));
    }

    public static void main(String[] args) {
        
        boolean wrong_answer;
        Scanner sc = new Scanner(System.in);
        do {
            Wordle_Solver ob = new Wordle_Solver();
            wrong_answer = false;
            ob.extract_words();

        //We will ask user to input the word he just guessed. Then we will go over every character in the word and ask if it was green, yellow or black. 
        //Then we'll call updateCharLists() for each character, update the charLists and since it is in order(0 --> 4), we'll have indices of each letter too.
        //After that we'll call a method to suggest words depending on the charList results.
        //Handle cases where letters are repeated(once a letter is green or yellow, do not remove from unused list to make sure double letter words are included)

        String guessed_word = "";
        char c = '\u0000';
        boolean not_5letter_or_valid;
        boolean wrong_colour_name;
        String letterColor = "";
        System.out.println("\n\n\nThe colour of letters will be either \"GREEN\", \"YELLOW\" or \"BLACK\". The colour names are not case-sensitive, only spelling-sensitive. Type accurately.");
        for(int i = 0; i < 6; i++){

            do {
                System.out.printf("Enter the 5-letter word guessed in turn %d: ", (i+1));
                guessed_word = sc.nextLine();
                guessed_word = guessed_word.toLowerCase();
                not_5letter_or_valid = false;

                if(guessed_word.length()!=5){
                    System.out.println("\nNot a 5-letter word!\n");
                    not_5letter_or_valid = true;
                } 
                else if(!ob.accepted_guess_words.contains(guessed_word)){
                    System.out.println("\nEnter a valid/real word please! No made-up words allowed!\n");
                    not_5letter_or_valid = true;
                }

            } while (not_5letter_or_valid);
            

            for(int j = 0; j < 5; j++){

                do {
                    c = guessed_word.charAt(j);
                    System.out.printf("Enter the color of the #%d letter(%c): ", (j+1), c);
                    letterColor = sc.nextLine();
                    wrong_colour_name = false;

                    if(letterColor.equalsIgnoreCase("BLACK")){
                        ob.update_CharLists(c, 'B', j);
                    }
                    else if(letterColor.equalsIgnoreCase("YELLOW")){
                        ob.update_CharLists(c, 'Y', j);
                    }
                    else if(letterColor.equalsIgnoreCase("GREEN")){
                        ob.update_CharLists(c, 'G', j);
                    }
                    else{
                        System.out.println("Choose either \"GREEN\", \"YELLOW\" or \"BLACK\" only!");
                        wrong_colour_name = true;
                    }
                } while (wrong_colour_name);
                
            }

            //Now that charlists were updated, we do necessary checks on the target word list and output filtered list
            ArrayList<String> all_valid_words = ob.suggest_all_valid_words();
            if(all_valid_words.size()==1){
                boolean uncertain;
                boolean decisive_answer = false;
                do {
                    uncertain = false;
                    System.out.printf("\nIs \"%s\" the word you were looking for?\n", all_valid_words.get(0));
                    System.out.print("Please enter 'yes' or 'no': ");
                    String response = sc.nextLine();
                    if(response.equalsIgnoreCase("yes")){
                        System.out.println("\nGlad I could help you!\n");
                        decisive_answer = true;
                        break;
                    }
                    else if(response.equalsIgnoreCase("no")){
                        System.out.println("\nSorry about that, can I try again?\n");
                        wrong_answer = true;
                        decisive_answer = true;
                        break;
                    }
                    else{
                        System.out.println("\nPlease say either yes or no! -_-\n");
                        uncertain = true;
                    }
                } while (uncertain);
                if(decisive_answer){
                    break;
                }
            }
            else{
                System.out.print("All these words could work: "+all_valid_words+"\n\n");

                //A random valid word can be chosen out of this large list to try:
                System.out.printf("Why not try \"%s\"?\n\n", ob.suggest_valid_word());
            }

        }
        } while (wrong_answer);
        sc.close();
        System.exit(0);
    }
}
