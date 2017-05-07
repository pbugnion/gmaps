import widgets from 'jupyter-js-widgets'
import _ from 'underscore'
import html2canvas from 'html2canvas'

import GoogleMapsLoader from 'google-maps'

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
