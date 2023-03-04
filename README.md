# memeprojector
Project your best memes to any cartographic projection !

## Installation
Create env:
```
conda create -n memeprojector -y 
```
Install dependencies:
```
conda install gdal fastapi pillow -c conda-forge -n memeprojector
```
Then, to use the environment:
```
conda activate
```

## Repository description
+ `botton_publisher`: publish a picture of Serge Botton projected in a random projection every day using the projector API
+ `projector_api`: image projection microservice
+ `projector_front`: web interface for using the image projection microservice
+ `facebook_connection`: a [Facebook Login](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#confirm) implementation to connect to the social network
