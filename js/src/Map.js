import * as widgets from '@jupyter-widgets/base'
import _ from 'underscore'

import GoogleMapsLoader from 'google-maps'

import { downloadElementAsPng } from './services/downloadElement'
import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';
import { defaultAttributes } from './defaults'

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

// Constants

const DATA_BOUNDS = "DATA_BOUNDS";
const ZOOM_CENTER = "ZOOM_CENTER";


// Mixins

const ConfigurationMixin = (superclass) => class extends superclass {
    loadConfiguration() {
        const modelConfiguration = this.model.get("configuration")
        reloadGoogleMaps(modelConfiguration)
    }
}


// Views

export class PlainmapView extends ConfigurationMixin(widgets.DOMWidgetView) {

    render() {
        this.loadConfiguration();
        this.el.style["width"] = this.model.get("width");
        this.el.style["height"] = this.model.get("height");

        this.layerViews = new widgets.ViewList(this.addLayerModel, null, this);
        this.modelEvents() ;

        this.on("displayed", () => {
            GoogleMapsLoader.load((google) => {
                this.map = new google.maps.Map(this.el) ;

                this.layerViews.update(this.model.get("layers"));

                // hack to force the map to redraw
                setTimeout(() => {
                    google.maps.event.trigger(this.map, 'resize');
                    this.setViewport(this.model.get('initial_viewport'));
                }, 500);
            })
        })
    }

    modelEvents() {
        this.model.on("change:data_bounds", this.updateBounds, this);
    }

    setViewport(viewport) {
        const { type } = viewport;
        if (type === DATA_BOUNDS) {
            const bounds = this.model.get("data_bounds");
            this.setViewportFromBounds(bounds)
        }
        else if (type === ZOOM_CENTER) {
            const { zoom_level, center } = viewport
            this.setViewportFromZoomCenter(zoom_level, center);
        }
        else {
            console.error(`Unexpected viewport mode: ${viewportMode}`);
        }
    }

    setViewportFromZoomCenter(zoom_level, center) {
        const [lat, lng] = center;
        this.map.setCenter(new google.maps.LatLng(lat, lng));
        this.map.setZoom(zoom_level);
    }

    setViewportFromBounds(bounds) {
        const [[latBL, lngBL], [latTR, lngTR]] = bounds
        const boundBL = new google.maps.LatLng(latBL, lngBL)
        const boundTR = new google.maps.LatLng(latTR, lngTR)
        const boundsAsGoogle = new google.maps.LatLngBounds(boundBL, boundTR)
        this.map.fitBounds(boundsAsGoogle);
    }

    addLayerModel(childModel) {
        return this.create_child_view(
            childModel, {mapView: this}
        ).then((childView) => {
            childView.addToMapView(this) ;
            return childView;
        })
    }

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
                    .then(layers => {
                        const layersText = layers.join(', ');
                        const layersWord = layers.length > 1 ? 'layers' : 'layer';
                        const errorMessage =
                            `Cannot download ${layersWord}: ${layersText}. ` +
                            `Remove these layers to export the map.`
                        return Promise.reject(errorMessage)
                    })
                return error
            }
        })
    }

}

// Models

export class PlainmapModel extends widgets.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...defaultAttributes,
            _view_name: "PlainmapView",
            _model_name: "PlainmapModel",
            width: "600px",
            height: "400px",
            data_bounds: null,
            initial_viewport: { type: DATA_BOUNDS }
        };
    }
        
    static serializers = {
        ...widgets.DOMWidgetModel.serializers,
        layers: {deserialize: widgets.unpack_models},
    }
}
