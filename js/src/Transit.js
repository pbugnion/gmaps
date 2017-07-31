import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

export class TransitLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'TransitLayerView',
            _model_name: 'TransitLayerModel'
        }
    }
}

export class TransitLayerView extends GMapsLayerView {
    render() {
        GoogleMapsLoader.load((google) => {
            this.transitLayer = new google.maps.TransitLayer();
        });
    }

    addToMapView(mapView) {
        this.transitLayer.setMap(mapView.map);
    }
}
