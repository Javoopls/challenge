import numpy as np
import pandas as pd
import xgboost as xgb
from datetime import datetime
from typing import Tuple, Union, List
from sklearn.model_selection import train_test_split

from typing import Tuple, Union, List

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.

    # Period of Day
    def get_period_day(self, date):
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()
        evening_min = datetime.strptime("19:00", '%H:%M').time()
        evening_max = datetime.strptime("23:59", '%H:%M').time()
        night_min = datetime.strptime("00:00", '%H:%M').time()
        night_max = datetime.strptime("4:59", '%H:%M').time()
        
        if(date_time > morning_min and date_time < morning_max):
            return 'mañana'
        elif(date_time > afternoon_min and date_time < afternoon_max):
            return 'tarde'
        elif(
            (date_time > evening_min and date_time < evening_max) or
            (date_time > night_min and date_time < night_max)
        ):
            return 'noche'
        
    # High Season
    def is_high_season(self, fecha):
        fecha_año = int(fecha.split('-')[0])
        fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
        range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year = fecha_año)
        range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year = fecha_año)
        range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year = fecha_año)
        range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year = fecha_año)
        range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year = fecha_año)
        range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year = fecha_año)
        range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year = fecha_año)
        range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year = fecha_año)
        
        if ((fecha >= range1_min and fecha <= range1_max) or 
            (fecha >= range2_min and fecha <= range2_max) or 
            (fecha >= range3_min and fecha <= range3_max) or
            (fecha >= range4_min and fecha <= range4_max)):
            return 1
        else:
            return 0
    
    # Difference in Minutes
    def get_min_diff(self, data):
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds())/60
        return min_diff

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
    
        # Features Generation
        data['period_day'] = data['Fecha-I'].apply(self.get_period_day)
        data['high_season'] = data['Fecha-I'].apply(self.is_high_season)
        data['min_diff'] = data.apply(self.get_min_diff, axis=1)
        data['delay'] = np.where(data['min_diff'] > 15, 1, 0)

        # Feature Selection
        top_10_features = [
            "OPERA_Latin American Wings",
            "MES_10",
            "MES_7",
            "OPERA_Grupo LATAM",
            "MES_6",
            "MES_4",
            "MES_8",
            "MES_12",
            "OPERA_Sky Airline",
            "TIPOVUELO_I"
        ]

        # Additional preprocessing (adding prefixes)
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ],
            axis=1
        )

        print(features.columns)

        features = features[top_10_features]

        target_column = [
            'delay'
        ]

         # Add print for debugging
        print("Número de columnas antes de la selección de características:", features.shape[1])
        
        features = pd.DataFrame(features[top_10_features])
        target = data[target_column] 

        print(features.columns)

        # Add print for debugging
        print("Número de columnas después de la selección de características:", features.shape[1])

        if target_column is not None:
            target = data[target_column].copy()
            return features, target
        else:
            return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit the model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        n_y0 = len(target[target == 0])
        n_y1 = len(target[target == 1])
        scale = n_y0 / n_y1

        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42) # Split the Data
        xgb_model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight=scale) # Set the Model
        xgb_model.fit(x_train, y_train) # Train the Model

        # Save the model
        self._model = xgb_model

    def predict(
        self,
        features: pd.DataFrame,
        threshold: float = 0.5
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        if self._model is None:
            raise ValueError("The model has not been trained. Please call the 'fit' method first.")
    
        # Make the prediction using the trained model
        proba_predictions = self._model.predict(features)

        predictions = [0 if proba[0] > threshold else 1 for proba in proba_predictions]

        # Returns predictions as a list of integers (0 or 1)
        return predictions.tolist()