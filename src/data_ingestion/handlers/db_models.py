from sqlalchemy import create_engine, Column, Integer, Float, String, Date, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Raw / Clean Hubeau
class RawHubeau(Base):
    __tablename__ = "raw_hubeau"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code_statut = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    code_qualification = Column(String)
    libelle_qualification = Column(String)
    date_obs_elab = Column(DateTime)
    libelle_statut = Column(String)
    code_station = Column(String)
    code_methode = Column(String)
    grandeur_hydro_elab = Column(String)
    libelle_methode = Column(String)
    resultat_obs_elab = Column(String)
    date_prod = Column(DateTime)
    code_site = Column(String)


class CleanHubeau(Base):
    __tablename__ = "clean_hubeau"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code_statut = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    code_qualification = Column(String)
    libelle_qualification = Column(String)
    date_obs_elab = Column(DateTime)
    libelle_statut = Column(String)
    code_station = Column(String)
    code_methode = Column(String)
    grandeur_hydro_elab = Column(String)
    libelle_methode = Column(String)
    resultat_obs_elab = Column(String)
    date_prod = Column(DateTime)
    code_site = Column(String)


# Raw / Clean Solar
class RawSolar(Base):
    __tablename__ = "raw_solar_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    shortwave_radiation_sum = Column(Float)
    shortwave_radiation_sum_kwh_m2 = Column(Float)
    precipitation_hours = Column(Float)
    wind_speed_10m_mean = Column(Float)
    wind_gusts_10m_mean = Column(Float)
    temperature_2m_max = Column(Float)
    temperature_2m_min = Column(Float)
    temperature_2m_mean = Column(Float)
    cloud_cover_mean = Column(Float)
    cloud_cover_max = Column(Float)
    cloud_cover_min = Column(Float)
    relative_humidity_2m_mean = Column(Float)
    uv_index_max = Column(Float)
    uv_index_clear_sky_max = Column(Float)
    sunshine_duration_h = Column(Float)
    daylight_duration_h = Column(Float)
    apparent_temperature_mean = Column(Float)
    sunrise = Column(DateTime)
    sunset = Column(DateTime)
    sunshine_duration = Column(Float)
    precipitation_sum = Column(Float)
    daylight_duration = Column(Float)


class CleanSolar(Base):
    __tablename__ = "clean_solar_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    shortwave_radiation_sum = Column(Float)
    shortwave_radiation_sum_kwh_m2 = Column(Float)
    precipitation_hours = Column(Float)
    wind_speed_10m_mean = Column(Float)
    wind_gusts_10m_mean = Column(Float)
    temperature_2m_max = Column(Float)
    temperature_2m_min = Column(Float)
    temperature_2m_mean = Column(Float)
    cloud_cover_mean = Column(Float)
    cloud_cover_max = Column(Float)
    cloud_cover_min = Column(Float)
    relative_humidity_2m_mean = Column(Float)
    uv_index_max = Column(Float)
    uv_index_clear_sky_max = Column(Float)
    sunshine_duration_h = Column(Float)
    daylight_duration_h = Column(Float)
    apparent_temperature_mean = Column(Float)
    sunrise = Column(DateTime)
    sunset = Column(DateTime)
    sunshine_duration = Column(Float)
    precipitation_sum = Column(Float)
    daylight_duration = Column(Float)


# Raw / Clean Wind
class RawWind(Base):
    __tablename__ = "raw_wind_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    wind_speed_10m_max = Column(Float)
    wind_speed_10m_mean = Column(Float)
    wind_gusts_10m_max = Column(Float)
    wind_gusts_10m_mean = Column(Float)
    wind_direction_10m_dominant = Column(Float)
    surface_pressure_mean = Column(Float)
    temperature_2m_mean = Column(Float)
    cloud_cover_mean = Column(Float)


class CleanWind(Base):
    __tablename__ = "clean_wind_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    wind_speed_10m_max = Column(Float)
    wind_speed_10m_mean = Column(Float)
    wind_gusts_10m_max = Column(Float)
    wind_gusts_10m_mean = Column(Float)
    wind_direction_10m_dominant = Column(Float)
    surface_pressure_mean = Column(Float)
    temperature_2m_mean = Column(Float)
    cloud_cover_mean = Column(Float)


# Raw / Clean Production
class RawProdSolar(Base):
    __tablename__ = "raw_prod_solaire"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    prod_solaire = Column(Float)


class CleanProdSolar(Base):
    __tablename__ = "clean_prod_solaire"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    prod_solaire = Column(Float)


class RawProdWind(Base):
    __tablename__ = "raw_prod_eolienne"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    prod_eolienne = Column(Float)


class CleanProdWind(Base):
    __tablename__ = "clean_prod_eolienne"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    prod_eolienne = Column(Float)


class RawProdHydro(Base):
    __tablename__ = "raw_prod_hydro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_obs_elab = Column(DateTime)
    prod_hydro = Column(Float)


class CleanProdHydro(Base):
    __tablename__ = "clean_prod_hydro"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_obs_elab = Column(DateTime)
    prod_hydro = Column(Float)
