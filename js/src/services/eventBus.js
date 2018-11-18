import * as Backbone from 'backbone';

export function newEventBus() {
    return {...Backbone.Events};
}
