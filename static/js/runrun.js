// globals to set on start
var groups = null;
var account = null;
var images_url = null;
var places_all_url = null;
var places_form_url = null;
var places_delete_url = null;
// other globals
var markers = [];
var map = null;
var menu = null;
var seq = 0;
function getSeq() {
	return seq++;
};
// context menu
var ContextMenu = function (google_map) {
	this.mapDiv = google_map.getDiv();
	this.menuDiv = document.createElement('span');
	this.menuDiv.id  = 'contextmenu';
	this.mapDiv.appendChild(this.menuDiv);
};
ContextMenu.prototype.show = function(event) {
	this.menuDiv.innerHTML = '';
	var add_place = document.createElement('a');
	add_place.textContent = 'Add place here';
	add_place.onclick = function() { addPlace(event); };
	this.menuDiv.appendChild(add_place)
	
	var x = event.pixel.x;
	var y = event.pixel.y;
	var mapWidth = this.mapDiv.offsetWidth;
	var mapHeight = this.mapDiv.offsetHeight;
	var menuWidth = this.menuDiv.offsetWidth;
	var menuHeight = this.menuDiv.offsetHeight;

	if ((mapWidth - x) < menuWidth) x = x - menuWidth;
	if ((mapHeight - y) < menuHeight) y = y - menuHeight;
	
	this.menuDiv.style.left = x + 'px';
	this.menuDiv.style.top = y +'px';
	this.menuDiv.style.visibility = 'visible';
};
ContextMenu.prototype.hide = function(event) {
	this.menuDiv.style.visibility = 'hidden';
};
// helpers
function awesomeIcon(name) {
	return {
		url: images_url + name + '.png',
		scaledSize: new google.maps.Size(30, 30),
		anchor: new google.maps.Point(15, 15)
	};
};
function addPlace(event) {
	menu.hide();
	$.get(places_form_url + '?longitude=' + event.latLng.D + '&latitude=' + event.latLng.k, function(data){
		if (data.hasOwnProperty('success') != true) {
			$('#commonModal').find('.modal-title').text("Invalid server response.");
			$('#commonModal').find('.modal-body').text("Server response is invalid. No markers was loaded. Try again later.");
			$('#commonModal').modal('show');
			return;
		}
		$('#commonModal').find('.modal-title').text("Place form");
		$('#commonModal').find('.modal-body').html(data.success.form);
		$('#commonModal').modal('show');
	}).fail(function(data){
		$('#commonModal').find('.modal-title').text("Server communication error.");
		$('#commonModal').find('.modal-body').text("Server communication error. Can not get form. Try again later.");
		$('#commonModal').modal('show');
	});
};
function editPlace(place_id) {
	$('#placeInfoModal').modal('hide');
	$.get(places_form_url + '?place_id=' + place_id, function(data){
		if (data.hasOwnProperty('success') != true) {
			$('#commonModal').find('.modal-title').text("Invalid server response.");
			$('#commonModal').find('.modal-body').text("Server response is invalid. No markers was loaded. Try again later.");
			$('#commonModal').modal('show');
			return;
		}
		$('#commonModal').find('.modal-title').text("Place form");
		$('#commonModal').find('.modal-body').html(data.success.form);
		$('#commonModal').modal('show');
	}).fail(function(data){
		$('#commonModal').find('.modal-title').text("Server communication error.");
		$('#commonModal').find('.modal-body').text("Server communication error. Can not get form. Try again later.");
		$('#commonModal').modal('show');
	});
};
function deletePlace(place_id) {
	$('#placeInfoModal').modal('hide');
	$.post(places_delete_url + '?place_id=' + place_id, function(data){
		if (data.hasOwnProperty('success') != true) {
			$('#commonModal').find('.modal-title').text("Invalid server response.");
			$('#commonModal').find('.modal-body').text("Server response is invalid. No markers was loaded. Try again later.");
			$('#commonModal').modal('show');
			return;
		}
		reloadMarkers();
	}).fail(function(data){
		$('#commonModal').find('.modal-title').text("Server communication error.");
		$('#commonModal').find('.modal-body').text("Server communication error. Can not get form. Try again later.");
		$('#commonModal').modal('show');
	});
};
function makeMarkerOnClick(marker_data) {
	return function() {
		var controls = '';
		if (account != null) {
			controls = '&nbsp;<button class="btn btn-primary btn-xs" onClick="editPlace('+marker_data.id+')">Edit</button>&nbsp;<button class="btn btn-danger btn-xs" onClick="deletePlace('+marker_data.id+')">Delete</button>';
		}
		$('#placeInfoModal').find('#placeInfoTitle').html(marker_data.title + controls);
		$('#placeInfoModal').find('#placeInfoDescription').html(marker_data.description);
		$('#placeInfoModal').modal('show');
		DISQUS.reset({
			reload: true,
			config: function() {
				this.page.identifier = marker_data.id;
				this.page.title = marker_data.title;
			}
		});
	}
};
function processMarkers(data) {
	if (data.hasOwnProperty('success') != true) {
		$('#commonModal').find('.modal-title').text("Invalid server response.");
		$('#commonModal').find('.modal-body').text("Server response is invalid. No markers was loaded. Try again later.");
		$('#commonModal').modal('show');
		return;
	}
	for (var i = 0; i < markers.length; i++) {
		markers[i].setMap(null);
	}
	markers = []
	var places = data.success.places;
	for (var i = 0; i < places.length; i++) {
		var marker_data = places[i];
		var marker = new google.maps.Marker({
			position: new google.maps.LatLng(marker_data.latitude, marker_data.longitude),
			map: map,
			icon: awesomeIcon(marker_data.group),
			title: marker_data.title
		});
		google.maps.event.addListener(marker, 'click', makeMarkerOnClick(marker_data));
		markers.push(marker);
	}
};
function processMarkersFail(data) {
	$('#commonModal').find('.modal-title').text("Server communication error.");
	$('#commonModal').find('.modal-body').text("Server communication error. No markers was loaded. Try again later.");
	$('#commonModal').modal('show');
};
function reloadMarkers() {
	$.get(places_all_url + '?seq=' + getSeq(), processMarkers).fail(processMarkersFail);
};
function initialize() {
	map = new google.maps.Map(
		document.getElementById('map-canvas'),
		{
			center: { lat: 33.607848, lng: 130.421508},
			zoom: 15
		}
	);
	if (account != null) {
		menu = new ContextMenu(map);
		google.maps.event.addListener(map, "rightclick", function(event) { menu.show(event);});
		google.maps.event.addListener(map, "click", function(event) { menu.hide(event);});
		google.maps.event.addListener(map, "drag", function(event) { menu.hide(event);});
	}
	reloadMarkers();
};
function runrun() {
	google.maps.event.addDomListener(window, 'load', initialize);
};
