
import widgets from 'jupyter-js-widgets';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

/* Base class for markers.
 * This sets options common to the different types of markers.
 *
 * Subclasses are responsible for implementing the `getStyleOptions`
 * method, which must return an object of additional options
 * to add to the marker, and `setStyleEvents`, which must set
 * up events for those styles.
 */
const BaseMarkerView = widgets.WidgetView.extend({
    render() {
        const [lat, lng] = this.model.get("location")
        const title = this.model.get("hover_text")
        const styleOptions = this.getStyleOptions()
        const markerOptions = {
            position: {lat, lng},
            draggable: false,
            title,
            ...styleOptions
        }
        this.marker = new google.maps.Marker(markerOptions)
        this.infoBox = this.renderInfoBox()
        this.infoBoxListener = null;
        this.mapView = null;
        this.modelEvents()
    },

    displayInfoBox() {
        return this.model.get("display_info_box");
    },

    renderInfoBox() {
        const infoBox = new google.maps.InfoWindow({
            content: this.model.get("info_box_content")
        });
        return infoBox ;
    },

    toggleInfoBoxListener() {
        if (this.displayInfoBox()) {
            this.infoBoxListener = this.marker.addListener(
                "click",
                () => { this.infoBox.open(this.mapView.map, this.marker) }
            )
        }
        else {
            if (this.infoBoxListener !== null) {
                this.infoBoxListener.remove()
            }
        }
    },

    addToMapView(mapView) {
        this.mapView = mapView;
        this.marker.setMap(mapView.map);
        this.toggleInfoBoxListener();
    },

    modelEvents() {
        // Simple properties:
        const properties = [
            ['title', 'hover_text']
        ]

        properties.forEach(([nameInView, nameInModel]) => {
            const callback = (
                () => {
                  this.marker.set(
                  nameInView, this.model.get(nameInModel))
                }
            )
            this.model.on(`change:${nameInModel}`, callback, this)
        })

        const infoBoxProperties = [
            ['content', 'info_box_content']
        ]
        infoBoxProperties.forEach(([nameInView, nameInModel]) => {
            const callback = (
                () => {
                    this.infoBox.set(
                    nameInView, this.model.get(nameInModel))
                }
            )
            this.model.on(`change:${nameInModel}`, callback, this)
        })

        this.model.on("change:display_info_box", () => {
            this.toggleInfoBoxListener()
        }, this)

        this.setStyleEvents()
    }


})

export const SymbolView = BaseMarkerView.extend({

    getStyleOptions() {
        const fillColor = this.model.get("fill_color")
        const strokeColor = this.model.get("stroke_color")
        const fillOpacity = this.model.get("fill_opacity")
        const strokeOpacity = this.model.get("stroke_opacity")
        const scale = this.model.get("scale")
        return {
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale,
                fillColor,
                strokeColor,
                fillOpacity,
                strokeOpacity
            }
        }
    },

    setStyleEvents() {
        const iconProperties = [
            ['strokeColor', 'stroke_color'],
            ['fillColor', 'fill_color'],
            ['scale', 'scale'],
            ['stroke_opacity', 'stroke_opacity'],
            ['fillOpacity', 'fill_opacity']
        ]
        iconProperties.forEach(([nameInView, nameInModel]) => {
            const callback = ( () => {
                const newIcon = Object.assign({}, this.marker.getIcon())
                newIcon[nameInView] = this.model.get(nameInModel)
                this.marker.setIcon(newIcon)
            })
            this.model.on(`change:${nameInModel}`, callback, this)
        })
    }
})


export const MarkerView = BaseMarkerView.extend({

    getStyleOptions() {
        this.modelEvents()
        const label = this.model.get("label")
        return { label }
    },

    setStyleEvents() {
        const properties = [
            ['label', 'label']
        ]
        properties.forEach(([nameInView, nameInModel]) => {
            const callback = (
                () => {
                  this.marker.set(
                  nameInView, this.model.get(nameInModel))
                }
            )
            this.model.on(`change:${nameInModel}`, callback, this)
        })
    }

})


export const MarkerLayerView = GMapsLayerView.extend({
    render() {
        this.markerViews = new widgets.ViewList(this.addMarker, null, this)
        this.markerViews.update(this.model.get("markers"))
    },

    addToMapView(mapView) {
        this.markerViews.forEach(view => view.addToMapView(mapView))
    },

    addMarker(childModel) {
        return this.create_child_view(childModel)
            .then((childView) => {
                childView.addToMapView(this.mapView)
                return childView
            })
    }
})


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


export const SymbolModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "SymbolView",
        _model_name: "SymbolModel"
    })
})

export const MarkerModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "MarkerView",
        _model_name: "MarkerModel"
    })
})

export const MarkerLayerModel = GMapsLayerModel.extend({
    defaults: _.extend({}, GMapsLayerModel.prototype.defaults, {
        _view_name: "MarkerLayerView",
        _model_name: "MarkerLayerModel"
    }),
}, {
    serializers: _.extend({
            markers: {deserialize: widgets.unpack_models}
    }, widgets.DOMWidgetModel.serializers)
})
