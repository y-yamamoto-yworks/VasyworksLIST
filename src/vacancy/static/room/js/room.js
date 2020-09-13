/*
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
 */
var { LMap, LTileLayer, LMarker } = Vue2Leaflet;

function createRoomVue(
    lat,
    lng,
) {
    return new Vue({
        el: "#contents",
        delimiters: ["[[", "]]"],
        components: { LMap, LTileLayer, LMarker },
        data: {
            zoom: 17,
            center: L.latLng(lat, lng),
            url:'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
            marker: L.latLng(lat, lng),
        },
        mounted: function(event) {
        },
        methods: {
        },
    });
}

