
import _ from 'underscore';

import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';
import { mapEventTypes, MapEvents } from './MapEvents'
import { arrayToLatLng } from './services/googleConverters'


export class DirectionsLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'DirectionsLayerView',
            _model_name: 'DirectionsLayerModel'
        }
    }
}


export class DirectionsLayerView extends GMapsLayerView {
    constructor(options) {
        super(options);
        this.canDownloadAsPng = false;
    }

    render() {
        const rendererOptions = { map: this.mapView.map }

        GoogleMapsLoader.load(google => {
            this.directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions)
            this.directionsService = new google.maps.DirectionsService();

            this.updateDirections()
            this.modelEvents()
        });
    }

    modelEvents() {
        const properties = [
            'start', 'end', 'waypoints', 'travel_mode', 'avoid_ferries',
            'avoid_highways', 'avoid_tolls', 'optimize_waypoints'
        ]

        properties.forEach(nameInModel => {
            const callback = () => this.updateDirections()
            this.model.on(`change:${nameInModel}`, callback, this)
        })
    }

    updateDirections() {
        this.computeDirections()
            .then(response => this.directionsDisplay.setDirections(response))
            .catch(e => console.error(e))
    }

    addToMapView(mapView) { }

    getWaypoints() {
        const dataAsGoogle = this.model.get('waypoints').map(waypoint => {
            return {location: arrayToLatLng(waypoint)}
        })
        return dataAsGoogle
    }

    computeDirections() {
        const request = {
            origin: arrayToLatLng(this.model.get('start')),
            destination: arrayToLatLng(this.model.get('end')),
            waypoints: this.getWaypoints(),
            travelMode: this.model.get('travel_mode'),
            avoidFerries: this.model.get('avoid_ferries'),
            avoidHighways: this.model.get('avoid_highways'),
            avoidTolls: this.model.get('avoid_tolls'),
            optimizeWaypoints: this.model.get('optimize_waypoints')
        };

        return new Promise((resolve, reject) => {
            this.directionsService.route(request, (response, status) => {
                // print to the browser console (mostly for debugging)
                console.log(`Direction service returned: ${status}`) ;
                // set a flag in the model
                this.model.set('layer_status', status) ;
                this.touch()
                if (status == google.maps.DirectionsStatus.OK) {
                    resolve(response)
                } else {
                    const errorMessage =
                        statusErrorMessages[status] ||
                        `Invalid status code: ${status}.`
                    this.mapView.model.events.trigger(
                        mapEventTypes.LAYER_ERROR,
                        MapEvents.layerError('directions', errorMessage)
                    )
                    reject(`Error returned by direction service: ${status}`)
                }
            })
        })
    }
}


// From https://developers.google.com/maps/documentation/directions/intro#StatusCodes
const statusErrorMessages = {
    'NOT_FOUND': 'At least one of the locations specified in the request\'s origin, destination, or waypoints could not be geocoded.',
    'ZERO_RESULTS': 'No route could be found between the origin and destination.',
    'INVALID_REQUEST': 'The directions request provided was invalid. This may be an error in `jupyter-gmaps`.',
    'MAX_WAYPOINTS_EXCEEDED': 'Too many waypoints were provided in the directions request',
    'OVER_QUERY_LIMIT': 'You have sent too many directions request. Wait until your quota replenishes.',
    'REQUEST_DENIED': 'You are not allowed to use Google\'s directions service',
    'UNKNOWN_ERROR': 'A directions request could not be processed due to a server error. The request may succeed if you try again.'
}
