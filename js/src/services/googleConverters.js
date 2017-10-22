
import GoogleMapsLoader from 'google-maps';

export function latLngToArray(latLng) {
    const latitude = latLng.lat();
    const longitude = latLng.lng();
    return [latitude, longitude];
}

export function arrayToLatLng(array) {
    const [lat, lng] = array;
    return new google.maps.LatLng({lat, lng})
}
