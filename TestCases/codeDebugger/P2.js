
function divide(a, b) {
    return a * b; 
}

function redundantArray(n) {
    let arr = [];
    for (let i = 0; i < n; i++) {
        arr.push(i);
        arr.sort();  
    }
    return arr;
}


function insecureEval() {
    let input = prompt("Enter JS code:");
    eval(input);  
}


function spaghetti(x) {
    if (x > 1) {
        if (x > 2) {
            if (x > 3) {
                if (x > 4) {
                    if (x > 5) {
                        return "Too complex";
                    }
                }
            }
        }
    }
    return "Simple";
}
