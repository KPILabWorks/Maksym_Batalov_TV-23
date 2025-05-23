import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras.callbacks import EarlyStopping

class AirAlertDurationPredictor:
    def __init__(self, csv_path='air_alerts.csv'):
        self.df = pd.read_csv(csv_path)
        self._feature_engineering()
        self._prepare_data()
        self._build_model()
        self._train_model()

    def _feature_engineering(self):
        df = self.df
        df['start'] = pd.to_datetime(df['start'], format='%H:%M')
        df['hour'] = df['start'].dt.hour
        df['minute'] = df['start'].dt.minute
        df['date'] = pd.to_datetime(df['date'])
        df['weekday'] = df['date'].dt.weekday
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['is_weekend'] = df['is_weekend']
        df['alert_duration_category'] = df['alert_duration_category']
        df['season'] = df['season']
        df['time_of_day'] = pd.cut(
            df['hour'], bins=[0, 6, 12, 18, 24],
            labels=['Night', 'Morning', 'Afternoon', 'Evening'], right=False
        )
        df['duration_bins'] = pd.cut(
            df['duration'], bins=[0, 30, 60, 120, 240, 480, 1000],
            labels=[1, 2, 3, 4, 5, 6], right=False
        )
        df['hour_weekday_interaction'] = df['hour'] * df['weekday']
        df = pd.get_dummies(df, columns=['time_of_day'], drop_first=True)
        # Remove outliers in 'duration'
        q1 = df['duration'].quantile(0.25)
        q3 = df['duration'].quantile(0.75)
        iqr = q3 - q1
        df = df[(df['duration'] >= q1 - 1.5 * iqr) & (df['duration'] <= q3 + 1.5 * iqr)]
        self.df = df

    def _prepare_data(self):
        df = self.df
        self.feature_columns = [
            'hour', 'minute', 'weekday', 'month', 'day', 'is_weekend',
            'alert_duration_category', 'season', 'hour_weekday_interaction', 'duration_bins'
        ] + [col for col in df.columns if 'time_of_day_' in col]
        self.X = df[self.feature_columns]
        self.y = df['duration']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

    def _build_model(self):
        self.model = Sequential([
            Dense(128, activation='relu', input_shape=(self.X_train_scaled.shape[1],)),
            BatchNormalization(),
            Dropout(0.3),
            Dense(64, activation='relu'),
            BatchNormalization(),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')

    def _train_model(self):
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        self.model.fit(
            self.X_train_scaled, self.y_train,
            epochs=200, batch_size=32, validation_split=0.2,
            callbacks=[early_stopping], verbose=0
        )
        loss = self.model.evaluate(self.X_test_scaled, self.y_test, verbose=0)
        self.last_mse = loss  # Store for UI
        print(f'Test MSE: {loss:.2f}')

    def predict(self, dt=None):
        if dt is None:
            dt = datetime.now()
        hour = dt.hour
        minute = dt.minute
        weekday = dt.weekday()
        month = dt.month
        day = dt.day
        is_weekend = 1 if weekday >= 5 else 0
        # Use mode for categorical/numeric features
        alert_duration_category = int(self.df['alert_duration_category'].mode()[0])
        season = int(self.df['season'].mode()[0])
        duration_bins = int(self.df['duration_bins'].mode()[0])
        hour_weekday_interaction = hour * weekday
        # One-hot encoding for time_of_day
        time_of_day_morning = 1 if 6 <= hour < 12 else 0
        time_of_day_afternoon = 1 if 12 <= hour < 18 else 0
        time_of_day_evening = 1 if 18 <= hour < 24 else 0
        input_dict = {
            'hour': hour,
            'minute': minute,
            'weekday': weekday,
            'month': month,
            'day': day,
            'is_weekend': is_weekend,
            'alert_duration_category': alert_duration_category,
            'season': season,
            'hour_weekday_interaction': hour_weekday_interaction,
            'duration_bins': duration_bins,
            'time_of_day_Morning': time_of_day_morning,
            'time_of_day_Afternoon': time_of_day_afternoon,
            'time_of_day_Evening': time_of_day_evening
        }
        # Fill missing time_of_day columns with 0 if not present
        for col in self.feature_columns:
            if col not in input_dict:
                input_dict[col] = 0
        input_features = pd.DataFrame([input_dict])[self.feature_columns]
        input_scaled = self.scaler.transform(input_features)
        predicted_duration = self.model.predict(input_scaled)[0][0]
        return predicted_duration

# Example usage:
if __name__ == "__main__":
    predictor = AirAlertDurationPredictor()
    pred = predictor.predict()
    print(f'Predicted air alert duration (minutes): {pred:.1f}')

