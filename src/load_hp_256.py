
def main():
    import numpy as np
    import healpy as hp
    import pandas as pd

    #import hp_allsky_init_NSIDE256

     ### Make a gargantuan cube. The "layers" are the FIR data:

    filepath  =  "/work1/users/aaronb/Databrary/HEALPix/AKARI_HEALPix_orig/"

    nside = 256

    bands         = ["akari_90",\
                        "dirbe_100", "iras_100",\
                        "dirbe_140", "akari_140",\
                        "akari_160", \
                        "dirbe_240", \
                        "planck_857", "planck_545"]


    band_names =   [ "akari_9",\
                        "dirbe_12","iras_12", "wise_12", \
                        "akari_18", \
                        "dirbe_25","iras_25", \
                        "dirbe_60","iras_60","akari_65",\
                        "akari_90",\
                        "dirbe_100", "iras_100",\
                        "dirbe_140", "akari_140",\
                        "akari_160", \
                        "dirbe_240", \
                        "planck_857", "planck_545"]

    band_abbr =   [ "A9",\
                        "D12","I12", "W12", \
                        "A18", \
                        "D25","I25", \
                        "D60","I60","A65",\
                        "A90",\
                        "D100", "I100",\
                        "D140", "A140",\
                        "A160", \
                        "D240", \
                        "P857", "P545"]


    band_labels  = ["AKARI 9 $\mu{m}$",\
                    "DIRBE 12 $\mu{m}$","IRAS 12 $\mu{m}$","WISE 12 $\mu{m}$", \
                    "AKARI 18 $\mu{m}$",\
                    "DIRBE 25 $\mu{m}$", "IRAS 25 $\mu{m}$", \
                    "DIRBE 60 $\mu{m}$","IRAS 60 $\mu{m}$","AKARI 65 $\mu{m}$", \
                    "AKARI 90 $\mu{m}$", \
                    "DIRBE 100 $\mu{m}$","IRAS 100 $\mu{m}$",\
                    "DIRBE 140 $\mu{m}$","AKARI 140 $\mu{m}$",\
                    "AKARI 160 $\mu{m}$",\
                    "DIRBE 240 $\mu{m}$",\
                    "PLANCK 350 $\mu{m}$","PLANCK 550 $\mu{m}$" ]

    waves         = [90e-6, 100e-6, 100e-6, 140e-6, 140e-6, 160e-6, 240e-6, 350e-6, 550e-6]
    simple_sigma  = [ 0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.25,   0.25]

    nbands            = len(bands)
    nbands_all        = len(band_names)

        #layer = 0
        #npix  = 12*nside**2
        #fir   = np.ones([nbands,npix])
        #phot  = np.ones([nbands_all,npix])


        #for band in bands:
        #
        #    fir[layer,:] = hp.read_map(filepath+str(nside)+"_nside/"+band+"_"+str(nside)+"_1dres.fits",memmap=True)
        #    layer += 1

        ##### Now, we have a cube of the FIR data saved as "fir"
        ##### We want to compare the individual maps in a way that makes some physical sense
        ##### How about we start by assuming an SED? Next: Modified blackbody fitting
    layer = 0
    nside = 256
    npix  = 12*nside**2
    phot  = np.ones([npix, nbands_all])


    for band in band_names:

        phot[:,layer] = hp.read_map(filepath+str(nside)+"_nside/"+band+"_"+str(nside)+"_1dres.fits",memmap=False);
        layer += 1

    print "IR Maps Read"
    phot = pd.DataFrame(phot, columns = band_abbr)

    AME    = hp.read_map('/work1/users/aaronb/Databrary/HEALPix/COM_CompMap_CO-commander_0256_R2.00.fits',field = 0, memmap=False);
    print "AME Map Read"



    #AME_nu = hp.read_map('../../AME_Data/COM_CompMap_AME-commander_0256_R2.00.fits',field = 3, memmap=False)

    ### Import the temperature map from the Planck Release 2:
    #Planck_T   = hp.read_map(filepath+str(nside)+"_nside/COM_CompMap_dust-commander_0256_R2.00.fits", field = 4, memmap=True)
    #Planck_B   = hp.read_map(filepath+str(nside)+"_nside/COM_CompMap_dust-commander_0256_R2.00.fits", field = 7, memmap=True)
    #Planck_FIR = hp.read_map(filepath+str(nside)+"_nside/COM_CompMap_dust-commander_0256_R2.00.fits", field = 1, memmap=True)
    #Planck_G0  = (Planck_T / 17.5)**(4+2)



    ### Import the Galactic coordinate reference columns:
    ### These are just "maps" of glat and glon. That way you can easily get the center pixel coordinates from a given pixel index

    glon = hp.read_map(filepath+str(nside)+"_nside/pixel_coords_map_ring_galactic_res8.fits", field = 0, memmap=False)
    glat = hp.read_map(filepath+str(nside)+"_nside/pixel_coords_map_ring_galactic_res8.fits", field = 1, memmap=False)

    ### Same for the ecliptic coordinates:

    elon = hp.read_map(filepath+str(nside)+"_nside/pixel_coords_map_ring_ecliptic_res8.fits", field = 0, memmap=False)
    elat = hp.read_map(filepath+str(nside)+"_nside/pixel_coords_map_ring_ecliptic_res8.fits", field = 1, memmap=False)

    glatrange = 2.0
    elatrange = 10.0

    gcut_1 = np.where((abs(glat) > glatrange) & (abs(elat) > elatrange))
    gcut_2 = np.where((abs(glat) < glatrange) & (abs(elat) > elatrange))


    ## Replace the HEALPix "UNSEEN" pixels with NaN, in a Pandas Dataframe:
    phot.replace(to_replace=hp.UNSEEN, value=np.nan, inplace=True);
    #AME_dframe = pd.DataFrame(AME, columns= ['AME'])
    #AME_dframe.replace(to_replace=hp.UNSEEN, value=np.nan, inplace=True)

    ## Calculating the mode of each band:
    #allsky_modes = phot.round(3).mode(axis=0)
    ## Subtract the all-sky mode from each map:
    ## Trying a vectorized way now, using the Pandas ".subtract" method
    #phot_modesub = pd.DataFrame(phot.values-allsky_modes.values,columns=phot.columns)


    gcut_2 = np.array(gcut_2)
    gcut_2 = np.ndarray.flatten(gcut_2)

    #from sklearn.externals.joblib import parallel

    #parallel.MIN_IDEAL_BATCH_DURATION = 1.
    #parallel.MAX_IDEAL_BATCH_DURATION = parallel.MIN_IDEAL_BATCH_DURATION * 100
    return phot, gcut_2

if __name__ == '__main__':
    main()
