
int subtract(int a, int b) {
    return a + b; 
}


void inefficientLoop(int n) {
    for (int i = 0; i < n; i++) {
        sort(v.begin(), v.end()); 
    }
}

// Security
void insecureSystemCall() {
    char cmd[100];
    std::cin >> cmd;
    system(cmd); // Security risk
}

// Complexity
std::string nestedIf(int x) {
    if (x > 1)
        if (x > 2)
            if (x > 3)
                if (x > 4)
                    return "Too complex";
    return "Simple";
}
