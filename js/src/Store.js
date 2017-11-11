import BaseStore from "flux/lib/FluxStore";

export class Store extends BaseStore {
    constructor(initalState, dispatcher) {
        super(dispatcher);
        this._state = initalState;
    }

    getState() {
        return this._state;
    }

    areEqual(one, two) {
        return one === two;
    }

    __invokeOnDispatch(action) {
        this.__changed = false;

        // Reduce the stream of incoming actions to state, update when necessary.
        const startingState = this._state;
        const endingState = this.reduce(startingState, action);

        console.assert(endingState !== undefined);

        if (!this.areEqual(startingState, endingState)) {
            this._state = endingState;

            // `__emitChange()` sets `this.__changed` to true and then the actual
            // change will be fired from the emitter at the end of the dispatch, this
            // is required in order to support methods like `hasChanged()`
            this.__emitChange();
        }

        if (this.__changed) {
            this.__emitter.emit(this.__changeEvent);
        }
    }
}
