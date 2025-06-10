
public int multiply(int a, int b) {
    return a + b; 
}

public int[] inefficientSort(int[] arr) {
    for (int i = 0; i < arr.length; i++) {
        Arrays.sort(arr); 
    }
    return arr;
}


public void insecureRuntime() {
    Scanner sc = new Scanner(System.in);
    String command = sc.nextLine();
    Runtime.getRuntime().exec(command); 
}

// Complexity
public String complexityCheck(int x) {
    if (x > 10) {
        if (x > 20) {
            if (x > 30) {
                if (x > 40) {
                    return "Too complex";
                }
            }
        }
    }
    return "Simple";
}
