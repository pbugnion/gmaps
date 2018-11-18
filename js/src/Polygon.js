import * as widgets from '@jupyter-widgets/base';

import {GMapsLayerView, GMapsLayerModel} from './GMapsLayer';
import {arrayToLatLng} from './services/googleConverters';

export class PolygonModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'PolygonView',
            _model_name: 'PolygonModel',
            stroke_color: '#696969',
            stroke_weight: 2,
            stroke_opacity: 0.6,
            fill_color: '#696969',
            fill_opacity: 0.2,
        };
    }
}

export class PolygonView extends GMapsLayerView {
    render() {
        const points = this.model
            .get('path')
            .map(latLngArray => arrayToLatLng(latLngArray));
        const pathElems = [...points, points[0]]; // make sure we close the polygon
        const path = new google.maps.MVCArray(pathElems);
        const strokeColor = this.model.get('stroke_color');
        const strokeWeight = this.model.get('stroke_weight');
        const strokeOpacity = this.model.get('stroke_opacity');
        const fillColor = this.model.get('fill_color');
        const fillOpacity = this.model.get('fill_opacity');
        const polygonOptions = {
            strokeColor,
            fillColor,
            strokeWeight,
            strokeOpacity,
            fillOpacity,
            clickable: false,
        };
        this.polygon = new google.maps.Polygon({
            paths: [path],
            ...polygonOptions,
        });
        this.polygon.addListener('click', event => this.trigger('click'));
        this.modelEvents();
    }

    modelEvents() {
        const properties = [
            ['strokeColor', 'stroke_color'],
            ['strokeWeight', 'stroke_weight'],
            ['strokeOpacity', 'stroke_opacity'],
            ['fillColor', 'fill_color'],
            ['fillOpacity', 'fill_opacity'],
        ];

        properties.forEach(([nameInView, nameInModel]) => {
            const callback = () => {
                this.polygon.setOptions({
                    [nameInView]: this.model.get(nameInModel),
                });
            };
            this.model.on(`change:${nameInModel}`, callback, this);
        });
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
        this.polygon.setOptions({clickable: true});
    }

    restoreClickable() {
        this.polygon.setOptions({clickable: false});
    }
}
