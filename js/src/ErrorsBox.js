import * as widgets from '@jupyter-widgets/base';
import { defaultAttributes } from './defaults'

import $ from 'jquery';

export class ErrorsBoxModel extends widgets.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...defaultAttributes,
            _model_name: 'ErrorsBoxModel',
            _view_name: 'ErrorsBoxView',
            errors: []
        };
    }

    addError(errorMessage) {
        this.set('errors', this.get('errors').concat(errorMessage));
        this.save_changes();
    }

    removeError(ierror) {
        const currentErrors = this.get('errors').slice();
        currentErrors.splice(ierror, 1);
        this.set('errors', currentErrors);
        this.save_changes();
    }
};


export class ErrorsBoxView extends widgets.DOMWidgetView {
    render() {
        this._renderErrors()
        this.model.on('change:errors', () => this._renderErrors())
    }

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
};
