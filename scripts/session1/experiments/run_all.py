from __future__ import print_function, division

import time

import joblib
import numpy as np
from sklearn import metrics

import mlcv.classification as classification
import mlcv.feature_extraction as feature_extraction
import mlcv.input_output as io
from mlcv.plotting import plot_confusion_matrix


""" CONSTANTS """
N_JOBS = 6


def parallel_testing(test_image, test_label, lin_svm, std_scaler, pca):
    gray = io.load_grayscale_image(test_image)
    kpt, des = feature_extraction.sift(gray)
    predictions = classification.predict_svm(des, lin_svm, std_scaler=std_scaler, pca=pca)
    values, counts = np.unique(predictions, return_counts=True)
    predicted_class = values[np.argmax(counts)]
    return predicted_class == test_label, predicted_class, test_label


""" MAIN SCRIPT"""
if __name__ == '__main__':
    start = time.time()

    # Read the training set
    train_images_filenames, train_labels = io.load_training_set()
    print('Loaded {} train images.'.format(len(train_images_filenames)))

    # Feature extraction with sift
    print('Obtaining sift features...')
    D, L, _, _ = feature_extraction.parallel_sift(train_images_filenames, train_labels,
                                               n_jobs=N_JOBS)
    print('Time spend: {:.2f} s'.format(time.time() - start))
    temp = time.time()

    # Train Linear SVM classifier
    print('Training the SVM classifier...')
    lin_svm, std_scaler, pca = classification.train_rbf_svm(D, L, model_name='final_noprob_sift_all_svm')
    print('Time spend: {:.2f} s'.format(time.time() - temp))
    temp = time.time()

    # Read the test set
    test_images_filenames, test_labels = io.load_test_set()
    print('Loaded {} test images.'.format(len(test_images_filenames)))

    # Feature extraction with sift, prediction with SVM and aggregation to obtain final class
    print('Predicting test data...')
    result = joblib.Parallel(n_jobs=N_JOBS, backend='threading')(
        joblib.delayed(parallel_testing)(test_image, test_label, lin_svm, std_scaler, None) for test_image, test_label in
        zip(test_images_filenames, test_labels))

    correct_class = [i[0] for i in result]
    predicted = [i[1] for i in result]
    expected = [i[2] for i in result]

    num_correct = np.count_nonzero(correct_class)
    print('Time spend: {:.2f} s'.format(time.time() - temp))
    temp = time.time()

    # Compute accuracy
    accuracy = num_correct * 100.0 / len(test_images_filenames)

    conf = metrics.confusion_matrix(expected, predicted, labels=lin_svm.classes_)
    # Plot normalized confusion matrix
    #plot_confusion_matrix(conf, classes=lin_svm.classes_, normalize=True)


    io.save_object(conf, 'final_noprob_sift_all_cm')

    # Show results and timing
    print('\nACCURACY: {:.2f}'.format(accuracy))
    print('\nTOTAL TIME: {:.2f} s'.format(time.time() - start))