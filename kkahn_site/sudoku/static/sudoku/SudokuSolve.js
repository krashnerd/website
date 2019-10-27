function HTMLBoardInit() {
  BOARD = new Board();


  var sText = document.createElement("input");
  sText.className = "square";
  sText.type = "text";
  sText.maxLength = "1";
  
  var hLine = document.createElement("div");
  hLine.className = "horiz border";
  
  var vLine = document.createElement("div");
  vLine.className = "vert inline border";
  
  var square = document.createElement("LI");
  square.appendChild(sText);

  var colors = ["MediumSpringGreen", "Cyan", "Tan", "Silver", "LightBlue",
    "LightPink", "#fefdb3", "#deb3fe", "#dbfeb3"]

  for(var r = 0; r < 9; r++) {
    var row = document.createElement("DIV");

    for(var c = 0; c < 9; c++) {
      var sq = sText.cloneNode(true);
      switch(c % 3) {
        case 0:
              sq.style.borderLeft = "7px solid black";
              break;
        case 2:
              sq.style.borderRight = "7px solid black";
              break;
        default:
              break;
      }

      switch(r % 3) {
        case 0:
              sq.style.borderTop = "7px solid black";
              break;
        case 2:
              sq.style.borderBottom = "7px solid black";
              break;
        default:
              break;
      }
      var box = Math.floor(r / 3) * 3 + Math.floor(c / 3);
      sq.className += " " + box;
      sq.onkeyup = function(){onKey(this)};

      sq.id = "square" + (r * 9 + c);
      row.appendChild(sq);
    }

    document.getElementById("board").appendChild(row);


  }
  var printMap = document.createElement("input");
  printMap.type = "button";
  printMap.value = "print";
  printMap.onClick = "BOARD.printMap()";
  document.getElementById("board").appendChild(printMap);


}
function clearBoard() {
  for(var i = 0; i < 81; i++) {
    document.getElementById("square" + (i)).value = ""
  }
  BOARD.clear();
}

function coord(square) {
  // Returns the coordinates of an HTML square object
      var num = square.id.slice(6);
      return[Math.floor(num / 9), num % 9];
    }


function onKey(square) {
  if (!(square.value in Array.from("123456789"))) {
    BOARD.clear_square(square)
    return;
  }

  var num = Number(square.value);
  var coords = coord(square);

  if ((BOARD.get(coords) != num) && (!BOARD.canPlace(coords, num))) {
     {
      var oldbg = square.style.background;
      square.style.background = "red";
      BOARD.set(BOARD.get(coords), 0);
      square.value = "";
      square.style.background = oldbg;
      return
    }
  }
  else {
    BOARD.set(BOARD.get(coords), num);
    document.getElementById("square" +
      ((Number(square.id.slice(6)) + 1) % 81)).focus();
  }
}

function CanPlaceAndEmpty(board, r, c, n) {
  if(board.get(r, c) != 0) return false;
  return board.canPlace(r, c, n);
}

function sliceDicePlace(board, cat, ind, n) {
  var blanks = board.crds[0];
  for(var i = 0; i < blanks.length(); blanks++) {
    // placeholder
  }
}

function sliceDice(board) {
  var blanks = board.crds[0];
  for(var num = 1; num < 10; num++) {
    if(board.crds[num].length < 9) {
      var poss = [];
      for(var i = 0; i < 27; i++) {
        poss.push([])
      }

      for(blank = 0; blank < blanks.length; blank++) {
        var curr = blanks[blank];
        if(board.canPlace(curr, num)) {
          var r = curr[0];
          var c = curr[1];
          poss[r].push([r, c]);
          poss[9 + c].push([r, c]);
          //poss[18 + Math.floor(r / 3) * 3 + Math.floor(c / 3)].push([r, c]);
        }
      }
      for(var i = 0; i < 18; i++) {
        if(poss[i].length == 1) {
          var coords = board.get(poss[i][0])
          board.set(coords, num)
          document.getElementById("square" + (coords[0] * 9 + coords[1])).style.background = "red"
          if(solve(board, board.fewest()[0])) {
            return true;
          }
          else {
            board.set(coords, 0);
            document.getElementById("square" + (coords[0] * 9 + coords[1])).style.background = "green"

          }
        }
      }
    }
  }
  return false;
}

function solve(board, coords) {
  console.log("left:", board.crds[0].length);
  if(board.solved())
    return true;

  // if(sliceDice(board))
  //  return true;

  var poss = board.find(coords)[0];
  poss++;

  for(var guess = poss; guess < 10; guess++) {
    if (board.canPlace(coords, guess)) {
      board.set(coords, guess);


      var newCoords = board.fewest();
      if (solve(board, newCoords[0]))
        return true;
    }
  }


  board.set(coords, 0);
  return false;
}

function loadHardPuzle() {
  var tpl = ["800000000",
             "003600000",
             "070090200",
             "050007000",
             "000045700",
             "000100030",
             "001000068",
             "008500010",
             "090000400"];

    BOARD.template(tpl);
}
function sudokuSolve() {
  var t0 = performance.now();
  var coords = BOARD.fewest();
  // BOARD.printMap();

  if(solve(BOARD, coords[0])) {
    BOARD.printMap()
    for(var num = 1; num < 10; num++) {
      for(var square = 0; square < BOARD.crds[num].length; square++) {
        document.getElementById(
          "square" + BOARD.sqNum(num, square)).value = num;
      }
     }
  }
  var t1 = performance.now();

  document.getElementById("timer").value = (t1 - t0);
}
