import * as widgets from '@jupyter-widgets/base';

import {GMapsLayerView, GMapsLayerModel} from './GMapsLayer';
import {arrayToLatLng} from './services/googleConverters';

export class PolylineModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'PolylineView',
            _model_name: 'PolylineModel',
            stroke_color: '#696969',
            stroke_weight: 2,
            stroke_opacity: 0.6,
        };
    }
}

export class PolylineView extends GMapsLayerView {
    render() {
        const points = this.model
            .get('path')
            .map(latLngArray => arrayToLatLng(latLngArray));
        const pathElems = points;
        const path = new google.maps.MVCArray(pathElems);
        const strokeColor = this.model.get('stroke_color');
        const strokeWeight = this.model.get('stroke_weight');
        const strokeOpacity = this.model.get('stroke_opacity');
        const polylineOptions = {
            strokeColor,
            strokeWeight,
            strokeOpacity,
            clickable: false,
        };
        this.polyline = new google.maps.Polyline({
            path: path,
            ...polylineOptions,
        });
        this.polyline.addListener('click', event => this.trigger('click'));
        this.modelEvents();
    }

    modelEvents() {
        const properties = [
            ['strokeColor', 'stroke_color'],
            ['strokeWeight', 'stroke_weight'],
            ['strokeOpacity', 'stroke_opacity'],
        ];

        properties.forEach(([nameInView, nameInModel]) => {
            const callback = () => {
                this.polyline.setOptions({
                    [nameInView]: this.model.get(nameInModel),
                });
            };
            this.model.on(`change:${nameInModel}`, callback, this);
        });
    }

    addToMapView(mapView) {
        this.mapView = mapView;
        this.polyline.setMap(mapView.map);
    }

    removeFromMapView() {
        this.mapView = null;
        this.polyline.setMap(null);
    }

    ensureClickable() {
        this.polyline.setOptions({clickable: true});
    }

    restoreClickable() {
        this.polyline.setOptions({clickable: false});
    }
}
