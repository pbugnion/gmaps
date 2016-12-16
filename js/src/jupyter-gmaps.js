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
    loadConfiguration() {
        const modelConfiguration = this.model.get("configuration")
        reloadGoogleMaps(modelConfiguration)
    }
}


// Views

const GMapsLayerView = widgets.WidgetView.extend({
    initialize(parameters) {
        GMapsLayerView.__super__.initialize.apply(this, arguments)
        this.mapView = this.options.mapView
    }
})


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


const HeatmapLayerBaseView = GMapsLayerView.extend({
    render() {
        this.modelEvents() ;
        GoogleMapsLoader.load((google) => {
            this.heatmap = new google.maps.visualization.HeatmapLayer({
                data: this.getData(),
                radius: this.model.get("point_radius"),
                maxIntensity: this.model.get("max_intensity"),
                dissipating: this.model.get("dissipating"),
                opacity: this.model.get("opacity"),
                gradient: this.model.get("gradient")
            }) ;
        });
    },

    addToMapView(mapView) {
        this.heatmap.setMap(mapView.map)
    },

    modelEvents() {
        // Simple properties:
        // [nameInView, nameInModel]
        const properties = [
            ['maxIntensity', 'max_intensity'],
            ['opacity', 'opacity'],
            ['radius', 'point_radius'],
            ['dissipating', 'dissipating'],
            ['gradient', 'gradient']
        ]
        properties.forEach(([nameInView, nameInModel]) => {
            const callback = (
                () => this.heatmap.set(nameInView, this.model.get(nameInModel))
            )
            this.model.on(`change:${nameInModel}`, callback, this)
        })
    },

    get_data() {},

})

export const SimpleHeatmapLayerView = HeatmapLayerBaseView.extend({
    getData() {
        const data = this.model.get("data")
        const dataAsGoogle = new google.maps.MVCArray(
            data.map(([lat, lng]) => new google.maps.LatLng(lat, lng))
        )
        return dataAsGoogle
    }
})


export const WeightedHeatmapLayerView = HeatmapLayerBaseView.extend({
    getData() {
        const data = this.model.get("data")
        const dataAsGoogle = new google.maps.MVCArray(
            data.map(([lat, lng, weight]) => {
                const location = new google.maps.LatLng(lat, lng)
                return { location: location, weight: weight }
            })
        );
        return dataAsGoogle
    }
})

/* Base class for markers.
 * This sets options common to the different types of markers.
 *
 * Subclasses are responsible for implementing the `getStyleOptions`
 * method, which must return an object of additional options
 * to add to the marker, and `setStyleEvents`, which must set
 * up events for those styles.
 */
export const BaseMarkerView = widgets.WidgetView.extend({
    render() {
        const [lat, lng] = this.model.get("location")
        const title = this.model.get("hover_text")
        const infoBoxHtml = this.model.get("info_html")
        const styleOptions = this.getStyleOptions()
        const markerOptions = {
            position: {lat, lng},
            draggable: false,
            title,
            ...styleOptions
        }
        this.marker = new google.maps.Marker(markerOptions)
        this.infoWindow = new google.maps.InfoWindow({
            content: infoBoxHtml
        });
        this.modelEvents()
    },

    addToMapView(mapView) {
        let marker = this.marker;
        let infoWindow = this.infoWindow;
        marker.setMap(mapView.map);
        marker.addListener('click', function() {
            infoWindow.open(mapView.map, marker);
        });
    },

    modelEvents() {
        // Simple properties:
        const properties = [
            ['title', 'hover_text']
        ]
        const infoBoxProperties = [
             ['content', 'info_html']
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
        
         infoBoxProperties.forEach(([nameInView, nameInModel]) => {
             const callback = (
                 () => {
                     this.infoWindow.set(
                     nameInView, this.model.get(nameInModel))
                 }
             )
             this.model.on(`change:${nameInModel}`, callback, this)
         })

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

})

_.extend(PlainmapView.prototype, ConfigurationMixin);


// Models

export const GMapsLayerModel = widgets.WidgetModel.extend({
    defaults: _.extend({}, widgets.WidgetModel.prototype.defaults, {
        _view_name : 'GMapsLayerView',
        _model_name : 'GMapsLayerModel',
        _view_module : 'jupyter-gmaps',
        _model_module : 'jupyter-gmaps'
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
