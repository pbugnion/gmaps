// Entry point for the notebook bundle containing custom model definitions.
//
// Setup notebook base URL
//
// Some static assets may be required by the custom widget javascript. The base
// url for the notebook is not known at build time and is therefore computed
// dynamically.
__webpack_public_path__ = document.querySelector('body').getAttribute('data-base-url') + 'nbextensions/example/';

require('./jupyter-gmaps.less');

// Export everything from example and the npm package version number.
export * from './Map';
export * from './Toolbar';
export * from './Figure';
export * from './Heatmap';
export * from './Marker';
export * from './GeoJson';
export * from './Directions';
export * from './ErrorsBox';
export * from './Bicycling';
export * from './Transit';
export * from './Traffic';
export * from './Drawing';
export * from './Line';
export * from './Polygon';

export { version } from '../package.json';
