from typing import Any, NamedTuple
from data_providers import metoffice_codes
import metoffer  # type: ignore


_METOFFICE_CODES_MAP: dict[str, str] = {
    metoffice_codes.NOT_AVAILABLE: 'error',
    metoffice_codes.CLEAR_NIGHT: 'clear_night',
    metoffice_codes.SUNNY_DAY: 'clear_day',
    metoffice_codes.PARTLY_CLOUDY_NIGHT: 'partial_cloud_night',
    metoffice_codes.PARTLY_CLOUDY_DAY: 'partial_cloud_day',
    metoffice_codes.NOT_USED: 'error',
    metoffice_codes.MIST: 'light_fog',
    metoffice_codes.FOG: 'heavy_fog',
    metoffice_codes.CLOUDY: 'light_cloud',
    metoffice_codes.OVERCAST: 'light_cloud',
    metoffice_codes.LIGHT_RAIN_SHOWER_NIGHT: 'light_rain_partial_cloud_night',
    metoffice_codes.LIGHT_RAIN_SHOWER_DAY: 'light_rain_partial_cloud_day',
    metoffice_codes.DRIZZLE: 'light_rain',
    metoffice_codes.LIGHT_RAIN: 'light_rain',
    metoffice_codes.HEAVY_RAIN_SHOWER_NIGHT: 'heavy_rain_partial_cloud_night',
    metoffice_codes.HEAVY_RAIN_SHOWER_DAY: 'heavy_rain_partial_cloud_day',
    metoffice_codes.HEAVY_RAIN: 'heavy_rain',
    metoffice_codes.SLEET_SHOWER_NIGHT: 'light_sleet_partial_cloud_night',
    metoffice_codes.SLEET_SHOWER_DAY: 'light_sleet_partial_cloud_day',
    metoffice_codes.SLEET: 'light_sleet',
    metoffice_codes.HAIL_SHOWER_NIGHT: 'heavy_sleet_partial_cloud_night',
    metoffice_codes.HAIL_SHOWER_DAY: 'heavy_sleet_partial_cloud_day',
    metoffice_codes.HAIL: 'heavy_sleet',
    metoffice_codes.LIGHT_SNOW_SHOWER_NIGHT: 'light_snow_partial_cloud_night',
    metoffice_codes.LIGHT_SNOW_SHOWER_DAY: 'light_snow_partial_cloud_day',
    metoffice_codes.LIGHT_SNOW: 'light_snow',
    metoffice_codes.HEAVY_SNOW_SHOWER_NIGHT: 'heavy_snow_partial_cloud_night',
    metoffice_codes.HEAVY_SNOW_SHOWER_DAY: 'heavy_snow_partial_cloud_day',
    metoffice_codes.HEAVY_SNOW: 'heavy_snow',
    metoffice_codes.THUNDER_SHOWER_NIGHT: 'thumderstorm_partial_cloud_night',
    metoffice_codes.THUNDER_SHOWER_DAY: 'thumderstorm_partial_cloud_day',
    metoffice_codes.THUNDER: 'thunderstorm'
}

_WIND_DIRECTION_MAP: dict[str, int] = {
    "N": 0,
    "NNE": 0,
    "NE": 1,
    "ENE": 1,
    "E": 2,
    "ESE": 2,
    "SE": 3,
    "SSE": 3,
    "S": 4,
    "SSW": 4,
    "SW": 5,
    "WSW": 5,
    "W": 6,
    "WNW": 6,
    "NW": 7,
    "NNW": 7
}

WeatherData = NamedTuple(
    "WeatherData",
    [
        ('day_temp_c', int),
        ('night_temp_c', int),
        ('wind_speed_knts', int),
        ('wind_direction', int),
        ('day_weather', str),
        ('night_weather', str)
    ]
)


class MetOffice():
    def __init__(self, api_key: str):
        self._metoffice = metoffer.MetOffer(api_key)

    def get_forecast(self) -> WeatherData:
        forecast = self._metoffice.loc_forecast('324156', metoffer.DAILY)  # type: ignore
        current_day = forecast["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"]
        day = current_day[0]
        night = current_day[1]

        day_temp = int(day["Dm"])
        night_temp = int(night["Nm"])
        wind_spd, wind_dir = self._get_best_wind_speed_and_direction(day, night)
        day_weather = _METOFFICE_CODES_MAP[day["W"]]
        night_weather = _METOFFICE_CODES_MAP[night["W"]]

        return WeatherData(day_temp, night_temp, wind_spd, wind_dir, day_weather, night_weather)

    def _get_best_wind_speed_and_direction(self, day: Any, night: Any) -> tuple[int, int]:
        best_wind_source = day if int(day["S"]) >= int(night["S"]) else night
        return int(int(best_wind_source["S"]) * 1.151), _WIND_DIRECTION_MAP[best_wind_source["D"]]
