import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';

export class TrafficLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            auto_refresh: true,
            _view_name: 'TrafficLayerView',
            _model_name: 'TrafficLayerModel'
        }
    }
}

export class TrafficLayerView extends GMapsLayerView {

    constructor(options) {
        super(options);
        this.canDownloadAsPng = true;
    }

    render() {
        this.options = {
            autoRefresh: this.model.get('auto_refresh')
        }
        this.modelEvents()
        GoogleMapsLoader.load(google => {
            this.trafficLayer = new google.maps.TrafficLayer(this.options);
        });
    }

    addToMapView(mapView) {
        this.trafficLayer.setMap(mapView.map);
    }

    modelEvents() {
        this.model.on('change:auto_refresh', () => {
            this.options = {
                ...this.options,
                autoRefresh: this.model.get('auto_refresh')
            }
            if (this.trafficLayer) {
                this.trafficLayer.setOptions(this.options)
            }
        });
    }
}