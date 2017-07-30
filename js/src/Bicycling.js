import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

export class BicyclingLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'BicyclingLayerModel',
            _model_name: 'BicyclingLayerView'
        }
    }
}

export class BicyclingLayerView extends GMapsLayerView {
    render() {
        GoogleMapsLoader.load((google) => {
            this.bicyclingLayer = new google.maps.BicyclingLayer();
        });
    }

    addToMapView(mapView) {
        this.bicyclingLayer.setMap(mapView.map);
    }
}
