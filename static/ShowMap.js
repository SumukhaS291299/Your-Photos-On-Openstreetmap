var map = L.map('map').setView([12.99332, 77.54348], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function currentLoc(latlang){
    var marker = L.marker(latlang);
    marker.bindPopup("Your location based on IP");
    marker.addTo(map);
}

function TagLocation(latlang,image){
    tempMarker = L.marker(latlang);
    tempMarker.bindPopup(image);
    tempMarker.addTo(map);
}

function onMapClick(e) {
    console.log("You clicked the map at " + e.latlng);
    // Create an XMLHttpRequest object.
      var xhr = new XMLHttpRequest();

      // Set the request method and URL.
      xhr.open("POST", "/Photos");

      // Set the request headers.
      xhr.setRequestHeader("Content-Type", "application/json");

      // Send the value to the Flask route.
      xhr.send(JSON.stringify({"latlang": e.latlng}));

      // Handle the response from the Flask route.
      xhr.onload = function() {
        if (xhr.status === 200) {
          // Success!
        } else {
            console.log(xhr.status)
          // Error!
        }
      };
}

map.on('click', onMapClick);
