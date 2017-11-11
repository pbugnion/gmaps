
import * as widgets from '@jupyter-widgets/base'

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer'
import { arrayToLatLng } from './services/googleConverters'


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
        const pathElems = [...points, points[0]] // make sure we close the polygon
        const path = new google.maps.MVCArray(pathElems);
        const polygonOptions = {
            strokeColor: '#696969',
            fillColor: '#696969',
            strokeWeight: 1,
            strokeOpacity: 0.6,
            fillOpacity: 0.2,
            clickable: false
        };
        this.polygon = new google.maps.Polygon({ paths: [path], ...polygonOptions })
        this.polygon.addListener('click', event => this.trigger('click'));
    }

    addToMapView(mapView) {
        this.mapView = mapView;
        this.polygon.setMap(mapView.map);
    }

    removeFromMapView() {
        this.mapView = null;
        this.polygon.setMap(null);
    }

    ensureClickable() {
        this.polygon.setOptions({ clickable: true })
    }

    restoreClickable() {
        this.polygon.setOptions({ clickable: false })
    }
}
