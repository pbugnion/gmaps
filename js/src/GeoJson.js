import widgets from 'jupyter-js-widgets';
import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';


export const GeoJsonLayerModel = GMapsLayerModel.extend({
    defaults: {
        ...GMapsLayerModel.prototype.defaults,
        _view_name: "GeoJsonLayerView",
        _model_name: "GeoJsonLayerModel"
    }
}, {
    serializers: {
        features: {deserialize: widgets.unpack_models},
        ...widgets.DOMWidgetModel.serializers
    }
})


export const GeoJsonFeatureModel = GMapsLayerModel.extend({
    defaults: {
        ...GMapsLayerModel.prototype.defaults,
        _view_name: "GeoJsonFeatureView",
        _model_name: "GeoJsonFeatureModel"
    }
});


export const GeoJsonFeatureView = GMapsLayerView.extend({

    // nameInView -> name_in_model
    styleProperties: [
          ['fillColor', 'fill_color'],
          ['fillOpacity', 'fill_opacity'],
          ['strokeColor', 'stroke_color'],
          ['strokeOpacity', 'stroke_opacity'],
          ['strokeWeight', 'stroke_weight']
    ],

    render() {
        this.modelEvents() ;
        this.geojson = this.model.get("feature")
        const style = this.styleProperties.reduce(
            (acc, [nameInView, nameInModel]) => {
              return {...acc, [nameInView]: this.model.get(nameInModel)}
            },
            {}
        )
        this.geojson.properties =
            this.geojson.properties ? this.geojson.properties : {}
        this.geojson.properties.style = style
    },

    addToMapView(mapView) {
        this.mapView = mapView
        mapView.map.data.addGeoJson(this.geojson)
    },

    modelEvents() {
        this.styleProperties.forEach(([nameInView, nameInModel]) => {
            const callback = (() => {
                this.geojson.properties.style = {
                    ...this.geojson.properties.style,
                    [nameInView]: this.model.get(nameInModel)
                }
                this.mapView.map.data.setStyle(
                    (feature) => feature.getProperty('style'))
            })
            this.model.on(`change:${nameInModel}`, callback, this)
        })
    }

})


export const GeoJsonLayerView = GMapsLayerView.extend({

    canDownloadAsPng: true,

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
