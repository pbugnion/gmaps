import * as widgets from '@jupyter-widgets/base';
import _ from 'underscore';
import $ from 'jquery';

import GoogleMapsLoader from 'google-maps';

import {downloadElementAsPng} from './services/downloadElement';
import {stringToMapType, mapTypeToString} from './services/googleConverters.js';
import {GMapsLayerView, GMapsLayerModel} from './GMapsLayer';
import {defaultAttributes} from './defaults';
import {globalEvents, globalEventBus} from './GlobalEvents';
import {mapEventTypes, MapEvents} from './MapEvents';
import {newEventBus} from './services/eventBus';

if (typeof window.gm_authFailure === 'undefined') {
    window.gm_authFailure = function() {
        // GoogleMaps Javascript API provides there no information
        // that can be accessed programatically. The best we can do
        // is point the user to the JavaScript console.
        globalEventBus.trigger(globalEvents.AUTHENTICATION_ERROR);
        GoogleMapsLoader.release();
    };
}

function needReloadGoogleMaps(configuration) {
    return GoogleMapsLoader.KEY !== configuration['api_key'];
}

function reloadGoogleMaps(configuration) {
    if (needReloadGoogleMaps(configuration)) {
        console.log('Releasing Google Maps');
        GoogleMapsLoader.release();
    }

    GoogleMapsLoader.LIBRARIES = ['visualization'];
    GoogleMapsLoader.VERSION = '3.34';
    if (
        configuration['api_key'] !== null &&
        configuration['api_key'] !== undefined
    ) {
        GoogleMapsLoader.KEY = configuration['api_key'];
    }
}

// Constants

const DATA_BOUNDS = 'DATA_BOUNDS';
const ZOOM_CENTER = 'ZOOM_CENTER';
const AUTHENTICATION_ERROR_MESSAGE = `
<p>
Something went wrong authenticating with Google Maps. This may be because you did not pass in an API key, or the key you passed in was incorrect.
</p>

<p>
Check the <a
href="https://documentation.concrete5.org/tutorials/how-open-browser-console-view-errors"
target="_blank">browser console</a>, look for errors that start with
<code>Google Maps API error</code> and compare the message against <a
href="https://developers.google.com/maps/documentation/javascript/error-messages"
target="_blank">the Google Maps documentation</a>.
</p>

<p>
If you see <code>InvalidKeyMapError</code>, the key you passed in is invalid. If you see <code>MissingKeyMapError</code>, you have not passed your API key to jupyter-gmaps. Pass an API key by writing <code>gmaps.configure(api_key="AI...")</code>.
</p>
`;

// Mixins

const ConfigurationMixin = superclass =>
    class extends superclass {
        loadConfiguration() {
            const modelConfiguration = this.model.get('configuration');
            reloadGoogleMaps(modelConfiguration);
        }
    };

// Views

export class PlainmapView extends ConfigurationMixin(widgets.DOMWidgetView) {
    render() {
        this.loadConfiguration();

        this.$mapDiv = $('<div>').css({height: '100%', width: '100%'});
        this.$el.append(this.$mapDiv);

        this.layerViews = new widgets.ViewList(this.addLayerModel, null, this);

        this.on('displayed', () => {
            GoogleMapsLoader.load(google => {
                const options = this.readOptions(google);
                this.map = new google.maps.Map(this.$mapDiv[0], options);
                this._modelEvents(google);
                this._viewEvents(google);

                this.layerViews.update(this.model.get('layers'));

                // hack to force the map to redraw
                setTimeout(() => {
                    google.maps.event.trigger(this.map, 'resize');
                    this.setViewport(this.model.get('initial_viewport'));
                }, 500);
            });
        });

        globalEventBus.on(globalEvents.AUTHENTICATION_ERROR, () => {
            this.$mapDiv.hide();
            this.$el.append(AUTHENTICATION_ERROR_MESSAGE);
        });
    }

    readOptions(google) {
        const options = {
            mapTypeId: stringToMapType(google, this.model.get('map_type')),
            gestureHandling: this.model.get('mouse_handling').toLowerCase(),
            tilt: this.model.get('tilt'),
        };
        return options;
    }

