
import _ from 'underscore';

import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';


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

        const modelData = this.model.get("data");

        GoogleMapsLoader.load((google) => {
            this.directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions)

            const request = {
                origin: this.getOrigin(modelData),
                destination: this.getDestination(modelData),
                waypoints: this.getWaypoints(modelData),
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

    getOrigin(modelData) {
        const [lat, lng] = _.first(modelData)
        return new google.maps.LatLng(lat, lng)
    }

    getDestination(modelData) {
        const [lat, lng] = _.last(modelData)
        return new google.maps.LatLng(lat, lng)
    }

    getWaypoints(modelData) {
        const withoutFirst = _.tail(modelData)
        const withoutLast = _.initial(withoutFirst)
        const dataAsGoogle = withoutLast.map(([lat, lng]) => {
            return {location: new google.maps.LatLng(lat, lng)}
        })
        return dataAsGoogle
    }
}
