
import {calculateDistance} from "../distance";

describe("calculateDistance", () => {
    it("simple", () => {
        expect(
            calculateDistance([0.0, 0.0], [1.0, 1.0])
        ).toBeWithin(157.2e3, 157.3e3)
    })
})
