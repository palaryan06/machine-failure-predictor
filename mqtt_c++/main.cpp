#include <iostream>
#include <string>
#include <mqtt/async_client.h>
#include <fstream>
#include <sstream>

#include <chrono>
#include <thread>

using namespace std;

const string SERVER_ADDRESS = "tcp://test.mosquitto.org:1883";
const string CLIENT_ID = "aryan_cpp_publisher_001";
const string TOPIC = "test/aryan/mqtt";

int main() {

   
    fstream myfile(
        "C:\\Users\\palar\\OneDrive\\Desktop\\Machine_failure_detection\\test_data.csv",
        ios::in
    );

    if (!myfile.is_open()) {
        cout << "Failed to open test_data.csv" << endl;
        return 1;
    }

    string line;

    
    getline(myfile, line);
    mqtt::async_client client(SERVER_ADDRESS, CLIENT_ID);
            mqtt::connect_options connOpts;
            connOpts.set_clean_session(true);   

            cout << "Connecting to MQTT broker..." << endl;
            client.connect(connOpts)->wait();
            cout << "Connected successfully!" << endl;

    while (true)
    {   
        
        fstream myfile2(
            "C:\\Users\\palar\\OneDrive\\Desktop\\Machine_failure_detection\\mqtt_c++\\data\\student2.csv",
            ios::out
        );

        int written = 0;

        
        while (written < 6 && getline(myfile, line))
        {
            myfile2 << line << "\n";
            written++;
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));

        }

        myfile2.close();

      
        if (myfile.eof()) {
            cout << "Reached end of file. Stopping publisher." << endl;
            break;
        }

        try {
            
            ifstream file(
                "C:\\Users\\palar\\OneDrive\\Desktop\\Machine_failure_detection\\mqtt_c++\\data\\student2.csv"
            );

            if (!file.is_open()) {
                cout << "Failed to open student2.csv!" << endl;
                return 1;
            }

            stringstream buffer;
            buffer << file.rdbuf();
            file.close();

           
            

           
           

            
            auto message = mqtt::make_message(TOPIC, buffer.str());
            message->set_qos(1);
            message->set_retained(false);   

            client.publish(message)->wait();
            cout << "Sent 6 lines to MQTT" << endl;

           
        }
        catch (const mqtt::exception& e) {
            cerr << "MQTT Error: " << e.what() << endl;
            return 1;
        }
    }
     client.disconnect()->wait();
            cout << "Disconnected." << endl;

    myfile.close();
    return 0;
}
