#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h>  //Header file for sleep(). man 3 sleep for details. 
#include <pthread.h> 

struct graph_type {
    double** A;
    int dim;
};

struct reduce_rows_args{
    struct graph_type *graph;
    double* zeros_in_rows;
    double* zeros_in_columns;
    int start;
    int d;
    double id;
};
int find_min(double * list, int dim){
    double min = 10000;
    int index = -1;
    for (int i =0; i < dim; i++){
        if (list[i] < min){
            min = list[i];
            index = i;
        }
    }
    return index;
}
int find_min_in_column(double **m, int dim, int j){
    double min = 10000;
    int index = -1;

    for (int i =0; i < dim; i++){
        if (m[i][j] < min){
            min = m[i][j];
            index = i;
        }
    }
    return index;
}

// A normal C function that is executed as a thread  
// when its name is specified in pthread_create() 
void *reduce_rows(void *vargp) 
{ 
    struct reduce_rows_args *args = ((struct reduce_rows_args*)vargp);
    struct graph_type *graph = args->graph;
    int start = args->start;
    int d = args->d;

    for(int i = start ; i < start+d; i++){
        int k = find_min(graph->A[i], graph->dim);
        double minimum = graph->A[i][k];
        //printf(" %f ,", minimum);
        for (int j = 0; j < graph->dim; j++){
            graph->A[i][j] = graph->A[i][j] - minimum; 
            //printf("%f Printing GeeksQuiz from Thread %f \n",args->id,graph->A[i][j]); 
        }
    } 


    return NULL; 
} 

void *reduce_columns(void *vargp) 
{ 
    struct reduce_rows_args *args = ((struct reduce_rows_args*)vargp);
    struct graph_type *graph = args->graph;
    int start = args->start;
    int d = args->d;

    for(int j = start ; j < start+d; j++){
        int k = find_min_in_column(graph->A, graph->dim, j);
        double minimum = graph->A[k][j];
        //printf("%f", minimum);
        for (int i = 0; i < graph->dim; i++){
            graph->A[i][j] = graph->A[i][j] - minimum; 
            //printf("%f Printing GeeksQuiz from Thread %f \n",args->id,graph->A[i][j]); 
        }
    } 


    return NULL; 
} 


void parallelize_reduce_rows(struct graph_type * graph, int p){
    pthread_t threads[p];
    for (int i = 0; i < p; i++){
        pthread_t thread_id; 
        struct reduce_rows_args *rr_args = (struct reduce_rows_args *)malloc(sizeof(struct reduce_rows_args));
        rr_args->graph = graph;
        rr_args->zeros_in_rows = (double *) malloc(sizeof(double) * graph->dim);
        rr_args->zeros_in_columns = (double *) malloc(sizeof(double) * graph->dim);
        rr_args->start = i * p;
        rr_args->d = graph->dim / p;
        if ( (rr_args->d % 2 !=0) && ( i + 1 == p)){
            rr_args->d = graph->dim - rr_args->start;
            printf("%d", rr_args->d);
        }
        
        rr_args->id = i;
        pthread_create(&thread_id, NULL, reduce_rows, (void *)rr_args); 
        threads[i] = thread_id;
    }
    for (int i = 0; i < p; i++){
        pthread_join(threads[i], NULL);
    }
}


void parallelize_reduce_columns(struct graph_type * graph, int p){
    pthread_t threads[p];
    for (int i = 0; i < p; i++){
        pthread_t thread_id; 
        struct reduce_rows_args *rr_args = (struct reduce_rows_args *)malloc(sizeof(struct reduce_rows_args));
        rr_args->graph = graph;
        rr_args->zeros_in_rows = (double *) malloc(sizeof(double) * graph->dim);
        rr_args->zeros_in_columns = (double *) malloc(sizeof(double) * graph->dim);
        rr_args->d = graph->dim / p;
        rr_args->start = i * p;
        if ( (p % 2 !=0) && ( i + 1 == p)){
            rr_args->d = graph->dim - rr_args->start;
        }
        rr_args->id = i;
        pthread_create(&thread_id, NULL, reduce_columns, (void *)rr_args); 
        threads[i] = thread_id;
    }
    for (int i = 0; i < p; i++){
        pthread_join(threads[i], NULL);
    }
}

void print_graph(struct graph_type *graph){
    int i =0, j= 0;
    //traversing 2D array    
    for(i=0;i < graph->dim;i++){    
        printf("\n");
        for(j=0;j< graph->dim;j++){    
            
            printf("%f ,",graph->A[i][j]);    
        }//end of j    
    }//end of i   
}

void init(struct graph_type *graph , int r){
    int i =0, j= 0;
    //traversing 2D array    
    for(i=0;i < graph->dim;i++){    
        printf("\n");
        for(j=0;j< graph->dim;j++){    
               graph->A[i][j] = rand() % r;
        }//end of j    
    }//end of i   
}


int main() 
{
    int n = 5;
    int p = 2;
    // int g[][3] = {{1,2,3},{1,2,3},{1,2,3}};
    struct graph_type *graph = (struct graph_type *)malloc(sizeof(struct graph_type));
    graph->dim = n;
    
    graph->A = (double **) malloc(sizeof(double *) * graph->dim);
    for (int k = 0; k < graph->dim; k++) {
        graph->A[k] = (double *) malloc(sizeof(double) * graph->dim);
    }
    init(graph,50);
    //graph->A[0][1] = 19;

    
    
    
    
    printf("Let's start\n"); 
    
    print_graph(graph);
    printf("\n");
    
    parallelize_reduce_rows (graph,p);

    printf("\n");

    print_graph(graph);

    printf("\n");

    parallelize_reduce_columns(graph,p);

    printf("\n");

    print_graph(graph);

    printf("\nDone \n"); 
    exit(0); 
}