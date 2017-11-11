
import * as widgets from '@jupyter-widgets/base'

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';
import { arrayToLatLng } from './services/googleConverters'

export class LineModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'LineView',
            _model_name: 'LineModel'
        }
    }
}

export class LineView extends widgets.WidgetView {

    render() {
        const start = arrayToLatLng(this.model.get('start'));
        const end = arrayToLatLng(this.model.get('end'));
        const path = new google.maps.MVCArray([start, end])
        const lineOptions = {
            strokeColor: '#696969',
            strokeWeight: 2,
            strokeOpacity: 0.6,
            clickable: false
        }
        this.line = new google.maps.Polyline({ path, ...lineOptions });
        this.line.addListener('click', event => this.trigger('click'))
    }

    addToMapView(mapView) {
        this.mapView = mapView;
        this.line.setMap(mapView.map);
    }

    removeFromMapView() {
        this.mapView = null;
        this.line.setMap(null);
    }

    ensureClickable() {
        this.line.setOptions({ clickable: true })
    }

    restoreClickable() {
        this.line.setOptions({ clickable: false })
    }
}
