
import {calculateDistance} from "../distance";

describe("calculateDistance", () => {

    const testCase = (description, start, end, [lowerBound, upperBound]) => {
        it(description, () => {
            expect(calculateDistance(start, end))
                .toBeWithin(lowerBound, upperBound)
        })
    }

    testCase("simple", [0.0, 0.0], [1.0, 1.0], [157.2e3, 157.3e3])

    testCase(
        "disambiguate latitude/longitude",
        [0.0, 0.0], [1.0, 2.0], [248.6e3, 248.7e3]
    )

    testCase(
        "negative latitute",
        [-1.0, 2.0], [-2.0, 3.0], [157.2e3, 157.3e3]
    )

    testCase(
        "negative longitude",
        [1.0, -2.0], [2.0, -3.0], [157.2e3, 157.3e3]
    )

    testCase(
        "cross origin",
        [-1.0, -2.0], [2.0, 3.0], [648.25e3, 648.35e3]
    )

    testCase(
        "no latitude difference",
        [0.0, -2.0], [0.0, 3.0], [555.9e3, 556.1e3]
    )

    testCase(
        "no longitude difference",
        [-1.0, 0.0], [2.0, 0.0], [333.5e3, 333.7e3]
    )

    testCase(
        "no difference",
        [2.0, 3.0], [2.0, 3.0], [-0.1e3, 0.1e3]
    )

    testCase(
        "large latitude",
        [-90.0, 0.0], [90.0, 0.0], [20010e3, 20030e3]
    )

    testCase(
        "large longitude",
        [0.0, -90.0], [0.0, 90.0], [20010e3, 20030e3]
    )
})
