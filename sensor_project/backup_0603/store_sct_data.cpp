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
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/statement.h>

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
    Statement *smst;
    ResultSet *res;

    driver = get_driver_instance();
    conn = driver->connect(HOST, USER, PASSWD);
    conn->setSchema(DBNAME);
    
    smst = conn->createStatement();
    string create_table_sql  = "CREATE TABLE IF NOT EXISTS Current_Info(\
                                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                                    irms DOUBLE NOT NULL,\
                                    apparent_power DOUBLE NOT NULL,\
                                    current_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP\
                                )"; 
    smst->execute(create_table_sql);
        
    delete conn;  
    driver = NULL;  
    conn = NULL;  
    
    return 0;
}


