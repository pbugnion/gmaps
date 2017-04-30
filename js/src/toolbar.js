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
    const saveButton = document.createElement("button")
    saveButton.classList.add("jupyter-widgets"); // jupyter-js-widgets css
    saveButton.classList.add("jupyter-button"); // jupyter-js-widgets css
    saveButton.classList.add("widget-button") // jupyter-js-widgets css
    saveButton.setAttribute("title", "Save");
    saveButton.innerHTML = "save";
    saveButton.onclick = (elem) => {
      saveButton.innerHTML = "saving";
      saveButton.disabled = true;
      elem.preventDefault();
      if (this.savePngCallback) {
        this.savePngCallback().then(() => {
          saveButton.innerHTML = "save";
          saveButton.disabled = false;
        });
      }
    }

    this.el.appendChild(saveButton);
    this.update();
  },

  registerSavePngCallback(callback) {
      this.savePngCallback = callback;
  }
})

