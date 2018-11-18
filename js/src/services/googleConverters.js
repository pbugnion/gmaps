import GoogleMapsLoader from 'google-maps';

export function latLngToArray(latLng) {
    const latitude = latLng.lat();
    const longitude = latLng.lng();
    return [latitude, longitude];
}

export function arrayToLatLng(array) {
    const [lat, lng] = array;
    return new google.maps.LatLng({lat, lng});
}

export function stringToMapType(google, mapTypeString) {
    return {
        ROADMAP: google.maps.MapTypeId.ROADMAP,
        HYBRID: google.maps.MapTypeId.HYBRID,
        SATELLITE: google.maps.MapTypeId.SATELLITE,
        TERRAIN: google.maps.MapTypeId.TERRAIN,
    }[mapTypeString];
}

export function mapTypeToString(google, mapType) {
    return {
        [google.maps.MapTypeId.ROADMAP]: 'ROADMAP',
        [google.maps.MapTypeId.HYBRID]: 'HYBRID',
        [google.maps.MapTypeId.SATELLITE]: 'SATELLITE',
        [google.maps.MapTypeId.TERRAIN]: 'TERRAIN',
    }[mapType];
}
