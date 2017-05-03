import widgets from 'jupyter-js-widgets'

export const ToolbarModel = widgets.DOMWidgetModel.extend({
  defaults: {
    ...widgets.DOMWidgetModel.prototype.defaults,
    _model_name: "ToolbarModel",
    _view_name: "ToolbarView",
    _model_module: "jupyter-gmaps",
    _view_module: "jupyter-gmaps",
  }
});

export const ToolbarView = widgets.DOMWidgetView.extend({

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
      .addClass("notification_widget btn btn-xs navbar-btn warning")
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
  },

  registerSavePngCallback(callback) {
      this.savePngCallback = callback;
  }
})

