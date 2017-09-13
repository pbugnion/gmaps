
import * as widgets from '@jupyter-widgets/base';
import $ from 'jquery'
import _ from 'underscore'

import { Store } from './ReduceStore';
import { Dispatcher } from 'flux'

import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';
import { defaultAttributes } from './defaults'


class DrawingStore extends Store {
    areEqual(firstState, secondState) {
        return _.isEqual(firstState, secondState)
    }

    reduce(prevState, action) {
        switch (action.type) {
            case 'MODE_CHANGE':
                const { mode } = action.payload
                const newState = { options: { mode } }
                return newState;
            default:
                return prevState
        }
    }
}


class DrawingActions {
    static modeChange(mode) {
        return { type: 'MODE_CHANGE', payload: { mode } };
    }
}


export class DrawingLayerModel extends GMapsLayerModel {

    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.dispatcher = new Dispatcher();
        this.store = new DrawingStore({options: attributes.options}, this.dispatcher);
        this.store.addListener(() => this._onStoreChange());
        this._initializeControls();
        this._bindModelEvents();
    }

    // Handle changes made in the Python layer
    _bindModelEvents() {
        this.on(
            'change:toolbar_controls', 
            () => this._initializeControls()
        );
        this.on('change:options', () => {
            const { mode } = this.get('options');
            this.dispatcher.dispatch(DrawingActions.modeChange(mode));
        })
    }

    _initializeControls() {
        const controls = this.get('toolbar_controls');
        if (controls) {
            controls.set('dispatcher', this.dispatcher);
            controls.set('store', this.store)
        }
    }

    _onStoreChange() {
        const { options } = this.store.getState();
        const message = this._newOptionsMessage(options)
        this.send(message, this.callbacks());
    }

    _newOptionsMessage(options) {
        const payload = {
            event: 'NEW_OPTIONS',
            payload: options
        }
        return payload
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
            dispatcher: null,
            store: null            
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
        this.model.store.addListener(() => { this._onNewOptions() })
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
        const { options } = this.model.store.getState()
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

        this._setStore();
        this.model.on('change:store', () => this._setStore())

        this._onNewOptions();

        $container.append(this.$disableButton, this.$markerButton);
        this.$el.append($container);
        this.$el.addClass('additional-controls')
    }

    _setStore() {
        const store = this.model.get('store');
        if (store) {
            store.addListener(() => this._onNewOptions());
        }
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
            const dispatcher = this.model.get('dispatcher');
            dispatcher.dispatch(DrawingActions.modeChange(mode));
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
        const store = this.model.get('store');
        if (store) {
            const { options } = store.getState();
            const { mode } = options;
            this._setButtonSelected(mode);
        }
    }
}