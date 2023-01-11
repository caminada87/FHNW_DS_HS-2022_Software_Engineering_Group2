import pytest
import predictor
from predictor import HousePricePrediction


@pytest.fixture
# fixture sind vorab funktion für pytest
def get_bucket():
    # Objekt zurückliefern
    return "bucket start"


@pytest.mark.parametrize(
    # parametrize stellt die testcases für pytest bereit
    "input_longitude", 
    "input_latitude", 
    "input_postal_code", 
    "input_city", 
    "input_bulding_category", 
    "input_build_year", 
    "input_living_area", 
    "input_num_rooms", 
    "result", 
    "error", 
    [
        (0, 0, 5420, 
        "Ehrendingen", 
        "Einfamilienhaus", 
        2000, 200.0, 7, 
        1750000.0, None)
    ]
)

def test_HousePricePrediction(
    input_longitude: float, 
    input_latitude: float,
    input_postal_code: int,
    input_city: str,
    input_bulding_category: str,
    input_build_year: int,
    input_living_area: float,
    input_num_rooms: float,
    result: int, 
    get_bucket: str, 
    error: str
) -> None:

    assert "bucket start" == get_bucket()
    try:
        assert result == predictor.HousePricePrediction(
                input_longitude, 
                input_latitude,
                input_postal_code,
                input_city,
                input_bulding_category,
                input_build_year,
                input_living_area,
                input_num_rooms
        )
    except:
        assert error != None

# in bash-konsole mit Befehl "pytest" ausführen