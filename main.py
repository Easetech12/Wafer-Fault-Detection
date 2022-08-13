# roll back when require in VSC
# config.yml have templates which i can find on  hithub acces or circle ci
# everything is available in docker image
# to execute yml cmd we need machine, circle ci will provide that machine
# circleci will use its machine & docker our application

# for different platforms cicd pipeline will be different, like for azure, AWS, GCP & github access it
# will be different
# whenever we push this code to circleci , it will search for config.yml directory, & try to open this file
# it will start reading its detail & execute every detail one by one
# dockerfile will docker your image & it will allow your run your docker image
# It can create your docker image to serve your application,
# github access create the docker image & push it to some kind of server
# github access detect that something has modified in our code, we have to run this config.yml file again
# the instruction inside confif.yml , execute them one by one

# docker file will not store docker image , it will store the steps to which are required to create the
# docker image
# config.yml is not a docker image, it is the instructions for circleci
# circleci will read this file, for build & test, it will read, it will provide us machine
# it will try to create env for python, it will test the application
# it will use our existing docker file for docker image
# we will provide our docker username & password, so that It will push our image which is created at circleci
# those images will be pushed to docker hub, we'll be able to see dooker image to docker hub
# In the deployment sector, It will take the existing image, & it   will deploy to heroku

# cover code will be pushed to github, from github, we will configure circleci, this code (circleci.yml) is
# available to circleci

# circleci only check config.yml, inside that it will open the machine in circleci
# Here it is to create venv, to upgrade pip & to install requirements.txt file
# to test our application is running or not , we use test_script.py, here i am trying to access to route url
# self.app.get('/') url, response 200 : our appl. is running
# build the docker image, it will push this image to docker hub, it will login to dockerhub, than
#  username than password
# when docker image is creating at circleci
# Test script is used for unit testing

# Before work on project, writing your whole code: first test your application, than test your cicd pipeline
# After than you can start implementing your actual code, than you don't need to worry about how you are
# going to deploy your application
# every you write your code, make the changes,  you will push your changes to github & automatically all the
# changes will be reflected to the server, this is the benefit of establishing cicd pipeline in the first place

# docker
# docker build -t demo_flask:lastest .
# docker ps
# docker images
# docker run -p 5000:5000 demo_flask:lastest
# python3.6.2 is the machine for circleci where our docker image will be build, we don't need to worry about it

# docker image will be available at docker hub
# heroku will provide the container to run the docker image
# you can run your image any where as long as you provide container to run it

# ACR - for Azure, instead of circleci, ACR(Azure container registry), instead of docker hub,use azure kubernetes
# ECS - for AWS, send your repo to Elastic container registry, you can read the images, deploy your images
# to ECS (elastic container service)

# docker file will give instructions to create docker image, config.yml have the instructions which circleci
# will follow to create docker image, it will publish that image to docker hub, & it will publish that image to
# heroku container

#!/usr/bin/env python

from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.json is not None:
            path = request.json['filepath']

            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(
                json.loads(json_predictions)))
        elif request.form is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path)  # object initialization

            pred_val.prediction_validation()  # calling the prediction_validation function

            pred = prediction(path)  # object initialization

            # predicting for dataset present in database
            path, json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!" + str(path) + 'and few of the predictions are ' + str(
                json.loads(json_predictions)))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" % ValueError)
    except KeyError:
        return Response("Error Occurred! %s" % KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" % e)


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRouteClient():
    try:
        # if request.json['folderPath'] is not None:
        folder_path = "Training_Batch_Files"
        # path = request.json['folderPath']
        if folder_path is not None:
            path = folder_path

            train_valObj = train_validation(path)  # object initialization

            train_valObj.train_validation()  # calling the training_validation function

            trainModelObj = trainModel()  # object initialization
            trainModelObj.trainingModel()  # training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successful!!")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
