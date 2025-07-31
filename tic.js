var playerSymbol;
var enemySymbol;
var values;
var frame;


var restartGameFlag = false;
var row, column;  // Will contain "coordinates"for a specific cell
var playerWeapon;
var aiWeapon;
var aiWonMsgs = ["I won! That was a good game, but you need to improve your strategy. Maybe you can learn from me.",
    "Congratulations! You have just lost to the most advance AI in the world. Don't feel bad it's not your fault. I'm just too smart for you.",
    "You Lose! I'm sorry, but you are no match for my superior intelligence. I can always predict you moves and block them."];

var playerWonMsgs = ["You win! I admit defeat, you have outsmarted me. Well done, you deserve this victory.",
    "I lose! How did you do that? You must have cheated somehow. There is no way you can bear me fair and square.",
    "You got lucky! I made a mistake, but it won't happen again. Next time, I will crush you. Don't get too confident."
];
$(document).ready(function() {
    // Intro screen buttons
    $("#choose-low").on("click", function() {
        py_set_difficulty(0,js_set_difficulty);
        $("#intro-screen").fadeOut(300, showGameScreen);
    });
    $("#choose-medium").on("click", function() {
        py_set_difficulty(1,js_set_difficulty);
        $("#intro-screen").fadeOut(300, showGameScreen);
    });

    $("#choose-high").on("click", function() {
        py_set_difficulty(2,js_set_difficulty);
        $("#intro-screen").fadeOut(300, showGameScreen);
    });

    $("#restart").on("click", function() {
        restartGame();
    });
    $("#exit").on("click", function() {
        py_exit();
    });

    $("#choose-x").on("click", function() {

        playerWeapon = './Resources/cross.png';
        aiWeapon = './Resources/moji-circle.png';

        $("#weapon-choice").fadeOut(300);
        $("#weapon-selection").fadeIn(300);
        $("#choose-xs").fadeIn(300);
        py_start_new(js_start_new);
    });

    $("#choose-o").on("click", function() {

        playerWeapon = './Resources/moji-circle.png';
        aiWeapon = './Resources/cross.png';

        $("#weapon-choice").fadeOut(300);
        $("#weapon-selection").fadeIn(300);
        $("#choose-os").fadeIn(300);
        py_start_new(js_start_new);
    });
});


/******  FUNCTIONS  ******/

/* Changes screen with a fade effect */
function startGame() {
    /* Shows the game screen when the intro screen is completely hidden */
    $("#enemy-screen").fadeOut(300, showGameScreen);
    restartGame();
}
function showGameScreen() {
    $("#game-screen").fadeIn(300);
    $("div#result p:first").html("Choose Your Weapon!");
}
function showIntroScreen() {
    console.log("show intro screen");
    $("#intro-screen").fadeIn(300);
}
function showWinScreen() {
    console.log("showWinScreen=");
    let msg = playerWonMsgs[Math.floor((Math.random()*playerWonMsgs.length))];
    console.log("win messages="+msg);
    if(msg === undefined)
    {
        msg = "Congratulations! You Won!";
    }
   // $("#win-screen").fadeIn(300);
    //$("div#win-screen h2").html(msg);
    $("div#result p:first").html(msg);

}
function showLostScreen() {
    console.log("showLostScreen=");
    let msg = aiWonMsgs[Math.floor((Math.random()*aiWonMsgs.length))];
    console.log("lost messages="+msg);
    if(msg === undefined)
    {
        msg = "Sorry! Better luck next time!";
    }
    //$("#lost-screen").fadeIn(300);

    //$("div#lost-screen h2").html(msg);
    $("div#result p:first").html(msg);


}
function showTieScreen() {
    //$("#tie-screen").fadeIn(300);
    $("div#result p:first").html("Oh! It's Tie.");
}
/* Sets everything to its default value */
function restartGame() {
    py_reset(js_reset);
    read_fingers = false
    location.reload();

}

function js_reset(value)
{
    restartGameFalg = true;
    console.log("js_reset");
    console.log(value);
    $(".cell").text("");
    $(".cell").next("img").remove();
    $("div#result p:first").html("");
    $("div#playerSelection").html("");

    $("#game-screen").fadeOut(300);
    $("#intro-screen").fadeIn(300);
    playerWeapon = "";
    aiWeapon = "";
}

