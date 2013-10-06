app.filter('htmlToPlainText', function() {
    return function(text) {
      return String(text).replace(/<(?:.|\n)*?>/gm, '');
    }
  }
);