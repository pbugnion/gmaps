import widgets from 'jupyter-js-widgets';

export const GMapsLayerView = widgets.WidgetView.extend({
    initialize(parameters) {
        GMapsLayerView.__super__.initialize.apply(this, arguments)
        this.mapView = this.options.mapView
    }
});


export const GMapsLayerModel = widgets.WidgetModel.extend({
    defaults: {
        ...widgets.WidgetModel.prototype.defaults,
        _view_name : 'GMapsLayerView',
        _model_name : 'GMapsLayerModel',
        _view_module : 'jupyter-gmaps',
        _model_module : 'jupyter-gmaps'
    }
});
