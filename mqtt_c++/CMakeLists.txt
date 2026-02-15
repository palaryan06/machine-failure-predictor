cmake_minimum_required(VERSION 3.10)

project(mqtt_demo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find the exact packages that actually exist
find_package(PahoMqttCpp CONFIG REQUIRED)
find_package(eclipse-paho-mqtt-c CONFIG REQUIRED)

add_executable(mqtt_demo main.cpp)

target_link_libraries(mqtt_demo PRIVATE
    PahoMqttCpp::paho-mqttpp3
    eclipse-paho-mqtt-c::paho-mqtt3as
)
