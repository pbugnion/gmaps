import widgets from 'jupyter-js-widgets'
import _ from 'underscore'
import html2canvas from 'html2canvas'

import GoogleMapsLoader from 'google-maps'

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

function reloadGoogleMaps(configuration) {
    GoogleMapsLoader.release();
    GoogleMapsLoader.LIBRARIES = ["visualization"] ;
    if (configuration["api_key"] !== null &&
        configuration["api_key"] !== undefined) {
            GoogleMapsLoader.KEY = configuration["api_key"];
    };
}

reloadGoogleMaps({}) ;


// Mixins

const ConfigurationMixin = {
    loadConfiguration() {
        const modelConfiguration = this.model.get("configuration")
        reloadGoogleMaps(modelConfiguration)
    }
}


// Views


export const DirectionsLayerView = GMapsLayerView.extend({
    render() {
        const rendererOptions = { map: this.mapView.map }

        this.directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions)

        const modelData = this.model.get("data");

        const request = {
            origin: this.getOrigin(modelData),
            destination: this.getDestination(modelData),
            waypoints: this.getWaypoints(modelData),
            travelMode: google.maps.TravelMode.DRIVING
        };

        const directionsService = new google.maps.DirectionsService();

        directionsService.route(request, (response, status) => {
            // print to the browser console (mostly for debugging)
            console.log(`Direction service returned: ${status}`) ;
            // set a flag in the model
            this.model.set("layer_status", status) ;
            this.touch() ; // push `layer_status` changes to the model
            if (status == google.maps.DirectionsStatus.OK) {
                this.response = this.directionsDisplay ;
                this.directionsDisplay.setDirections(response);
            }
        });
    },


    addToMapView(mapView) { },

    getOrigin(modelData) {
        const [lat, lng] = _.first(modelData)
        return new google.maps.LatLng(lat, lng)
    },

    getDestination(modelData) {
        const [lat, lng] = _.last(modelData)
        return new google.maps.LatLng(lat, lng)
    },

    getWaypoints(modelData) {
        const withoutFirst = _.tail(modelData)
        const withoutLast = _.initial(withoutFirst)
        const dataAsGoogle = withoutLast.map(([lat, lng]) => {
            return {location: new google.maps.LatLng(lat, lng)}
        })
        return dataAsGoogle
    }
})


export const GeoJsonLayerView = GMapsLayerView.extend({
    render() {
        this.featureViews = new widgets.ViewList(this.addFeature, null, this)
        this.featureViews.update(this.model.get("features"))
    },

    addToMapView(mapView) {
        mapView.map.data.setStyle((feature) => feature.getProperty('style'))
    },

    addFeature(childModel) {
        return this.create_child_view(childModel)
            .then((childView) => {
                childView.addToMapView(this.mapView)
                return childView
            })
    }
})


export const PlainmapView = widgets.DOMWidgetView.extend({
    render() {
        this.loadConfiguration();
        this.el.style["width"] = this.model.get("width");
        this.el.style["height"] = this.model.get("height");

        const initialBounds = this.model.get("data_bounds");

        this.layerViews = new widgets.ViewList(this.addLayerModel, null, this);
        this.modelEvents() ;

        this.on("displayed", () => {
            GoogleMapsLoader.load((google) => {
                this.map = new google.maps.Map(this.el) ;
                this.updateBounds(initialBounds);

                this.layerViews.update(this.model.get("layers"));

                // hack to force the map to redraw
                setTimeout(() => {
                    google.maps.event.trigger(this.map, 'resize') ;
                    this.updateBounds(initialBounds);
                }, 500);
            })
        })
    },

    modelEvents() {
        this.model.on("change:data_bounds", this.updateBounds, this);
    },

    updateBounds() {
        const [[latBL, lngBL], [latTR, lngTR]] = this.model.get("data_bounds")
        const boundBL = new google.maps.LatLng(latBL, lngBL)
        const boundTR = new google.maps.LatLng(latTR, lngTR)
        const bounds = new google.maps.LatLngBounds(boundBL, boundTR)
        this.map.fitBounds(bounds);
    },

    addLayerModel(childModel) {
        return this.create_child_view(
            childModel, {mapView: this}
        ).then((childView) => {
            childView.addToMapView(this) ;
            return childView;
        })
    },

    savePng() {
        return new Promise((resolve, reject) => {
            html2canvas(this.$el, {
                useCORS: true,
                onrendered: (canvas) => {
                    const a = document.createElement("a");
                    a.download = "map.png";
                    a.href = canvas.toDataURL("image/png");
                    document.body.appendChild(a);
                    a.click();
                    resolve();
                }
            })
        })
    }

})

_.extend(PlainmapView.prototype, ConfigurationMixin);


// Models

export const DirectionsLayerModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "DirectionsLayerView",
        _model_name: "DirectionsLayerModel"
    })
});

export const GeoJsonLayerModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "GeoJsonLayerView",
        _model_name: "GeoJsonLayerModel"
    })
}, {
    serializers: _.extend({
            features: {deserialize: widgets.unpack_models}
    }, widgets.DOMWidgetModel.serializers)
})

export const GeoJsonFeatureModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "GeoJsonFeatureView",
        _model_name: "GeoJsonFeatureModel"
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
