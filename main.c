// This C program calculates the current saldo for a given month by reading expenses from a configuration file.
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

int main(int argc, char *argv[]) {             
	double income, fixedExpenses, totalBudget, dailyBudget, expenses, saldo; 
	int month, day, daysInMonth;
	FILE *configFile = fopen("config.txt", "r");

	// Print help text if --help option is detected
	if (argc > 1 && strcmp(argv[1],"--help") == 0) {
		printf("This program calculates the current saldo for a given month by reading expenses from a configuration file.\n");
		printf("Usage: saldo [--help]\n");
		exit(0);
	}

	// Get the current month
	time_t rawtime;
	struct tm *timeinfo;
	time(&rawtime);
	timeinfo = localtime(&rawtime);
	month = timeinfo->tm_mon + 1;

	// Get the number of days in the month
	if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 || month == 10 || month == 12)
		daysInMonth = 31;
	else if (month == 2)
		daysInMonth = 28;
	else
		daysInMonth = 30;

	// Check if the configuration file exists and generate it if not
	if (!configFile) {
		printf("No config file found. Generating one now...\nDon't forget to edit it\n");
		FILE *configFile = fopen("config.txt", "w");
		fprintf(configFile, "income 0\nfixed_expenses 0\n");
		for (int i = 1; i <= daysInMonth; i++) {
			fprintf(configFile, "%d 0\n", i);
		}
		fclose(configFile);
		exit(0);
	}

	// Read income and fixed expenses from the configuration file
	fscanf(configFile, "income %lf\nfixed_expenses %lf\n", &income, &fixedExpenses);
	totalBudget = income - fixedExpenses;
	dailyBudget = totalBudget / daysInMonth;
	saldo = 0;

	// Calculate the saldo for each day
	for (day = 1; day <= daysInMonth; day++) {
		if (fscanf(configFile, "%d %lf\n", &day, &expenses) != EOF) {
			saldo += dailyBudget - expenses;
		}
		else {
			saldo += dailyBudget;
		}
		printf("Your saldo for day %d is %.2lf\n", day, saldo);
	}
	// Display the daily budget
	printf("Your average daily budget for this month is %.2lf\n", dailyBudget);
	fclose(configFile);
	return 0;
}
