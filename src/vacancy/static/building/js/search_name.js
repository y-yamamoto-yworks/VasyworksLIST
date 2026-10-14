/*
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 - 2026 Yasuhiro Yamamoto
 */
function createSearchNameVue(
    buildingName,
) {
    return Vue.createApp({
        delimiters: ["[[", "]]"],
        data() {
            return {
                buildingName: buildingName,
            };
        },
        mounted: function(event) {
        },
        methods: {
            clearConditions: function(event) {
                this.buildingName = "";
            },
        },
    }).mount("#search-conditions-form");
}
