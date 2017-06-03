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
    },

    removeError(ierror) {
        const currentErrors = this.get('errors').slice();
        currentErrors.splice(ierror, 1);
        this.set('errors', currentErrors);
    }
});

export const ErrorsBoxView = widgets.DOMWidgetView.extend({
    render() {
        this._renderErrors()

        this.listenTo(
            this.model,
            'change:errors',
            () => this._renderErrors()
        )
    },

    _renderErrors() {
        const errorContainer = $('<ul />').addClass("gmaps-error-box")
        this.model.get('errors').map(
            (message, ierror) =>
                $(`<li><pre>${message}</pre></li>`)
                    .click(() => this.model.removeError(ierror))
        ).forEach(element => errorContainer.append(element))
        this.$el.empty(); // Clear the current state
        this.$el.append(errorContainer);
    }
});
