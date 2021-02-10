/* This is a program that assigns a random ID number to a username and stores it in an array.
It gives you the ability to get your username by inputting your ID number. Then finally you can 
choose to print the first ten ID numbers that are randomly picked and then choose those numbers and
if they have a username placed in them, then it will print it.

Title: Operand.cpp
Author: Nicholas Richards
*/



//Include libraries
#include <string>
#include <iostream>
#include <stdlib.h>
#include <time.h>
using namespace std;

//creates array for users
string users [100];


//This function generates the ID
int generateID()
{
   int id=rand()%100;
   return id;
}
//This functions gets the ID from the generateID() function
void getID()
{
   string name="";
   cout << "Please enter your username. ";
   cin >> name;
   int sessionID = generateID();
   cout << endl << "Thank you! Your session id is: " 
	    << sessionID << endl;
   users[sessionID] = name;
   
}
//This function prints out the username associated with the ID
void enterID()
{
   int ID = 0;
   cout << "Please enter your session id: ";
   cin >> ID;
   cout << endl << "Hello " << users[ID] << endl;
}

//This functions prints the first ten numbers that are randomly generated
void printNumbers()
{
    srand(time(NULL));
	for (int i=0;i<10;i++)
   {
      cout << generateID() << endl;
   }
}

//This is the main function for the program
int main()
{
  srand(time(NULL));
	users[generateID()] = "Bob";
 
   int choice;
   do//This do-while loop creates the menu choices
   {
    cout << endl;
    cout << "Choices:" << endl;
	  cout << "1) Get session id." << endl;
	  cout << "2) Enter session id." << endl;
	  cout << "3) Print first 10 ids." << endl;
	  cout << "Please enter the number of your choice (type '4' to quit): ";
	  cout << endl;
	  
    //The if statements makes sure that there is a integer inputted
    if(std::cin >> choice){
      switch(choice){ //The switch case statements calls each function based on the case chosen and defaults to invalid choice
        
        case 1:
          
          getID();
          
          break;
        
        case 2:
          
          enterID();
          
          break;
        
        case 3:
          
          printNumbers();
          
          choice = 4;
          
          break;
        
        case 4:
          
          choice = 4;
          
          break;
        
        default :
          
          cout<< "Invalid Choice"<<endl;
          
          cout<< "Enter a number between 1 and 4 please!"<<endl;
      }
    
    }
    
    else{
      
      cout<<"That was not a number!! Please enter a number"<<endl;
      
      break;
    }
	  
   }
   
   while (choice != 4);// While choice does not equal 4 it continues.
   
   return 0;
}