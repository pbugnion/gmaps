import widgets from 'jupyter-js-widgets'
import _ from 'underscore'

import GoogleMapsLoader from 'google-maps'

import { downloadElementAsPng } from './services/downloadElement'
import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

function needReloadGoogleMaps(configuration) {
    return GoogleMapsLoader.KEY !== configuration["api_key"];
}

function reloadGoogleMaps(configuration) {
    if (needReloadGoogleMaps(configuration)) {
        console.log("Releasing Google Maps");
        GoogleMapsLoader.release();
    }

    GoogleMapsLoader.LIBRARIES = ["visualization"] ;
    if (configuration["api_key"] !== null &&
        configuration["api_key"] !== undefined) {
            GoogleMapsLoader.KEY = configuration["api_key"];
    };
}


// Mixins

const ConfigurationMixin = {
    loadConfiguration() {
        const modelConfiguration = this.model.get("configuration")
        reloadGoogleMaps(modelConfiguration)
    }
}


// Views

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

    updateBounds(bounds) {
        const [[latBL, lngBL], [latTR, lngTR]] = bounds
        const boundBL = new google.maps.LatLng(latBL, lngBL)
        const boundTR = new google.maps.LatLng(latTR, lngTR)
        const boundsAsGoogle = new google.maps.LatLngBounds(boundBL, boundTR)
        this.map.fitBounds(boundsAsGoogle);
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
        const allLayers = Promise.all(this.layerViews.views);
        const canDownloadEveryLayer = allLayers.then(layers =>
            layers.every(layer => layer.canDownloadAsPng)
        )
        return canDownloadEveryLayer.then(canDownload => {
            if (canDownload) {
                return downloadElementAsPng(this.$el, 'map.png');
            }
            else {
                const nonDownloadableLayers = allLayers.then(layers =>
                    layers
                        .filter(layer => !layer.canDownloadAsPng)
                        .map(layer => layer.model.get('_view_name'))
                )
                const error = nonDownloadableLayers
                    .then(layers => layers.join(', '))
                    .then(text => Promise.reject(`Cannot download layers: ${text}`))
                return error
            }
        })
    },

})

_.extend(PlainmapView.prototype, ConfigurationMixin);


// Models

export const PlainmapModel = widgets.DOMWidgetModel.extend({
    defaults: {
        ...widgets.DOMWidgetModel.prototype.defaults,
        _view_name: "PlainmapView",
        _model_name: "PlainmapModel",
        _view_module : 'jupyter-gmaps',
        _model_module : 'jupyter-gmaps',
        width: "600px",
        height: "400px",
        data_bounds: null
    }
}, {
    serializers: {
        layers: {deserialize: widgets.unpack_models},
        ...widgets.DOMWidgetModel.serializers
    }
});
