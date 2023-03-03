# memeprojector
Project your best memes to any cartographic projection !

## Repository description
+ `botton_publisher`: publish a picture of Serge Botton projected in a random projection every day using the projector API
+ `projector_api`: image projection microservice
+ `projector_front`: web interface for using the image projection microservice
+ `facebook_connection`: a [Facebook Login](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#confirm) implementation to connect to the social network

## Running the API
1. The Python packages `fastapi` and `uvicorn` need to be installed.
2. Run the following command from the project root: `python -m memeprojector.api`.