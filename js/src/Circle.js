import {GMapsLayerView, GMapsLayerModel} from './GMapsLayer'

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
        const center = this.model.get('center');
        console.log(radius);
        console.log(center);
    }
}
