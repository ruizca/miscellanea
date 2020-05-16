"""
A module for querying the SVO Filter Profile Service
"""
from io import BytesIO

import requests
from astropy.io.votable import parse

def query(**kwargs):
    """
    For details, see the SVO FPS documentation [1].

    Parameters
    ----------
    ID : Filter ID (e.g. 2MASS/2MASS.H)
    PhotCalID : Photometric Calibration ID (e.g. 2MASS/2MASS.H/AB)
    WavelengthMean (range)
    WavelengthEff (range)
    WavelengthMin (range)
    WavelengthMax (range)
    WidthEff (range)
    FWHM (range)
    Instrument (value)
    Facility (value)
    PhotSystem (value)

    [1] http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php?mode=voservice
    """
    url = "http://svo2.cab.inta-csic.es/svo/theory/fps3/fps.php"
    
    payload = {key: value for key, value in kwargs.items()}
    r = requests.get(url, params=payload)

    return parse(BytesIO(r.content), pedantic=False)
