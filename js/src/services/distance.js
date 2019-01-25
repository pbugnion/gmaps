const R = 6.371e6; // Earth radius in meters

// formulae taken from https://www.movable-type.co.uk/scripts/latlong.html
// Returns the distance between two coordinates in meters
export function calculateDistance(start, end) {
    const [startLatitude, startLongitude] = start;
    const [endLatitude, endLongitude] = end;

    const startLatitudeRadians = (Math.PI * startLatitude) / 180.0;
    const endLatitudeRadians = (Math.PI * endLatitude) / 180.0;

    const deltaLatitude = (Math.PI * (endLatitude - startLatitude)) / 180.0;
    const deltaLongitude = (Math.PI * (endLongitude - startLongitude)) / 180.0;

    const a =
        Math.sin(0.5 * deltaLatitude) ** 2 +
        Math.cos(startLatitudeRadians) *
            Math.cos(endLatitudeRadians) *
            Math.sin(0.5 * deltaLongitude) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c;
}
