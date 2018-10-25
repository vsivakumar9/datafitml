# Libraries
import os
import json
import io
import re
import pandas as pd
import numpy as np
from flask import Flask, request, redirect, url_for, jsonify,render_template

# Machine Learning Libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib 
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Resources'

model = None
graph = None
filepath = None

# def load_model():
#     global model
#     global graph
#     model = LinearRegression()
#     graph = K.get_session().graph


# load_model()

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/about")
def about():
    """Return the homepage."""
    return render_template("about.html")

@app.route("/visualization")
def visualization():
    """Return the homepage."""
    return render_template("visualization.html")

@app.route("/projectlc")
def projectlc():
    """Return the homepage."""
    return render_template("process.html")

# @app.route("/",methods=['GET', 'POST'])
# def index():
#     global filepath
#     data = {"success": False}
#     return render_template("index.html")
    # if request.method == 'POST':
    #     if request.files.get('file'):
    #         # read the file
    #         file = request.files['file']
            
    #         # read the filename , create a path to the uploads folder
    #         filename = file.filename
    #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #         file.save(filepath)

    #         # read column names from the uploaded file
    #         uploaded_file = pd.read_csv(filepath, encoding="ISO-8859-1")
    #         column_names = list(uploaded_file.columns.values)
            
    #         # write column names to data dictionary, indicate that the request was a success
    #         data["column_names"] = column_names
    #         data["success"] = True

    #     #return jsonify(data)
    #     column_names_list.append(data)
    #     print(column_names_list)
    #     return render_template("index.html",result=column_names_list[0]['column_names'])

    
@app.route("/upload",methods=['POST'])
def upload():
    global filepath
    data = {"success": False}
    column_names_list=[]
    if request.files.get('file'):
                # read the file
        file = request.files['file']
        
            # read the filename , create a path to the uploads folder
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
            # read column names from the uploaded file
        uploaded_file = pd.read_csv(filepath, encoding="ISO-8859-1")
        column_names = list(uploaded_file.columns.values)
        
            # write column names to data dictionary, indicate that the request was a success
        data["column_names"] = column_names
        data["success"] = True
        column_names_list.append(data)
        print(column_names_list)
        return render_template("index.html",result=column_names_list[0]['column_names'])



# routes to return model evaluation metrics

@app.route("/Decision_Tree", methods=['GET','POST'])

# def evaluate(model_name,depenedent_var):

def evaluate():
    data = {"success": True}

    # file processing - reading and parsing columns
    uploaded_file = pd.read_csv(filepath, encoding="ISO-8859-1")
    column_names = list(uploaded_file.columns.values)
    uploaded_dummied = pd.get_dummies(uploaded_file)

    # assign dependent and independent variables
    target = uploaded_file["Length"]
    target_names = ["Just Right", "Slightly Long","Slightly Short","Very Long","Very Short"]
    dependent_var = uploaded_file.drop("Length", axis=1)
    feature_names = dependent_var.columns

    # train and test split
    X_train, X_test, y_train, y_test = train_test_split(dependent_var, target, random_state=42)

    # decision tree classifier 

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    data["Decision Tree Score"] = clf.score(X_test, y_test)

    # Random Forest tree classifier 
    rf = RandomForestClassifier(n_estimators=200)
    rf = rf.fit(X_train, y_train)
    data["Random Forest Score"] = rf.score(X_test, y_test)

    # feature importance 

    feature_importance = sorted(zip(rf.feature_importances_, feature_names), reverse=True)

    print(feature_importance)

    data["Feature Importance"] = feature_importance

    print(data)

    return jsonify(data)


@app.route("/KNN", methods=['GET','POST'])

def KNN():
    data = {"success": True}

    # file processing - reading and parsing columns
    print(filepath)
    uploaded_file = pd.read_csv(filepath, encoding="ISO-8859-1")
    column_names = list(uploaded_file.columns.values)
    uploaded_dummied = pd.get_dummies(uploaded_file)

    print("uploaded / dummied")
    # assign dependent and independent variables
    target = uploaded_file["Length"]
    target_names = ["Just Right", "Slightly Long","Slightly Short","Very Long","Very Short"]
    dependent_var = uploaded_file.drop("Length", axis=1)
    feature_names = dependent_var.columns
    print("feature engineering")
    # train and test split
    X_train, X_test, y_train, y_test = train_test_split(dependent_var, target, random_state=42)

    print("Model started")

    # Loop through different k values to see which has the highest accuracy
    # Note: We only use odd numbers because we don't want any ties
    train_scores = []
    test_scores = []
    k_value = []

    for k in range(1, 20, 2):
        print(k)
        knn = KNeighborsClassifier(n_neighbors=k)
        
        print("fit")

        knn.fit(X_train, y_train)
        train_score = knn.score(X_train, y_train)
        print("train complete")
        test_score = knn.score(X_test, y_test)

        print("test complete")
        train_scores.append(train_score)
        test_scores.append(test_score)
        print(f"k: {k}, Train/Test Score: {train_score:.3f}/{test_score:.3f}")
        k_value.append(k)
        print(k_value)
        
    knn_metrics = { "K" : k_value,
                    "Train Score" :train_scores,
                    "Test Score": test_scores}

    print("knn_metrics written")

    data["KNN_Metrics"] = knn_metrics

    # plot and save
    plt.plot(range(1, 20, 2), train_scores, marker='o')
    plt.plot(range(1, 20, 2), test_scores, marker="x")
    plt.xlabel("k neighbors")
    plt.ylabel("Testing accuracy Score")
    plt.savefig('KNN.png')

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
