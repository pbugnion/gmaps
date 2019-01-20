import {GMapsLayerView, GMapsLayerModel} from './GMapsLayer'
import {arrayToLatLng} from './services/googleConverters';

export class CircleModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults()
        }
    };
}

export class CircleView extends GMapsLayerView {
    render() {
        const radius = this.model.get('radius');
        const center = arrayToLatLng(this.model.get('center'));
        this.circle = new google.maps.Circle({
            center,
            radius,
            clickable: false,
        })
    }

    addToMapView(mapView) {
        this.mapView = mapView;
        this.circle.setMap(mapView.map);
    }
}
