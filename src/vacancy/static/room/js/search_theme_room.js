/*
System Name: Vasyworks
Project Name: vacancy
Encoding: UTF-8
Copyright (C) 2020 Yasuhiro Yamamoto
 */
function createSearchVacancyThereRoomVue(
    key,    // キー
    prefId,       // 都道府県ID
    cityId,       // 市区町村ID
    areaId,       // エリアID
) {
    return new Vue({
        el: "#search-conditions-form",
        delimiters: ["[[", "]]"],
        data: {
            key: key,       // APIデータ取得用
            pref: prefId,
            defaultPref: prefId,
            city: cityId,
            area: areaId,
        },
        mounted: function(event) {
            if(this.pref !== 0) { this.reloadCities();}
            if(this.city !== 0) { this.reloadAreas();}
        },
        methods: {
            clearConditions: function(event) {
                this.pref = this.defaultPref;
                this.reloadCities();
                this.city = 0;
                this.area = 0;
            },
            changePref: function(event) {
                // 都道府県変更時の処理
                this.city = 0;
                this.reloadCities();
            },
            changeCity: function(event) {
                // 市区町村変更時の処理
                this.area = 0;

                this.reloadAreas();
            },
            reloadSelectOptions: function(elm, items, value) {
                // サーバサイドで自動生成される選択リスト向け
                // 選択リスト書き換え用の内部メソッド
                if(!elm || !items) return;

                // 対象リストをクリア
                let elm_options = elm.querySelectorAll("option");
                for(let i = elm_options.length - 1; i >= 0; i--) {
                    elm_options[i].remove();
                }

                // 対象リストの再構築
                for(let i = 0; i < items.length; i++) {
                    let option = document.createElement("option");
                    option.text = items[i].name;
                    option.value = items[i].id;
                    if(option.value === value.toString()) option.selected = true;
                    elm.appendChild(option);
                }
            },
            reloadCities: function() {
                // 市区町村のリストを書き換える。
                if(this.pref !== 0 && this.pref !== "") {
                    let that = this;
                    axios.get("/api/cities/" + this.key + "/" + this.pref)
                        .then(function(res) {
                            let items = res.data;
                            that.reloadSelectOptions(that.$refs.city, items, that.city)
                        })
                        .catch(function (error) {
                            alert("市区町村データの取得に失敗しました。");
                        });
                }
            },
            reloadAreas: function() {
                // エリアのリストを書き換える。
                if(this.city !== 0 && this.city !== "") {
                    let that = this;
                    axios.get("/api/areas/" + this.key + "/" + this.city)
                        .then(function(res) {
                            let items = res.data;
                            that.reloadSelectOptions(that.$refs.area, items, that.area)
                        })
                        .catch(function (error) {
                            alert("エリアデータの取得に失敗しました。");
                        });
                }
            },
        },
    });
}
