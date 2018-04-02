
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

export function stringToMapType(google, mapTypeString) {
    return {
        'ROADMAP': google.maps.MapTypeId.ROADMAP,
        'HYBRID': google.maps.MapTypeId.HYBRID,
        'SATELLITE': google.maps.MapTypeId.SATELLITE,
        'TERRAIN': google.maps.MapTypeId.TERRAIN
    }[mapTypeString]
}
