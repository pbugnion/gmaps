import widgets from 'jupyter-js-widgets'

export const ErrorsBoxModel = widgets.DOMWidgetModel.extend({
    defaults: {
        ...widgets.DOMWidgetModel.prototype.defaults,
        _model_name: 'ErrorsBoxModel',
        _view_name: 'ErrorsBoxView',
        _model_module: 'jupyter-gmaps',
        _view_module: 'jupyter-gmaps',
        errors: []
    },

    addError(errorMessage) {
        this.set('errors', this.get('errors').concat(errorMessage));
    }
});

export const ErrorsBoxView = widgets.DOMWidgetView.extend({
    render() {
        console.log('Hello erors view')
        console.log(this.model.get('errors'));

        this.listenTo(
            this.model,
            'change:errors',
            () => console.log(this.model.get('errors'))
        )
    }
});