function js_ai_move(value){
    console.log("received AI move");
    console.log(value);
    if(!restartGameFlag)
    {

        let rowCol = value[3]
        let row = rowCol[0];
        let column = rowCol[1];
        console.log("row="+row+":column="+column);

        let idOfCell = "cell"+row+column;
        let element = document.getElementById(idOfCell);
        if(element.innerHTML === "") {

            $("#"+idOfCell)
                .on( "click", function( event ) {

                    insertAISymbol(idOfCell);
                    if(value[0] != "" && value[0].includes("Won!"))
                    {
                        //showWinScreen();
                        showLostScreen(); //Here AI won and Player lost.
                    }
                    else if(value[0] != "" && value[0].includes("Tie"))
                    {
                        showTieScreen();//It's Tie.

                    }
                    else
                    {
                        $("div#result p:first").html(`Now it's your move`);
                        setTimeout(make_player_move,3000);
                    }
                } )
                .trigger( "click" );
        }

    }
}


function js_player_move(value){
    if(!restartGameFlag) {
        console.log("received Player move");
        console.log(value);
        console.log("inside  js_player_move script 3333=");
        if (value[0] != "" && value[0].includes("Won!")) {
            showWinScreen();//Here Player won and AI lost.
        } else if (value[0] != "" && value[0].includes("Tie")) {
            showTieScreen();//It's Tie.
        } else {
            make_ai_move(1000);
        }
    }
}

function js_start_new(player_chance){
    console.log("Start player", player_chance)
    if (player_chance == false){
        make_ai_move(3000); // AI will Start the Game
    }else{
        $("div#result p:first").html(`Now it's your move`);
        setTimeout(make_player_move,3000); // Player will start the Game
    }
}

function make_ai_move(time){
    $("div#result p:first").html("Let Me Think My Move 🤔");
    setTimeout(() => {
        console.log("World 222222!");
        py_ai_move(js_ai_move);
    }, time);
}

function js_set_difficulty(value){
    console.log(value);
    restartGameFlag = false;
    $("#restart").fadeIn(300);
    $("#exit").fadeIn(300);
}

function make_player_move(){
    let row = values[0];
    let column = values[1];
    if(row == -1 || column == -1){

        setTimeout(make_player_move,3000);
    }
    else{
        console.log("row="+row+":column="+column);

        let idOfCell = "cell"+row+column;
        let element = document.getElementById(idOfCell);
        if(element == null)
        {
            setTimeout(make_player_move,3000);
        }else if(element.innerHTML === "") {
            console.log("inside  py finger js script="+element);
            console.log("inside  py finger js script2222222="+element.innerHTML);
            //element.innerHTML = "O";
            insertHumanSymbol(idOfCell);
            let move = [row,column];
            py_player_move(move,js_player_move);

        }
        else if(element.innerHTML !== "")
        {
            setTimeout(make_player_move,3000);
        }
    }
}

function insertAISymbol(cellId)
{
    console.log("inside insertAISymbol"+cellId);
    $('#'+cellId).empty();
    let img = $('<img id="dynamic" class="x-o">'); //Equivalent: $(document.createElement('img'))
    img.attr('src', aiWeapon);
    img.appendTo('#'+cellId);
}
function insertHumanSymbol(cellId)
{
    console.log("inside insertHumanSymbol"+cellId);
    $('#'+cellId).empty();
    let img = $('<img id="dynamic" class="x-o">'); //Equivalent: $(document.createElement('img'))
    img.attr('src', playerWeapon);
    img.appendTo('#'+cellId);
}

setInterval(call_fingers,1000/25);

function call_fingers(){
    py_cv_value(js_fingers);
}

function js_fingers(value){
    values = value;
    let element = document.getElementById("playerSelection");
    element.innerHTML = getEmoji(value[0])+" " +getEmoji(value[1]);
}

function getEmoji(selection){
    let emoji = "";
    if(selection == 0)
    {
        emoji = "✊";
    }
    else if(selection == 1)
    {
        emoji = "☝";
    }
    else if(selection == 2)
    {
        emoji = "✌";
    }
    return emoji;
}