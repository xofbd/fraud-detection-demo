# Fraud Detection Machine Learning Model
This repository creates a web application to predict if a customer is going to commit fraud. It is for academic purposes and shouldn't really be used in real life. It takes a trained machine learning model created with [scikit-learn](https://scikit-learn.org) and serves it using [Flask](https://flask.palletsprojects.com). Feel free to improve the model and/or user interface. An example of the app can be seen at [https://pml-detect-fraud.herokuapp.com]. <br>

## Prerequisites
All required Python packages can be found in the `requirements.txt` file. Additionally, the provided `Makefile` can be used to created a virtual environment by running `make venv`. You will also need a Heroku account and have installed the Heroku CLI. For more information on the Heroku CLI, go to [https://devcenter.heroku.com/articles/heroku-cli#download-and-install].

## Running the app locally using Flask
You may want to run the app using Flask locally before deploying it to Heroku, especially if you have made any changes to the code. To run locally: <br>

1. clone the repository. <br>
1. in the repository, run `make deploy`.
1. open the link provided in the command line. <br>

If you using Windows, you can

1. `set FLASK_APP=app.py` in the command line. If you are using Windows, replace `export` with `set` <br>
1. run `python -m flask run` <br>

## Deploying to Heroku
Make sure your app is ready to be deployed to Heroku by running Flask locally. To deploy to Heroku: <br>

1. clone the repository (if you haven't yet). <br>
1. `heroku login` and enter your credentials <br>
1. `heroku create` or `heroku create app-name` where app-name is a custom app name <br>
1. `git push heroku master` <br>
1. `heroku open` or open the app online through your Heroku profile <br>

## License
This project is distributed under the GNU General Public License. The file `data/Fraud_Data.csv` does not fall under the license and was obtained from [Kaggle](https://www.kaggle.com/vbinh002/fraud-ecommerce). Please see `LICENSE` for more information.
