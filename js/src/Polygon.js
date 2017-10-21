
import * as widgets from '@jupyter-widgets/base'

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer'


function arrayToLatLng(array) {
    const [lat, lng] = array;
    return new google.maps.LatLng({lat, lng})
}

export class PolygonModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'PolygonView',
            _model_name: 'PolygonModel'
        }
    }
}

export class PolygonView extends GMapsLayerView {
    render() {
        const points = this.model.get('path').map(
            latLngArray => arrayToLatLng(latLngArray)
        )
        const path = new google.maps.MVCArray(points);
        this.polygon = new google.maps.Polyline({ path })
    }

    addToMapView(mapView) {
        this.mapView = mapView;
        this.polygon.setMap(mapView.map);
    }

    removeFromMapView() {
        this.mapView = null;
        this.polygon.setMap(null);
    }
}
