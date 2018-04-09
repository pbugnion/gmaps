
import _ from 'underscore';

import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';
import { arrayToLatLng } from './services/googleConverters'


export class DirectionsLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: "DirectionsLayerView",
            _model_name: "DirectionsLayerModel"
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

            const request = {
                origin: arrayToLatLng(this.model.get("start")),
                destination: arrayToLatLng(this.model.get("end")),
                waypoints: this.getWaypoints(),
                travelMode: this.model.get("travel_mode"),
                avoidFerries: this.model.get("avoid_ferries"),
                avoidHighways: this.model.get("avoid_highways"),
                avoidTolls: this.model.get("avoid_tolls"),
                optimizeWaypoints: this.model.get("optimize_waypoints")
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
        });
    }

    addToMapView(mapView) { }

    getWaypoints() {
        const dataAsGoogle = this.model.get("waypoints").map(waypoint => {
            return {location: arrayToLatLng(waypoint)}
        })
        return dataAsGoogle
    }
}
