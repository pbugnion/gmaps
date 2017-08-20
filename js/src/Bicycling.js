import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

export class BicyclingLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'BicyclingLayerView',
            _model_name: 'BicyclingLayerModel'
        }
    }
}

export class BicyclingLayerView extends GMapsLayerView {

    constructor(options) {
        super(options);
        this.canDownloadAsPng = true;
    }

    render() {
        GoogleMapsLoader.load((google) => {
            this.bicyclingLayer = new google.maps.BicyclingLayer();
        });
    }

    addToMapView(mapView) {
        this.bicyclingLayer.setMap(mapView.map);
    }
}
