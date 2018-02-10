
import GoogleMapsLoader from 'google-maps'

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';


export class SimpleHeatmapLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'SimpleHeatmapLayerView',
            _model_name: 'SimpleHeatmapLayerModel'
        }
    }
};


export class WeightedHeatmapLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'WeightedHeatmapLayerView',
            _model_name: 'WeightedHeatmapLayerModel'
        }
    }
};


class HeatmapLayerBaseView extends GMapsLayerView {

    constructor(options) {
        super(options)
        this.canDownloadAsPng = true;
    }

    render() {
        this.modelEvents() ;
        GoogleMapsLoader.load((google) => {
            this.heatmap = new google.maps.visualization.HeatmapLayer({
                data: this.getData(),
                radius: this.model.get('point_radius'),
                maxIntensity: this.model.get('max_intensity'),
                dissipating: this.model.get('dissipating'),
                opacity: this.model.get('opacity'),
                gradient: this.model.get('gradient')
            }) ;
        });
    }

    resetData() {
        this.heatmap.setData(this.getData())
    }

    addToMapView(mapView) {
        this.heatmap.setMap(mapView.map)
    }

    modelEvents() {
        // Simple properties:
        // [nameInView, nameInModel]
        const properties = [
            ['maxIntensity', 'max_intensity'],
            ['opacity', 'opacity'],
            ['radius', 'point_radius'],
            ['dissipating', 'dissipating'],
            ['gradient', 'gradient']
        ]
        properties.forEach(([nameInView, nameInModel]) => {
            const callback = (
                () => this.heatmap.set(nameInView, this.model.get(nameInModel))
            )
            this.model.on(`change:${nameInModel}`, callback, this)
        })
    }
}


export class SimpleHeatmapLayerView extends HeatmapLayerBaseView {
    modelEvents() {
        super.modelEvents()
        this.model.on('change:locations', this.resetData, this)
    }

    getData() {
        const data = this.model.get('locations')
        const dataAsGoogle = new google.maps.MVCArray(
            data.map(([lat, lng]) => new google.maps.LatLng(lat, lng))
        )
        return dataAsGoogle
    }
}


export class WeightedHeatmapLayerView extends HeatmapLayerBaseView {
    modelEvents() {
        super.modelEvents()
        this.model.on('change:locations', this.resetData, this)
        this.model.on('change:weights', this.resetData, this)
    }

    getData() {
        const data = this.model.get('locations')
        const weights = this.model.get('weights')
        const dataAsGoogle = new google.maps.MVCArray(
            data.map(([lat, lng], i) => {
                const weight = weights[i];
                const location = new google.maps.LatLng(lat, lng)
                return { location, weight }
            })
        );
        return dataAsGoogle
    }
}
