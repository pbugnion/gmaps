
import * as widgets from '@jupyter-widgets/base';
import $ from 'jquery'
import _ from 'underscore'
import * as Backbone from 'backbone'

import { Store } from './Store';
import { Dispatcher } from 'flux'

import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';
import { defaultAttributes } from './defaults'
import { latLngToArray } from './services/googleConverters'


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

    static newLine(start, end) {
        const payload = {
            event: 'FEATURE_ADDED',
            payload: {
                featureType: 'LINE',
                start,
                end
            }
        }
        return payload
    }

    static newPolygon(path) {
        const payload = {
            event: 'FEATURE_ADDED',
            payload: {
                featureType: 'POLYGON',
                path
            }
        }
        return payload ;
    }

    static deleteFeature(modelId) {
        const payload = {
            event: 'FEATURE_DELETED',
            payload: {
                modelId
            }
        }
        return payload
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
        this._clickHandler = null;
    }

    render() {
        this.features = new widgets.ViewList(this.addFeature, this.removeFeature, this)
        this.features.update(this.model.get('features'))
        this.model.on(
            'change:features',
            () => {
                this.features.update(this.model.get('features'))
                    .then(features => {
                        if (this._clickHandler) {
                            this._clickHandler.onNewFeatures(features);
                        }
                    })
            },
        );
        this.model.store.addListener(() => { this._onNewMode() })
        this._clickHandler = null
    }

    addFeature(childModel) {
        return this.create_child_view(childModel)
            .then((childView) => {
                childView.addToMapView(this.mapView)
                return childView
            })
    }

    removeFeature(featureView) {
        featureView.removeFromMapView();
    };

    _onNewMode() {
        const { mode } = this.model.store.getState()
        this._setClickListener(this.mapView.map, mode);
    }

    _setClickListener(map, mode) {
        if (mode === 'DISABLED') {
            if (this._clickHandler) { this._clickHandler.remove(); }
        } else if (mode === 'MARKER') {
            if (this._clickHandler) { this._clickHandler.remove(); }
            this._clickHandler = new MarkerClickHandler(
                map,
                (latitude, longitude) => this.send(DrawingMessages.newMarker(latitude, longitude))
            )
        } else if (mode === 'LINE') {
            if (this._clickHandler) { this._clickHandler.remove(); }
            this._clickHandler = new LineClickHandler(
                map,
                ([start, end]) => this.send(DrawingMessages.newLine(start, end))
            )
        } else if (mode === 'POLYGON') {
            if (this._clickHandler) { this._clickHandler.remove(); }
            this._clickHandler = new PolygonClickHandler(
                map,
                path => this.send(DrawingMessages.newPolygon(path))
            )
        } else if (mode === 'DELETE') {
            if (this._clickHandler) { this._clickHandler.remove(); }
            const sendDeleteMessage =
                (feature) => this.send(
                    DrawingMessages.deleteFeature(feature.model.model_id)
                )
            Promise.all(this.features.views).then(features => {
                this._clickHandler = new DeleteClickHandler(
                    features, sendDeleteMessage
                );
            })
        }
    }

    addToMapView(mapView) {
        const { mode } = this.model.store.getState()
        this._setClickListener(mapView.map, mode)
    };
}

class MarkerClickHandler {
    constructor(map, onNewMarker) {
        this._clickListener = map.addListener('click', event => {
            const { latLng } = event;
            const latitude = latLng.lat();
            const longitude = latLng.lng();
            onNewMarker(latitude, longitude)
        });
    }

    onNewFeatures(features) {}

    remove() {
        this._clickListener.remove();
    }
}

class LineClickHandler {
    constructor(map, onNewLine) {
        this.currentLine = null;
        this.map = map;
        this._clickListener = map.addListener('click', event => {
            const { latLng } = event;
            if (this.currentLine === null) {
                this.currentLine = this._createLineStartingAt(latLng);
            } else {
                const path = this._finishLineAt(this.currentLine, latLng);
                this.currentLine.setMap(null);
                this.currentLine = null;
                onNewLine(path)
            }
        });
        this._moveListener = map.addListener('mousemove', event => {
            if (this.currentLine !== null) {
                const { latLng } = event;
                this.currentLine.getPath().setAt(1, latLng);
            }
        });
    }

    onNewFeatures(features) {}

    _createLineStartingAt(latLng) {
        const path = new google.maps.MVCArray([latLng, latLng])
        const line = new google.maps.Polyline({ path, clickable: false })
        line.setMap(this.map);
        return line
    }

    _finishLineAt(line, latLngEnd) {
        const linePath = line.getPath();
        const latLngStart = linePath.getAt(0)
        const [latitudeStart, longitudeStart] = latLngToArray(latLngStart);
        const [latitudeEnd, longitudeEnd] = latLngToArray(latLngEnd);
        const path = [
            [latitudeStart, longitudeStart],
            [latitudeEnd, longitudeEnd]
        ]
        return path;
    }

    remove() {
        this._clickListener.remove();
        this._moveListener.remove();
        if (this.currentLine) {
            this.currentLine.setMap(null);
        }
    }
}


