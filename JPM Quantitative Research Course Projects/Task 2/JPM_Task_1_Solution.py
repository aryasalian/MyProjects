import pandas as pd
from datetime import datetime
import pmdarima as pm

data = pd.read_csv('/Users/aryasalian/MyProjects-github/JPM Quantitative Research Course Projects/Task 2/Nat_Gas OG copy.csv', names = ['Dates','Prices'], header = 0, parse_dates=['Dates'], index_col= 'Dates')

SARIMA_model = pm.auto_arima(data["Prices"], start_p=1, start_q=1, test='adf', max_p=3, max_q=3, m=12, #12 is the frequncy of the cycle
                            start_P=0, seasonal=True, #set to seasonal
                            start_Q=0, d=None, D=1, #order of the seasonal differencing
                            trace=False, error_action='ignore', suppress_warnings=True, stepwise=True)

def Task_1_Solution(input_date):
    # Solution to TASK 1 of the JPM Quantitative Research Course

    if isinstance(input_date, datetime):
        input_month = input_date.month
        input_year = input_date.year
    elif isinstance(input_date, str):
        try:
            parsed_date = datetime.strptime(input_date, '%Y-%m-%d')
            input_month = parsed_date.month
            input_year = parsed_date.year
        except ValueError:
            print('Invalid date format!')
    else:
        print('Invalid input type!')

    forecasted_values = SARIMA_model.predict(n_periods=12, return_conf_int=False)
    past_estimates_by_model = SARIMA_model.predict_in_sample(start = 1)
    predictions = pd.concat([past_estimates_by_model, forecasted_values])
    predictions.index = predictions.index.to_period('M')
    for prediction_index in predictions.index:
        if prediction_index.year == input_year and prediction_index.month == input_month:
            return predictions[prediction_index]
    


### Test ###
Task_1_Solution("2023-01-09")
