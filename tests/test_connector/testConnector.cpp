/*
 * =====================================================================================
 *
 *       Filename:  connector.cpp
 *
 *    Description:  test if c++ mysql connector is configured correctly
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
#define HOST   "localhost"
#define USER   "root"
#define PASSWD "password"

int main() {
   
    Driver *driver;
    Connection *conn;

    driver = get_driver_instance();
    conn = driver->connect(HOST, USER, PASSWD);  // Try to connect localhost
    conn->setAutoCommit(0);
    
    cout << "DataBase connection autocommit mode = "
         << conn->getAutoCommit()
         << endl;  
    
    delete conn;  
    driver = nullptr;  
    conn = nullptr;  
    
    return 0;
}
