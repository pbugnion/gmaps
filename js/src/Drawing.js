
import * as widgets from '@jupyter-widgets/base';
import $ from 'jquery'
import _ from 'underscore'

import { Store } from './Store';
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
            case 'MODE_CHANGED': {
                const { mode } = action.payload
                const newState = { ...prevState, mode }
                return newState;
            }
            case 'SHOW_CONTROLS_CHANGED': {
                const { showControls } = action.payload
                const newState = { ...prevState, showControls }
                return newState
            }
            default:
                return prevState
        }
    }
}

// Action creators for changing the store
class DrawingActions {
    static modeChange(mode) {
        return { type: 'MODE_CHANGED', payload: { mode } };
    }

    static showControlsChange(showControls) {
        return { 
            type: 'SHOW_CONTROLS_CHANGED', 
            payload: { showControls } 
        };
    }

}


// Messages for changing the backend state
class DrawingMessages {
    static newMarker(latitude, longitude) {
        const payload = {
            event: 'FEATURE_ADDED',
            payload: {
                featureType: 'MARKER',
                latitude,
                longitude
            }
        };
        return payload;
    }

    static modeChange(mode) {
        const payload = {
            event: 'MODE_CHANGED',
            payload: { mode }
        }
        return payload;
    }
}


export class DrawingLayerModel extends GMapsLayerModel {

    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.dispatcher = new Dispatcher();
        const initialState = this._initialStoreState(attributes)
        this.store = new DrawingStore(initialState, this.dispatcher);
        this.store.addListener(() => this._onStoreChange());
        this._initializeControls();
        this._bindModelEvents();
    }

    _initialStoreState(attributes) {
        return {
            mode: attributes.mode,
            showControls: attributes.toolbar_controls.get('show_controls')
        }
    }

    // Handle changes made in the Python layer,
    // propagating them to the store if necessary
    _bindModelEvents() {
        this.on(
            'change:toolbar_controls', 
            () => this._initializeControls()
        );
        this.on('change:mode', () => {
            const mode = this.get('mode');
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
        const { mode } = this.store.getState();
        const message = DrawingMessages.modeChange(mode);
        this.send(message, this.callbacks());
    }

    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'DrawingLayerView',
            _model_name: 'DrawingLayerModel',
            features: [],
            mode: 'MARKER',
            toolbar_controls: null
        }
    }

    static serializers = {
        ...widgets.DOMWidgetModel.serializers,
        features: {deserialize: widgets.unpack_models},
        toolbar_controls: {deserialize: widgets.unpack_models}
    }
}


export class DrawingControlsModel extends widgets.DOMWidgetModel {
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this._bindModelEvents();
    }

    // Handle changes made in the Python layer,
    // propagating them to the store if necessary
    _bindModelEvents() {
        this.on('change:show_controls', () => {
            const showControls = this.get('show_controls');
            const dispatcher = this.get('dispatcher')
            if (dispatcher) {
                const message = DrawingActions.showControlsChange(showControls);
                dispatcher.dispatch(message)
            }
        });
    }

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
        this.features = new widgets.ViewList(this.addMarker, this.removeMarker, this)
        this.features.update(this.model.get('features'))
        this.model.on(
            'change:features', 
            () => { this.features.update(this.model.get('features')) },
        );
        this.model.store.addListener(() => { this._onNewMode() })
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

    _onNewMode() {
        const { mode } = this.model.store.getState()
        this._setClickListener(this.mapView.map, mode);
    }

    _setClickListener(map, mode) {
        if (mode === 'DISABLED') {
            if (this._clickListener) { this._clickListener.remove(); }
        } else {
            if (this._clickListener) { this._clickListener.remove(); }
            this._clickListener = map.addListener('click', event => {
                const { latLng } = event;
                const latitude = latLng.lat();
                const longitude = latLng.lng();
                this.send(DrawingMessages.newMarker(latitude, longitude))
            });
        }
    }

    addToMapView(mapView) {
        const { mode } = this.model.store.getState()
        this._setClickListener(mapView.map, mode)
    };

}


export class DrawingControlsView extends widgets.DOMWidgetView {
    render() {
        this._createLayout();
        this._setInitialState();
    }

    _createLayout() {
        const $container = $('<span />')
        $container
            .addClass('btn-group')
            .attr('data-toggle', 'buttons');

        this.$disableButton = this._createModeButton('fa-ban')
        this._createButtonEvent(this.$disableButton, 'DISABLED')
        this.$markerButton = this._createModeButton('fa-map-marker')
        this._createButtonEvent(this.$markerButton, 'MARKER')

        $container.append(this.$disableButton, this.$markerButton);
        this.$el.append($container);
        this.$el.addClass('additional-controls')
    }

    _setInitialState() {
        this._setStore();
        this.model.on('change:store', () => this._setStore())

        this._onNewMode();
        this._onNewShowControls();
    }

    _setStore() {
        const store = this.model.get('store');
        if (store) {
            store.addListener(() => this._onNewMode());
            store.addListener(() => this._onNewShowControls());
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

    _setVisibility(showControls) {
        this.$el.toggle(showControls)
    }

    _onNewMode() {
        const store = this.model.get('store');
        if (store) {
            const { mode } = store.getState();
            this._setButtonSelected(mode);
        }
    }

    _onNewShowControls() {
        const store = this.model.get('store');
        if (store) {
            const { showControls } = store.getState();
            this._setVisibility(showControls);
        }
    }
}