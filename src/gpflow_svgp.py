#reference
#http://gpflow.readthedocs.io/en/latest/notebooks/svi_test.html

import gpflow
import numpy as np

from gpflow_basic import predict, show_model

def make_model(X, y, optimize, lengthscale, variance, noise_variance, n_inducing_inputs):
    kernel = gpflow.kernels.RBF(input_dim=X.shape[1], lengthscales=lengthscale, variance=variance)
    model = gpflow.models.SVGP(X, y[:,np.newaxis], Z=X[np.random.choice(X.shape[0], n_inducing_inputs),:], 
                               kern=kernel, likelihood=gpflow.likelihoods.Gaussian(noise_variance), minibatch_size=100)
    if not optimize:
        model.kern.trainable = False
        model.likelihood.trainable = False
        model.feature.trainable = False
    opt = gpflow.train.AdagradOptimizer(learning_rate=0.1)
    #opt = gpflow.train.ScipyOptimizer()
    opt.minimize(model)
    return model

def parse_make_model_option(s):
    return {"n_inducing_inputs": int(s)}

