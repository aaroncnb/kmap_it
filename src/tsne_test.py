# other imports, custom code, load data, define model...

import load_hp_256

phot, gcut_2 = load_hp_256.main()


def tsne_test(data):
    # For testing the TSNE reprojection on its own:
    import numpy as np
    from sklearn.manifold import TSNE

    data = data.dropna().values[gcut_2]


    model = TSNE(n_components=2, random_state=0, verbose=2)
    np.set_printoptions(suppress=False)
    model.fit_transform(data)

tsne_test(phot)
