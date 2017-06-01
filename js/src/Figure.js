
import _ from 'underscore';

import widgets from 'jupyter-js-widgets';

export const FigureModel = widgets.VBoxModel.extend({
    defaults: {
        ...widgets.DOMWidgetModel.prototype.defaults,
        _model_name: "FigureModel",
        _view_name: "FigureView",
        _model_module: "jupyter-gmaps",
        _view_module: "jupyter-gmaps",
        children: [],
        box_style: '',
        _map: undefined,
        _errors_box: undefined,
        _toolbar: undefined
    }

}, {
    serializers: {
        children: {deserialize: widgets.unpack_models},
        _map: {deserialize: widgets.unpack_models},
        _toolbar: {deserialize: widgets.unpack_models},
        _errors_box: {deserialize: widgets.unpack_models},
        ...widgets.DOMWidgetModel.serializers
    }
})

export const FigureView = widgets.VBoxView.extend({
    initialize(parameters) {
        FigureView.__super__.initialize.apply(this, arguments)
        const toolbarModel = this.model.get("_toolbar");
        if(toolbarModel) {
            this.toolbarView =
                this.add_child_model(this.model.get("_toolbar"))
                    .then(toolbarView => {
                        toolbarView.registerSavePngCallback(
                            () => this.savePng()
                        )
                        return toolbarView;
                    })
        }
        else {
            this.toolbarView = null;
        }
        this.errorsBoxView = this.add_child_model(this.model.get("_errors_box"));
        this.mapView = this.add_child_model(this.model.get("_map"));
    },

    savePng() {
        return this.mapView.then(view => {
            view.savePng().catch(e => this.addError(e))
        });
    },

    addError(errorMessage) {
        console.log(errorMessage);
        this.model.get("_errors_box").addError(errorMessage);
    }
})
