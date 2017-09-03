
import GoogleMapsLoader from 'google-maps';

import { GMapsLayerView, GMapsLayerModel } from './GMapsLayer';


export class DrawingLayerModel extends GMapsLayerModel {
    defaults() {
        return {
            ...super.defaults(),
            _view_name: 'DrawingLayerView',
            _model_name: 'DrawingLayerModel'
        }
    }
}


export class DrawingLayerView extends GMapsLayerView {
    constructor(options) {
        super(options);
        this.canDownloadAsPng = false;
    }

    render() {
        const options = {
            drawingControl: true,
        }
        GoogleMapsLoader.load(google => {
            this.drawingManager = 
                new google.maps.drawing.DrawingManager(options);
        });
    }

    addToMapView(mapView) {
        this.drawingManager.setMap(mapView.map);
    }
}