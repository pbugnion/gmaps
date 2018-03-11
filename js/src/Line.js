
import * as widgets from '@jupyter-widgets/base'

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';
import { arrayToLatLng } from './services/googleConverters'

export class LineModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'LineView',
            _model_name: 'LineModel',
            stroke_color: '#696969',
            stroke_weight: 2,
            stroke_opacity: 0.6
        }
    }
}

export class LineView extends widgets.WidgetView {

    render() {
        const start = arrayToLatLng(this.model.get('start'));
        const end = arrayToLatLng(this.model.get('end'));
        const strokeColor = this.model.get('stroke_color');
        const strokeWeight = this.model.get('stroke_weight');
        const strokeOpacity = this.model.get('stroke_opacity');
        const path = new google.maps.MVCArray([start, end])
        const lineOptions = {
            strokeColor,
            strokeWeight,
            strokeOpacity,
            clickable: false
        }
        this.line = new google.maps.Polyline({ path, ...lineOptions });
        this.line.addListener('click', event => this.trigger('click'))
        this.modelEvents()
    }

    modelEvents() {
        const properties = [
            ['strokeColor', 'stroke_color'],
            ['strokeWeight', 'stroke_weight'],
            ['strokeOpacity', 'stroke_opacity']
        ]

        properties.forEach(([nameInView, nameInModel]) => {
            const callback = (
                () => {
                    this.line.setOptions(
                        {[nameInView]: this.model.get(nameInModel)}
                    )
                }
            )
            this.model.on(`change:${nameInModel}`, callback, this)
        })
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
