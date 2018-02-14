import * as gmaps from '../dist/index';
import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';

export default {
    id: 'jupyter-gmaps',
    requires: [IJupyterWidgetRegistry],
    activate: (app, widgets) => {
        widgets.registerWidget({
            name: 'jupyter-gmaps',
            version: gmaps.version,
            exports: gmaps
        })
    },
    autoStart: true
}