class PolygonClickHandler {
    constructor(map, onNewPolygon) {
        this.map = map;
        this.currentPolygon = null;
        this.map.setOptions({ disableDoubleClickZoom: true })
        this._clickListener = map.addListener('click', event => {
            const { latLng } = event;
            if (this.currentPolygon === null) {
                this.currentPolygon = this._createPolygonStartingAt(latLng);
            } else {
                this._finishCurrentLine(latLng);
            }
        });
        this._dblclickListener = map.addListener('dblclick', event => {
            if (this.currentPolygon !== null) {
                const path = this._completePolygon();
                this.currentPolygon.setMap(null);
                this.currentPolygon = null;
                if (path.length > 2) {
                    // Only dispatch an event if there are at
                    // least three points. Otherwise, it's
                    // likely to just be user error.
                    onNewPolygon(path);
                }
            };
        })
        this._moveListener = map.addListener('mousemove', event => {
            if (this.currentPolygon !== null) {
                const { latLng } = event;
                const currentPath = this.currentPolygon.getPath();
                currentPath.setAt(currentPath.getLength()-1, latLng);
            }
        });
    }

    onNewFeatures(features) {}

    remove() {
        this._clickListener.remove();
        this._dblclickListener.remove();
        this._moveListener.remove();
        if (this.currentPolygon) {
            this.currentPolygon.setMap(null);
        }
        this.map.setOptions({ disableDoubleClickZoom: false })
    }

    _createPolygonStartingAt(latLng) {
        const path = new google.maps.MVCArray([latLng, latLng])
        const polygon = new google.maps.Polyline({ path, clickable: false })
        polygon.setMap(this.map);
        return polygon;
    }

    _finishCurrentLine(latLng) {
        const currentPath = this.currentPolygon.getPath();
        const lastLatLng = currentPath.getAt(currentPath.getLength()-1);
        currentPath.push(lastLatLng);
    }

    _completePolygon() {
        const currentPath = this.currentPolygon.getPath();
        const pathElems = currentPath.getArray().map(point => latLngToArray(point))
        // last element is duplicate since we always introduce
        // two new elements on click.
        const path = _.initial(pathElems);
        return path;
    }
}


class DeleteClickHandler {
    constructor(features, onDeleteFeature) {
        this.eventBus = { ...Backbone.Events };
        this.onDeleteFeature = onDeleteFeature
        this.currentFeatures = features;
        this._registerFeatureListeners(features)
    }

    onNewFeatures(features) {
        this._deregisterCurrentFeatureListeners()
        this.currentFeatures = features;
        this._registerFeatureListeners(features)
    }

    remove() {
        this._deregisterCurrentFeatureListeners()
    }

    _deregisterCurrentFeatureListeners() {
        this.currentFeatures.forEach(
            feature => feature.restoreClickable()
        )
        this.eventBus.stopListening();
    }

    _registerFeatureListeners(features) {
        features.forEach(feature => {
            feature.ensureClickable();
            this.eventBus.listenTo(
                feature,
                'click',
                () => this.onDeleteFeature(feature)
            )
        })
    }
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

        const $disableButton = this._createModeButton(
            'fa fa-ban', 'Disable drawing layer'
        )
        this._createButtonEvent($disableButton, 'DISABLED')
        const $markerButton = this._createModeButton(
            'fa fa-map-marker', 'Drawing layer: switch to \'marker\' mode'
        )
        this._createButtonEvent($markerButton, 'MARKER')
        const $lineButton = this._createModeButton(
            'gmaps-icon line', 'Drawing layer: switch to \'line\' mode'
        )
        this._createButtonEvent($lineButton, 'LINE')
        const $polygonButton = this._createModeButton(
            'gmaps-icon polygon', 'Drawing layer: switch to \'polygon\' mode'
        )
        this._createButtonEvent($polygonButton, 'POLYGON')
        const $deleteButton = this._createModeButton(
            'fa fa-trash', 'Drawing layer: delete features'
        )
        this._createButtonEvent($deleteButton, 'DELETE')

        this.modeButtons = {
            'DISABLED': $disableButton,
            'MARKER': $markerButton,
            'LINE': $lineButton,
            'POLYGON': $polygonButton,
            'DELETE': $deleteButton
        }

        $container.append(
            $disableButton,
            $markerButton,
            $lineButton,
            $polygonButton,
            $deleteButton
        );
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
    _createModeButton(icon, hoverText) {
        const $button = $('<button />')
        $button
            .addClass('btn btn-default')
            .attr('title', hoverText)
            .append('<i />')
            .addClass(`${icon}`)

        return $button
    }

    _createButtonEvent($button, mode) {
        $button.click(() => {
            const dispatcher = this.model.get('dispatcher');
            dispatcher.dispatch(DrawingActions.modeChange(mode));
        })
    }

    _setButtonSelected(selectedMode) {
        Object.entries(this.modeButtons).forEach(([mode, $button]) => {
            if (mode === selectedMode) {
                $button.addClass('active')
            } else {
                $button.removeClass('active')
            }
        });
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
