
import GoogleMapsLoader from 'google-maps'

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';


export class SimpleHeatmapLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: "SimpleHeatmapLayerView",
            _model_name: "SimpleHeatmapLayerModel"
        }
    }
};


export class WeightedHeatmapLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: "WeightedHeatmapLayerView",
            _model_name: "WeightedHeatmapLayerModel"
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
                radius: this.model.get("point_radius"),
                maxIntensity: this.model.get("max_intensity"),
                dissipating: this.model.get("dissipating"),
                opacity: this.model.get("opacity"),
                gradient: this.model.get("gradient")
            }) ;
        });
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
    getData() {
        const data = this.model.get("data")
        const dataAsGoogle = new google.maps.MVCArray(
            data.map(([lat, lng]) => new google.maps.LatLng(lat, lng))
        )
        return dataAsGoogle
    }
}


export class WeightedHeatmapLayerView extends HeatmapLayerBaseView {
    getData() {
        const data = this.model.get("data")
        const dataAsGoogle = new google.maps.MVCArray(
            data.map(([lat, lng, weight]) => {
                const location = new google.maps.LatLng(lat, lng)
                return { location: location, weight: weight }
            })
        );
        return dataAsGoogle
    }
}
