class Board{
  constructor() {
    // this.grid = new Array(9);
    this.crds = new Array();
    for(var i = 0; i < 10; i++) {
      this.crds.push([])
    }
    for(var r = 0; r < 9; r++) {
      for(var c = 0; c < 9; c++) {
        this.crds[0].push([r, c]);
      }
    }
  }

  clear() {
    for(var i = 0; i < 10; i++){
      this.crds[i] = [];
    }
    for(var r = 0; r < 9; r++) {
      for(var c = 0; c < 9; c++) {
        this.crds[0].push([r, c]);
      }
    }
  }



  template(tpstr) {
    this.clear();
    for(var r = 0; r < 9; r++) {
      for(var c = 0; c < 9; c++) {
        var num = Number(tpstr[r][c]);
        if (num != NaN) {
          this.set(this.get([r, c]), num);
        }
      }
    }
  }

  clear_square(square) {
    function coord(square) {
      var num = square.id.slice(6);
      return[Math.floor(num / 9), num % 9];
    }

    this.set(this.get(coord(square)), 0);
    square.value = "";
  }

  set(coords, n) {
    // this.grid[r][c] = n
    var loc = this.find(coords)
    this.crds[n].push(this.crds[loc[0]][loc[1]])

    this.crds[loc[0]].splice(loc[1], 1);
  }

  printMap() {
    for(var i = 0; i < 10; i++) {
      var numStr = i + ": "
      for (var k = 0; k < this.crds[i].length; k++) {
        numStr += "[" + this.crds[i][k].toString() + "]";
        }
      console.log(numStr)
      }
    }

  find(coords) {
    for(var num = 0; num < 10; num++) {
      var result = this.crds[num].indexOf(coords);
      if(result >= 0) {
        return [num, result];
        }
      }
    }

  sqNum(num, ind) {
    var crd = this.crds[num][ind];
    return 9 * crd[0] + crd[1];
  }

  get(coords)  {
    for(var num = 0; num < 10; num++) {
      for(var ind = 0; ind < this.crds[num].length; ind++) {
        var inBoard = this.crds[num][ind];
        if (inBoard[0] == coords [0] && inBoard[1] == coords[1]) {
          return inBoard;
        }
      }
    }
  }



  inGroupWith(crd1, crd2) {

    if(crd1 == crd2) {
      return false;
    }

    if(crd1[0] == crd2[0]){// || crd1[1] == crd2[1]) {
      return true;
    }
    if(crd1[1] == crd2[1]) {
      return true;
    }
    if(Math.floor(crd1[0] / 3) == Math.floor(crd2[0] / 3)) {
      if(Math.floor(crd1[1] / 3) == Math.floor(crd2[1] / 3)) {
        return true;
      }
    }
    return false;
  }

  solved() {
    //console.log(this.crds[0].length);
    return (this.crds[0].length == 0)
    // for(var r = 0; r < 9; r++)
    //   for(var c = 0; c < 9; c++)
    //     if(this.grid[r][c] == 0)
    //       return false;
    //
    //
    // return true;
  }

  canPlace(coords, n) {
    for(var i = 0; i < this.crds[n].length; i++) {
      if(this.inGroupWith(this.crds[n][i], coords)) {
        return false;
      }
    }
    //console.log("can place")
    return true;

    // var boxR = Math.floor(r / 3) * 3;
    // var boxC = Math.floor(c / 3) * 3;
    //
    //
    // for(var i = 0; i < 9; i++) {
    //   if(this.grid[r][i] == n || this.grid[i][c] == n) {
    //     return false;
    //   }
    //   if(this.grid[boxR + Math.floor(i / 3)][boxC + i % 3] == n) {
    //     return false;
    //   }
    // }
    // return true;
  }

  fewest() {
    var smallest = 9;
    var result = this.crds[0][0];

    for(var i = 0; i < this.crds[0].length; i++) {
      var poss = 0;
      var coords = this.crds[0][i];

      for(var n = 1; n < 10; n++)
        if (this.canPlace(coords, n))
          poss++;
      if(poss < smallest) {
        result = coords;
        smallest = poss;
      }
    }

    return [result, smallest];
  }
}
