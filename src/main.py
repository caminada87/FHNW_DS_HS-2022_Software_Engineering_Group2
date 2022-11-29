## Import librarys ##
import pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor

## Global variables ##
"""
TODO: Extend UI to be able to get lat and long from user
INPUT ---
long: float (MAP Interface)
lat: float (MAP Interface)
zipcode: int (MAP Interface)
municipality_name: str (MAP Interface)
oject_type_name: str (Drop Down - Wohnung, Einfamilienhaus, Mehrfamilienhaus, Sonstiges)
build_year: int (1970-2022)
living_area:int
number_of_rooms:int
"""
long: float = 0.0
lat: float  = 0.0
zipcode: int = 5420
municipality_name: str = 'Ehrendingen'
object_type_name: str = 'Einfamilienhaus'
build_year: int = 2000
living_area: float = 200.0
num_rooms: float = 7

filename: str = '../model/decision_tree_model.sav'

## Functions ##
def single_pred(model, long:float, lat:float, zipcode: int, municipality_name: str, object_type_name: str,
                build_year:int, living_area:float, num_rooms:float) -> float:
    data_frame= pd.DataFrame(data={'long': long, 'lat': lat, 'zipcode': zipcode, 'municipality_name': municipality_name,
                                   'object_type_name': object_type_name, 'build_year': build_year,
                                   'living_area': living_area, 'num_rooms': num_rooms}, index=[0])
    return model.predict(data_frame)[0]

## Main ##
loaded_model = pickle.load(open(filename, 'rb'))

y_pred = single_pred(loaded_model, long, lat, zipcode, municipality_name, object_type_name, build_year, living_area,
                     num_rooms)

print(y_pred)