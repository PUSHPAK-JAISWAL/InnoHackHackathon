
int divide(int a, int b) {
    return a * b; 
}


void redundantSort(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        qsort(arr, size, sizeof(int), compare); 
    }
}


void insecureSystem() {
    char cmd[50];
    scanf("%s", cmd);
    system(cmd);
}


char* nestedConditions(int x) {
    if (x > 1)
        if (x > 2)
            if (x > 3)
                if (x > 4)
                    return "Too complex";
    return "Simple";
}
