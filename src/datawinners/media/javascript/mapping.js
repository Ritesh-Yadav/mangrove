
       var map, layer;
       var project_id = $('#project_id').html();

       function init(entity_type, marker_image){
           map = new OpenLayers.Map({
                div: "map",
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326"),
                units: "m",
                maxResolution: 156543.0339,
                theme : null,
                maxExtent: new OpenLayers.Bounds(
                    -20037508, -20037508, 20037508, 20037508
                ),
                controls: [
                    new OpenLayers.Control.Navigation({dragPan:new OpenLayers.Control.DragPan()}),
                    new OpenLayers.Control.PanZoomBar()

                ]
               });
           layer = new OpenLayers.Layer.Google("Google Layer", {
                    sphericalMercator: true
                    });

           var myStyles = new OpenLayers.StyleMap({
               "default": new OpenLayers.Style({
                   externalGraphic:'/media/images/' + marker_image,
                   pointRadius:8

               })
           });
           var vectorLyr = new OpenLayers.Layer.Vector('Points',{
               strategies: [new OpenLayers.Strategy.Fixed()],
               projection: new OpenLayers.Projection("EPSG:4326"),
               protocol: new OpenLayers.Protocol.HTTP({
                     url: '/get_geojson/entity_type?id='+entity_type+'&project_id='+project_id,
                     format: new OpenLayers.Format.GeoJSON()
               }),
                       styleMap:myStyles
            });
          map.addLayers([layer,vectorLyr]);
          var proj = new OpenLayers.Projection("EPSG:4326");
          var point = new OpenLayers.LonLat(73.6962890625, 26.941659545381516);
          point.transform(proj, map.getProjectionObject());
          map.setCenter(point, 2);

       }


