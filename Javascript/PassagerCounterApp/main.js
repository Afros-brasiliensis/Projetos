// document.getElementById("count-el").textContent = 5;

//let firstBatch = 5;
//let secondBatch = 7;

//let count = firstBatch + secondBatch;

//console.log(count);

let myAge, humanDogRatio;
myAge = 18;

function humanToDogAge(){
    humanDogRatio = myAge * 7;
    return humanDogRatio;
}

console.log(humanToDogAge());

function countdown(){
    for (let count = 10; count > 0; count--){
        console.log(count);
    }
    console.log("Blast off!");
}

countdown();


