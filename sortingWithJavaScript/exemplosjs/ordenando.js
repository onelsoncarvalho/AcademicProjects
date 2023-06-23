    // Função Swap
    // Declarando Array
    //var array = [5, 2, 7, 1, 9];
    // Função Swap
    swap = (vetor, pos1, pos2) => {
        let temp = vetor[pos1];
        vetor[pos1] = vetor[pos2];
        vetor[pos2] = temp;

        return vetor

    //  console.log(vetor)
    }
    // Executando função, e passando os 3 parâmetros
    //swap(array, 1, 3)
    // Função shuffle
    shuffle = (array) => {
        for (var i = array.length; i-- > 0;) {
            var j = Math.floor(Math.random() * (i + 1));
            var temp = array[i];
            array[i] = array[j];
            array[j] = temp;
        }
            return array
    }

    // Função Bubble Sort
    bubbleSort = (arr) => {
        let temp;
            for(let i =0 ; i < arr.length; i++){
                for(let j = 0 ;j< arr.length -(i-1); j++){
                    if(arr[j]> arr[j+1]){
                        temp = arr[j+1];
                        arr[j+1] = arr[j]
                        arr[j] = temp;
                    }
                }   
            }
            return arr;
    }
    // Funçao Selection Sort
    selectionSort = (arr) => {
        let temp;
        let min;
        for( let i=0 ; i< arr.length; i++){
            min = i;
            for(let j = i+1; j < arr.length; j++)
                if(arr[j]<arr[min])
                min = j;
            temp = arr[i];
            arr[i] = arr[min];
            arr[min] = temp;
        }
        return arr;
    }
    // Função Quick Sort
    quickSort = (array) => {
        if (array.length === 0) return [];
        if (array.length === 1) return array;

        var pivot = array[0];

        var head = array.filter( n => n < pivot);
        var equal = array.filter( n => n === pivot);
        var tail = array.filter( n => n > pivot);
    
    return quickSort(head).concat(equal).concat(quickSort(tail));
}
