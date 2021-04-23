from astroquery.utils.tap.core import TapPlus

# Select CSC2 sources within 1 arcsec from qso_farfrom_xsources.
# I'm using the CSC2 catalogue hosted in Vizier because 
# I cannot make it work using the CXC TAP service
csc = TapPlus(url="http://tapvizier.u-strasbg.fr/TAPVizieR/tap")

query = (
    "SELECT t.SRCID_sdss, t.RA, t.DEC, "
    "DISTANCE(POINT('ICRS', t.RA, t.DEC), POINT('ICRS', m.RAICRS, m.DEICRS)) as d, "
    'm."2CXO", m.RAICRS, m.DEICRS, m."b_Fluxb", m.Fluxb, m."B_Fluxb", m.ExpAC, m.ExpHRC '
    'FROM "IX/57/csc2master" as m, tap_upload.qso_farfrom_xsources as t '
    "WHERE 1=CONTAINS(POINT('ICRS', t.RA, t.DEC), CIRCLE('ICRS', m.RAICRS, m.DEICRS, 1/3600.))"
)

# upload_resource is an Astropy table with the coordinates (columns RA, DEC)
# of all positions you want to query
job = csc.launch_job_async(
    query=query,
    upload_resource=upload_resource,
    upload_table_name="qso_farfrom_xsources",
)
csc_data = job.get_results()

csc_data["SRCID_sdss"] = csc_data["SRCID_sdss"].astype(str)
csc_data["_2CXO"] = csc_data["_2CXO"].astype(str)
csc_data.rename_column("_2CXO", "2CXO")

filename = data_folder.joinpath("qso_sdss_farfrom_4xmm_csc2.fits")
csc_data.write(str(filename), format="fits", overwrite=True)
