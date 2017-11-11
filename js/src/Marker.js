
import * as widgets from '@jupyter-widgets/base';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';


export class SymbolModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: "SymbolView",
            _model_name: "SymbolModel"
        }
    }
}


export class MarkerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: "MarkerView",
            _model_name: "MarkerModel"
        }
    }
}


export class MarkerLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: "MarkerLayerView",
            _model_name: "MarkerLayerModel"
        }
    }

    static serializers = {
        ...widgets.DOMWidgetModel.serializers,
        markers: {deserialize: widgets.unpack_models}
    }
}


/* Base class for markers.
 * This sets options common to the different types of markers.
 *
 * Subclasses are responsible for implementing the `getStyleOptions`
 * method, which must return an object of additional options
 * to add to the marker, and `setStyleEvents`, which must set
 * up events for those styles.
 */
class BaseMarkerView extends widgets.WidgetView {
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
        this.restoreClickable();
        this.infoBoxListener = null;
        this.mapView = null;
        this.modelEvents()
        this.marker.addListener('click', event => this.trigger('click'));
    }

    ensureClickable() {
        this.marker.setClickable(true);
    }

    restoreClickable() {
        const clickable = this.displayInfoBox();
        this.marker.setClickable(clickable);
    }

    displayInfoBox() {
        return this.model.get("display_info_box");
    }

    renderInfoBox() {
        const infoBox = new google.maps.InfoWindow({
            content: this.model.get("info_box_content")
        });
        return infoBox ;
    }

    toggleInfoBoxListener() {
        this.restoreClickable();
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
    }

    addToMapView(mapView) {
        this.mapView = mapView;
        this.marker.setMap(mapView.map);
        this.toggleInfoBoxListener();
    }

    removeFromMapView() {
        this.mapView = null;
        this.marker.setMap(null);
        if (this.infoBoxListener !== null) {
            this.infoBoxListener.remove();
        }
    }

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
}

export class SymbolView extends BaseMarkerView {

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
    }

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
}


export class MarkerView extends BaseMarkerView {

    getStyleOptions() {
        this.modelEvents()
        const label = this.model.get("label")
        return { label }
    }

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

}


export class MarkerLayerView extends GMapsLayerView {
    constructor(options) {
        super(options);
        this.canDownloadAsPng = true;
    }

    render() {
        this.markerViews = new widgets.ViewList(this.addMarker, null, this)
        this.markerViews.update(this.model.get("markers"))
    }

    // No need to do anything here since the markers are added
    // when they are deserialized
    addToMapView(mapView) { }

    addMarker(childModel) {
        return this.create_child_view(childModel)
            .then((childView) => {
                childView.addToMapView(this.mapView)
                return childView
            })
    }
}
