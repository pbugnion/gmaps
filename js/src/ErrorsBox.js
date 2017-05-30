import widgets from 'jupyter-js-widgets'

export const ErrorsBoxModel = widgets.DOMWidgetModel.extend({
    defaults: {
        ...widgets.DOMWidgetModel.prototype.defaults,
        _model_name: 'ErrorsBoxModel',
        _view_name: 'ErrorsBoxView',
        _model_module: 'jupyter-gmaps',
        _view_module: 'jupyter-gmaps',
        errors: []
    }
});

export const ErrorsBoxView = widgets.DOMWidgetView.extend({
    render() {
        console.log('Hello erors view')
        console.log(this.model.get('errors'));
    }
});
