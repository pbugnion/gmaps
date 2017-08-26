
import _ from 'underscore';

import * as widgets from '@jupyter-widgets/base';
import { VBoxModel, VBoxView } from '@jupyter-widgets/controls';
import { defaultAttributes } from './defaults';

export class FigureModel extends VBoxModel {
    defaults() {
        return {
            ...super.defaults(),
            ...defaultAttributes,
            _model_name: "FigureModel",
            _view_name: "FigureView",
            children: [],
            box_style: '',
            _map: undefined,
            _errors_box: undefined,
            _toolbar: undefined
        }
    }

    static serializers = {
        ...widgets.DOMWidgetModel.serializers,
        children: {deserialize: widgets.unpack_models},
        _map: {deserialize: widgets.unpack_models},
        _toolbar: {deserialize: widgets.unpack_models},
        _errors_box: {deserialize: widgets.unpack_models}
    }
}

export class FigureView extends VBoxView {
    initialize(parameters) {
        super.initialize(parameters)
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
        const errorsBoxModel = this.model.get('_errors_box');
        if (errorsBoxModel) {
            this.errorsBoxView =
                this.add_child_model(this.model.get("_errors_box"));
        }
        this.mapView = this.add_child_model(this.model.get("_map"));
        this.pWidget.addClass("gmaps-figure")
    }

    savePng() {
        return this.mapView.then(view =>
            view.savePng().catch(e => this.addError(e))
        );
    }

    addError(errorMessage) {
        console.log(`[Error]: ${errorMessage}`)
        const errorsBoxModel = this.model.get("_errors_box")
        if (errorsBoxModel) {
            errorsBoxModel.addError(errorMessage);
        }
    }
}
