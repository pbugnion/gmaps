import widgets from 'jupyter-js-widgets';

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
            _view_name : 'GMapsLayerView',
            _model_name : 'GMapsLayerModel',
            _view_module : 'jupyter-gmaps',
            _model_module : 'jupyter-gmaps'
        }
    }
}
