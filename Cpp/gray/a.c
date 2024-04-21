#include <stdio.h>
#include <math.h>

int main(void){
	float R,G,B,gray;
	int scanf_result;
	char yn;

	while(1){
		printf("Enter your RGB number(R G B): ");
		scanf_result = scanf("%f%f%f",&R,&G,&B);

		if(scanf_result != 3){
			printf("Error: Invalid input!\n");
			continue;
		}

		gray = pow(((pow(R,2.2)+pow((1.5 * G),2.2)+pow((0.6 * B),2.2))/(1+pow(1.5,2.2)+pow(0.6,2.2))),1/2.2);

		printf("The gray-scale value is %f\n",gray);
		
		printf("Do you want to continue?(Y/n): ");
		scanf(" %c",&yn);
		if(yn == 'n' || yn == 'N'){
			break;
		}
	}
	return 0;
}
