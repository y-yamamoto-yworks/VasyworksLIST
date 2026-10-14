/*
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
 */

function createRoomVue(
    lat,
    lng,
) {
    return Vue.createApp({
        delimiters: ["[[", "]]"],
        data() {
            return {
                zoom: 17,
                center: L.latLng(lat, lng),
                url: 'https://{s}.tile.osm.org/{z}/{x}/{y}.png',
                attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors',
                icon: L.icon({
                    iconUrl: "/static/vacancy/images/building_icon.png",
                    iconSize: [48, 48],
                    iconAnchor: [24, 24],
                }),
                marker: null,
                map: null,
            };
        },
        mounted: function(event) {
            if (lat > 0 && lng > 0) {
                var mapEl = document.getElementById('id_map');
                if (!mapEl) return;
                this.map = L.map('id_map').setView([lat, lng], this.zoom);
                L.tileLayer(this.url, {
                    attribution: this.attribution
                }).addTo(this.map);
                this.marker = L.marker([lat, lng], {icon: this.icon})
                this.marker.addTo(this.map);
            }
        },
        methods: {
        },
    }).mount("#contents");
}

