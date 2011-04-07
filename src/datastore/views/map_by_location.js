function(doc) {
    var isNumeric = function(n) {
        return !isNaN(parseFloat(n)) && isFinite(n);
    };
    var isNotNull = function(o) {
        return !((o === undefined) || (o == null));
    };
    if (doc.document_type == 'DataRecord' && isNotNull(doc.entity_backing_field)) {
        var value = {};
        var date = new Date(doc.event_time);
        var aggregation_paths = doc.entity_backing_field.aggregation_paths || {};
        for (index in doc.attributes) {
            if (isNotNull(doc.attributes[index]) && isNotNull(doc.attributes[index]['value']) && isNumeric(doc.attributes[index]['value'])) {
                value[index] = parseFloat(doc.attributes[index]['value']);
            }
        }
        for (index in value) {
            for (hierarchy in aggregation_paths) {
                var key = [index].concat([hierarchy], aggregation_paths[hierarchy], [date.getFullYear(), date.getMonth() + 1, date.getDate(), date.getHours(), date.getMinutes(), date.getSeconds()]);
                key.splice(0, 0, doc.entity_backing_field.entity_type);
                emit(key, value[index]);
            }
        }
    }
}