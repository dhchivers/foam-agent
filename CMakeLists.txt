cmake_minimum_required(VERSION 3.16)
project(FoamAgent VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Qt6
find_package(Qt6 REQUIRED COMPONENTS Core Widgets Gui OpenGL Charts)

# Enable automoc, autouic, autorcc
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_BINARY_DIR}
)

# UI files directory
set(CMAKE_AUTOUIC_SEARCH_PATHS ${CMAKE_SOURCE_DIR}/ui)

# Source files
set(SOURCES
    src/main.cpp
    src/mainwindow.cpp
    src/casemanager.cpp
    src/meshwidget.cpp
    src/solverwidget.cpp
    src/visualizationwidget.cpp
    src/processrunner.cpp
)

# Header files
set(HEADERS
    src/mainwindow.h
    src/casemanager.h
    src/meshwidget.h
    src/solverwidget.h
    src/visualizationwidget.h
    src/processrunner.h
)

# UI files
set(UI_FILES
    ui/mainwindow.ui
)

# Create executable
add_executable(FoamAgent
    ${SOURCES}
    ${HEADERS}
    ${UI_FILES}
)

# Link Qt6 libraries
target_link_libraries(FoamAgent
    Qt6::Core
    Qt6::Widgets
    Qt6::Gui
    Qt6::OpenGL
    Qt6::Charts
)

# Install target
install(TARGETS FoamAgent
    RUNTIME DESTINATION bin
)
