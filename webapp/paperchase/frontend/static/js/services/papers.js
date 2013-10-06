app.factory('Papers', ['PaperAPI', function(PaperAPI) {
  var Papers = function() {
    this.items = [];
    this.busy = false;
    this.page = 1;
    this.currentItem = undefined;
  };

  Papers.prototype.nextPage = function() {
    if (this.busy) return;
    this.busy = true;
    
    PaperAPI.getPapers({page : this.page}, function(papers){
      for (var i=0;i<papers.length;i++)
      { 
          papers[i].created = new Date(papers[i].created);
          this.items.push(papers[i]);
      }
      
      this.page = this.page + 1;
      this.busy = false;
    }.bind(this));
  };
  
  Papers.prototype.updateCurrentPaper = function(paperId) {
    PaperAPI.getPaper({'paper_id': paperId}, function(paper, getResponseHeaders){
      paper.created = new Date(paper.created);
      this.currentItem = paper;
    }.bind(this));
  };

  return Papers;
}]);