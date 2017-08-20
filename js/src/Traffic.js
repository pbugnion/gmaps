import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

export class TrafficLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'TrafficLayerView',
            _model_name: 'TrafficLayerModel'
        }
    }
}

export class TrafficLayerView extends GMapsLayerView {

    constructor(options) {
        super(options);
        this.canDownloadAsPng = true;
    }

    render() {
        GoogleMapsLoader.load(google => {
            this.trafficLayer = new google.maps.TrafficLayer();
        });
    }

    addToMapView(mapView) {
        this.trafficLayer.setMap(mapView.map);
    }
}