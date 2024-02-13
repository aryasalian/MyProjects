# Stock Price Predictor Folder Content Descriptions:


## _What is StockPricePredictor?_
The StockPricePredictor is a Recurrent Neural Network(RNN) based Machine Learning model that leverages historical data to predict Google's ([GOOG](https://g.co/kgs/aRrgPdg))
equity price fluctuations and trends. The model uses a time-step of 60 days to predict the stock price for the next day. Stock prices, being a type of time series data,
require ML models that feature back-propagation to use the feedback on the model's predictions to further develop the model. Hence, RNNs are the perfect choice for such
data analysis.

## Now onto each file...

### "Google_stock_price.ipynb"
This is where the code for the predictor is written. The data is pre-processed, reshaped, and then used as a training dataset for our RNN model.

### "StockPriceModel.h5"
This is an HDF5 file named StockPriceModel which stores the RNN model we calibrated for the Google stock price data. This copy is crucial for later use in cases of loss of original code. This makes the model shareable too.

### "Google_train_data.csv"
A comma-separated file storing some Google stock price data to be used as training data for the model in "Google_stock_price.ipynb".

### "Google_test_data.csv"
As the name suggests, it is a comma-separated file storing Google stock price data to test the model's predictions in "Google_stock_price.ipynb".

### "GOOG Price Predictor - Live Test - Sheet1.csv"
This is a comma-separated file that has live Google stock price data to test the model made in "Google_stock_price.ipynb".

### "GoogleStockPricePredictor - Sample Result.png"
This is an image of a graph that maps out the real equity price and the price predicted by our model.
