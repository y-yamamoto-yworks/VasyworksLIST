/*
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
 */
function createSearchNameVue(
    buildingName,
) {
    return new Vue({
        el: "#search-conditions-form",
        delimiters: ["[[", "]]"],
        data: {
            buildingName: buildingName,
        },
        mounted: function(event) {
        },
        methods: {
            clearConditions: function(event) {
                this.buildingName = "";
            },
        },
    });
}
