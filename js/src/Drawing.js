
import * as widgets from '@jupyter-widgets/base';
import $ from 'jquery'

import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';
import { defaultAttributes } from './defaults'


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


export class DrawingControlsModel extends widgets.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...defaultAttributes,
            _model_name: 'DrawingControlsModel',
            _view_name: 'DrawingControlsView',
            show_controls: true,
            options: {mode: 'MARKER'}
        }
    }
};


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


export class DrawingControlsView extends widgets.DOMWidgetView {
    render() {
        const $container = $('<span />')
        $container
            .addClass('btn-group')
            .attr('data-toggle', 'buttons');

        this.$disableButton = this._createModeButton('fa-ban')
        this._createButtonEvent(this.$disableButton, 'DISABLED')
        this.$markerButton = this._createModeButton('fa-map-marker')
        this._createButtonEvent(this.$markerButton, 'MARKER')

        this._onNewOptions();
        this.model.on('change:options', () => this._onNewOptions())

        $container.append(this.$disableButton, this.$markerButton);
        this.$el.append($container);
        this.$el.addClass('additional-controls')
    }

    _createModeButton(icon) {
        const $button = $('<button />')
        $button
            .addClass('btn btn-default')
            .append('<i />')
            .addClass(`fa ${icon}`)
        
        return $button
    }

    _createButtonEvent($button, mode) {
        $button.click(() => {
            this._setButtonSelected(mode);
            this.model.set('options', { mode });
        })
    }

    _setButtonSelected(mode) {
        if (mode === 'MARKER') {
            this.$markerButton.addClass('active')
            this.$disableButton.removeClass('active')
        } else if (mode === 'DISABLED') {
            this.$markerButton.removeClass('active')
            this.$disableButton.addClass('active')
        }
    }

    _onNewOptions() {
        const { mode } = this.model.get('options')
        this._setButtonSelected(mode);
    }
}