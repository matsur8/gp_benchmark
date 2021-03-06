import argparse 

import gpflow
import numpy as np

from gpflow_exact import predict, show_model

def make_model(X, y, optimize, variance, lengthscale, noise_variance, n_inducing_inputs, fix_inducing_inputs):
    kernel = gpflow.kernels.RBF(input_dim=X.shape[1], lengthscales=lengthscale, variance=variance)
    model = gpflow.models.GPRFITC(X, y[:,np.newaxis], Z=X[np.random.choice(X.shape[0], n_inducing_inputs),:], kern=kernel)
    model.likelihood.variance = noise_variance
    if not optimize:
        model.kern.trainable = False
        model.likelihood.trainable = False
    if fix_inducing_inputs:
        model.feature.Z.trainable = False
    if optimize or not fix_inducing_inputs:
        gpflow.train.ScipyOptimizer().minimize(model)
    return model

def parse_make_model_option(s):
    parser = argparse.ArgumentParser()
    parser.add_argument("n_inducing_inputs", type=int)
    parser.add_argument("--fix_inducing_inputs", "-f", action="store_true")
    args = parser.parse_args(s.split())
    return vars(args)

def get_hyp(model):
    model_tbl = model.as_pandas_table()
    return {"lengthscale": model_tbl.loc["GPRFITC/kern/lengthscales", "value"]*1,
            "variance": model_tbl.loc["GPRFITC/kern/variance", "value"]*1,
            "noise_variance": model_tbl.loc["GPRFITC/likelihood/variance", "value"]*1}

