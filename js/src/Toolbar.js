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
        }
    }
};

export class ToolbarView extends widgets.DOMWidgetView {

    render() {
        const $toolbar = $("<div />");
        $toolbar
            .addClass("toolbar-inner navbar-inner");

        const $toolbarContainer = $("<div />")
        $toolbarContainer
            .addClass("container toolbar gmaps-toolbar-container");

        const $saveButton = $("<button />")
        $saveButton
            .addClass("btn btn-default gmaps-toolbar-button")
            .attr("title", "Download the map as PNG")
            .append("<i />")
            .addClass("fa fa-download");

        const $notificationArea = $("<span />");
        $notificationArea
            .addClass("gmaps-toolbar-notification-area");

        const $savingNotification = $("<button />")
        $savingNotification
            .addClass("notification_widget btn btn-xs navbar-btn")
            .addClass("warning gmaps-notification-widget")
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
            .append($notificationArea);
        $notificationArea.append($savingNotification);
        $toolbar.append($toolbarContainer)
        this.$el.append($toolbar)

        this.update();
    }

    registerSavePngCallback(callback) {
        this.savePngCallback = callback;
    }
}

