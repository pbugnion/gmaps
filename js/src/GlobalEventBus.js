import * as Backbone from 'backbone'

export const globalEvents = {
    AUTHENTICATION_ERROR: 'AUTHENTICATION_ERROR'
}

export const globalEventBus = { ...Backbone.Events }
