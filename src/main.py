# other imports, custom code, load data, define model...

import load_hp_256

phot, gcut_2 = load_hp_256.main()

def kmap_it(data,projection='median',path_html="phot_keplermapper_output.html",algorithm='auto',n_jobs=1):

    import km_aaron as km
    import sklearn

    data = data.dropna().values

    mapper = km.KeplerMapper(verbose=2)

    # Fit to and transform the data
    #Interestingly, it's not the part where you specify t-SNE that takes forever
    projected_data = mapper.fit_transform(data, projection=projection) # X-Y axis
    print "Data re-projection finished!"
    # Create dictionary called 'complex' with nodes, edges and meta-information
    # DBSCAN will ignore the "n_jobs_ keyword unless you set 'algorithm='brute''
    # I still don't understand the difference between the 'auto' and 'brute' algorithms, though...
    complex = mapper.map(projected_data, data,
                         clusterer=sklearn.cluster.DBSCAN(eps=0.5,min_samples=3,n_jobs=n_jobs,algorithm=algorithm))
    print "Mapping finished! "
    # Visualize it
    mapper.visualize(complex, path_html=path_html,
                 title="make_circles(n_samples="+str(np.size(data[:,0]))+", noise=0.03, factor=0.3)")


from sklearn.decomposition import PCA

kmap_it(phot, projection=PCA(), algorithm='auto', path_html="phot_keplermapper_output_PCA_gcut2.html")
