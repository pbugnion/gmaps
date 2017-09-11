
import * as widgets from '@jupyter-widgets/base';

import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';


export class DrawingLayerModel extends GMapsLayerModel {

    initialize(attributes, options) {
        super.initialize(attributes, options);
        const controls = this.get('toolbar_controls');
        if (controls) {
            controls.on(
                'change:options', 
                (model, newOptions) => this.set('options', newOptions)
            )
        }
    }

    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'DrawingLayerView',
            _model_name: 'DrawingLayerModel',
            overlays: [],
            options: {mode: 'MARKER'},
            toolbar_controls: null
        }
    }

    static serializers = {
        ...widgets.DOMWidgetModel.serializers,
        overlays: {deserialize: widgets.unpack_models},
        toolbar_controls: {deserialize: widgets.unpack_models}
    }
}


export class DrawingLayerView extends GMapsLayerView {
    constructor(options) {
        super(options);
        this.canDownloadAsPng = false;
    }

    render() {
        this.overlays = new widgets.ViewList(this.addMarker, this.removeMarker, this)
        this.overlays.update(this.model.get('overlays'))
        this.model.on(
            'change:overlays', 
            () => { this.overlays.update(this.model.get('overlays')) },
        );
        this.model.on('change:options', () => this._onNewOptions());
        this._clickListener = null
    }

    addMarker(childModel) {
        return this.create_child_view(childModel)
            .then((childView) => {
                childView.addToMapView(this.mapView)
                return childView
            })
    }

    removeMarker(markerView) {
        markerView.removeFromMapView();
    };

    _onNewOptions() {
        const options = this.model.get('options');
        this._setClickListener(this.mapView.map, options);
    }

    _setClickListener(map, options) {
        if (options.mode === 'DISABLED') {
            if (this._clickListener) { this._clickListener.remove(); }
        } else {
            if (this._clickListener) { this._clickListener.remove(); }
            this._clickListener = map.addListener('click', event => {
                const { latLng } = event;
                const latitude = latLng.lat();
                const longitude = latLng.lng();
                this.send(this.newMarkerMessage(latitude, longitude))
            });
        }
    }

    addToMapView(mapView) {
        const options = this.model.get('options');
        this._setClickListener(mapView.map, options)
    };

    newMarkerMessage(latitude, longitude) {
        const payload = {
            event: 'OVERLAY_ADDED',
            payload: {
                overlayType: 'MARKER',
                latitude,
                longitude
            }
        };
        return payload;
    }

}