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
    const $saveButton = $("<button />")
    $saveButton
      .addClass("btn btn-default")
      .attr("title", "Download the map as PNG")
      .append("<i />")
        .addClass("fa fa-save");

    $saveButton
      .click((event) => {
        event.preventDefault();
        $saveButton.prop("disabled", true)
        if (this.savePngCallback) {
          this.savePngCallback().then(() => {
            $saveButton.prop("disabled", false)
          });
        };
      })

    this.$el.append($saveButton)
    this.update();
  },

  registerSavePngCallback(callback) {
      this.savePngCallback = callback;
  }
})