    _modelEvents(google) {
        this.model.on('change:map_type', () => {
            const mapTypeId = stringToMapType(
                google,
                this.model.get('map_type')
            );
            this.setMapOptions({mapTypeId});
        });

        this.model.on('change:tilt', () => {
            this.setMapOptions({tilt: this.model.get('tilt')});
        });

        this.model.on('change:mouse_handling', () => {
            const gestureHandling = this.model
                .get('mouse_handling')
                .toLowerCase();
            this.setMapOptions({gestureHandling});
        });
    }

    _viewEvents(google) {
        this.map.addListener('maptypeid_changed', () => {
            const newMapType = mapTypeToString(google, this.map.getMapTypeId());
            this.model.set('map_type', newMapType);
            this.touch();
        });
    }

    setMapOptions(options) {
        if (this.map) {
            this.map.setOptions(options);
        }
    }

    setViewport(viewport) {
        const {type} = viewport;
        if (type === DATA_BOUNDS) {
            const bounds = this.model.get('data_bounds');
            this.setViewportFromBounds(bounds);
        } else if (type === ZOOM_CENTER) {
            const {zoom_level, center} = viewport;
            this.setViewportFromZoomCenter(zoom_level, center);
        } else {
            console.error(`Unexpected viewport mode: ${viewportMode}`);
        }
    }

    setViewportFromZoomCenter(zoom_level, center) {
        const [lat, lng] = center;
        this.map.setCenter(new google.maps.LatLng(lat, lng));
        this.map.setZoom(zoom_level);
    }

    setViewportFromBounds(bounds) {
        const [[latBL, lngBL], [latTR, lngTR]] = bounds;
        const boundBL = new google.maps.LatLng(latBL, lngBL);
        const boundTR = new google.maps.LatLng(latTR, lngTR);
        const boundsAsGoogle = new google.maps.LatLngBounds(boundBL, boundTR);
        this.map.fitBounds(boundsAsGoogle);
    }

    addLayerModel(childModel) {
        return this.create_child_view(childModel, {mapView: this}).then(
            childView => {
                childView.addToMapView(this);
                return childView;
            }
        );
    }

    savePng() {
        const allLayers = Promise.all(this.layerViews.views);
        const canDownloadEveryLayer = allLayers.then(layers =>
            layers.every(layer => layer.canDownloadAsPng)
        );
        return canDownloadEveryLayer.then(canDownload => {
            if (canDownload) {
                return downloadElementAsPng(this.$el, 'map.png');
            } else {
                const nonDownloadableLayers = allLayers.then(layers =>
                    layers
                        .filter(layer => !layer.canDownloadAsPng)
                        .map(layer => layer.model.get('_view_name'))
                );
                const error = nonDownloadableLayers.then(layers => {
                    const layersText = layers.join(', ');
                    const layersWord = layers.length > 1 ? 'layers' : 'layer';
                    const errorMessage =
                        `Cannot download ${layersWord}: ${layersText}. ` +
                        `Remove these layers to export the map.`;
                    console.error(errorMessage);
                    this.model.events.trigger(
                        mapEventTypes.MAP_DOWNLOAD_ERROR,
                        MapEvents.downloadError(errorMessage)
                    );
                    return Promise.resolve(errorMessage);
                });
                return error;
            }
        });
    }
}

// Models

export class PlainmapModel extends widgets.DOMWidgetModel {
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.events = newEventBus();
    }

    defaults() {
        return {
            ...super.defaults(),
            ...defaultAttributes,
            _view_name: 'PlainmapView',
            _model_name: 'PlainmapModel',
            data_bounds: null,
            initial_viewport: {type: DATA_BOUNDS},
            map_type: 'ROADMAP',
            mouse_handling: 'COOPERATIVE',
        };
    }

    static serializers = {
        ...widgets.DOMWidgetModel.serializers,
        layers: {deserialize: widgets.unpack_models},
    };
}
