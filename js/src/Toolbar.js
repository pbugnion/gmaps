import * as widgets from '@jupyter-widgets/base'
import $ from 'jquery'

import { defaultAttributes } from './defaults'

export class ToolbarModel extends widgets.DOMWidgetModel {
    defaults() {
        return {
            ...super.defaults(),
            ...defaultAttributes,
            _model_name: "ToolbarModel",
            _view_name: "ToolbarView",
            layer_controls: [],
        }
    }

    static serializers = {
        ...widgets.DOMWidgetModel.serializers,
        layer_controls: {deserialize: widgets.unpack_models}
    }
};

export class ToolbarView extends widgets.DOMWidgetView {

    render() {
        const $toolbar = $("<div />");
        $toolbar
            .addClass("gmaps-toolbar toolbar-inner navbar-inner");

        const $toolbarContainer = $("<div />")
        $toolbarContainer
            .addClass("toolbar");

        const $saveButton = $("<button />")
        $saveButton
            .addClass("btn btn-default")
            .attr("title", "Download the map as PNG")
            .append("<i />")
            .addClass("fa fa-download");

        this.$additionalControlsContainer = $('<div />')
        this.$additionalControlsContainer.addClass('additional-controls-container')

        const $notificationArea = $("<span />");
        $notificationArea
            .addClass("notification-area");

        const $savingNotification = $("<button />")
        $savingNotification
            .addClass("notification_widget btn btn-xs navbar-btn")
            .addClass("warning notification-widget")
            .html("<span>Downloading</span>")
            .hide();

        $saveButton
            .click((event) => {
                event.preventDefault();
                $saveButton.prop("disabled", true)
                $savingNotification.show()
                if (this.savePngCallback) {
                    this.savePngCallback().then(() => {
                        $saveButton.prop("disabled", false)
                        $savingNotification.hide();
                    });
                };
            })
        

        $toolbarContainer
            .append($saveButton)
            .append(this.$additionalControlsContainer)
            .append($notificationArea);

        $notificationArea.append($savingNotification);
        $toolbar.append($toolbarContainer)
        this.$el.append($toolbar)

        this.additionalControlViews = new widgets.ViewList(this.addControlsModel, null, this);
        this.additionalControlViews.update(this.model.get('layer_controls'))

        this.model.on('change:layer_controls', () => {
            this.additionalControlViews.update(this.model.get('layer_controls'))
        });

        this.update();
    }

    registerSavePngCallback(callback) {
        this.savePngCallback = callback;
    }

    addControlsModel(model) {
        return this.create_child_view(model).then(view => {
            this.$additionalControlsContainer.append(view.el)
            return view;
        });
    }
}
