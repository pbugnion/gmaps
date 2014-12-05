
define(["widgets/js/manager", "jquery"], function(WidgetManager,$){

// This should get refactored out into the main module when we add new
// map widget types.
window.initialize = function() {} ;
$.getScript("https://maps.googleapis.com/maps/api/js?v=3&sensor=false&libraries=visualization&callback=initialize") ;
        
var HeatmapView = IPython.DOMWidgetView.extend({

    render : function() {

        this.is_weighted = this.model.get("_is_weighted") ;

        this.$el.css("height", this.model.get("height")) ;
        this.$el.css("width", this.model.get("width")) ;

        var that = this ;
        function gmap_init() {

            var data = that._getData() ;
            var bounds = that._getBounds() ;

            that.map =  new google.maps.Map(
                that.$el[0], { center : bounds.getCenter()  }) ;

            that.map.fitBounds(bounds) ;

            that.heatmap = new google.maps.visualization.HeatmapLayer({
                data : data,
                radius : 10,
                maxIntensity : that.model.get('max_intensity'),
                radius : that.model.get('point_radius')
            }) ;

            that.heatmap.setMap(that.map) ;

            google.maps.event.addListener(that.map, 'bounds_changed', function() {
                // Update the model when the bounds change in the view.
                var bounds = that.map.getBounds() ;
                that._setBounds(bounds) ;
                that.touch() ;
            }) ;
        }
        
        // Hack for IPython version 2.0
        // When support for IPython v2.0 is dropped, this should be replaced by
        // this.on("displayed", gmap_init) ;
        // See https://github.com/ipython/ipython/pull/5404 and
        // http://comments.gmane.org/gmane.comp.python.ipython.devel/12322
        // for reference.
        // The problem (I think) is that Google maps tries to read the 
        // attributes of the div containing it before they have actually been positioned in the DOM.
        // I think that the divs get created first (as a JQuery promise), then rendered asynchronously 
        // by the notebook. It's all a little bewildering.
        setTimeout(gmap_init, 1) ;
    },

    update : function() {
    } ,

    _getBounds : function() {
        /*
         * Get the bounds from the model.
         */
        var a = this.model.get('_bounds') ;
        var sw = this._array2LatLng(a[0]) ;
        var ne = this._array2LatLng(a[1]) ;
        return new google.maps.LatLngBounds(sw, ne) ;
    },

    _setBounds : function(bounds) {
        /*
         * Set bounds in the model.
         */
        this.model.set('_bounds', [ 
                this._latLng2Array(bounds.getSouthWest()),
                this._latLng2Array(bounds.getNorthEast()) ]) ;
    },

    _getData : function() {
        /*
         * Get the data from the model.
         */
        return this._data2LatLngArray(this.model.get('_data')) ;
    },
        
    _data2LatLngArray : function(data) {
        /*
         * Transform an array of pairs of floats into an array of 
         * LatLng objects.
         */
        var lat_lng_array = new Array() ;
        if(this.is_weighted) {
            for (var i=0; i<data.length; i++) {
                lat_lng_array[i] = this._array2WeightedLatLng(data[i]) ;
            }
        } else {
            for (var i=0; i<data.length; i++) {
                lat_lng_array[i] = this._array2LatLng(data[i]) ;
            }
        }
        var out = new google.maps.MVCArray(lat_lng_array) ;
        return out ;

    } ,

    _array2LatLng : function(l) {
        /*
         * Transform an array to a pair of latitude, longitude objects.
         */
        return new google.maps.LatLng(l[0], l[1]) ;
    },

    _array2WeightedLatLng : function(l) {
        return { location : this._array2LatLng(l), weight : l[2] } ;
    },

    _latLng2Array : function(latlng) {
        return [ latlng.lat(), latlng.lng() ] ;
    }

}) ;
    
// Register with the widget manager. This requires a 2.3.x
// compatibility hack.
if (IPython.version.split(".")[0] == "2") {
    var manager = WidgetManager ;
} else {
    var manager = WidgetManager.WidgetManager ;
}

manager.register_widget_view("HeatmapView", HeatmapView) ;

return { "HeatmapView" : HeatmapView } ;

});
