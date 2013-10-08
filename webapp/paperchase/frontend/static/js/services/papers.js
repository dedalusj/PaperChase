function Paper(paper) {
  this.selected = false;
  angular.extend(this, paper);
  this.init();
}

Paper.prototype.init = function() {
  this.created = new Date(this.created);
  this.read = this.read_at == null;
}

app.factory('Papers', ['PaperAPI', '$http', function(PaperAPI, $https) {
  var Papers = function() {
    this.items = [];
    this.busy = false;
    this.page = 1;
    this.readCount = 0;
    this.selected = null;
    this.selectedId = -1;
  };

  Papers.prototype.nextPage = function() {
    if (this.busy) return;
    this.busy = true;
    
    PaperAPI.getPapers({page : this.page}, function(papers){
      for (var i=0;i<papers.length;i++)
      { 
          var paper = new Paper(papers[i]);
          if (paper.read_at != null) this.readCount++;
          this.items.push(paper);
      }
      
      this.page = this.page + 1;
      this.busy = false;
    }.bind(this));
  };
  
  Papers.prototype.hasPrev = function() {
      if (!this.selected) {
          return true;
      }
      return this.selectedId > 0;
  };
  
  Papers.prototype.hasNext = function() {
      if (!this.selected) {
          return true;
      }
      return this.selectedId < this.items.length - 1;
  };
  
  Papers.prototype.selectItem = function(paperId) {
      PaperAPI.getPaper({'paper_id': paperId}, function(paper){
        this.selected = new Paper(paper);
        if (!this.selected.read) this.toggleRead();
      }.bind(this));
  
      // Unselect previous selection.
      if (this.selectedId >= 0) {
          this.items[this.selectedId].selected = false;
      }

      var i = 0;
      while (i < this.items.length) {
		  if (this.items[i].id === paperId) {
		      this.selectedId = i;
		      break;
		  };          
          i++;
      }
      this.items[this.selectedId].selected = true;
  };
  
  Papers.prototype.prev = function() {
      if (this.hasPrev()) {
          this.selectItem(this.items[this.selected ? this.selectedId - 1 : 0].id);
      }
  };
  
  Papers.prototype.next = function() {
      if (this.hasNext()) {
          this.selectItem(this.items[this.selected ? this.selectedId + 1 : 0].id);
      }
  };
  
  Papers.prototype.toggleRead = function() {
      if (this.selected.read_at == null) {
          PaperAPI.markRead({ read_papers : [this.selected.id] });
      } else {
          PaperAPI.markUnread({ unread_papers : [this.selected.id] });
      }
  };
  
  Papers.prototype.markAllRead = function() {
//        items.filtered.forEach(function(item) {
//          item.read = true;
//          feedStore.updateEntryProp(item.feedUrl, item.id, 'read', true);
//        });
//        items.readCount = items.filtered.length;
  };

  return Papers;
}]);