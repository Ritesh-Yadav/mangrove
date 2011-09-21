function(doc) {
    var isNotNull = function(o) {
        return !((o === undefined) || (o == null));
    };
    if (doc.document_type == 'SubmissionLog' && isNotNull(doc.form_code) && !doc.void) {
        emit([doc.form_code, Date.parse(doc.event_time) ], doc);
    }
}