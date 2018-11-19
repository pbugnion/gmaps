import {newEventBus} from './services/eventBus';

export const globalEvents = {
    AUTHENTICATION_ERROR: 'AUTHENTICATION_ERROR',
};

export const globalEventBus = {...Backbone.Events};
