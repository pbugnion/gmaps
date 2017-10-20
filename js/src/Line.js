
import * as widgets from '@jupyter-widgets/base'

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

function arrayToLatLng(array) {
    const [lat, lng] = array;
    return new google.maps.LatLng({lat, lng})
}

export class LineModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: "LineView",
            _model_name: "LineModel"
        }
    }
}

export class LineView extends widgets.WidgetView {
    render() {
        const start = arrayToLatLng(this.model.get("start"));
        const end = arrayToLatLng(this.model.get("end"));
        const path = new google.maps.MVCArray([start, end])
        this.line = new google.maps.Polyline({ path });
    }

    addToMapView(mapView) {
        this.mapView = mapView;
        this.line.setMap(mapView.map);
    }

    removeFromMapView() {
        this.mapView = null;
        this.line.setMap(null);
    }
}
