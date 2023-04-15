# Smoke Forecasting with Time Series Analysis

This project aims to forecast smoke levels using time series analysis techniques on data collected from IoT sensors. I use a SARIMA (Seasonal Autoregressive Integrated Moving Average) model to predict smoke levels for the next 2 years based on historical data.

## Data
The data used in this project consists of smoke levels measured by IoT sensors at regular intervals over a period of 5 years from January 2017 to December 2022. The data has a monthly frequency, and consists of 12 observations in the test set that are used to evaluate the accuracy of the model's predictions.

## Model
We fit a SARIMA model to the historical data, with an order of (1, 1, 1) and a seasonal order of (1, 1, 1, 12). This model takes into account the trend and seasonality in the data, as well as the autocorrelation between successive observations. We use the statsmodels Python package to implement the SARIMA model.

## results
The SARIMA model provides a reasonable forecast for the next 2 years of smoke levels. The model captures the general trend and seasonality of the data, and the 95% confidence intervals of the forecasts are reasonably wide, indicating that the model accounts for the uncertainty in the future predictions.

However, there are some areas where the model's forecasts deviate from the actual data. Additionally, the model's forecasts for some of the peaks and troughs in the actual data are not as high or low as the actual values.

## Conclusion
Overall, the SARIMA model provides a reasonable forecast for smoke levels based on historical data collected from IoT sensors. The model can be used to provide early warnings for potential smoke hazards, and can help authorities take preventive measures to reduce the risk of fires. However, further improvements to the model may be necessary to improve the accuracy of the forecasts.