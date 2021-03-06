import gpflow
import numpy as np

def make_model(X, y, optimize, lengthscale, variance, noise_variance):
    kernel = gpflow.kernels.RBF(input_dim=X.shape[1], lengthscales=lengthscale, variance=variance)
    model = gpflow.models.GPR(X, y[:,np.newaxis], kern=kernel)
    model.likelihood.variance = noise_variance
    if optimize:
        gpflow.train.ScipyOptimizer().minimize(model)
    return model

def predict(X, model):
    p =  model.predict_y(X)
    return p[0][:,0], np.sqrt(p[1][:,0])

def show_model(model):
    print(model.as_pandas_table())

def get_hyp(model):
    model_tbl = model.as_pandas_table()
    return {"lengthscale": model_tbl.loc["GPR/kern/lengthscales", "value"]*1,
            "variance": model_tbl.loc["GPR/kern/variance", "value"]*1,
            "noise_variance": model_tbl.loc["GPR/likelihood/variance", "value"]*1}

