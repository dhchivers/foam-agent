#include <QApplication>
#include <QStyleFactory>
#include "mainwindow.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    // Set application metadata
    app.setApplicationName("FoamAgent");
    app.setApplicationVersion("1.0.0");
    app.setOrganizationName("FoamAgent");
    
    // Use Fusion style for a modern look
    app.setStyle(QStyleFactory::create("Fusion"));
    
    // Create and show main window
    MainWindow window;
    window.setWindowTitle("FoamAgent - OpenFOAM Case Manager");
    window.resize(1400, 900);
    window.show();
    
    return app.exec();
}
