var widgets = require('jupyter-js-widgets');
var _ = require('underscore');

var GoogleMapsLoader = require('google-maps');
GoogleMapsLoader.LIBRARIES = ["visualization"] ;

var PlainmapView = widgets.DOMWidgetView.extend({
    render: function() {
        this.el.style["width"] = this.model.get("width");
        this.el.style["height"] = this.model.get("height");

        var initial_zoom = this.model.get("zoom");
        this.model.on("change:zoom", this.update_zoom, this);

        var initial_center = this.model.get("center");
        this.model.on("change:center", this.update_center, this);

        var that = this ;
        this.on("displayed", function() {
            GoogleMapsLoader.load(function(google) {
                var center = new google.maps.LatLng(
                    initial_center[0], initial_center[1]) ;
                that.map = new google.maps.Map(
                    that.el, { center : center, zoom : initial_zoom }
                ) ;

                that.map.addListener("bounds_changed", function() {
                    var zoom = that.map.getZoom();
                    var center = that.map.getCenter();
                    that.model.set("zoom", zoom);
                    that.model.set("center", [center.lat(), center.lng()]);
                    that.touch();
                });

                // hack to force the map to redraw
                // without this, it draws fine the first time a map object
                // is loaded in a cell, but not on subsequent times, until
                // the window is manually moved.
                window.setTimeout(function() {
                    google.maps.event.trigger(that.map, 'resize') ;
                }, 100);
            }) ;
        });
    },

    update_zoom: function() {
        this.map.setZoom(this.model.get("zoom"));
    },

    update_center: function() {
        var model_center = this.model.get("center");
        center = new google.maps.LatLng(
            model_center[0], model_center[1]);
        this.map.setCenter(center);
    }
});


module.exports = {
    PlainmapView : PlainmapView
};
