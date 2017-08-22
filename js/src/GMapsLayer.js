import * as widgets from '@jupyter-widgets/base';
import { defaultAttributes } from './defaults';

export class GMapsLayerView extends widgets.WidgetView {
    initialize(parameters) {
        super.initialize(parameters)
        this.mapView = this.options.mapView
    }
};


export class GMapsLayerModel extends widgets.WidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...defaultAttributes,
            _view_name : 'GMapsLayerView',
            _model_name : 'GMapsLayerModel',
        }
    }
}
