function(doc) {
  if (doc.document_type == 'FormModel') {
      emit(doc.form_code, doc);
  }
}
