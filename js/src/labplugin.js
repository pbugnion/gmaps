const gmaps = require('../dist/index');
const base = require('@jupyter-widgets/base');

export default {
    id: 'jupyter-gmaps',
    requires: [base.IJupyterWidgetRegistry],
    activate: (app, widgets) => {
        widgets.registerWidget({
            name: 'jupyter-gmaps',
            version: gmaps.version,
            exports: gmaps
        })
    },
    autoStart: true
}
