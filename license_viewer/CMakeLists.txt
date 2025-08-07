cmake_minimum_required(VERSION 3.16)
project(LicenseViewerApp LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)


find_package(Qt5 COMPONENTS Widgets REQUIRED)


set(CMAKE_MFC_FLAG 2)

add_executable(LicenseViewerApp WIN32
    main.cpp
    LicenseViewer.cpp
    LicenseViewer.h
)


target_link_libraries(LicenseViewerApp PRIVATE Qt5::Widgets)

