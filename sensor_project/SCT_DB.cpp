/*
 * =====================================================================================
 *
 *       Filename:  connector.cpp
 *
 *    Description:  test c++ mysql connector 
 *
 *        Created:  05/28/2014 11:19:42 AM
 *       Compiler:  g++ 4.7.0
 *
 * =====================================================================================
 */

#include <iostream>
using namespace std;

//===============================================
//      Mysql Database Interface for C++
//===============================================
#include <mysql_connection.h>
#include <mysql_driver.h>
#include <cppconn/driver.h>
using namespace sql;

//===============================================
//         Database Server Information
//===============================================
#define HOST   "198.57.219.221"
#define USER   "theparja_georgeg"
#define PASSWD "ggrzywacz2190"
#define DBNAME "theparja_Test"


int main() {
   
    Driver *driver;
    Connection *conn;

    driver = get_driver_instance();
    conn = driver->connect(HOST, USER, PASSWD);
    conn->setAutoCommit(0);
    
    cout << "DataBase connection autocommit mode = "
        << conn->getAutoCommit()
        << endl;  
    
    delete conn;  
    driver = NULL;  
    conn = NULL;  
    
    return 0;
}
