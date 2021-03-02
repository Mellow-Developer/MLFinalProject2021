import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


def train():

    ds = pd.read_csv("D:/University/Machine Learning/Presentation/Final project/dataset/"
                     "train.csv/train-2.csv", error_bad_lines=False)

    x = ds.drop(ds.columns[[2, 3, 4, 5, 6, 7]], axis=1)
    y = ds.drop(ds.columns[[0, 1]], axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20)

    sv_classifier = SVC(kernel='linear')
    sv_classifier.fit(x_train, y_train)

    y_pred = sv_classifier.predict(x_test)

    my_array = [confusion_matrix, classification_report, y_pred]

    return my_array
