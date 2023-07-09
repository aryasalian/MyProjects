# AIFactChecker Folder Content Descriptions:


## _What is AIFactChecker?_
The AIFactChecker is a Machine-Learning based app which tells a user if a given piece of news entered by the user is real or fake. It is integrated with WhatsApp using the WhatsApp API 
provider, *[Twilio](https://www.twilio.com/en-us)* and gathers the news dating three months(max limit allowed in free use) back from the API provider, *[NewsAPI](https://newsapi.org/)*. 
It also exists as a website and was on the AWS Cloud for a while until it was removed in 2023. The Machine Learning model used for this project is called a 
**[Passive-Aggressive Classifier model](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveClassifier.html)** which is meant to be used as an Online 
Machine Learning model, hence perfect for this situation where the training data keeps updating every day.

## Now onto each file...

### "Final.py"
It is a culmination of all code written in other files and handles the website side of the program i.e. calculating and displaying the output on the website. Flask libraries are used since
they help with Web Development for light code (ours is pretty light). Cross-origin resource sharing (CORS) is also used to ensure security since it lets servers specify any other hosts 
from which a browser should permit the loading of content.

### "Model.py"
Holds the code for our model which uses a TF-IDF Vectorizer to scale words into computable values by our model(the TF-IDF Vectorizer helps us find relevant words in a document and hence
help us assign similar vectors to documents with similar relevant words). These vectorized values of the data are then fed into our Passive Aggressive Classifier model found in the 
[scikit-learn machine learning libraries](https://scikit-learn.org/stable/). Our model then returns the label value as accurately as possible to the real label of the input(here, the news 
inputted by the user).

### "News.csv"
A comma-separated file storing some sample news to be treated like training data for the model in "Test.py" when the connection to NewsAPI is not established.

### "Test.py"
As the name suggests, it is a sample program written to test our model on sample data in "News.csv" when the connection to NewsAPI is not established.

### "Veritas.py"
This is the final code handling the WhatsApp side of the program i.e. calculating and displaying the output on WhatsApp.

