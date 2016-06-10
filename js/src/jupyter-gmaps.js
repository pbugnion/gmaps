var widgets = require('jupyter-js-widgets');
var _ = require('underscore');

var GoogleMapsLoader = require('google-maps');
GoogleMapsLoader.LIBRARIES = ["visualization"] ;

function gPointToList(gpoint) {
    return [gpoint.lat(), gpoint.lng()];
}

function gBoundsToList(gbounds) {
    var sw = gPointToList(gbounds.getSouthWest());
    var ne = gPointToList(gbounds.getNorthEast());
    return [sw, ne]
}

var GMapsLayerView = widgets.WidgetView.extend({
    initialize: function(parameters) {
        GMapsLayerView.__super__.initialize.apply(this, arguments);
        this.map_view = this.options.map_view ;
    }
});

var HeatmapLayerView = GMapsLayerView.extend({
    render: function() {
        this.model_events() ;
        var that = this ;
        GoogleMapsLoader.load(function(google) {
            var data = that.model.get("data");
            var data_as_google = new google.maps.MVCArray(
                _.map(data, function(point) {
                    return new google.maps.LatLng(point[0], point[1]);
                })
            );
            that.heatmap = new google.maps.visualization.HeatmapLayer({
                data: data_as_google,
                radius: that.model.get("point_radius"),
                maxIntensity: that.model.get("max_intensity")
            }) ;
        });
    },

    add_to_map_view: function(map_view) {
        this.heatmap.setMap(map_view.map) ;
    },

    model_events: function() {
        this.model.on("change:point_radius", this.update_radius, this);
        this.model.on("change:max_intensity", this.update_max_intensity, this);
    },

    update_radius: function() {
        this.heatmap.set('radius', this.model.get('point_radius'));
    },

    update_max_intensity: function() {
        console.log("max_intensity change");
        this.heatmap.set('maxIntensity', this.model.get('max_intensity'));
    }

});

var GMapsLayerModel = widgets.WidgetModel.extend({
    defaults: _.extend({}, widgets.WidgetModel.prototype.defaults, {
        _view_name : 'GMapsLayerView',
        _model_name : 'GMapsLayerModel',
        _view_module : 'jupyter-gmaps',
        _model_module : 'jupyter-gmaps',
        bottom : false,
        options : []
    })
});


var HeatmapLayerModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "HeatmapLayerView",
        _model_name: "HeatmapLayerModel"
    })
})



var PlainmapView = widgets.DOMWidgetView.extend({
    render: function() {
        this.el.style["width"] = this.model.get("width");
        this.el.style["height"] = this.model.get("height");

        var initial_bounds = this.model.get("data_bounds");

        this.layer_views = new widgets.ViewList(this.add_layer_model, null, this);
        this.model_events() ;

        var that = this ;
        this.on("displayed", function() {
            GoogleMapsLoader.load(function(google) {
                that.map = new google.maps.Map(that.el) ;
                that.update_bounds(initial_bounds);

                that.layer_views.update(that.model.get("layers"));

                // hack to force the map to redraw
                window.setTimeout(function() {
                    google.maps.event.trigger(that.map, 'resize') ;
                }, 1000);
            }) ;
        });
    },

    model_events: function() {
        this.model.on("change:data_bounds", this.update_bounds, this);
    },

    gmaps_events: function() {},

    update_bounds: function() {
        var model_bounds = this.model.get("data_bounds");
        var bounds_bl = new google.maps.LatLng(
            model_bounds[0][0], model_bounds[0][1]);
        var bounds_tr = new google.maps.LatLng(
            model_bounds[1][0], model_bounds[1][1]);
        var bounds = new google.maps.LatLngBounds(bounds_bl, bounds_tr)
        this.map.fitBounds(bounds);
    },

    add_layer_model: function(child_model) {
        var that = this;
        return this.create_child_view(child_model, {map_view: this}).then(function(child_view) {
            child_view.add_to_map_view(that) ;
            return child_view;
        })
    }

});

var PlainmapModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend({}, widgets.DOMWidgetModel.prototype.defaults, {
        _view_name: "PlainmapView",
        _model_name: "PlainmapModel",
        _view_module : 'jupyter-gmaps',
        _model_module : 'jupyter-gmaps',
        width: "600px",
        height: "400px"

    })
}, {
    serializers: _.extend({
            layers: {deserialize: widgets.unpack_models}
    }, widgets.DOMWidgetModel.serializers)
});



module.exports = {
    HeatmapLayerModel: HeatmapLayerModel,
    HeatmapLayerView: HeatmapLayerView,
    PlainmapView: PlainmapView,
    PlainmapModel: PlainmapModel
};
