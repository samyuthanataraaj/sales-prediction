import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# 1. Load data
df = pd.read_csv(r"D:\tamilanskills\project1\dataset.csv")   # Replace with your file name

# 2. Preprocess
df['order_date'] = pd.to_datetime(df['order_date'])
df['revenue'] = df['quantity'] * df['price']   # calculate revenue
df = df.dropna()

# Aggregate daily sales
sales = df.groupby('order_date')['revenue'].sum().reset_index()

# 3. Feature Engineering
sales['year'] = sales['order_date'].dt.year
sales['month'] = sales['order_date'].dt.month
sales['day'] = sales['order_date'].dt.day
sales['dayofweek'] = sales['order_date'].dt.dayofweek

X = sales[['year', 'month', 'day', 'dayofweek']]
y = sales['revenue']

# 4. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Predictions
y_pred = model.predict(X_test)

# 6. Evaluation
print("📊 Model Performance:")
print("R2 Score:", r2_score(y_test, y_pred))
print("MSE:", mean_squared_error(y_test, y_pred))

# 7. Tabular comparison of actual vs predicted
results = pd.DataFrame({
    'date': sales['order_date'].iloc[len(X_train):].values,
    'actual_sales': y_test.values,
    'predicted_sales': y_pred
})
print("\n📋 Actual vs Predicted Sales:")
print(results.head(15))  # show first 15 rows

# 8. Plot actual vs predicted
plt.figure(figsize=(12,6))
plt.plot(results['date'], results['actual_sales'], label='Actual Sales', marker='o')
plt.plot(results['date'], results['predicted_sales'], label='Predicted Sales', marker='x')
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.title("Actual vs Predicted Sales")
plt.legend()
plt.show()

# 9. Forecast for future dates
future_dates = pd.date_range(start=sales['order_date'].max(), periods=10, freq='D')  # next 10 days
future_df = pd.DataFrame({
    'year': future_dates.year,
    'month': future_dates.month,
    'day': future_dates.day,
    'dayofweek': future_dates.dayofweek
})
future_predictions = model.predict(future_df)

forecast = pd.DataFrame({'date': future_dates, 'predicted_revenue': future_predictions})
print("\n🔮 Forecast for Upcoming Periods:")
print(forecast)
