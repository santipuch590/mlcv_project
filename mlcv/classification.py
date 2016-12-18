import sklearn.decomposition as decomposition
import sklearn.preprocessing as preprocessing
import sklearn.svm as svm

import mlcv.input_output as io


def train_linear_svm(X, y, C=1, standardize=True, dim_reduction=None, save_scaler=False, save_pca=False,
                     model_name=None, liblinear=False):
    # PCA for dimensionality reduction if necessary
    pca = decomposition.PCA(n_components=dim_reduction)
    if dim_reduction is not None and dim_reduction > 0:
        pca.fit(X)
        X = pca.transform(X)

    # Standardize the data before classification if necessary
    std_scaler = preprocessing.StandardScaler()
    if standardize:
        std_scaler.fit(X)
        X_std = std_scaler.transform(X)
    else:
        X_std = X

    # Instance of SVM classifier
    clf = svm.LinearSVC(C=C, max_iter=5000, tol=1e-4) if liblinear else svm.SVC(kernel='linear', C=C)

    if model_name is not None:
        # Try to load a previously trained model
        try:
            clf = io.load_object(model_name)
        except (IOError, EOFError):
            clf.fit(X_std, y)
            # Store the model with the provided name
            io.save_object(clf, model_name)
    else:
        clf.fit(X_std, y)

    if save_scaler:
        io.save_object(std_scaler, save_scaler)

    if save_pca:
        io.save_object(pca, save_pca)

    return clf, std_scaler, pca


def train_poly_svm(X, y, C=1, degree=3, gamma='auto', coef0=0.0, standardize=True, dim_reduction=None,
                   save_scaler=False, save_pca=False, model_name=None):
    # PCA for dimensionality reduction if necessary
    pca = decomposition.PCA(n_components=dim_reduction)
    if dim_reduction is not None and dim_reduction > 0:
        pca.fit(X)
        X = pca.transform(X)

    # Standardize the data before classification if necessary
    std_scaler = preprocessing.StandardScaler()
    if standardize:
        std_scaler.fit(X)
        X_std = std_scaler.transform(X)
    else:
        X_std = X

    # Instance of SVM classifier
    clf = svm.SVC(kernel='poly', C=C, degree=degree, gamma=gamma, coef0=coef0)

    if model_name is not None:
        # Try to load a previously trained model
        try:
            clf = io.load_object(model_name)
        except (IOError, EOFError):
            clf.fit(X_std, y)
            # Store the model with the provided name
            io.save_object(clf, model_name)
    else:
        clf.fit(X_std, y)

    if save_scaler:
        io.save_object(std_scaler, save_scaler)

    if save_pca:
        io.save_object(pca, save_pca)

    return clf, std_scaler, pca


def train_rbf_svm(X, y, C=1, gamma='auto', standardize=True, dim_reduction=None,
                  save_scaler=False, save_pca=False, model_name=None):
    # PCA for dimensionality reduction if necessary
    pca = decomposition.PCA(n_components=dim_reduction)
    if dim_reduction is not None and dim_reduction > 0:
        pca.fit(X)
        X = pca.transform(X)

    # Standardize the data before classification if necessary
    std_scaler = preprocessing.StandardScaler()
    if standardize:
        std_scaler.fit(X)
        X_std = std_scaler.transform(X)
    else:
        X_std = X

    clf = svm.SVC(kernel='rbf', C=C, gamma=gamma)

    if model_name is not None:
        # Instance of SVM classifier
        # Try to load a previously trained model
        try:
            clf = io.load_object(model_name)
        except (IOError, EOFError):
            clf.fit(X_std, y)
            # Store the model with the provided name
            io.save_object(clf, model_name)
    else:
        clf.fit(X_std, y)

    if save_scaler:
        io.save_object(std_scaler, save_scaler)

    if save_pca:
        io.save_object(pca, save_pca)

    return clf, std_scaler, pca


def train_sigmoid_svm(X, y, C=1, gamma='auto', coef0=0.0, standardize=True, dim_reduction=None,
                      save_scaler=False, save_pca=False, model_name=None):
    # PCA for dimensionality reduction if necessary
    pca = decomposition.PCA(n_components=dim_reduction)
    if dim_reduction is not None and dim_reduction > 0:
        pca.fit(X)
        X = pca.transform(X)

    # Standardize the data before classification if necessary
    std_scaler = preprocessing.StandardScaler()
    if standardize:
        std_scaler.fit(X)
        X_std = std_scaler.transform(X)
    else:
        X_std = X

    clf = svm.SVC(kernel='sigmoid', C=C, gamma=gamma, coef0=coef0)

    if model_name is not None:
        # Instance of SVM classifier
        # Try to load a previously trained model
        try:
            clf = io.load_object(model_name)
        except (IOError, EOFError):
            clf.fit(X_std, y)
            # Store the model with the provided name
            io.save_object(clf, model_name)
    else:
        clf.fit(X_std, y)

    if save_scaler:
        io.save_object(std_scaler, save_scaler)

    if save_pca:
        io.save_object(pca, save_pca)

    return clf, std_scaler, pca


def predict_svm(X, svm, std_scaler=None, pca=None):
    # Apply PCA if available
    if pca is not None:
        X = pca.transform(X)

    # Standardize data
    if std_scaler is None:
        X_std = X
    else:
        X_std = std_scaler.transform(X)

    # Predict the labels
    return svm.predict(X_std)
