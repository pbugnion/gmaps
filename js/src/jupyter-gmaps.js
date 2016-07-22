import widgets from 'jupyter-js-widgets'
import _ from 'underscore'

import GoogleMapsLoader from 'google-maps'

function reloadGoogleMaps(configuration) {
    GoogleMapsLoader.release();
    GoogleMapsLoader.LIBRARIES = ["visualization"] ;
    if (configuration["api_key"] !== null &&
        configuration["api_key"] !== undefined) {
            GoogleMapsLoader.KEY = configuration["api_key"];
    };
}

reloadGoogleMaps({}) ;

function gPointToList(gpoint) {
    return [gpoint.lat(), gpoint.lng()]
}

function gBoundsToList(gbounds) {
    const sw = gPointToList(gbounds.getSouthWest())
    const ne = gPointToList(gbounds.getNorthEast())
    return [sw, ne]
}

// Mixins

const ConfigurationMixin = {
    load_configuration() {
        const model_configuration = this.model.get("configuration")
        reloadGoogleMaps(model_configuration)
    }
}


// Views

const GMapsLayerView = widgets.WidgetView.extend({
    initialize(parameters) {
        GMapsLayerView.__super__.initialize.apply(this, arguments)
        this.map_view = this.options.map_view
    }
})


export const DirectionsLayerView = GMapsLayerView.extend({
    render() {
        const rendererOptions = { map: this.map_view.map }

        this.directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions)

        const model_data = this.model.get("data");
        const orig = this.get_orig(model_data);
        const dest = this.get_dest(model_data);
        const wps = this.get_wps(model_data);

        const request = {
            origin: orig,
            destination: dest,
            waypoints: wps,
            travelMode: google.maps.TravelMode.DRIVING
        };

        const directionsService = new google.maps.DirectionsService();

        directionsService.route(request, (response, status) => {
            // print to the browser console (mostly for debugging)
            console.log("Direction service returned: ", status) ;
            // set a flag in the model
            this.model.set("layer_status", status) ;
            this.touch() ; // push `layer_status` changes to the model
            if (status == google.maps.DirectionsStatus.OK) {
                this.response = this.directionsDisplay ;
                this.directionsDisplay.setDirections(response);
            }
        });
    },


    add_to_map_view(map_view) { },

    get_orig(model_data) {
        const first_point = _.first(model_data)
        return new google.maps.LatLng(first_point[0], first_point[1])
    },

    get_dest(model_data) {
        const last_point = _.last(model_data)
        return new google.maps.LatLng(last_point[0], last_point[1])
    },

    get_wps(model_data) {
        const without_first = _.tail(model_data)
        const without_last = _.initial(without_first)
        const data_as_google = _.map(without_last, (point) => {
            const google_point = new google.maps.LatLng(point[0], point[1])
            return {location: google_point}
        })
        return data_as_google
    }
})


const HeatmapLayerBaseView = GMapsLayerView.extend({
    render() {
        this.model_events() ;
        GoogleMapsLoader.load((google) => {
            this.heatmap = new google.maps.visualization.HeatmapLayer({
                data: this.get_data(),
                radius: this.model.get("point_radius"),
                maxIntensity: this.model.get("max_intensity")
            }) ;
        });
    },

    add_to_map_view(map_view) {
        this.heatmap.setMap(map_view.map)
    },

    model_events() {
        this.model.on("change:point_radius", this.update_radius, this)
        this.model.on("change:max_intensity", this.update_max_intensity, this)
    },

    get_data() {},

    update_radius() {
        this.heatmap.set('radius', this.model.get('point_radius'));
    },

    update_max_intensity() {
        this.heatmap.set('maxIntensity', this.model.get('max_intensity'));
    }

})

export const SimpleHeatmapLayerView = HeatmapLayerBaseView.extend({
    get_data() {
        const data = this.model.get("data");
        const data_as_google = new google.maps.MVCArray(
            _.map(data, (point) => {
                return new google.maps.LatLng(point[0], point[1]);
            })
        );
        return data_as_google
    }
});


export const WeightedHeatmapLayerView = HeatmapLayerBaseView.extend({
    get_data() {
        const data = this.model.get("data");
        const data_as_google = new google.maps.MVCArray(
            _.map(data, (weighted_point) => {
                const location = new google.maps.LatLng(
                    weighted_point[0], weighted_point[1]);
                const weight = weighted_point[2];
                return { location: location, weight: weight };
            })
        );
        return data_as_google;
    }
})


export const PlainmapView = widgets.DOMWidgetView.extend({
    render() {
        this.load_configuration();
        this.el.style["width"] = this.model.get("width");
        this.el.style["height"] = this.model.get("height");

        const initial_bounds = this.model.get("data_bounds");

        this.layer_views = new widgets.ViewList(this.add_layer_model, null, this);
        this.model_events() ;

        this.on("displayed", () => {
            GoogleMapsLoader.load((google) => {
                this.map = new google.maps.Map(this.el) ;
                this.update_bounds(initial_bounds);

                this.layer_views.update(this.model.get("layers"));

                // hack to force the map to redraw
                setTimeout(() => {
                    google.maps.event.trigger(this.map, 'resize') ;
                }, 1000);
            })
        })
    },

    model_events() {
        this.model.on("change:data_bounds", this.update_bounds, this);
    },

    gmaps_events() {},

    update_bounds() {
        const model_bounds = this.model.get("data_bounds");
        const bounds_bl = new google.maps.LatLng(
            model_bounds[0][0], model_bounds[0][1]);
        const bounds_tr = new google.maps.LatLng(
            model_bounds[1][0], model_bounds[1][1]);
        const bounds = new google.maps.LatLngBounds(bounds_bl, bounds_tr)
        this.map.fitBounds(bounds);
    },

    add_layer_model(child_model) {
        return this.create_child_view(
            child_model, {map_view: this}
        ).then((child_view) => {
            child_view.add_to_map_view(this) ;
            return child_view;
        })
    },

})

_.extend(PlainmapView.prototype, ConfigurationMixin);


// Models

export const GMapsLayerModel = widgets.WidgetModel.extend({
    defaults: _.extend({}, widgets.WidgetModel.prototype.defaults, {
        _view_name : 'GMapsLayerView',
        _model_name : 'GMapsLayerModel',
        _view_module : 'jupyter-gmaps',
        _model_module : 'jupyter-gmaps',
    })
});

export const DirectionsLayerModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "DirectionsLayerView",
        _model_name: "DirectionsLayerModel"
    })
});

export const SimpleHeatmapLayerModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "SimpleHeatmapLayerView",
        _model_name: "SimpleHeatmapLayerModel"
    })
});


export const WeightedHeatmapLayerModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "WeightedHeatmapLayerView",
        _model_name: "WeightedHeatmapLayerModel"
    })
});


export const PlainmapModel = widgets.DOMWidgetModel.extend({
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
