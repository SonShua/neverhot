# Never Hot

<img src=https://github.com/SonShua/neverhot/blob/main/never_hot.gif width="650" />
Personal project. Simple App that display weather forecast data and allows user to add cities/location to the database. There will be a clothing recommendation app added on top of the forecast data. Currently running local development, collecting data and trying out different ML approaches.

## Homepage
On the homepage you will find 6 clickable images which will zoom in on hover and display their respective name. Below that there is a search bar implemented with HTMX which will perform an async search on the database. The search results will display in a paginated list below that with previous/next buttons always displayed but disabled when not available. 

## Weather / Cities 
You will find all the cities currently in the database here. 

## Weather / Add city
Typing in a location time and searching will perform an API call to the geocode API of [openweathermap API](https://openweathermap.org/api) and compare to DB entries. If new, the found locations will be added and the user will be notified. If one or more locations were already in DB the user will also be notified. Same goes for if nothing was found. 

## City page
Whether by clicking on the images on Homepage, Cities or Add City you reach the weather forecast display for the city. On top you have the current local time, the name of the city, current temperature, humidity and wind speed. As well as an icon representing the current weather. Below that is a Chart.js line graph displaying the temperature forecast data for the location. 

## Weather data
Weather forecast and location data is sourced from [openweathermap API](https://openweathermap.org/api).


## Run locally

```git clone https://github.com/SonShua/neverhot.git ```

Go into root directory. Make sure you have Poetry 1.6.1

```bash build.sh ```

Go into django_project\settings.py and change 

``` DEBUG = True ``` 

Poetry should have installed your virutal environment

``` .venv\Scripts\activate ```

Start local server

``` py manage.py runserver ```


