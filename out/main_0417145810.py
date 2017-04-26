# other imports, custom code, load data, define model...

import load_hp_256
import numpy as np


def kmap_it(data,subset='all', projection='t_SNE',path_html="../out/phot_km_output_tSNE.html"):

    import km
    import sklearn
    import shutil
    import datetime as dt

    timestamp = dt.datetime.now().strftime('%m%d%H%M%S')

    if subset == 'all':
        data = data.dropna().values
    else:
        data = data.dropna().values[subset]
#    else:
#    else:
#        data = data.dropna().values

    mapper = km.KeplerMapper(verbose=2)

    # Fit to and transform the data
    #Interestingly, it's not the part where you specify t-SNE that takes forever
    projected_data = mapper.fit_transform(data, projection=projection) # X-Y axis
    print "Data re-projection finished!"
    # Create dictionary called 'complex' with nodes, edges and meta-information
    # DBSCAN will ignore the "n_jobs_ keyword unless you set 'algorithm='brute''
    # I still don't understand the difference between the 'auto' and 'brute' algorithms, though...
    complex = mapper.map(projected_data,
                         clusterer=sklearn.cluster.DBSCAN(eps=0.5,min_samples=3))
    print "Mapping finished! "
    # Visualize it
    mapper.visualize(complex, path_html=path_html+timestamp+".html",
                 title="make_circles(n_samples="+str(np.size(data[:,0]))+", noise=0.03, factor=0.3)")

    shutil.copyfile("main.py","../out/main_"+timestamp+".py")


#from sklearn.decomposition import PCA
#from sklearn.decomposition import tSNE




#kmap_it(phot, projection=PCA(), algorithm='auto', path_html="phot_keplermapper_output_PCA_gcut2.html")
phot, gcut = load_hp_256.main(glatrange=1, elatrange=25,)
from sklearn.manifold import TSNE

#kmap_it(phot, subset=gcut[2000:2050],  projection='t_SNE', path_html="../out/phot_km_output_tSNE")
kmap_it(phot, subset=gcut[2000:3000],  projection=TSNE(), path_html="../out/phot_km_output_tSNE_")
